<template lang="pug">
v-img(:aspect-ratio="4/3"
  src="@/assets/keyboard.jpg"
  gradient="0.5turn, rgba(18, 18, 18, 1) 50%, rgba(0,0,0,0)")
  v-container
    v-row(justify="center" align="start")
      v-col(cols="12")
        h1.display-2.font-weight-bold
          | Recommend

    OnboardingFirst#OnboardingNeeded(v-if="onboarding")
    #OnboardingDone.mt-2(v-else)
      #RecommendationsLoaded(v-if="recommendationsLoaded")
        v-row(justify="center" align="center")
          v-col(cols="12" sm="8")
            h2.display-1
              | The games you might want to try
          v-col(cols="6" sm="4" align="end")
            v-btn(@click="$store.dispatch('retrieveRecommendations')"
              color="primary")
              v-icon.mr-2 mdi-refresh
              | Refresh

        v-row(justify="center" align="start")
          v-col(v-for="recommendation in recommendations"
            cols="12" sm="8" md="6" lg="4")
            GameCard(:game="recommendation"
              dismissible)
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
      'recommendationsLoaded'])
  },
  mounted () {
    this.$store.dispatch('retrieveRecommendations')
  }
}
</script>
