<template lang="pug">
v-img(:aspect-ratio="4/3" src="../assets/vgr.png")
  v-container(fluid)
    v-row
      v-col(md="4" sm="6" cols="8")
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
            p.font-weight-light.text-justify
              | Our mission is to keep you playing forever.
              | This is your life now.
              | Enjoy.

        v-row.mt-10(justify="start")
          v-col
            h2.display-1 Login

        v-row(justify="start")
          v-col
            v-text-field(color="primary_var"
              prepend-inner-icon="mdi-email"
              label="E-Mail"
              hide-details)

        v-row(justify="start")
          v-col
            v-text-field(color="primary_var"
              prepend-inner-icon="mdi-lock"
              label="Password"
              v-model="password"
              :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
              :rules="[rules.required, rules.min]"
              :type="showPassword ? 'text' : 'password'"
              counter
              @click:append="show = !show")

        v-row(justify="start")
          v-col(align="end")
            v-btn.mr-4 Register
            v-btn Login
</template>

<script>

export default {
  name: 'Landing',
  data () {
    return {
      password: '',
      showPassword: false,
      rules: {
        required: value => !!value || 'Required.',
        min: v => v.length >= 8 || 'Min 8 characters'
      }
    }
  }
}
</script>
