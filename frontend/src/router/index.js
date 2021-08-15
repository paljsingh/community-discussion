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

import Vue from 'vue'
import Router from 'vue-router'
import 'semantic-ui-css/semantic.min.css'

import Home from '@/components/Home'
import Profile from '@/components/Profile'
import Users from '@/components/Users'
import UserGroups from '@/components/UserGroups'
import Communities from '@/components/Communities'
import Dashboard from '@/components/Dashboard'

import { OktaAuth } from '@okta/okta-auth-js'
import OktaVue, { LoginCallback } from '@okta/okta-vue'
import authConfig from '@/config'

Vue.use(Router)

const oktaAuth = new OktaAuth(authConfig.oidc)

Vue.use(OktaVue, { oktaAuth })

const router = new Router({
  mode: 'history',
  routes: [
    {
      // handles OAuth callback
      path: '/login/callback',
      component: LoginCallback
    },
    // default path
    {
      path: '/',
      component: Home,
    },
    {
      path: '/communities',
      component: Communities,
      meta: { 'isLoggedIn': true},
    },
    {
      path: '/usergroups',
      component: UserGroups,
      meta: { 'isLoggedIn': true},
    },
    {
      path: '/users',
      component: Users,
      meta: { 'isLoggedIn': true},
    },
    {
      path: '/dashboard',
      component: Dashboard,
      meta: { 'isLoggedIn': true, 'isOktaUser': true },
    },
    {
      path: '/profile',
      component: Profile,
      meta: { 'isLoggedIn': true},
    }
  ]
})


router.beforeEach(async (to, from, next) => {
  if (to.matched.some((record) => record.meta.isLoggedIn)) {
      if (isAuthenticated()) {
          next()
      } else {
          next('/')
      }
  } else {
      next()
  }
})

function isAuthenticated() {
  let authenticated = false
  if(localStorage.getItem('dummy-jwt-token')) {
      authenticated = true
  } else if (localStorage.getItem('okta-token-storage')) {
      authenticated = true
  }
  return authenticated
}

export default router;