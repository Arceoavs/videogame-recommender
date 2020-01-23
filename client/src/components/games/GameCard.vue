<template lang="pug">
v-card.card-outter(color="dp1"
  outlined
  height="500px"
  :elevation="elevation")
  v-img.mx-auto(v-if="game.image_url"
    :src="game.image_url"
    height="200")
    v-row(justify="end"
      no-gutters
      v-if="dismissible")
      v-btn(icon
        color="error"
        large
        @click="dismiss")
        v-icon mdi-close

  v-card-title
    .overline.mr-3(v-for="platform in game.platforms.slice(0,4)"
      :key="platform.id")
      span {{platform.name}}
    span.ml-1.overline(v-if="game.platforms.length > 4")
      | and more

  v-card-title.my-0
    #text
      span {{game.title}}
      v-btn(color="primary"
        icon
        @click="dialog=true")
        v-icon mdi-information-variant
  v-card-subtitle.font-weight-light
    span
    | From {{game.year}},
    v-chip.mx-2(label
      small
      :color="ratingsColor(game.avarage_rating)"
      outlined)
      | {{game.avarage_rating}}
    span
    | &empty; of {{game.ratings_count}} ratings

  v-card-text
    .mr-7
      v-chip.mx-1.my-1(v-for="genre in game.genres.slice(0,4)"
        :key="genre.id"
        color="primary"
        label
        outlined
        small
        v-ripple)
        | {{genre.name}}
      v-chip.ml-7-my-1(v-if="game.genres.length > 4"
        outlined
        small
        label
        color="primary"
        @click="dialog='true'")
        | ...

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
      :platforms="game.platforms"
      :genres="game.genres"
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
    ratingsColor (rating) {
      if (rating > 8) return 'success'
      else if (rating > 5) return 'primary'
      else return 'error'
    },
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
.v-card__text, .v-card__title {
  word-break: normal; /* maybe !important  */
}
</style>
