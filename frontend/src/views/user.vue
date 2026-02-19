<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import api from '../api.js'
import { useTimeAgo } from '../composables/timeago.js'
import postCard from '../components/post-card.vue'
import loadingSpinner from '../components/loading-spinner.vue'

const route = useRoute()
const profile = ref(null)
const loading = ref(true)
const error = ref(false)

const commentsPage = ref(1)
const votesPage = ref(1)
const perPage = 5

const pagedComments = computed(() => {
  if (!profile.value) return []
  return profile.value.comments.slice(0, commentsPage.value * perPage)
})

const hasMoreComments = computed(() => {
  if (!profile.value) return false
  return profile.value.comments.length > commentsPage.value * perPage
})

const pagedVotes = computed(() => {
  if (!profile.value) return []
  return profile.value.votes.slice(0, votesPage.value * perPage)
})

const hasMoreVotes = computed(() => {
  if (!profile.value) return false
  return profile.value.votes.length > votesPage.value * perPage
})

async function load() {
  loading.value = true
  error.value = false
  commentsPage.value = 1
  votesPage.value = 1
  try {
    profile.value = await api.getUserProfile(route.params.username)
  } catch {
    error.value = true
  } finally {
    loading.value = false
  }
}

onMounted(load)
watch(() => route.params.username, load)
</script>

<template>
  <div>
    <router-link to="/" class="back-btn">← back</router-link>

    <loadingSpinner v-if="loading" />

    <div v-else-if="error" class="error-msg">user not found</div>

    <div v-else-if="profile" class="profile">
      <div class="profile-header">
        <div class="profile-name-row">
          <h1 class="username">{{ profile.username }}</h1>
          <span v-if="profile.is_regular" class="regular-badge">regular</span>
        </div>
        <div v-if="profile.bio" class="bio">{{ profile.bio }}</div>
        <div class="profile-stats">
          <span class="stat">{{ profile.post_count }} posts</span>
          <span class="dot">·</span>
          <span class="stat">{{ profile.comment_count }} comments</span>
          <span class="dot">·</span>
          <span class="stat">{{ profile.votes.length }} votes</span>
        </div>
      </div>

      <!-- posts -->
      <section v-if="profile.posts.length" class="section">
        <h2 class="section-title">posts</h2>
        <div class="post-list">
          <postCard v-for="p in profile.posts" :key="p.id" :post="p" />
        </div>
      </section>

      <!-- comments -->
      <section v-if="profile.comments.length" class="section">
        <h2 class="section-title">comments ({{ profile.comments.length }})</h2>
        <div class="comment-list">
          <div v-for="c in pagedComments" :key="c.id" class="comment-item">
            <div class="comment-meta">
              <router-link :to="`/post/${c.post_slug}`" class="comment-post-link">{{ c.post_title }}</router-link>
              <span class="comment-time">{{ useTimeAgo(c.created_at) }}</span>
            </div>
            <div class="comment-body">{{ c.content }}</div>
          </div>
        </div>
        <button v-if="hasMoreComments" class="show-more" @click="commentsPage++">
          show more comments ({{ profile.comments.length - commentsPage * perPage }} remaining)
        </button>
      </section>

      <!-- votes -->
      <section v-if="profile.votes.length" class="section">
        <h2 class="section-title">votes ({{ profile.votes.length }})</h2>
        <div class="vote-list">
          <div v-for="v in pagedVotes" :key="v.post_id" class="vote-item">
            <span :class="['vote-indicator', v.value === 1 ? 'up' : 'down']">
              {{ v.value === 1 ? '▲' : '▼' }}
            </span>
            <router-link :to="`/post/${v.post_slug}`" class="vote-post-link">{{ v.post_title }}</router-link>
          </div>
        </div>
        <button v-if="hasMoreVotes" class="show-more" @click="votesPage++">
          show more votes ({{ profile.votes.length - votesPage * perPage }} remaining)
        </button>
      </section>
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

.error-msg {
  text-align: center;
  padding: 3rem;
  color: var(--text-muted);
  font-family: var(--font-mono);
}

.profile-header {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 1.25rem;
  margin-bottom: 1.5rem;
}

.profile-name-row {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.username {
  font-family: var(--font-mono);
  font-size: 1.3rem;
  font-weight: 700;
}

.regular-badge {
  font-family: var(--font-mono);
  font-size: 0.65rem;
  font-weight: 600;
  color: var(--green);
  background: var(--green-dim);
  padding: 0.1rem 0.4rem;
  border-radius: 3px;
}

.bio {
  margin-top: 0.5rem;
  font-size: 0.85rem;
  line-height: 1.5;
  color: var(--text-muted);
}

.profile-stats {
  margin-top: 0.5rem;
  font-family: var(--font-mono);
  font-size: 0.8rem;
  color: var(--text-muted);
  display: flex;
  align-items: center;
  gap: 0.35rem;
}

.dot {
  opacity: 0.4;
}

.section {
  margin-bottom: 1.5rem;
}

.section-title {
  font-family: var(--font-mono);
  font-size: 0.85rem;
  font-weight: 600;
  color: var(--text-muted);
  text-transform: lowercase;
  margin-bottom: 0.75rem;
}

.post-list {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.comment-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.comment-item {
  padding: 0.75rem;
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 6px;
}

.comment-meta {
  font-size: 0.75rem;
  color: var(--text-muted);
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 0.3rem;
}

.comment-post-link {
  font-family: var(--font-mono);
  color: var(--accent);
  text-decoration: none;
  font-weight: 500;
}

.comment-post-link:hover {
  text-decoration: underline;
}

.comment-time {
  font-family: var(--font-mono);
  font-size: 0.7rem;
}

.comment-body {
  font-size: 0.85rem;
  line-height: 1.5;
}

.vote-list {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
}

.vote-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 0.75rem;
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 6px;
  font-size: 0.85rem;
}

.vote-indicator {
  font-size: 0.75rem;
  font-weight: 700;
}

.vote-indicator.up {
  color: var(--green);
}

.vote-indicator.down {
  color: var(--text-muted);
}

.vote-post-link {
  font-family: var(--font-mono);
  color: var(--accent);
  text-decoration: none;
  font-size: 0.8rem;
}

.vote-post-link:hover {
  text-decoration: underline;
}

.show-more {
  margin-top: 0.75rem;
  background: none;
  border: 1px solid var(--border);
  border-radius: 6px;
  padding: 0.45rem 1rem;
  font-family: var(--font-mono);
  font-size: 0.75rem;
  color: var(--text-muted);
  width: 100%;
  transition: all 0.15s ease;
}

.show-more:hover {
  border-color: var(--accent);
  color: var(--accent);
}
</style>
