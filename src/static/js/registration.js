function submitSingUp(event){
    var form = document.getElementById('singUpform')
    
    var password = document.getElementById('id_password1').value
    if (password != document.getElementById('id_password2').value){
        var errorMessage = 'The two password fields didn’t match.'
        alert_bootstrap(errorMessage, 'danger', 'singUpErrors')
        form.reset()
        return
    } 
    
    body = {
        'username': document.getElementById('id_username').value,
        'password': password,
    }
    var data = {
        method: "POST",
        body: JSON.stringify(body),
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken()
        }
    }

    var apiRegister = new Request(getBaseUrlAPIV1() + 'register/')

    apiRequestPost(apiRegister, data).then( response => {
        if (response.status != 201) {
            json = response.json
            Object.keys(body).forEach(key => {
                if (json.hasOwnProperty(key)) {
                    alert_bootstrap(json[key], 'danger', 'singUpErrors')
                }
            });
            console.log(json)
        }else {
            window.location.href = getLoginUrl()
        }
    })

}