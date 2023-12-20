function getAllLobby() {
    const request = new Request(getBaseUrlLobbyAPI() + 'allNames/')

    apiRequest(request).then(response => {
        showLobbies(response.json)
    })
}

function getLobbyName() {
    const searchParams = new URLSearchParams(window.location.search);
    return searchParams.get('lobby')
    
}

function joinLobby(){
    var lobbyName = document.getElementById('lobby-name').value
    var lobbyPass = document.getElementById('lobby-password').value

    const request = new Request(getBaseUrlLobbyAPI() + 'action/' + lobbyName);
    
    var postData = {
        "password": lobbyPass
    }

    var data = {
        method: "POST",
        body: JSON.stringify(postData),
    }

    apiRequest(request, data).then(response => {
        console.log(response);
        if (response.status != 201){
            alert_bootstrap(response.json, 'warning', 'global_alert')
        } else{
            document.location.reload()
        };
    })
}

function createLobby(){
    var lobbyName = document.getElementById('lobby-name-create').value
    var lobbyPass = parseInt(document.getElementById('lobby-password-create').value)
    var lobbyLimit = document.getElementById('user-limit-create').value

    const request = new Request(getBaseUrlLobbyAPI() + 'create/');
    
    var postData = {
        "lobby_name": lobbyName,
        "password": lobbyPass,
        "user_limit": lobbyLimit
    }

    var data = {
        method: "POST",
        body: JSON.stringify(postData),
    }

    apiRequest(request, data).then(response => {
        if (response.status != 201){
            json = response.json
            if (json.hasOwnProperty('password')) {
                alert_bootstrap(json['password'], 'danger', 'password_alert')
            }
            if (json.hasOwnProperty('lobby_name')) {
                alert_bootstrap(json['lobby_name'], 'danger', 'lobby_name_alert')
            }
            if (json.hasOwnProperty('user_limit')) {
                alert_bootstrap(json['user_limit'], 'danger', 'user_limit_alert')
            }
        } else {
            document.location.reload()
        }

    })
}

function loadMessagesFromAPI() {
    var lobbyName = document.location.pathname.split('/chat/')[1].slice(0, -1);
    
    const request = new Request(getBaseUrlLobbyAPI() + 'getLobby/' + lobbyName)
    apiRequest(request).then(response => {
        response = response.json
        response.messages.forEach(message => {
            createBubble(
                message.user.username,
                message.message,
                new Date(message.created_at),
                message.id,
                (message.user.username === username)
            )
            createLikeForBubble(message.user_liked, message.id)
        });
    }).then(function() {
        scrollToLastMessage()
    })
}

function scrollToLastMessage() {
    var bubbles = document.getElementsByClassName('bubble');
    var lastBubble = bubbles.item(bubbles.length - 1);
    lastBubble.scrollIntoView({behavior: 'smooth'})
}


function deleteOrExitFromLobby(event) {
    var lobbyName = event.target.id.split('exit-')[1];
    var api = {
        'Delete': 'delete',
        'Exit': 'action'
    }

    const request = new Request(`${getBaseUrlLobbyAPI()}${api[event.target.textContent]}/${lobbyName}`);

    var data = {
        method: "DELETE",
    }

    apiRequest(request, data).then(response => {
        if (response.status === 204){
            document.location.reload();
        } else {
            console.log(response)
        }
    })
}

function showLobby(json_lobby){
    var tbody = document.getElementById('lobby-tbody')
    var lobbyName = document.createElement('td')
    var connectedUser = document.createElement('td')
    var open = document.createElement('td')
    var action = document.createElement('td')
    var tr = document.createElement('tr')
    
    var joinButton = document.createElement('a')
    var exitButton = document.createElement('div')
    var deleteButton = document.createElement('div')

    connectedUser.textContent = json_lobby['user_connected']
    lobbyName.textContent = json_lobby['lobby_name']

    joinButton.type = "button"
    joinButton.className = "btn btn-outline-success"
    joinButton.textContent = 'Join'
    joinButton.href = "/chat/" + json_lobby['lobby_name'] + "/"
    joinButton.style = "--bs-btn-padding-y: .25rem; --bs-btn-padding-x: .5rem; --bs-btn-font-size: .75rem;"

    exitButton.title = "button"
    exitButton.className = "btn btn-outline-warning"
    exitButton.textContent = 'Exit'
    exitButton.id = 'exit-' + json_lobby['lobby_name']
    exitButton.onclick = deleteOrExitFromLobby
    exitButton.style = "--bs-btn-padding-y: .25rem; --bs-btn-padding-x: .5rem; --bs-btn-font-size: .75rem; margin-right: 7px"

    deleteButton.title = "button"
    deleteButton.className = "btn btn-outline-danger"
    deleteButton.textContent = 'Delete'
    deleteButton.id = 'exit-' + json_lobby['lobby_name']
    deleteButton.onclick = deleteOrExitFromLobby
    deleteButton.style = "--bs-btn-padding-y: .25rem; --bs-btn-padding-x: .5rem; --bs-btn-font-size: .75rem; margin-right: 7px"

    if (json_lobby['owner']){
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

function showLobbies(json) {
    for (let index = 0; index < json.length; index++) {
        showLobby(json[index]);
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

function alert_bootstrap(message, type, elementId) {
    const alertPlaceholder = document.getElementById(elementId)

    const wrapper = document.createElement('div')
    wrapper.innerHTML = [
      `<div class="alert alert-${type} alert-dismissible" role="alert">`,
      `   <div>${message}</div>`,
      '   <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>',
      '</div>'
    ].join('')

    alertPlaceholder.append(wrapper)
}