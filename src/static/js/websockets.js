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
    console.log(data);

    if (data.type === 'chat_message') {
        if (data.name !== username) {
            createBubble(data.name, data.message, new Date(data.timestamp * 1000), false)
        }else {
            createBubble(data.name, data.message, new Date(data.timestamp * 1000))
        }
    }
}

function sendMessage() {
    var message = document.getElementById('floatingTextarea').value;
    if (message.length < 1) {
        return
    } 

    socket.send(JSON.stringify({
        'type': 'message',
        'message': message,
        'name': username,
    }))
    resetMessageArea()
}

function resetMessageArea() {
    document.getElementById('floatingTextarea').value = ''
}

function createBubble(name, message, date, alt=true) {
    const outerDiv = document.createElement('div');
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

    innerDiv.appendChild(nameParagraph);
    innerDiv.appendChild(messageParagraph);
    innerDiv.appendChild(timestampSpan);

    outerDiv.appendChild(innerDiv);

    document.getElementById('speech').appendChild(outerDiv);
}