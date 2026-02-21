import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  { path: '/', component: () => import('./views/home.vue') },
  { path: '/post/:slug', component: () => import('./views/post.vue') },
  { path: '/tag/:slug', component: () => import('./views/tag.vue') },
  { path: '/about', component: () => import('./views/about.vue') },
  { path: '/sponsor', component: () => import('./views/sponsor.vue') },
  { path: '/user/:username', component: () => import('./views/user.vue') },
  { path: '/regulars', component: () => import('./views/regulars.vue') },
  { path: '/regulars/:name', component: () => import('./views/regular.vue') },
  { path: '/:pathMatch(.*)*', component: () => import('./views/not-found.vue') },
]

export default createRouter({
  history: createWebHistory(),
  routes,
})
