<template lang="pug">
#login
  v-row(justify="start")
    v-col
      h2.display-1 Login

  v-row(justify="start")
    v-col
      v-text-field(v-model="email"
        color="primary_var"
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
  name: 'Login',
  data () {
    return {
      email: null,
      password: '',
      showPassword: false,
      rules: {
        required: value => !!value || 'Required.',
        min: v => v.length >= 8 || 'Min 8 characters'
      }
    }
  },
  methods: {
    login () {

    }
  }
}
</script>
