/*!
 * Copyright (c) 2018-Present, Okta, Inc. and/or its affiliates. All rights reserved.
 * The Okta software accompanied by this notice is provided pursuant to the Apache License, Version 2.0 (the "License.")
 *
 * You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0.
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
 * WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 *
 * See the License for the specific language governing permissions and limitations under the License.
 */
<template>
  <div id="app">
    <div class="ui inverted top fixed menu">
      <router-link to="/" class="header item">
        <img class="ui mini image" src="./assets/logo.png" />
      </router-link>
      <router-link
        to="/login"
        class="header item"
        v-if="!authState.isAuthenticated"
      >
        <a class="item" v-on:click="login()">Login</a>
      </router-link>
      <router-link
        to="/profile"
        class="header item"
        v-if="authState.isAuthenticated"
      >
        <a class="item">Profile</a>
      </router-link>
      <router-link
        to="/dashboard"
        class="header item"
        v-if="authState.isAuthenticated"
      >
        <a class="item">Dashboard</a>
      </router-link>
    </div>
    <div class="ui text container">
      <router-view />
    </div>
  </div>
</template>

<script>
export default {
  name: "app",
  methods: {
    login() {
      this.$auth.signInWithRedirect("/");
    },
    async logout() {
      await this.$auth.signOut();
    },
  },
  mounted: async function() {
      let tokens = await this.$auth.tokenManager.getTokens();
      this.$store.commit('setToken', tokens.accessToken.accessToken)
  }
};
</script>
