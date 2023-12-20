function submitLogin() {
    var username = document.getElementById('id_username').value
    var password = document.getElementById('id_password').value 

    var body = {
        'username': username,
        'password': password,
    }
    var data = {
        'method': 'POST',
        'body': JSON.stringify(body),
    }
    var request = new Request(getBaseUrlAPIV1() + 'token/') 
    apiRequest(request, data).then(response => {
        // TODO: status check, showing errors
        var json = response.json
        console.log(json)
        localStorage.setItem('access', json['access'])
        localStorage.setItem('refresh', json['refresh'])
        document.getElementById('login-form').submit()
    })
}