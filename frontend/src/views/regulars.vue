<script setup>
import { ref, onMounted } from 'vue'
import api from '../api.js'
import loadingSpinner from '../components/loading-spinner.vue'

const regulars = ref([])
const loading = ref(true)

onMounted(async () => {
  try {
    regulars.value = await api.getRegulars()
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <div class="regulars-page">
    <router-link to="/" class="back-btn">← back</router-link>

    <div class="page-header">
      <h1 class="title">the regulars</h1>
      <p class="subtitle">the people who keep this place alive. they comment, they vote, they argue.</p>
    </div>

    <loadingSpinner v-if="loading" />

    <div v-else class="regulars-list">
      <router-link
        v-for="(r, i) in regulars"
        :key="r.name"
        :to="`/regulars/${encodeURIComponent(r.name)}`"
        class="regular-card"
      >
        <div class="regular-rank">{{ i + 1 }}</div>
        <div class="regular-body">
          <div class="regular-name">{{ r.name }}</div>
          <div class="regular-bio">{{ r.bio }}</div>
          <div class="regular-stats">
            <span class="stat">{{ r.comments }} comments</span>
            <span class="dot">·</span>
            <span class="stat">{{ r.votes_cast }} votes</span>
          </div>
        </div>
      </router-link>
    </div>
  </div>
</template>

<style scoped>
.regulars-page {
  max-width: 640px;
}

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

.page-header {
  margin-bottom: 1.75rem;
}

.title {
  font-family: var(--font-mono);
  font-size: 1.4rem;
  font-weight: 700;
  margin-bottom: 0.3rem;
}

.subtitle {
  font-size: 0.85rem;
  color: var(--text-muted);
}

.regulars-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.regular-card {
  display: flex;
  align-items: flex-start;
  gap: 1rem;
  padding: 1rem 1.1rem;
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 8px;
  text-decoration: none;
  color: inherit;
  transition: border-color 0.15s ease;
}

.regular-card:hover {
  border-color: var(--accent);
}

.regular-rank {
  font-family: var(--font-mono);
  font-size: 0.75rem;
  color: var(--text-muted);
  min-width: 1.2rem;
  padding-top: 0.15rem;
}

.regular-body {
  flex: 1;
  min-width: 0;
}

.regular-name {
  font-family: var(--font-mono);
  font-size: 0.95rem;
  font-weight: 600;
  color: var(--accent);
  margin-bottom: 0.3rem;
}

.regular-bio {
  font-size: 0.82rem;
  color: var(--text-muted);
  line-height: 1.5;
  margin-bottom: 0.5rem;
}

.regular-stats {
  display: flex;
  align-items: center;
  gap: 0.35rem;
  font-family: var(--font-mono);
  font-size: 0.72rem;
  color: var(--text-muted);
}

.dot {
  opacity: 0.4;
}
</style>
