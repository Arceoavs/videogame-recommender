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
  data: () => ({
    //
  }),
  computed: {
    theme () {
      return this.$vuetify.theme.dark ? 'dark' : 'light'
    }
  }
}
</script>
