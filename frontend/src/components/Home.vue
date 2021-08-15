<template>
  <div class="home" v-if="!this.isLoggedIn">
    <div class="logo">
      <img class="image" src="@/assets/logo.png" />
    </div>
    <div class="content">
      <p>
        The c18n app is a PoC app to demonstrate <br/>
        a community discussion platform using the <br/>
        stream processing applications.<br/>
      </p>
      <v-btn v-on:click="login()">
        Login with Okta
      </v-btn>
      <v-tooltip bottom>
        <template v-slot:activator="{ on, attrs }">
          <v-icon color="primary" dark v-bind="attrs" v-on="on">mdi-information</v-icon>
        </template>
        <p>
          Users authenticated with okta sso are treated as admin users.
          <br/>
          Admin users can access the dashboard and create communities, user groups and dummy users.
        </p>
      </v-tooltip>

      <p>or</p>

      <div data-app>
        <div class="elem">
          <v-text-field dark ref="jwt_token" label="Paste JWT Token" outlined clearable ></v-text-field>
          <v-btn v-on:click="login_dummy()">
            Impersonate a Dummy User
          </v-btn>
          <v-tooltip bottom>
            <template v-slot:activator="{ on, attrs }">
              <v-icon color="primary" dark v-bind="attrs" v-on="on">mdi-information</v-icon>
            </template>
            <p>
              Dummy users are fake users with randomized ids and auto-generated JWT tokens.<br/>
              The backend application assigns these users with role having limited capabilities<br/>
              (e.g. send direct messages to other users or user groups.)<br/>
              The JWT tokens of the dummy users are visible to the admin user on the dashboard.<br/>
              It is advisable to use an 'incognito window' for impersonating multiple dummy users.
            </p>
          </v-tooltip>
        </div>
      </div>
    </div>  <!-- div class="content" -->
  </div>  <!-- home -->
</template>

<script>
import authHelper from '../helpers/auth.js';
import { decodeToken } from "@okta/okta-auth-js";

export default {
  name: 'home',
  mixins: [authHelper],
  methods: {
    async login () {
      await this.$auth.signInWithRedirect({ originalUri: '/profile' })
      localStorage.setItem('usertype', "okta");
    },
    login_dummy () {
      let dummy_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJuYW1lIjoiRWxpemFiZXRoIEJhbmtzIiwic3ViIjoiNzdlYjBiZTAtMDU5MC00ZmIwLWFhN2EtNjA4OWUyYmFkZmY1IiwiZW1haWwiOiJlbGl6YWJldGhfYmFua3NAbG9jYWxob3N0Iiwicm9sZSI6InVzZXIiLCJ2ZXIiOjEsImlzcyI6InB5dGhvbi9mbGFzayIsImlhdCI6MTYyODgzMzI0NC43ODU5MzUsImV4cCI6MTYyOTQzODA0NC43ODU5NDF9.shXLAM0M7iZ4a2fP9o4glZspslcwNHRyRLVN7DufQfQ'
      let decoded = decodeToken(dummy_token);
      if (parseInt(Date.now()/1000) < parseInt(decoded.payload.exp)) {
          let claims = [
              {'claim': 'name', 'value': decoded.payload.name},
              {'claim': 'email', 'value': decoded.payload.email},
              {'claim': 'sub', 'value': decoded.payload.sub},
              {'claim': 'iss', 'value': decoded.payload.iss},
              {'claim': 'iat', 'value': decoded.payload.iat},
              {'claim': 'exp', 'value': decoded.payload.exp},
          ]
          // save the token.
          localStorage.setItem('dummy-jwt-token', dummy_token);
          localStorage.setItem('claims', JSON.stringify(claims));
          localStorage.setItem('usertype', "dummy");
          this.force_update
          this.$router.push('/profile')
          this.$router.go()
      } else {
          console.log("token has expired")
      }
    }
  }
}

</script>

<style scoped>
.home {
    text-align: left;
    width: 100%;
    height: 1000px;
}
.home .content {
    position: relative;
    float: left;
    margin-left: 50px;
    width: 60%;
}
.home .logo {
    position: relative;
    width: 400px !important;
    float: right;
    width: 40%;
    margin-right: 50px;
}
img {
    max-width:100%;
    max-height:100%;
}
</style>