import Vue from 'vue'

function concanateSting ({ offset, limit }) {
  let url = '/games'
  if (offset || limit) {
    url += '?'
    if (offset) url += 'offset=' + offset + '&'
    if (limit) url += 'limit=' + limit
  }
  return url
}

export default {
  state: {
    games: [],
    ratedGames: []
  },
  mutations: {
    resetGames (state) {
      state.games = []
      state.ratedGames = []
    },
    setRatedGames (state, games) {
      state.ratedGames = games
    },
    addGames (state, games) {
      // All games that are not already in the list
      state.games.push(
        ...games.filter(
          game => !state.games.find(
            g => g.id === game.id)))
    }
  },
  actions: {
    async retrieveGames ({ commit }, { offset, limit }) {
      try {
        const res = await Vue.prototype.$http.get(
          concanateSting({ offset, limit }))
        commit('addGames', res.data.games)
      } catch (err) {
        commit('authError', err.message)
      }
    },
    async loadNext ({ dispatch, getters }) {
      await dispatch('retrieveGames',
        { offset: getters.range.max, limit: 10 })
    },
    async loadPrev ({ dispatch, getters }) {
      await dispatch('retrieveGames',
        { offset: getters.range.min - 2, limit: 1 })
    },
    async retrieveGamesRatedByUser ({ commit, rootState, dispatch }) {
      await dispatch('retrieveUserData')
      const ratedGames = []
      rootState.userData.userData.ratings.forEach(async rating => {
        try {
          const res = await Vue.prototype.$http.get('/games/' + rating.game_id)
          ratedGames.push(res.data.game)
        } catch (err) {
          commit('authError', err.message)
        }
      })
      commit('setRatedGames', ratedGames)
    }
  },
  getters: {
    games: state => state.games,
    sortedGames: state => state.games.sort((a, b) => a.id - b.id),
    range: state => {
      return { max: Math.max(...state.games.map(o => o.id), 0),
        min: Math.min(...state.games.map(o => o.id), Number.MAX_SAFE_INTEGER) }
    },
    ratedGames: state => state.ratedGames
  }
}
