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

function apiRequest(request, data = {}) {
    
    if (!data.hasOwnProperty('headers')){
        data['headers'] = {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken(),
            'Authorization': getLocalAccessTokenString(),
        }
    }

    return fetch(request, data)
        .then(response => {
            if (response.status === 401){
                refreshToken()
            }
            return response.json()
                .then(json => ({ json, status: response.status, response}));
        });
}

function refreshToken() {
    var data = {
        'method': 'POST',
        'body': JSON.stringify({
            'refresh': localStorage.getItem('refresh'),
        })
    }

    var request = new Request(`${getBaseUrlAPIV1()}token/refresh/`)
    apiRequest(request, data).then(response => {
        if (response.status === 200) {
            localStorage.setItem('access', response.json['access'])
        } else {
            document.location.href = getLoginUrl()
        }
        console.log(response.json)
    })
}

function getLocalAccessTokenString(){
    return `Token ${localStorage.getItem('access')}`
}

function getBaseUrlLobbyAPI(){
    return getBaseUrlAPIV1() + 'lobby/'
}

function getBaseUrlAccountAPI() {
    return getBaseUrlAPIV1() + 'account/'
}

function getBaseUrlAPIV1() {
    return window.location.origin + '/api/v1/'
}

function getAccountUrl() {
    return window.location.origin + '/account/' 
}

function getLoginUrl() {
    return getAccountUrl() + 'login/'
}

