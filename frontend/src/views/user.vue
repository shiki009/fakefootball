<script setup>
import { onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { isRegular } from '../composables/authorlink.js'

const route = useRoute()
const router = useRouter()

onMounted(() => {
  const name = route.params.username
  if (isRegular(name)) {
    router.replace(`/regulars/${encodeURIComponent(name)}`)
  }
})
</script>

<template>
  <div>
    <router-link to="/" class="back-btn">← back</router-link>
    <div v-if="!isRegular($route.params.username)" class="not-found">
      <div class="not-found-title">user not found</div>
      <div class="not-found-sub">this person doesn't have a profile here.</div>
    </div>
  </div>
</template>

<style scoped>
.back-btn {
  display: inline-block;
  color: var(--text-muted);
  font-family: var(--font-mono);
  font-size: 0.8rem;
  padding: 0.3rem 0;
  margin-bottom: 1rem;
  text-decoration: none;
  transition: color 0.15s ease;
}

.back-btn:hover {
  color: var(--accent);
}

.not-found {
  text-align: center;
  padding: 4rem 2rem;
  color: var(--text-muted);
}

.not-found-title {
  font-family: var(--font-mono);
  font-size: 1.1rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
}

.not-found-sub {
  font-size: 0.85rem;
  opacity: 0.7;
}
</style>
