function getMe() {
    var request = new Request(getBaseUrlAccountAPI() + 'me/')
    apiRequest(request).then(response => {
        var json = response.json
        document.getElementById('avatar-img').src = json['avatar']
        document.getElementById('username-profile').textContent = json['username']
    })
}