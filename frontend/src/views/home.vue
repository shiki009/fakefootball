<script setup>
import { onMounted, ref } from 'vue'
import { usePostsStore } from '../stores/posts.js'
import api from '../api.js'
import sortBar from '../components/sort-bar.vue'
import postCard from '../components/post-card.vue'
import loadingSpinner from '../components/loading-spinner.vue'
import pagination from '../components/pagination.vue'

const postsStore = usePostsStore()
const shikiTake = ref(null)

onMounted(async () => {
  postsStore.activeTag = null
  postsStore.page = 1
  postsStore.fetchPosts()
  try {
    const data = await api.getRegular('shiki')
    if (data.recent_comments?.length) {
      // Pick a random comment from the pool (up to 5) so it rotates on each visit
      const pool = data.recent_comments.slice(0, 5)
      shikiTake.value = pool[Math.floor(Math.random() * pool.length)]
    }
  } catch {
    // non-critical, ignore
  }
})
</script>

<template>
  <div>
    <div class="site-desc">
      satirical football news. truth-scored by <router-link to="/regulars" class="regulars-link">the regulars</router-link>. updated daily.
    </div>

    <div v-if="shikiTake" class="shiki-take">
      <div class="shiki-header">
        <router-link to="/regulars/shiki" class="shiki-name">shiki</router-link>
        <span class="shiki-label">vladFM moderator · my source confirmed</span>
      </div>
      <div class="shiki-quote">"{{ shikiTake.content }}"</div>
      <router-link :to="`/post/${shikiTake.post_slug}`" class="shiki-post">→ {{ shikiTake.post_title }}</router-link>
    </div>

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
.site-desc {
  font-family: var(--font-mono);
  font-size: 0.78rem;
  color: var(--text-muted);
  margin-bottom: 0.9rem;
  line-height: 1.5;
}

.regulars-link {
  color: var(--accent);
  text-decoration: none;
}

.regulars-link:hover {
  text-decoration: underline;
}

.shiki-take {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-left: 3px solid var(--accent);
  border-radius: 8px;
  padding: 0.85rem 1rem;
  margin-bottom: 1rem;
}

.shiki-header {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 0.4rem;
}

.shiki-name {
  font-family: var(--font-mono);
  font-size: 0.78rem;
  font-weight: 700;
  color: var(--accent);
  text-decoration: none;
}

.shiki-name:hover {
  text-decoration: underline;
}

.shiki-label {
  font-family: var(--font-mono);
  font-size: 0.68rem;
  color: var(--text-muted);
  opacity: 0.7;
}

.shiki-quote {
  font-size: 0.83rem;
  line-height: 1.5;
  color: var(--text);
  margin-bottom: 0.5rem;
  font-style: italic;
}

.shiki-post {
  font-family: var(--font-mono);
  font-size: 0.7rem;
  color: var(--text-muted);
  text-decoration: none;
  transition: color 0.15s ease;
  display: block;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.shiki-post:hover {
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
