<script setup>
import { usePostsStore } from '../stores/posts.js'

const postsStore = usePostsStore()

const tabs = [
  { key: 'new', label: 'new' },
  { key: 'top', label: 'top' },
  { key: 'discussed', label: 'discussed' },
]
</script>

<template>
  <div class="sort-bar">
    <button
      v-for="tab in tabs"
      :key="tab.key"
      :class="['tab', { active: postsStore.sort === tab.key }]"
      @click="postsStore.setSort(tab.key)"
    >
      {{ tab.label }}
    </button>
  </div>
</template>

<style scoped>
.sort-bar {
  display: flex;
  gap: 0.25rem;
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 0.25rem;
  margin-bottom: 1rem;
}

.tab {
  flex: 1;
  padding: 0.5rem;
  background: none;
  border: none;
  border-radius: 6px;
  font-family: var(--font-mono);
  font-size: 0.8rem;
  font-weight: 500;
  color: var(--text-muted);
  transition: all 0.15s ease;
}

.tab:hover {
  color: var(--text);
  background: var(--bg-hover);
}

.tab.active {
  color: var(--accent);
  background: var(--bg-hover);
}
</style>
