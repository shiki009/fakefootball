<script setup>
import { computed } from 'vue'
import { usePostsStore } from '../stores/posts.js'

const postsStore = usePostsStore()

// windowed page list: 1 … current-1 current current+1 … last
const pageList = computed(() => {
  const total = postsStore.totalPages
  const current = postsStore.page
  const pages = new Set([1, total, current - 1, current, current + 1])
  const sorted = [...pages].filter(p => p >= 1 && p <= total).sort((a, b) => a - b)
  const out = []
  let prev = 0
  for (const p of sorted) {
    if (p - prev > 1) out.push('…')
    out.push(p)
    prev = p
  }
  return out
})
</script>

<template>
  <div v-if="postsStore.totalPages > 1" class="pagination">
    <button
      class="page-btn"
      :disabled="postsStore.page <= 1"
      @click="postsStore.setPage(postsStore.page - 1)"
    >&lt;</button>
    <template v-for="(p, i) in pageList" :key="`${p}-${i}`">
      <span v-if="p === '…'" class="ellipsis">…</span>
      <button
        v-else
        class="page-btn"
        :class="{ active: p === postsStore.page }"
        @click="postsStore.setPage(p)"
      >{{ p }}</button>
    </template>
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
  white-space: nowrap;
  word-break: normal;
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

.ellipsis {
  color: var(--text-muted);
  padding: 0.3rem 0.1rem;
  font-size: 0.85rem;
}
</style>
