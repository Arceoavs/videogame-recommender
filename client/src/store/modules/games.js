import Vue from 'vue'

function concanateSting (offset, limit) {
  let base = '/games'
  if (offset || limit) {
    base += '?'
    if (offset) base += 'offset=' + offset + '&'
    if (limit) base += 'limit=' + limit
  }
  return base
}
export default {
  state: {
    games: []
  },
  mutations: {
    resetGames (state) {
      state.games = []
    },
    setGames (state, games) {
      state.games = games
    }
  },
  actions: {
    async retrieveGames ({ commit }, offset, limit) {
      try {
        const res = await Vue.prototype.$http.get(concanateSting(offset, limit))
        commit('setGames', res.data.data)
      } catch (err) {
        commit('authError', err.message)
      }
    }
  },
  getters: { games: state => state.games }
}
