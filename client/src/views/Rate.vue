<template lang="pug">
#ratings
  vue-particles.particles-js(color="#dedede"
    :particleOpacity="0.7"
    :particlesNumber="80"
    shapeType="circle"
    :particleSize="4"
    linesColor="#dedede"
    :linesWidth="1"
    :lineLinked="true"
    :lineOpacity="0.4"
    :linesDistance="150"
    :moveSpeed="3"
    :hoverEffect="true"
    hoverMode="grab"
    :clickEffect="true"
    clickMode="repulse")
  v-container.foreground
    v-row(justify="center" align="start")
      v-col(cols="12")
        #headlineOnboarding(v-if="onboarding")
          h1.display-2.font-weight-bold
            | Onboarding
          p.font-weight-light.title
            span You still have to rate
            span.mx-1.font-weight-bold.primary--text {{neededRatingsAmount}}
            span games in order to get recommendations!

        h1#headline.display-2.font-weight-bold(v-else)
          | Ratings
    #rateNewGames
      v-row(justify="center" align="start")
        v-col(cols="12")
          h2.display-1
            | Rate new games

      v-row.mt-2(justify="space-between" align="center" no-gutters)
        v-col(cols="12" lg="3" md="3" sm="3")
          v-text-field(outlined
            dense
            clearable
            prepend-inner-icon="mdi-magnify"
            placeholder="Search for games")

        v-col(cols="5" lg="3" md="3" sm="4")
          v-autocomplete(outlined
            dense
            prepend-inner-icon="mdi-gamepad-variant-outline"
            v-model="selectedPlatforms"
            :items="sortedPlatforms"
            item-text="name"
            item-value="id"
            chips
            small-chips
            multiple
            placeholder="Filter platforms")

        v-col(cols="5" lg="3" md="3" sm="3")
          v-autocomplete(outlined
            dense
            prepend-inner-icon="mdi-format-list-text"
            v-model="selectedGenres"
            :items="sortedGenres"
            item-text="name"
            item-value="id"
            chips
            small-chips
            multiple
            placeholder="Filter genres")

      v-row(justify="start" align="center")
        v-col(cols="12")
          Swiper(ref="swiperNewRatings"
            @reachEnd="$store.dispatch('loadNext')"
            @reachBeginning="$store.dispatch('loadPrev')"
            :slidesPerView="3"
            :spaceBetween="30"
            :games="sortedGames"
            :rated="rerenderSwiper")

      v-row(justify="start" align="center")
        v-col(align="center")
          v-icon mdi-chevron-left
        v-col(align="center")
          p.font-weight-light.font-italic
            | Swipe left and right
        v-col(align="center")
          v-icon mdi-chevron-right

    #existingRatings
      v-row.mt-2(justify="center" align="start")
        v-col(cols="12")
          h2.display-1 Your ratings

      v-row(no-gutters)
        v-col
          p.font-weight-light.title
            | The more games you rate, the better the recommendations get!

      #existingRatings(v-if="ratings && ratings.length")
        v-row(justify="start" align="center")
          v-col(cols="12")
            Swiper(ref="swiperOldRatings"
              :slidesPerView="3"
              :spaceBetween="30"
              :games="ratedGames"
              :key="swiperKey")

        v-row(justify="start" align="center")
          v-col(align="center")
            v-icon mdi-chevron-left
          v-col(align="center")
            p.font-weight-light.font-italic
              | Swipe left and right
          v-col(align="center")
            v-icon mdi-chevron-right

      #noExistingRatings(v-else)
        v-row(justify="start" align="center")
          v-col
            p.font-weight-light
              | You have not yet rated any games.
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
      selectedGenres: [],
      selectedPlatforms: [],
      swiperKey: 0
    }
  },
  computed: {
    ...mapGetters(['sortedGames',
      'range',
      'sortedGenres',
      'ratedGames',
      'ratings',
      'sortedPlatforms',
      'neededRatingsAmount',
      'onboarding'])
  },
  mounted () {
    this.$store.dispatch('retrieveGames', { limit: 10 })
    this.$store.dispatch('retrieveGenres')
    this.$store.dispatch('retrievePlatforms')
    this.$store.dispatch('retrieveGamesRatedByUser')
  },
  methods: {
    rerenderSwiper () {
      this.swiperKey += 1
    }
  }
}
</script>

<style scoped>
.primary-border {
    border-radius: 5px;
    box-shadow:
        0 0 20px #FFC107;
}
.particles-js {
  z-index: -1;
  position: fixed; /* Sit on top of the page content */
  width: 100%; /* Full width (cover the whole page) */
  height: 100%; /* Full height (cover the whole page) */
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 0; /* Specify a stack order in case you're using a different order for other elements */
}
</style>
