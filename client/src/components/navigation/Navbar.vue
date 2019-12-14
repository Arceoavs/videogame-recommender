<template lang="pug">
v-app-bar(app color="dp1" dense)
  v-app-bar-nav-icon.hidden-md-and-up(@click.stop="$emit('drawer', true)")
  v-toolbar-title
    //- v-img(src="@/assets/logos/logo-watchtrainer-white.png"
      max-height="30px"
      contain)
  v-spacer
  v-divider(vertical, inset)
  v-toolbar-items.hidden-sm-and-down
    v-btn(v-for="item in items"
      :key="item.tag"
      text
      :to="item.to")
      | {{item.tag}}
</template>

<script>
import navItems from './navItems.json'
export default {
  data () {
    return {
      items: navItems
    }
  }
}
</script>
