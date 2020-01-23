<template lang="pug">
v-img(height="100%"
  src="@/assets/keyboard.jpg"
  gradient="0.5turn, rgba(18, 18, 18, 1) 50%, rgba(0,0,0,0)")
  v-container
    v-row(justify="center" align="start")
      v-col(cols="12")
        h1.display-2.font-weight-bold
          | Recommendations

    OnboardingFirst#OnboardingNeeded(v-if="onboarding")

    #OnboardingDone.mt-2(v-else)
      #RecommendationsLoaded(v-if="recommendationsLoaded")
        v-row(justify="center" align="center")
          v-col(cols="12" sm="8")
            h2.display-1
              | The games you might want to try
            p.mt-1.font-weight-light.title
              | If you already habe played a game of the list, just give it a rating.
          v-col(cols="6" sm="4" align="end")
            v-btn(@click="reretrieve"
              color="primary"
              outlined)
              v-icon.mr-2 mdi-refresh
              | Refresh

        v-row(justify="center" align="start")
          v-col(v-for="recommendation in recommendations"
            :key="recommendation.id"
            cols="12" sm="8" md="6" lg="4")
            v-hover(v-slot:default="{ hover }")
              GameCard(:game="recommendation"
                :elevation="hover ? 22 : 1"
                dismissible)

        v-row(justify="start" align="start")
          v-col
            p.font-weight-light.title
              | These are all the recommendations we can show you at this moment.

      #Loading(v-else)
        v-row(justify="start" align="center")
          v-col(cols="12")
            h2.display-1
              | Calculating recommendations
            p.mt-1.font-weight-light.title
              | Please be patient.
        v-row(justify="center" align="center")
          v-progress-circular(color="primary"
            indeterminate
            size="80"
            width="8")

</template>

<script>
import { mapGetters } from 'vuex'
import OnboardingFirst from '@/components/recommendations/OnboardingFirst'
import GameCard from '@/components/games/GameCard'

export default {
  name: 'Recommendations',
  components: { OnboardingFirst,
    GameCard },
  computed: {
    ...mapGetters(['onboarding',
      'neededRatingsAmount',
      'recommendations',
      'excludedRatings',
      'recommendationsLoaded']),
    filteredRecommendations () {
      return this.recommendations.filter(rec => !this.excludedRatings.includes(rec))
    }
  },
  async mounted () {
    await this.reretrieve()
  },
  methods: {
    async reretrieve () {
      await this.$store.commit('resetRecommendations')
      await this.$store.dispatch('retrieveRecommendations')
    }
  }
}
</script>
