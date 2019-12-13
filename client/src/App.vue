<template lang="pug">
v-app(:style="{background: $vuetify.theme.themes[theme].background}")
  Navbar
  v-content
    router-view
</template>

<script>

import Navbar from './components/navigation/Navbar'

export default {
  name: 'App',
  components: { Navbar },
  data: () => ({
    //
  }),
  computed: {
    theme () {
      console.log(this.$vuetify.theme.themes['dark'])
      return this.$vuetify.theme.dark ? 'dark' : 'light'
    }
  }
}
</script>
