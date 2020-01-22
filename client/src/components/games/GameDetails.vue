<template lang="pug">
v-card
  v-card-title
    | {{title}}
  v-card-text
    p.text-justify {{description}}
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
    description: { type: String, default: null }
  }
}
</script>
