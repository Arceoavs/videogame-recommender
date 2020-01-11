<template lang="pug">
  v-container(fluid)
    v-row(justify="center" align="start")
      v-col(cols="10")
        h1.display-2.font-weight-bold Ratings
    v-row(justify="start" align="center")
      v-col(cols="1")
        v-icon.prev-button(size="100")
            | mdi-chevron-left
      v-col(cols="10")
        swiper.primary-border(:options="swiperOptions"
          ref="swiper")
          swiper-slide(v-for="game in games"
            :key="game.id")
            v-card(color="dp1"
              outlined)
              v-skeleton-loader(class="mx-auto"
                type="image")
              v-card-title
                .overline.mr-3(v-for="platform in game.platforms"
                  :key="platform.id")
                  | {{platform.name}}
              v-card-title
                | {{game.title}}
              v-card-text
                v-chip.mx-1.my-1(v-for="genre in game.genres"
                  :key="genre.id"
                  color="primary"
                  label
                  outlined
                  small)
                  | {{genre.name}}
              v-card-text
                p.mr-7.text-justify {{game.description}}
      v-col(cols="1")
        v-icon.next-button(size="100")
            | mdi-chevron-right
</template>

<script>
import { mapGetters } from 'vuex'
import 'swiper/dist/css/swiper.css'
import { swiper, swiperSlide } from 'vue-awesome-swiper'

export default {
  name: 'Ratings',
  components: {
    swiper,
    swiperSlide
  },
  data () {
    return {
      currentDisplay: null,
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
      }
    }
  },
  computed: {
    ...mapGetters(['games'])
  },
  mounted () {
    this.$store.dispatch('retrieveGames')
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
