import Vue from 'vue'
import VueRouter from 'vue-router'
import store from '@/store/index'

Vue.use(VueRouter)

// route level code-splitting
// this generates a separate chunk (about.[hash].js) for this route
// which is lazy-loaded when the route is visited.
const routes = [
  {
    path: '/',
    name: 'home',
    component: () => import(/* webpackChunkName: "home" */ '@/views/Landing.vue')
  },
  {
    path: '/register',
    name: 'register',
    component: () =>
      import(/* webpackChunkName: "register" */ '@/views/Landing.vue'),
    props: { showRegister: true }
  },
  {
    path: '/login',
    name: 'login',
    component: () =>
      import(/* webpackChunkName: "login" */ '@/views/Landing.vue'),
    props: { showLogin: true }
  },
  {
    path: '/about',
    name: 'about'
    // component: () => import(/* webpackChunkName: "about" */ '../views/About.vue')
  },
  {
    path: '/recommend',
    name: 'recommend',
    meta: {
      requiresAuth: true
    },
    component: () => import(/* webpackChunkName: "recommend" */ '../views/Recommend.vue')
  },
  {
    path: '/rate',
    name: 'rate',
    meta: {
      requiresAuth: true
    },
    component: () => import(/* webpackChunkName: "rate" */ '../views/Rate.vue')
  },
  {
    path: '/logout',
    name: 'logout',
    meta: {
      requiresAuth: true
    },
    beforeEnter: (toolbar, from, next) => {
      store.dispatch('logout')
      next('/')
    }
  },
  {
    path: '/*',
    name: '404',
    component: () =>
      import(/* webpackChunkName: "error" */ '@/views/errors/404.vue')
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

router.beforeEach((to, from, next) => {
  if (to.matched.some(record => record.meta.requiresAuth)) {
    if (store.getters.loggedIn) {
      next()
      return
    }
    next('/login')
  } else (next())
})

export default router
