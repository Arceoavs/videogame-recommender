import Vue from 'vue'
import Vuex from 'vuex'

// Modules
import games from './modules/games'
import genres from './modules/genres'
import platforms from './modules/platforms'
import userData from './modules/user'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    showSnackbar: false,
    status: '',
    token: localStorage.getItem('token') || '',
    user: {}
  },
  mutations: {
    toggleSnackbar (state) {
      state.showSnackbar = true
    },
    authRequest (state) {
      state.status = 'loading'
    },
    authSuccess (state, token) {
      state.status = 'success'
      state.token = token
      Vue.prototype.$http.defaults.headers.common['Authorization'] = `Bearer ${token}`
      localStorage.setItem('token', token)
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
        commit('authSuccess', token)
      } catch (err) {
        commit('authError', err.message)
        localStorage.removeItem('token')
      } finally {
        commit('toggleSnackbar')
      }
    },

    async register ({ commit }, user) {
      commit('authRequest')
      try {
        const res = await Vue.prototype.$http.post('/registration', user)
        const token = res.data.access_token
        commit('authSuccess', token)
      } catch (err) {
        commit('authError', err)
        localStorage.removeItem('token')
      } finally {
        commit('toggleSnackbar')
      }
    },

    logout ({ commit }) {
      commit('logout')
      commit('resetGenres')
      commit('resetGames')
      commit('resetPlatforms')
      commit('resetUser')
      localStorage.removeItem('token')
      delete Vue.prototype.$http.defaults.headers.common['Authorization']
    }
  },
  getters: {
    loggedIn: state => !!state.token,
    authStatus: state => state.status
  },
  modules: { games, genres, userData, platforms }
})
