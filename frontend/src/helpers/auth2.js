function token() {
    if (usertype() === "dummy") {
        return localStorage.getItem('dummy-jwt-token')
    }
    if (usertype() === "okta") {
        return JSON.parse(localStorage.getItem("okta-token-storage"))['accessToken']['value']
    }
}

function username() {
    let c = claims();
    if (c) {
        for (let i=0; i<c.length; i++) {
            if (c[i].claim === "name") {
                return c[i].value;
            }
        }
    } else {
        return ""
    }
}

function usertype() {
    return localStorage.getItem('usertype')
}

function claims() {
    return JSON.parse(localStorage.getItem('claims'))
}

function isLoggedIn () {
    if (usertype()) {
        return true
    } else {
        return false
    }
}

export {isLoggedIn, claims, usertype, username, token}
