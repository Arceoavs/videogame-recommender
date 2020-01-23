<template lang="pug">
v-snackbar(v-model="showSnackbar"
  :color="color")
  | {{message}}
  //- v-btn(text
  //-   @click="$emit('update', false)")
  //-   | Close
</template>>

<script>
import { mapState } from 'vuex'
export default {
  name: 'ConfirmationMessage',
  model: {
    prop: 'show',
    event: 'update'
  },
  props: {
    show: { type: Boolean, default: false }
  },
  data () {
    return {
      showMessage: this.show
    }
  },
  computed: {
    ...mapState([ 'status' ]),
    color () {
      if (this.status === 'success') return 'success'
      else return 'error'
    },
    message () {
      if (this.status === 'success') return 'Logged in successfully!'
      else return this.status
    },
    showSnackbar: {
      get () {
        return this.$store.state.showSnackbar
      },
      set (val) {
        return this.$store.commit('toggleSnackbar', val)
      }
    }
  },
  methods: {
    handleInput (value) {
      this.$emit('update', value)
    }
  }
}
</script>
