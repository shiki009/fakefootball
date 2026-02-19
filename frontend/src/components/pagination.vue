<script setup>
import { usePostsStore } from '../stores/posts.js'

const postsStore = usePostsStore()
</script>

<template>
  <div v-if="postsStore.totalPages > 1" class="pagination">
    <button
      class="page-btn"
      :disabled="postsStore.page <= 1"
      @click="postsStore.setPage(postsStore.page - 1)"
    >&lt;</button>
    <button
      v-for="p in postsStore.totalPages"
      :key="p"
      class="page-btn"
      :class="{ active: p === postsStore.page }"
      @click="postsStore.setPage(p)"
    >{{ p }}</button>
    <button
      class="page-btn"
      :disabled="postsStore.page >= postsStore.totalPages"
      @click="postsStore.setPage(postsStore.page + 1)"
    >&gt;</button>
  </div>
</template>

<style scoped>
.pagination {
  display: flex;
  justify-content: center;
  gap: 0.4rem;
  margin-top: 1.2rem;
  font-family: var(--font-mono);
}

.page-btn {
  background: var(--bg-card);
  color: var(--text-muted);
  border: 1px solid var(--border);
  border-radius: 4px;
  padding: 0.3rem 0.65rem;
  font-size: 0.85rem;
  font-family: var(--font-mono);
  cursor: pointer;
  transition: background 0.15s, color 0.15s, border-color 0.15s;
}

.page-btn:hover:not(:disabled):not(.active) {
  background: var(--bg-hover);
  color: var(--text);
}

.page-btn.active {
  background: var(--accent);
  color: var(--bg);
  border-color: var(--accent);
  font-weight: 600;
}

.page-btn:disabled {
  opacity: 0.3;
  cursor: default;
}
</style>
