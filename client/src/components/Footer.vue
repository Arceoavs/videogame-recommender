<template lang="pug">
v-footer(padless elevation="2")
  v-card.flex(flat tile color="dp1")
    v-card-title
      #buttons.hidden-sm-and-down
        v-btn(text color="white") {{"home"}}
        v-btn(text color="white") {{"about"}}
        v-btn(text color="white") {{"contact"}}
      v-spacer

      #social.hidden-xs-only
        v-tooltip(top)
          template(v-slot:activator="{on}")
            v-btn.mx-4(dark icon v-on="on")
              v-icon(color="white") mdi-facebook
          span Facebook

        v-tooltip(top)
          template(v-slot:activator="{on}")
            v-btn.mx-4(dark icon v-on="on")
              v-icon(color="white") mdi-twitter
          span Twitter

        v-tooltip(top)
          template(v-slot:activator="{on}")
            v-btn.mx-4(dark icon v-on="on")
              v-icon(color="white") mdi-linkedin
          span LindedIn

        v-tooltip(top)
          template(v-slot:activator="{on}")
            v-btn.mx-4(dark icon v-on="on")
              v-icon(color="white") mdi-instagram
          span Instagram

        v-tooltip(top)
          template(v-slot:activator="{on}")
            v-btn.mx-4(dark icon v-on="on")
              v-icon(color="white") mdi-youtube
          span Youtube

    v-divider
    v-card-text.py-2.text-center
      #legal
        v-btn(text small color="white") {{"imprint"}}
        v-btn(text  small color="white") {{"privacy"}}
        v-btn(text  small color="white") {{"terms"}}
        | &copy; {{new Date().getFullYear()}} - VGR
</template>

<script>
export default {
  name: 'Footer'
}
</script>
