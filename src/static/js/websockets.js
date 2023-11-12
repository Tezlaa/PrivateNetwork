var onMessageFunc = {
    'chat_message': chat_message,
    'chat_like': chat_like,
    'chat_delete_like': chat_delete_like,
}


function startSocket() {
    var lobby_name = window.location.pathname.split('/chat/')[1].slice(0, -1);
    socket = new WebSocket(url=`ws://${window.location.host}/ws/chat/${lobby_name}`, )

    socket.onmessage = function(e) {
        console.log('onMessage');
        onMessage(JSON.parse(e.data))
    }

    socket.onopen = function(e) {
        console.log('onOpen');
    }

    socket.onclose = function(e) {
        console.log('onClose');
    }
}

function onMessage(data) {
    onMessageFunc[data.type](data)
}

function chat_message(data) {
    var alt = true
    if (data.username !== username) {
        alt = false
    }
    createBubble(
        name=data.username,
        message=data.message,
        date=new Date(data.timestamp * 1000),
        message_id=data.message_id,
        alt=alt
    )
}

function chat_like(data) {
    var bubble = document.querySelector(`div[messageid="${data.message_id}"]`);
    
    if (bubble.querySelector('.message-like').children.length === 0){
        createLikeForBubble([{'username': data.username}], data.message_id)
    } else {
        var likes = bubble.querySelector('.likes')
        var messageLike = likes.querySelector('.message-like')
        title = messageLike.getAttribute('title')
    
        var userIndexInTitle = title.indexOf(data.username)
    
        if (userIndexInTitle === -1) {
            numberLikes = parseInt(messageLike.querySelector('.number-likes').textContent)
            messageLike.querySelector('.number-likes').textContent = numberLikes + 1
            messageLike.setAttribute('title', `${title}${data.username}`)
        }
    }
}

function chat_delete_like(data) {
    var bubble = document.querySelector(`div[messageid="${data.message_id}"]`);
        
    var likes = bubble.querySelector('.likes')
    var messageLike = likes.querySelector('.message-like')
    title = messageLike.getAttribute('title')

    numberLikes = parseInt(messageLike.querySelector('.number-likes').textContent)

    var newNumber = numberLikes - 1
    if (newNumber >= 1){
        messageLike.querySelector('.number-likes').textContent = numberLikes - 1;
        newTitle = ''
        title.split('\n').forEach(username => {
            if (username != data.username){
                newTitle += username + '\n'
            }
        })
        messageLike.setAttribute('title', newTitle);
    }else {
        messageLike.innerHTML = '';
        messageLike.setAttribute('title', '')
    }
}

function createLikeForBubble(users, message_id) {
    if (users.length === 0){
        return
    }

    var bubble = document.querySelector(`div[messageid="${message_id}"]`);
    
    var likes = bubble.querySelector('.likes')
    var messageLike = likes.querySelector('.message-like')

    var usersTitle = ''
    users.forEach(user => {
        usersTitle += user.username + '\n'
    });

    messageLike.setAttribute('title', usersTitle);
    var likeImg = document.createElement('img');
    likeImg.src = "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f1/Heart_coraz%C3%B3n.svg/800px-Heart_coraz%C3%B3n.svg.png";
    likeImg.classList.add('like')

    var numberLikesSpan = document.createElement('span');
    numberLikesSpan.classList.add('number-likes');
    numberLikesSpan.textContent = users.length;

    messageLike.appendChild(likeImg);
    messageLike.appendChild(numberLikesSpan);

    likes.appendChild(messageLike)
    bubble.appendChild(likes);
}

function sendMessage() {
    var message = document.getElementById('floatingTextarea').value;
    if (message.length < 1) {
        return
    } 

    socket.send(JSON.stringify({
        'type': 'message',
        'message': message,
        'username': username,
    }))
    resetMessageArea()
}

function resetMessageArea() {
    document.getElementById('floatingTextarea').value = ''
}

function createBubble(name, message, date, message_id, alt=true) {
    const outerDiv = document.createElement('div');

    outerDiv.setAttribute('messageId', message_id)
    outerDiv.addEventListener('dblclick', (e) => {
        dblclickEvent(e);
    })

    const nameParagraph = document.createElement('p');
    if (alt) {
        outerDiv.className = 'bubble alt';
        nameParagraph.className = 'name alt';
    }else {
        outerDiv.className = 'bubble';
        nameParagraph.className = 'name';
    }
    nameParagraph.textContent = name;

    const innerDiv = document.createElement('div');
    innerDiv.className = 'txt';

    const messageParagraph = document.createElement('p');
    messageParagraph.className = 'message';
    messageParagraph.textContent = message;

    const timestampSpan = document.createElement('span');
    timestampSpan.className = 'timestamp';
    timestampSpan.textContent = `${date.toDateString()} - ${date.toLocaleTimeString()}`;

    const likesDiv = document.createElement('div');
    likesDiv.className = 'likes'

    const messageLikeDiv = document.createElement('div');
    messageLikeDiv.className = 'message-like'
    messageLikeDiv.setAttribute('data-bs-toggle', 'tooltip')
    messageLikeDiv.setAttribute('data-bs-placement', 'left')
    messageLikeDiv.setAttribute('title', '')

    likesDiv.appendChild(messageLikeDiv)

    innerDiv.appendChild(nameParagraph);
    innerDiv.appendChild(messageParagraph);
    innerDiv.appendChild(timestampSpan);
    innerDiv.appendChild(likesDiv);

    outerDiv.appendChild(innerDiv);

    document.getElementById('speech').appendChild(outerDiv);
}

function dblclickEvent(event) {
    var perent = event.target.parentElement.parentElement

    var messageId = perent.getAttribute('messageid')
    if (messageId === null){
        messageId = event.target.parentElement.getAttribute('messageid')
    }

    if (messageId === null) {
        return 
    }

    var bubble = document.querySelector(`div[messageid="${messageId}"]`);
    var likes = bubble.querySelector('.likes')
    var messageLike = likes.querySelector('.message-like')
    title = messageLike.getAttribute('title').split('\n')

    if (title.includes(username)) {
        socket.send(JSON.stringify({
            'type': 'delete_like',
            'message_id': messageId,
            'username': username,
        }))
    }else {
        socket.send(JSON.stringify({
            'type': 'like',
            'message_id': messageId,
            'username': username,
        }))
    }
}
