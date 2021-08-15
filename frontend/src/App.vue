<template>
  <div id="app">
    <div class="ui inverted top fixed menu">
      
      <router-link to="/" class="header item">
        <img class="ui mini image" src="./assets/logo.png" />
      </router-link>

      <router-link v-if="!this.isLoggedIn" to="/login" class="header item">
        <a class="item" v-on:click="login()">Login</a>
      </router-link>
      
      <router-link v-if="this.isLoggedIn" to="/profile" class="header item">
        <a class="item">Profile > {{this.username}} </a>
      </router-link>

      <router-link v-if="this.isLoggedIn" to="/communities" class="header item">
        <a class="item">Communities</a>
      </router-link>

      <router-link v-if="this.isLoggedIn" to="/usergroups" class="header item">
        <a class="item">User Groups</a>
      </router-link>

      <router-link v-if="this.isLoggedIn" to="/users" class="header item">
        <a class="item">Users</a>
      </router-link>

      <router-link v-if="this.isLoggedIn && this.usertype==='okta'" to="/dashboard" class="header item">
        <a class="item">Dashboard</a>
      </router-link>

      <router-link v-if="this.isLoggedIn && this.usertype==='okta'" to="/admin" class="header item">
        <a class="item">Admin Console</a>
      </router-link>

      <router-link v-if="this.isLoggedIn" to="/" class="header item">
        <a class="item" v-on:click="logout()">Logout</a>
      </router-link>

    </div>
    <div class="ui text " style="margin-top: 7em;">
      <router-view />
    </div>
  </div>
</template>

<script>
import authHelper from './helpers/auth.js'


export default {
  name: "app",
  mixins: [authHelper],
  methods: {
    login () {
      this.$auth.signInWithRedirect({ originalUri: '/' })
    },
    async logout () {
        if (this.usertype === "okta") {
            await this.$auth.signOut()
            localStorage.removeItem('okta-cache-storage');
            localStorage.removeItem('okta-token-storage');
            document.cookie = 'okta-oauth-state' +'=; Path=/; Expires=Thu, 01 Jan 1970 00:00:01 GMT;';
        } else {
              localStorage.removeItem('dummy-jwt-token');
        }
        localStorage.removeItem('claims');
        localStorage.removeItem('usertype');
        this.force_update
        this.$router.push('/')
        this.$router.go()
    }
  }
};
</script>
