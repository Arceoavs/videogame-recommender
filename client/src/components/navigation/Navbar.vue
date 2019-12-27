<template lang="pug">
v-app-bar(app color="dp1" dense)
  v-row(justify="start" align="center" no-gutters)
    v-col(cols="2")
      v-app-bar-nav-icon.hidden-md-and-up(
        @click.stop="$emit('drawer', true)")
    v-col(cols="2")
      router-link(:to="{name: 'home'}")
        v-img(src="@/assets/logos/vgrlogo_white.svg"
          max-height="30px"
          contain)
  v-spacer
  v-divider(vertical, inset)
  v-toolbar-items.hidden-sm-and-down
    v-btn(v-for="item in items"
      v-if="item.loggedIn"
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
