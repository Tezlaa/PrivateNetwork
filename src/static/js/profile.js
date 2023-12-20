function getMe() {
    var request = new Request(getBaseUrlAccountAPI() + 'me/')
    apiRequest(request).then(json => {
        console.log(json)
    })
}