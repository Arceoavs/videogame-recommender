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

      GameFilter

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
      v-row.mt-2(justify="center" align="center")
        v-col(cols="12" sm="6"
          align="center")
          h2.display-1 Your ratings
          v-btn.mt-3(outlined
            color="primary"
            :to="{name: 'existingRatings'}")
            v-icon.mr-2 mdi-star
            | Show rated games

        v-col(cols="12" sm="6"
          align="center")
          h2.display-1 Excluded games
          v-btn.mt-3(outlined
            color="primary"
            :to="{name: 'excludedRatings'}")
            v-icon.mr-2 mdi-close
            | Show excluded games

</template>

<script>
import { mapGetters } from 'vuex'
import Swiper from '@/components/games/Swiper'
import Particles from '@/components/Particles'
import GameFilter from '@/components/games/GameFilter'

export default {
  name: 'Ratings',
  components: {
    Swiper,
    Particles,
    GameFilter
  },
  computed: {
    ...mapGetters(['sortedGames',
      'gamesLoaded',
      'ratings',
      'neededRatingsAmount',
      'onboarding'])
  },
  mounted () {
    this.$store.commit('resetGames')
    this.$store.commit('resetFilter')
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
