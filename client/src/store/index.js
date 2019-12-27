import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    statis: '',
    token: localStorage.getItem('token') || '',
    user: {}
  },
  mutations: {
    authRequest (state) {
      state.status = 'loading'
    },
    authSuccess (state, token) {
      state.status = 'success'
      state.token = token
    },
    authError (state, err) {
      state.status = err
    },
    logout (state) {
      state.status = ''
      state.token = ''
    }
  },
  actions: {
    async login ({ commit }, user) {
      commit('authRequest')
      try {
        const res = await Vue.prototype.$http.post('/login', user)
        const token = res.data.access_token
        localStorage.setItem('token', token)
        commit('authSuccess', token)
      } catch (err) {
        commit('authError', err)
        localStorage.removeItem('token')
      }
    },

    async register ({ commit }, user) {
      commit('authRequest')
      try {
        const res = await Vue.prototype.$http.post('/register', user)
        const token = res.data.access_token
        localStorage.setItem('token', token)
        commit('authSuccess', token)
      } catch (err) {
        commit('authError', err)
        localStorage.removeItem('token')
      }
    },

    logout ({ commit }) {
      commit('logout')
      localStorage.removeItem('token')
      delete Vue.prototype.$http.defaults.headers.common['Authorization']
    }
  },
  getters: {
    loggedIn: state => !!state.token,
    authStatus: state => state.status
  },
  modules: {
  }
})
