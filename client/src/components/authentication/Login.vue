<template lang="pug">
#login
  v-row(justify="start")
    v-col
      h2.display-1 Login

  v-form(v-model="valid")
    v-row(justify="start")
      v-col
        v-text-field(outlined
          v-model="email"
          color="primary"
          prepend-inner-icon="mdi-email"
          :rules="[rules.required, rules.email]",
          label="E-Mail")

    v-row(justify="start")
      v-col
        v-text-field(outlined
          color="primary"
          prepend-inner-icon="mdi-lock"
          label="Password"
          v-model="password"
          :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
          :rules="[rules.required, rules.min]"
          :type="showPassword ? 'text' : 'password'"
          counter
          @click:append="showPassword = !showPassword")

    v-row(justify="start")
      v-col(align="end")
        v-btn.mr-4(:to="{name: 'register'}")
          | Register
        v-btn.black--text(:disabled="!valid"
          @click="login"
          color="primary")
          | Login
</template>

<script>
import ruleCollection from './rules'

export default {
  name: 'Login',
  data () {
    return {
      email: null,
      password: '',
      showPassword: false,
      rules: ruleCollection,
      valid: false
    }
  },
  methods: {
    async login () {
      const username = this.email; const password = this.password
      await this.$store.dispatch('login', { username, password })
      this.$router.push({ name: 'rate' })
      this.$store.dispatch('retrieveUserData')
    }
  }
}
</script>
