import Vuex from 'vuex'
import Vue from 'vue'

Vue.use(Vuex)

const store = new Vuex.Store({
    state: {
      token: ''
    },
    mutations: {
      setToken (state, data) {
        state.token = data
      }
    }
  })

export default store;
  