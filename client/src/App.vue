<template lang="pug">
v-app(:style="{background: $vuetify.theme.themes[theme].background}")
  Navbar(@drawer="toggleDrawer")
  Drawer.hidden-md-and-up(v-model="drawer")
  v-content
    router-view
    Confirmation
  Footer
</template>

<script>
import Navbar from "@/components/navigation/Navbar";
import Drawer from "@/components/navigation/Drawer";
import Footer from "@/components/navigation/Footer";
import Confirmation from "@/components/authentication/SnackMessage";

export default {
  name: "App",
  components: { Navbar, Drawer, Footer, Confirmation },
  data() {
    return {
      drawer: false,
      snackbar: false
    };
  },
  computed: {
    theme() {
      return this.$vuetify.theme.dark ? "dark" : "light";
    }
  },
  created() {
    this.$http.interceptors.response.use(undefined, err => {
      if (err.status === 401 && err.config && !err.config.__isRetryRequest) {
        this.$store.dispatch("logout");
      }
      throw err;
    });
  },
  mounted() {
    this.$store.dispatch("retrieveGenres");
    this.$store.dispatch("retrievePlatforms");
  },
  methods: {
    toggleDrawer(val) {
      this.drawer = val;
    }
  }
};
</script>
