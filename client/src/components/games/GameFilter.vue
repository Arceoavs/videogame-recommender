<template lang="pug">
v-row#GameFilters.mt-2(justify="space-between" align="center" no-gutters)
  v-col(cols="12" lg="3" md="3")
    v-text-field(outlined
      v-model="searchQuery"
      dense
      clearable
      prepend-inner-icon="mdi-magnify"
      placeholder="Search for games"
      @input="isTyping = true")

  v-col(cols="12" lg="3" md="3" sm="5")
    v-autocomplete(outlined
      dense
      prepend-inner-icon="mdi-gamepad-variant-outline"
      v-model="selectedPlatforms"
      :items="platforms"
      item-text="name"
      item-value="id"
      chips
      small-chips
      multiple
      @change="filterPlatforms"
      placeholder="Filter platforms")

  v-col(cols="12" lg="3" md="3" sm="5")
    v-autocomplete(outlined
      dense
      prepend-inner-icon="mdi-format-list-text"
      v-model="selectedGenres"
      :items="genres"
      item-text="name"
      item-value="id"
      chips
      small-chips
      multiple
      @change="filterGenres"
      placeholder="Filter genres")
</template>

<script>
import { mapGetters } from 'vuex'
import debounce from 'debounce'

export default {
  name: 'GameFilter',
  data () {
    return {
      searchQuery: '',
      isTyping: false,
      selectedGenres: [],
      selectedPlatforms: []
    }
  },
  computed: {
    ...mapGetters(['genres', 'platforms'])
  },
  watch: {
    searchQuery: debounce(function () {
      console.log('true')
      this.isTyping = false
    }, 1000),
    isTyping (value) {
      if (!value) this.filterSearch(this.searchQuery)
    }
  },
  methods: {
    filterPlatforms () {
      this.$store.dispatch('filterPlatforms', this.selectedPlatforms)
    },
    filterGenres () {
      this.$store.dispatch('filterGenres', this.selectedGenres)
    },
    filterSearch () {
      this.$store.dispatch('search', this.searchQuery)
    }
  }
}
</script>
