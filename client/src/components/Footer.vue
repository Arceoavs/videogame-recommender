<template lang="pug">
v-footer(padless elevation="2")
  v-card.flex(flat tile color="dp1")
    v-card-text.py-2.text-center

      v-btn(dark
        text
        small
        :to="{name: 'team'}")
        |Team

      v-btn(dark
        text
        small
        href="mailto:info@vgr.best")
        | Contact

      v-btn(dark
        text
        small
        :to="{name: 'imprint'}")
        | Imprint

      v-btn(dark
        text
        small
        :to="{name: 'privacy'}")
        | Privacy

      v-btn(dark
        text
        small
        :to="{name: 'terms'}")
        | Terms

      | &copy; {{new Date().getFullYear()}} - VGR
</template>

<script>
export default {
  name: 'Footer'
}
</script>
