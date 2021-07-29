import { decodeToken } from "@okta/okta-auth-js";

export default {
    computed: {
        token() {
            let t = this.$store.state.account.token;
            return t;
        },
        username() {
            let c = this.$store.state.account.claims;
            console.log("username/claims - ", this.$store.state.account)
            if (c) {
                for (let i=0; i<c.length; i++) {
                    console.log("username - ", c[i])
                    if (c[i].claim === 'name') {
                        return c[i].value;
                    }
                }
            } else {
                return ""
            }
        }
    },
    methods: {
        async login() {
            this.$auth.signInWithRedirect('/');
            let okta_token = this.authState.accessToken.accessToken;
            this.$store.commit('login', okta_token);

            this.claims = await Object.entries(await this.$auth.getUser()).map(entry => ({ claim: entry[0], value: entry[1] }))
            this.$store.commit('claims', this.claims)      

            this.$store.commit("usertype", "okta")
        },
        login_dummy() {
            let dummy_token = this.$refs.jwt_token.lazyValue;
            this.$store.commit('login', dummy_token);

            let decoded = decodeToken(dummy_token);
            this.claims = [
                {'claim': 'name', 'value': decoded.payload.name},
                {'claim': 'email', 'value': decoded.payload.email},
                {'claim': 'sub', 'value': decoded.payload.sub},
                {'claim': 'iss', 'value': decoded.payload.iss},
                {'claim': 'iat', 'value': decoded.payload.iat},
                {'claim': 'exp', 'value': decoded.payload.exp},
              ]
            this.$store.commit('claims', this.claims)      

            this.$store.commit("usertype", "dummy")        
        },
        logout() {
            this.$store.commit('logout')
        }
    }
};
