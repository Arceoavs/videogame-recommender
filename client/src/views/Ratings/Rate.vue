<template lang="pug">
#ratings
  Particles
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
        v-col(cols="12" lg="3" md="3")
          v-text-field(outlined
            dense
            clearable
            prepend-inner-icon="mdi-magnify"
            placeholder="Search for games")

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
            placeholder="Filter genres")

      v-row(justify="start" align="center"
        v-if="!gamesLoaded")
        v-col
          v-progress-linear(indeterminate
            color="primary")

      #gamesLoaded(v-else)
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
        v-col(cols="6")
          p.font-weight-light.title
            | The more games you rate, the better the recommendations get!
          v-btn(outlined
            color="primary"
            :to="{name: 'existingRatings'}")
            v-icon.mr-2 mdi-star
            | Show rated games
</template>

<script>
import { mapGetters } from 'vuex'
import Swiper from '@/components/games/Swiper'
import Particles from '@/components/Particles'

export default {
  name: 'Ratings',
  components: {
    Swiper,
    Particles
  },
  data () {
    return {
      selectedGenres: [],
      selectedPlatforms: []
    }
  },
  computed: {
    ...mapGetters(['sortedGames',
      'range',
      'genres',
      'gamesLoaded',
      'ratings',
      'platforms',
      'neededRatingsAmount',
      'onboarding'])
  },
  mounted () {
    this.$store.dispatch('retrieveGames', { limit: 10 })
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
</style>
