function getAllLobby() {
    const request = new Request(getBaseUrl() + '/lobby/api/v1/allNames/')

    apiRequest(request).then(json => {
        showLobby(json)
    })
}

function getLobbyName() {
    const searchParams = new URLSearchParams(window.location.search);
    return searchParams.get('lobby')
    
}

function joinLobby(){
    var lobbyName = document.getElementById('lobby-name').value
    var lobbyPass = document.getElementById('lobby-password').value

    const request = new Request(getBaseUrl() + 'lobby/join/');
    
    var postData = {
        "lobby_name": lobbyName,
        "password": lobbyPass
    }

    var data = {
        method: "POST",
        body: JSON.stringify(postData),
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken(),
        }
    }

    apiRequestPost(request, data).then(json => {
        console.log(json);
        // document.location.reload();
    })
}

const loadChat = async () => {
    await updateChat();
    await setInterval(updateChat, 10000);
}

async function updateChat() {
    var from_id = 0
    try {
        from_id = parseInt(
            document.getElementById('chat-block').lastElementChild.getAttribute('message-id')
        );
    } catch (error) {}

    var lobbyName = await getLobbyName();

    const request = await new Request(getBaseUrl() + 'chat/all/' + lobbyName + '/?from_id=' + from_id)

    await apiRequest(request).then(json => {
        showChat(json[0])
    })
}

function sendMessage() {
    var message = document.getElementById('floatingTextarea').value;
    if (message.length < 1) {
        return
    } 
    const request = new Request(getBaseUrl() + 'chat/send/');
    
    var postData = {
        "lobby_name": getLobbyName(),
        "message": message,
    }

    var data = {
        method: "POST",
        body: JSON.stringify(postData),
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken(),
        }
    }

    apiRequestPost(request, data).then(json => {
        document.location.reload();
    })
}

function resetMessageArea() {
    document.getElementById('floatingTextarea').value = ''
}

function exitFromLobby(event) {
    var lobbyName = event.target.id.split('exit-')[1];
    const request = new Request(getBaseUrl() + 'lobby/exit/' + lobbyName + '/');

    var data = {
        method: "DELETE",
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken(),
        }
    }

    apiRequestPost(request, data).then(json => {
        document.location.reload();
    })
}

function showLobby(json) {
    for (let index = 0; index < json.length; index++) {
        const lobby = json[index];
        
        var tbody = document.getElementById('lobby-tbody')
        var lobbyName = document.createElement('td')
        var connectedUser = document.createElement('td')
        var open = document.createElement('td')
        var action = document.createElement('td')
        var tr = document.createElement('tr')
        
        var joinButton = document.createElement('a')
        var exitButton = document.createElement('div')
        var deleteButton = document.createElement('div')

        connectedUser.textContent = lobby['user_connected']
        lobbyName.textContent = lobby['lobby_name']

        joinButton.type = "button"
        joinButton.className = "btn btn-outline-success"
        joinButton.textContent = 'Join'
        joinButton.href = "/chat/?lobby=" + lobby['lobby_name']
        joinButton.style = "--bs-btn-padding-y: .25rem; --bs-btn-padding-x: .5rem; --bs-btn-font-size: .75rem;"

        exitButton.title = "button"
        exitButton.className = "btn btn-outline-warning"
        exitButton.textContent = 'Exit'
        exitButton.id = 'exit-' + lobby['lobby_name']
        exitButton.onclick = exitFromLobby
        exitButton.style = "--bs-btn-padding-y: .25rem; --bs-btn-padding-x: .5rem; --bs-btn-font-size: .75rem; margin-right: 7px"

        deleteButton.title = "button"
        deleteButton.className = "btn btn-outline-danger"
        deleteButton.textContent = 'Delete'
        deleteButton.id = 'exit-' + lobby['lobby_name']
        deleteButton.onclick = exitFromLobby
        deleteButton.style = "--bs-btn-padding-y: .25rem; --bs-btn-padding-x: .5rem; --bs-btn-font-size: .75rem; margin-right: 7px"

        if (lobby['owner']){
            action.appendChild(deleteButton)
        }

        open.appendChild(exitButton)
        open.appendChild(joinButton)

        tr.appendChild(lobbyName)
        tr.appendChild(connectedUser)
        tr.appendChild(action)
        tr.appendChild(open)
        tbody.appendChild(tr)
    }
}

function showChat(jsonChat) {
    messages = document.getElementById('chat-block')
    
    jsonChat['messages'].forEach(message => {
        messageBlock = document.createElement('div')
        messageBlock.className = 'row gx-1 p-2'
        messageBlock.setAttribute('message-id', message.id)

        userName = document.createElement('div')
        date = document.createElement('div')
        text = document.createElement('div')
        
        date.innerHTML = message.time
        userName.innerHTML = message.user.username
        text.innerHTML = message.message
        
        if (message.is_owner){
            messageBlock.style = "text-align: right;"
        }else {
            messageBlock.style = "text-align: left;"
        }

        messageBlock.appendChild(date)
        messageBlock.appendChild(userName)
        messageBlock.appendChild(text)

        messages.appendChild(messageBlock)
    });
}

function apiRequest(request) {
    return fetch(request, )
        .then(response => response.json());
}

function apiRequestPost(request, data) {
    return fetch(request, data)
        .then(response => response.json());
}

function getBaseUrl(){
    return window.location.origin
}

function getCSRFToken() {
	var cookieName = 'csrftoken';
	var cookieValue = null;
	var cookies = document.cookie.split(';');
	for (var i = 0; i < cookies.length; i++) {
		var cookie = cookies[i].trim();
		if (cookie.startsWith(cookieName + '=')) {
		cookieValue = cookie.substring(cookieName.length + 1);
		break;
		}
	}
	return cookieValue;
}