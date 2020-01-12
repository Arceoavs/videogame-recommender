import Vue from 'vue'
export default {
  state: {
    genres: []
  },
  mutations: {
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
    genres: state => state.genres,
    // Descending order by count
    sortedGenres: state => state.genres.sort((a, b) => b.count - a.count)
  }
}
