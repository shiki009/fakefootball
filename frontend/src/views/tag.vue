<script setup>
import { onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import { usePostsStore } from '../stores/posts.js'
import sortBar from '../components/sort-bar.vue'
import postCard from '../components/post-card.vue'
import loadingSpinner from '../components/loading-spinner.vue'
import pagination from '../components/pagination.vue'

const route = useRoute()
const postsStore = usePostsStore()

function load() {
  postsStore.setTag(route.params.slug)
}

onMounted(load)
watch(() => route.params.slug, load)
</script>

<template>
  <div>
    <div class="tag-header">
      <span class="tag-label">tag:</span>
      <span class="tag-name">{{ route.params.slug }}</span>
    </div>
    <sortBar />
    <loadingSpinner v-if="postsStore.loading" />
    <div v-else class="post-list">
      <postCard v-for="p in postsStore.posts" :key="p.id" :post="p" />
      <div v-if="!postsStore.posts.length" class="empty">no posts with this tag</div>
    </div>
    <pagination />
  </div>
</template>

<style scoped>
.tag-header {
  font-family: var(--font-mono);
  margin-bottom: 1rem;
  display: flex;
  align-items: center;
  gap: 0.4rem;
}

.tag-label {
  font-size: 0.8rem;
  color: var(--text-muted);
}

.tag-name {
  font-size: 1rem;
  font-weight: 600;
  color: var(--accent);
}

.post-list {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.empty {
  text-align: center;
  padding: 3rem;
  color: var(--text-muted);
  font-family: var(--font-mono);
}
</style>
