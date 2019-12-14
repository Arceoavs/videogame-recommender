<template lang="pug">
v-footer(padless elevation="2")
  v-card.flex(flat tile color="dp1")
    v-card-title
      .hidden-sm-and-down
        v-btn(text color="primary_var") {{"home"}}
        v-btn(text color="primary_var") {{"about"}}
        v-btn(text color="primary_var") {{"team"}}
        v-btn(text color="primary_var") {{"contact"}}
      v-spacer

      v-tooltip(top)
        template(v-slot:activator="{on}")
          v-btn.mx-4(dark icon v-on="on")
            v-icon(color="primary_var") mdi-facebook
        span Facebook

      v-tooltip(top)
        template(v-slot:activator="{on}")
          v-btn.mx-4(dark icon v-on="on")
            v-icon(color="primary_var") mdi-twitter
        span Twitter

      v-tooltip(top)
        template(v-slot:activator="{on}")
          v-btn.mx-4(dark icon v-on="on")
            v-icon(color="primary_var") mdi-linkedin
        span LindedIn

      v-tooltip(top)
        template(v-slot:activator="{on}")
          v-btn.mx-4(dark icon v-on="on")
            v-icon(color="primary_var") mdi-instagram
        span Instagram

      v-tooltip(top)
        template(v-slot:activator="{on}")
          v-btn.mx-4(dark icon v-on="on")
            v-icon(color="primary_var") mdi-youtube
        span Youtube

    v-divider
    v-card-text.py-2.white--textarea.text-center
      #legal
        v-btn(text, small) {{"imprint"}}
        v-btn(text, small) {{"privacy"}}
        v-btn(text, small) {{"terms"}}
        | &copy; {{new Date().getFullYear()}} - VGR
</template>

<script>
export default {
  name: 'Footer'
}
</script>
