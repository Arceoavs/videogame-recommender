<template lang="pug">
#register
  v-row(justify="start")
    v-col
      h2.display-1 Register

  v-form#RegisterForm(v-model="valid")
    v-row(justify="start"
      no-gutters)
      v-col
        v-text-field(outlined
          v-model="email"
          color="primary"
          prepend-inner-icon="mdi-email"
          label="E-Mail"
          :rules="[rules.required, rules.email]")

    v-row(justify="start"
      no-gutters)
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
          @click:append="show = !show")

    v-row(justify="start"
      no-gutters)
      v-col
        v-text-field(outlined
          color="primary"
          prepend-inner-icon="mdi-lock"
          label="Confirm Password"
          v-model="passwordConfirmation"
          :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
          :rules="[rules.required, rules.min, rules.passwordMatch(password, passwordConfirmation)]"
          :type="showPassword ? 'text' : 'password'"
          @click:append="show = !show")

    v-row(justify="start")
      v-col(align="end")
        v-btn.mr-4(:to="{name: 'login'}")
          | To Login
        v-btn.black--text(:disabled="!valid"
          @click="register"
          color="primary")
          | Register
</template>

<script>
import RuleCollection from './rules'

export default {
  name: 'Login',
  data () {
    return {
      email: null,
      password: '',
      passwordConfirmation: '',
      showPassword: false,
      valid: false,
      rules: RuleCollection
    }
  },
  methods: {
    async register () {
      const username = this.email; const password = this.password
      await this.$store.dispatch('register', { username, password })
      this.$router.push({ name: 'recommend' })
    }
  }
}
</script>
