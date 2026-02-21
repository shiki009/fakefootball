<script setup>
import { ref, onMounted } from 'vue'
import api from '../api.js'

const regulars = ref([])

onMounted(async () => {
  regulars.value = await api.getRegulars()
})
</script>

<template>
  <div class="widget" v-if="regulars.length">
    <div class="widget-header">
      <div class="widget-title">regulars</div>
      <router-link to="/regulars" class="see-all">see all →</router-link>
    </div>
    <div class="regulars-list">
      <div v-for="(r, i) in regulars" :key="r.name" class="regular">
        <span class="rank">{{ i + 1 }}.</span>
        <router-link :to="`/regulars/${encodeURIComponent(r.name)}`" class="name">{{ r.name }}</router-link>
        <span class="count">{{ r.comments }} <span class="label">cmts</span></span>
      </div>
    </div>
  </div>
</template>

<style scoped>
.widget {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 1rem;
}

.widget-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 0.75rem;
}

.widget-title {
  font-family: var(--font-mono);
  font-size: 0.8rem;
  font-weight: 600;
  color: var(--text-muted);
  text-transform: lowercase;
}

.see-all {
  font-family: var(--font-mono);
  font-size: 0.7rem;
  color: var(--accent);
  text-decoration: none;
  opacity: 0.7;
  transition: opacity 0.15s ease;
}

.see-all:hover {
  opacity: 1;
}

.regulars-list {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.regular {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  font-size: 0.8rem;
}

.rank {
  font-family: var(--font-mono);
  color: var(--text-muted);
  min-width: 1.2rem;
  font-size: 0.75rem;
}

.name {
  font-family: var(--font-mono);
  color: var(--accent);
  font-weight: 500;
  flex: 1;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  text-decoration: none;
}

.name:hover {
  text-decoration: underline;
}

.count {
  font-family: var(--font-mono);
  font-size: 0.7rem;
  color: var(--text-muted);
  white-space: nowrap;
}

.label {
  opacity: 0.6;
}
</style>
