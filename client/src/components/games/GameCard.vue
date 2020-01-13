<template lang="pug">
v-card.card-outter(color="dp1"
  outlined
  height="500px")
  v-skeleton-loader(class="mx-auto"
    type="image")

  v-card-title
    .overline.mr-3(v-for="platform in game.platforms"
      :key="platform.id")
      | {{platform.name}}

  v-card-title
    | {{game.title}}
    .font-weight-light.ml-2 ({{game.year}})
    v-btn(color="primary"
      icon
      @click="dialog=true")
      v-icon mdi-information-variant

  v-card-text
    .mr-7
      v-chip.mx-1.my-1(v-for="genre in game.genres"
        :key="genre.id"
        color="primary"
        label
        outlined
        small)
        | {{genre.name}}

  v-card-actions.card-actions.text-center.font-weight-light
    | Rate this game:
    .mx-2 ({{rating}})
    v-rating(v-model="rating"
      background-color="primary"
      color="yellow accent-4"
      dense
      hover
      size="18"
      @input="rate")

  v-dialog(v-model="dialog"
    width="500")
    GameDetails(:title="game.title"
      :description="game.description"
      @close="dialog=false")
</template>

<script>
import GameDetails from '@/components/games/GameDetails'
import { mapGetters } from 'vuex'

export default {
  name: 'GameCard',
  components: {
    GameDetails
  },
  props: {
    game: { type: Object, default: null }
  },
  data () {
    return {
      rating: 0,
      dialog: false
    }
  },
  computed: {
    ...mapGetters(['ratings'])
  },
  mounted () {
    this.ratings.forEach(rating => {
      if (rating.game_id === this.game.id) { this.rating = rating.value / 2 }
    })
  },
  methods: {
    async rate () {
      try {
        await this.$http.post('/rate', {
          game_id: this.game.id,
          value: this.rating
        })
      } catch (err) {
        console.log(err)
      } finally {
        this.$emit('rated')
        await this.$store.dispatch('retrieveGamesRatedByUser')
        await this.$store.dispatch('retrieveUserData')
      }
    },
    alreadyRated () {
      this.ratings.forEach(rating => {
        if (rating.game_id === this.game.id) return true
      })
      return false
    }
  }
}
</script>

<style scoped>
.card-outter {
  position: relative;
  padding-bottom: 50px;
}
.card-actions {
  position: absolute;
  bottom: 0;
}
</style>
