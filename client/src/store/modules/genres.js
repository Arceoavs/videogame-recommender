import Vue from 'vue'
export default {
  state: {
    genres: []
  },
  mutations: {
    resetGenres (state) {
      state.genres = []
    },
    setGenres (state, genres) {
      state.genres = genres
    }
  },
  actions: {
    async retrieveGenres ({ commit, dispatch }) {
      try {
        const res = await Vue.prototype.$http.get('/genres')
        commit('setGenres', res.data.genres)
      } catch (err) {
        commit('authError', err.message)
      }
    }
  },
  getters: {
    genres: state => state.genres
  }
}
