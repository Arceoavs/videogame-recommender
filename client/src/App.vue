<template lang="pug">
v-app(:style="{background: $vuetify.theme.themes[theme].background}")
  Navbar
  v-content
    router-view
  Footer
</template>

<script>

import Navbar from './components/navigation/Navbar'
import Footer from './components/Footer'

export default {
  name: 'App',
  components: { Navbar, Footer },
  computed: {
    theme () {
      return this.$vuetify.theme.dark ? 'dark' : 'light'
    }
  },
  created () {
    this.$http.interceptors.response.use(undefined, err => {
      if (err.status === 401 && err.config && !err.config.__isRetryRequest) { this.$store.dispatch('logout') }
      throw err
    })
  }
}
</script>
