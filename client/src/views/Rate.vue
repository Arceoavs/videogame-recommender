<template lang="pug">
v-container(fluid)
  v-row(justify="center" align="start")
    v-col(cols="10")
      h1.display-2.font-weight-bold Ratings

  v-row(justify="center" align="start")
    v-col(cols="10")
      h2.display-1 Rate new games

  v-row(justify="center" align="start")
    v-col(cols="1")
    v-col(cols="5")
      v-autocomplete(outlined
        dense
        prepend-inner-icon="mdi-gamepad-variant-outline"
        v-model="selectedGenres"
        :items="sortedGenres"
        item-text="name"
        item-value="id"
        chips
        small-chips
        multiple
        placeholder="Filter genres")

    v-col(cols="5")
      v-text-field(outlined
        dense
        clearable
        prepend-inner-icon="mdi-magnify"
        placeholder="Search for games")
    v-col(cols="1")

  v-row(justify="start" align="center")
    v-col.hide-sm-and-down(cols="1"
      align="right")
      v-icon.prev-button(size="50")
        | mdi-chevron-left

    v-col(cols="10")
      swiper(:options="swiperOptions"
        ref="swiper"
        @reachEnd="$store.dispatch('loadNext')"
        @reachBeginning="$store.dispatch('loadPrev')")
        swiper-slide(v-for="game in sortedGames"
          :key="game.id")
          GameCard(:game="game")

    v-col.hide-sm-and-down(cols="1"
      align="left")
      v-icon.next-button(size="50")
        | mdi-chevron-right

</template>

<script>
import { mapGetters } from 'vuex'
import 'swiper/dist/css/swiper.css'
import { swiper, swiperSlide } from 'vue-awesome-swiper'
import GameCard from '@/components/games/GameCard'

export default {
  name: 'Ratings',
  components: {
    swiper,
    swiperSlide,
    GameCard
  },
  data () {
    return {
      swiperOptions: {
        slidesPerView: 3,
        spaceBetween: 30,
        navigation: {
          nextEl: '.next-button',
          prevEl: '.prev-button'
        },
        breakpoints: {
          1264: {
            slidesPerView: 3,
            spaceBetween: 30
          },
          960: {
            slidesPerView: 2,
            spaceBetween: 20
          },
          600: {
            slidesPerView: 1,
            spaceBetween: 10
          }
        }
      },
      selectedGenres: []
    }
  },
  computed: {
    ...mapGetters(['sortedGames', 'range', 'sortedGenres'])

  },
  mounted () {
    this.$store.dispatch('retrieveGames', { limit: 10 })
    this.$store.dispatch('retrieveGenres')
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
