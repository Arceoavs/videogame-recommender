<template lang="pug">
v-card.card-outter(color="dp1"
  outlined
  height="500px"
  :elevation="elevation")
  v-img.mx-auto(v-if="game.image_url"
    :src="game.image_url"
    height="200")

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

  v-card-actions.card-actions.text-center.font-weight-light(v-if="rateable")
    | Rate this game:
    .mx-2 ({{rating}})
    v-rating(v-model="rating"
      background-color="primary"
      color="yellow accent-4"
      dense
      hover
      size="18"
      @input="rate")

  v-card-actions.card-actions(v-if="dismissible")
    v-btn.ml-3(color="error"
      outlined
      @click="dismiss")
      v-icon mdi-close
      | Dismiss

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
    game: { type: Object, default: null },
    dismissible: { type: Boolean, default: false },
    rateable: { type: Boolean, default: false },
    elevation: { type: Number, default: 0 }
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
    async dismiss () {
      try {
        await this.$http.post('/rate', {
          game_id: this.game.id,
          exclude: true
        })
      } catch (err) {

      } finally {
        this.$store.commit('hideRecommendation', this.game.id)
        await this.afterRated()
      }
    },
    async rate () {
      try {
        await this.$http.post('/rate', {
          game_id: this.game.id,
          value: this.rating
        })
      } catch (err) {

      } finally {
        await this.afterRated()
      }
    },
    async afterRated () {
      this.$emit('rated')
      await this.$store.dispatch('retrieveGamesRatedByUser')
      await this.$store.dispatch('retrieveUserData')
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