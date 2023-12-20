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
            return response.json()
                .then(json => ({ json, status: response.status, response }));
        });
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

