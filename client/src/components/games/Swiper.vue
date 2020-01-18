<template lang="pug">
swiper(:options="swiperOptions"
  @reachEnd="$emit('reachEnd')"
  @reachBeginning="$emit('reachEnd')")
  swiper-slide(v-for="game in games"
    :key="game.id")
    GameCard(:game="game"
      rateable
      @rated="$emit('rated')"
      :key="componentKey")
  //- .swiper-button-next.swiper-button-white(slot="button-next")
  //- .swiper-button-prev.swiper-button-white(slot="button-prev")
</template>

<script>
import 'swiper/dist/css/swiper.css'
import GameCard from '@/components/games/GameCard'
import { swiper, swiperSlide } from 'vue-awesome-swiper'

export default {
  name: 'Swiper',
  components: {
    swiper,
    swiperSlide,
    GameCard
  },
  props: {
    slidesPerView: { type: Number, default: 1 },
    spaceBetween: { type: Number, default: 30 },
    nextEl: { type: String, default: '.next-button' },
    prevEl: { type: String, default: '.prev-button' },
    games: { type: Array, default: () => [] }
  },
  data () {
    return {
      componentKey: 0,
      swiperOptions: {
        slidesPerView: this.slidesPerView,
        spaceBetween: this.spaceBetween,
        navigation: {
          nextEl: '.swiper-button-next',
          prevEl: '.swiper-button-next'
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
      }
    }
  },
  methods: {
    rated () {
      this.$emit('rated')
      this.componentKey += 1
    }
  }
}
</script>
