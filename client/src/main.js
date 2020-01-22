import Vue from 'vue'
import App from './App.vue'
import './registerServiceWorker'
import router from './router'
import store from './store'
import vuetify from './plugins/vuetify'
import axios from 'axios'
import VueParticles from 'vue-particles'
Vue.use(VueParticles)

Vue.config.productionTip = false

const instance = axios.create({ baseURL: process.env.VUE_APP_API_URL })
instance.defaults.headers.common['Authorization'] = `Bearer ${localStorage.getItem('token')}`
Vue.prototype.$http = instance

new Vue({
  router,
  store,
  vuetify,
  render: h => h(App)
}).$mount('#app')
