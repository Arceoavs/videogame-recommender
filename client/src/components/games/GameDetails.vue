<template lang="pug">
v-card
  v-card-title
    | {{title}}
  v-card-text
    p.text-justify {{description}}

  v-card-text
    p.mr-1.title.font-weight-light.my-0
      | Available on:
    v-divider
    span.mr-1.overline(v-for="platform in platforms")
      | {{platform.name}}

  v-card-text
    p.mr-1.title.font-weight-light.my-0
      | Genres:
    v-divider
    span.mr-1.overline(v-for="genre in genres")
      | {{genre.name}}

  v-card-actions
    v-spacer
    v-btn(text
      color="primary"
      @click="$emit('close')")
      | Close
</template>

<script>
export default {
  name: 'GameDetails',
  props: {
    title: { type: String, default: null },
    description: { type: String, default: null },
    platforms: { type: Array, default: null },
    genres: { type: Array, default: null }
  }
}
</script>
