import Vue from 'vue'
export default {
  state: {
    platforms: []
  },
  mutations: {
    resetPlatforms (state) {
      state.platforms = []
    },
    setPlatforms (state, platforms) {
      state.platforms = platforms
    }
  },
  actions: {
    async retrievePlatforms ({ commit }) {
      try {
        const res = await Vue.prototype.$http.get('/platforms')
        commit('setPlatforms', res.data.platforms)
      } catch (err) {
        commit('authError', err.message)
      }
    }
  },
  getters: {
    platforms: state => state.platforms
    // Descending order by count
    // sortedPlatforms: state => state.platforms.sort((a, b) => b.count - a.count)
  }
}
