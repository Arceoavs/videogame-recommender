<template lang="pug">
v-container
  v-row
    v-col
      h1.display-2.font-weight-bold
        | Meet the team

  v-row
    v-col
      h2.display-1
          | Who is behind the Video Game Recommender?

  v-row(justify="space-around")
    v-col(cols="12" lg="4" md="6" sm="6"
      v-for="dude in team"
      :key="dude.name")
      v-hover(v-slot:default="{ hover }")
        v-card(color="dp1"
          :elevation="hover ? 12 : 1")
          v-img.white--text.align-end(height="200px"
            :src="dude.image")
            v-card-title
              | {{dude.name}}
          v-card-subtitle.overline
            | {{dude.role}}
          v-card-actions
            v-btn(text
              color="primary"
              small
              :href="mailLink(dude.mail)")
              v-icon.mr-2 mdi-email
              | {{dude.mail}}
  v-row
    v-col
      p.font-weight-light.title
        | For suggestions and feedback, feel free to send us a mail!

</template>

<script>
export default {
  data () {
    return {
      team: [
        { name: 'Luca Daniel',
          role: 'Data Integrator',
          mail: 'arnold@vgr.best',
          image: 'https://cdn.vuetifyjs.com/images/cards/docks.jpg' },
        { name: 'Arnold Arz von Straussenburg',
          role: 'Frontend Developer',
          mail: 'arnold@vgr.best',
          image: 'https://cdn.vuetifyjs.com/images/cards/docks.jpg' },
        { name: 'David Wilhelm',
          role: 'Backend Developer',
          mail: 'arnold@vgr.best',
          image: 'https://cdn.vuetifyjs.com/images/cards/docks.jpg' },
        { name: 'Arnold Arz von Straussenburg',
          role: 'Frontend Developer',
          mail: 'arnold@vgr.best',
          image: 'https://cdn.vuetifyjs.com/images/cards/docks.jpg' },
        { name: 'Arnold Arz von Straussenburg',
          role: 'Frontend Developer',
          mail: 'arnold@vgr.best',
          image: 'https://cdn.vuetifyjs.com/images/cards/docks.jpg' },
        { name: 'Arnold Arz von Straussenburg',
          role: 'Frontend Developer',
          mail: 'arnold@vgr.best',
          image: 'https://cdn.vuetifyjs.com/images/cards/docks.jpg' }
      ]
    }
  },
  methods: {
    mailLink (address) {
      return 'mailto:' + address
    }
  }
}
</script>
