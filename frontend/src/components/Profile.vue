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
  <div class="profile">
    <table class="ui table">
      <thead>
        <tr>
          <th>Claim</th>
          <th>Value</th>
        </tr>
      </thead>
      <tbody>
        <tr
          v-for="(claim, index) in this.claims"
          :key="index"
        >
          <td>{{claim.claim}}</td>
          <td :id="'claim-' + claim.claim">{{claim.value}}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import authHelper from '../helpers/auth.js';

export default {
  name: 'Profile',
  mixins: [authHelper],
  async created() {
    if (this.usertype === "okta" && this.claims == null) {
      let idToken = await this.$auth.tokenManager.get('idToken')
      let claims = await Object.entries(idToken.claims).map(entry => ({ claim: entry[0], value: entry[1] }))
      localStorage.setItem('claims', JSON.stringify(claims));
      this.force_update
    }
  }
}
</script>

<style scoped>
.profile {
    position: fixed;
    width: 800px;
    left: 200px;
    top: 70px;
}
</style>