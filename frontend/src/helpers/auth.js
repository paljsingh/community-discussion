export default {
    data: function() {
        return {
            force_update_counter: 0
        }
    },
    computed: {
        force_update() {
            this.force_update_counter += 1;
        },
        token() {
            this.force_update_counter;
            if (this.usertype === "dummy") {
                return localStorage.getItem('dummy-jwt-token')
            }
            if (this.usertype === "okta") {
                return this.$auth.tokenManager.get("idToken")
            }
        },
        username() {
            this.force_update_counter;
            let c = this.claims;
            if (c) {
                for (let i=0; i<c.length; i++) {
                    if (c[i].claim === "name") {
                        return c[i].value;
                    }
                }
            } else {
                return ""
            }
        },
        usertype() {
            this.force_update_counter;
            return localStorage.getItem('usertype')
        },
        claims() {
            this.force_update_counter;
            return JSON.parse(localStorage.getItem('claims'))
        },
        isLoggedIn() {
            this.force_update_counter;
            if (this.usertype !== null) {
                return true
            } else {
                return false
            }
        }
    }
};
