<template lang="pug">

</template>

<script>
export default {
  async mounted () {
    const res = await this.$http.get('/secret')
    console.log(res.data)
  }
}
</script>
