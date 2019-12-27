<template lang="pug">

</template>

<script>
export default {
  async mounted () {
    const res = await this.$http.post('/register')
    console.log(res)
  }
}
</script>
