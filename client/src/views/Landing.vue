<template lang="pug">
v-img(src="../assets/background.jpg"
  gradient="0.25turn, rgba(0,0,0,1) 40%, rgba(0,0,0,0)"
  height="100%")
  v-container
    v-row
      v-col(sm="6" cols="10")
        v-row.mt-10(justify="start")
          v-col
            //- md and up
            .hidden-sm-and-down
              h1.display-2
                span.font-weight-black V
                | ideo
                span.font-weight-black G
                | ame
              h1.display-2
                span.font-weight-black R
                | ecommender

            //- sm
            h1.display-1.hidden-md-and-up.hidden-xs-only
              span.font-weight-black V
              | ideo
              span.font-weight-black G
              | ame
              span.font-weight-black R
              | ecommender

            //- xs
            h1.headline.hidden-sm-and-up
              span.font-weight-black V
              | ideo
              span.font-weight-black G
              | ame
              span.font-weight-black R
              | ecommender

        v-row(justify="start")
          v-col
            p.font-weight-light.text-justify
              | Welcome to the Video Game Recommender.
              | We use a data-driven approach to deliver you the best recommendations possible.
            VueTypedJs(:strings="['Our mission is to keep you playing forever.', \
              'This is your life now.', \
              'Enjoy.']")
              span.font-weight-light.text-justify.typing

        Register(v-if="showRegister")
        Login(v-else)
</template>

<script>
import Login from '@/components/authentication/Login'
import Register from '@/components/authentication/Register'
import { VueTypedJs } from 'vue-typed-js'

export default {
  name: 'Landing',
  components: { Login, Register, VueTypedJs },
  props: {
    showLogin: { type: Boolean, default: false },
    showRegister: { type: Boolean, default: false }
  }
}
</script>
