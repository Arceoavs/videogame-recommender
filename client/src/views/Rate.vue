<template lang="pug">
v-container
  v-row(justify="center" align="start")
    v-col(cols="12")
      h1.display-2.font-weight-bold Ratings

  v-row(justify="center" align="start")
    v-col(cols="12")
      h2.display-1 Rate new games

  v-row(justify="center" align="start")
    v-col(cols="6")
      v-autocomplete(outlined
        dense
        prepend-inner-icon="mdi-gamepad-variant-outline"
        v-model="selectedGenres"
        :items="sortedGenres"
        item-text="name"
        item-value="id"
        chips
        small-chips
        multiple
        placeholder="Filter genres")

    v-col(cols="6")
      v-text-field(outlined
        dense
        clearable
        prepend-inner-icon="mdi-magnify"
        placeholder="Search for games")

  v-row(justify="start" align="center")
    v-col(cols="12")
      Swiper(ref="swiperNewRatings"
        @reachEnd="$store.dispatch('loadNext')"
        @reachBeginning="$store.dispatch('loadPrev')"
        :slidesPerView="3"
        :spaceBetween="30"
        :games="sortedGames")

  v-row(justify="start" align="center")
    v-col(align="center")
      v-icon mdi-chevron-left
    v-col(align="center")
      p.font-weight-light.font-italic
        | Swipe left and right
    v-col(align="center")
      v-icon mdi-chevron-right

  v-row.mt-2(justify="center" align="start")
    v-col(cols="12")
      h2.display-1 Your ratings

  v-row(justify="start" align="center")
    v-col(cols="12")
      Swiper(ref="swiperOldRatings"
        :slidesPerView="3"
        :spaceBetween="30"
        :games="ratedGames")

  v-row(justify="start" align="center")
    v-col(align="center")
      v-icon mdi-chevron-left
    v-col(align="center")
      p.font-weight-light.font-italic
        | Swipe left and right
    v-col(align="center")
      v-icon mdi-chevron-right
</template>

<script>
import { mapGetters } from 'vuex'
import Swiper from '@/components/games/Swiper'

export default {
  name: 'Ratings',
  components: {
    Swiper
  },
  data () {
    return {
      selectedGenres: [] }
  },
  computed: {
    ...mapGetters(['sortedGames', 'range', 'sortedGenres', 'ratedGames', 'ratings'])
  },
  mounted () {
    this.$store.dispatch('retrieveGames', { limit: 10 })
    this.$store.dispatch('retrieveGenres')
    this.$store.dispatch('retrieveGamesRatedByUser')
  }
}
</script>

<style scoped>
.primary-border {
    border-radius: 5px;
    box-shadow:
        0 0 20px #FFC107;
}
</style>
