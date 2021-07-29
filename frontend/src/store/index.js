import Vue from 'vue'
import Vuex from 'vuex'
import account from './account'
import createPersistedState from "vuex-persistedstate";

Vue.use(Vuex);

const store = new Vuex.Store({
  modules: {
    account,
  },
  plugins: [createPersistedState()]
});

export default store