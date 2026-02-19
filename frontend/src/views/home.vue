<script setup>
import { onMounted } from 'vue'
import { usePostsStore } from '../stores/posts.js'
import sortBar from '../components/sort-bar.vue'
import postCard from '../components/post-card.vue'
import loadingSpinner from '../components/loading-spinner.vue'
import pagination from '../components/pagination.vue'

const postsStore = usePostsStore()

onMounted(() => {
  postsStore.activeTag = null
  postsStore.page = 1
  postsStore.fetchPosts()
})
</script>

<template>
  <div>
    <sortBar />
    <loadingSpinner v-if="postsStore.loading" />
    <div v-else class="post-list">
      <postCard v-for="p in postsStore.posts" :key="p.id" :post="p" />
      <div v-if="!postsStore.posts.length" class="empty">nothing here</div>
    </div>
    <pagination />
  </div>
</template>

<style scoped>
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
