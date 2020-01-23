<template lang="pug">
#youRatings
  Particles
  v-container.foreground
    v-row(justify="center" align="start")
      v-col(cols="12" sm="8")
        h1.display-2.font-weight-bold
          | Your ratings
      v-col(cols="6" sm="4" align="end")
        v-btn(color="primary"
          outlined
          :to="{name: 'rate'}")
          v-icon.mr-2 mdi-arrow-left
          | Back to ratings

    #existingRatings(v-if="ratings && ratings.length")
      v-row(justify="start" align="start")
        v-col(v-for="game in ratedGames"
          :key="game.id"
          cols="12" sm="8" md="6" lg="4")
          v-hover(v-slot:default="{ hover }")
            GameCard(:game="game"
              :elevation="hover ? 22 : 1"
              dismissible)

    #noExistingRatings(v-else)
      v-row(justify="start" align="center")
        v-col
          p.font-weight-light
            | You have not yet rated any games.

    v-row(justify="start" align="start")
      v-col
         p.font-weight-light.title
          | The more games you rate, the better recommendations you get!
</template>

<script>
import { mapGetters } from 'vuex'
import GameCard from '@/components/games/GameCard'
import Particles from '@/components/Particles'

export default {
  name: 'YourRatings',
  components: { GameCard,
    Particles },
  data () {
    return {
      swiperKey: 0 }
  },
  computed: {
    ...mapGetters(['ratedGames',
      'ratings'])
  },
  methods: {
    rerenderSwiper () {
      this.swiperKey += 1
    }
  }
}
</script>
