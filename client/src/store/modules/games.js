import Vue from 'vue'

function buildArgsString (args) {
  let url = '/games?'
  if (args.offset) url += 'offset=' + args.offset + '&'
  if (args.limit) url += 'limit=' + args.limit + '&'
  if (args.search) url += 'search=' + args.search + '&'
  if (args.genres && args.genres.length) {
    url += 'genres=' + args.genres + '&'
  }
  if (args.platforms && args.platforms.length) {
    url += 'platforms=' + args.platforms + '&'
  }
  return url
}

export default {
  state: {
    games: [],
    ratedGames: [],
    args: {
      offset: 0,
      limit: 10,
      search: null,
      genres: null,
      platforms: null
    }
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
    },
    setGames (state, games) {
      state.games = games
    },
    setPlatformFilter (state, platforms) {
      state.args.platforms = platforms
    },
    setGenresFilter (state, genres) {
      state.args.genres = genres
    },
    setSearchFilter (state, search) {
      state.args.search = search
    },
    setOffset (state, offset) {
      state.args.offset = offset
    },
    setLimit (state, limit) {
      state.args.limit = limit
    }
  },
  actions: {
    search ({ commit, dispatch }, search) {
      commit('resetGames')
      commit('setOffset', 0)
      commit('setSearchFilter', search)
      dispatch('retrieveGames')
    },
    filterPlatforms ({ commit, dispatch }, platforms) {
      commit('resetGames')
      commit('setOffset', 0)
      commit('setPlatformFilter', platforms)
      dispatch('retrieveGames')
    },
    filterGenres ({ commit, dispatch }, genres) {
      commit('resetGames')
      commit('setOffset', 0)
      commit('setGenresFilter', genres)
      dispatch('retrieveGames')
    },
    async retrieveGames ({ commit, state }) {
      try {
        const res = await Vue.prototype.$http.get(
          buildArgsString(state.args))
        commit('addGames', res.data.games)
      } catch (err) {
        commit('authError', err.message)
      }
    },
    async loadNext ({ commit, dispatch, state }) {
      commit('setLimit', 10)
      commit('setOffset', state.args.offset + state.args.limit)
      dispatch('retrieveGames')
    },
    async loadPrev ({ commit, dispatch, state }) {
      commit('setLimit', 1)
      commit('setOffset', state.args.offset - 1 - state.args.limit)
      dispatch('retrieveGames')
    },
    async retrieveGamesRatedByUser ({ commit, rootState, dispatch }) {
      await dispatch('retrieveUserData')
      const ratedGames = []
      rootState.userData.userData.ratings.forEach(async rating => {
        try {
          const res = await Vue.prototype.$http.get('/games/' + rating.game_id)
          res.data.game.user_rating = rating.value
          res.data.game.excluded = rating.exlude_from_model
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
    gamesLoaded: state => state.games
      ? !!state.games.length
      : false,
    sortedGames: state => state.games.sort((a, b) => a.id - b.id),
    range: state => {
      return { max: Math.max(...state.games.map(o => o.id), 0),
        min: Math.min(...state.games.map(o => o.id), Number.MAX_SAFE_INTEGER) }
    },
    ratedGames: state => state.ratedGames.filter(g => !g.excluded),
    excludedGames: state => state.ratedGames.filter(g => g.excluded)
  }
}
