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

    v-row#OnboardingDone.mt-2(v-else justify="center" align="start")
      v-col(cols="12")
        h2.display-1
          | The games you might want to try
</template>

<script>
import { mapGetters } from 'vuex'
import OnboardingFirst from '@/components/recommendations/OnboardingFirst'

export default {
  name: 'Recommendations',
  components: { OnboardingFirst },
  computed: {
    ...mapGetters(['onboarding',
      'neededRatingsAmount'])
  }
}
</script>
