<template lang="pug">
#noOnboardingYet
  v-row(justify="center" align="start")
    v-col(cols="12")
      h2.display-1 Please finish the onboarding process first!
  v-row
    v-col
      p.font-weight-light.title
        span You still have to rate
        span.mx-1.font-weight-bold.primary--text {{neededRatingsAmount}}
        span games in order to get recommendations!
  v-row
    v-col
      .font-weight-light.text-justify
        p
          | Welcome to the Video Game Recommender.
          | We use a data-driven approach to deliver you the best recommendations possible.
          | Our mission is to keep you playing forever.
          | This is your life now.
          | Enjoy.
        p
          | To give you the best recommendations possible, we need to know what kind of games you have
          | liked in the past. That way, we can suggest you the games that fit your specific user
          | profile. You still need to rate {{neededRatingsAmount}} games!

  v-row
    v-col
      v-btn(large
        color="primary"
        outlined
        :to="{name: 'rate'}")
        | To the ratings!
</template>

<script>
import { mapGetters } from 'vuex'
export default {
  name: 'OnboardingFirst',
  computed: {
    ...mapGetters(['neededRatingsAmount'])
  }
}
</script>
