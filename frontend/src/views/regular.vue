<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import api from '../api.js'
import { useTimeAgo } from '../composables/timeago.js'
import loadingSpinner from '../components/loading-spinner.vue'

const route = useRoute()
const profile = ref(null)
const loading = ref(true)
const error = ref(false)

async function load() {
  loading.value = true
  error.value = false
  try {
    profile.value = await api.getRegular(route.params.name)
  } catch {
    error.value = true
  } finally {
    loading.value = false
  }
}

onMounted(load)
watch(() => route.params.name, load)
</script>

<template>
  <div>
    <router-link to="/regulars" class="back-btn">← regulars</router-link>

    <loadingSpinner v-if="loading" />

    <div v-else-if="error" class="error-msg">regular not found</div>

    <div v-else-if="profile" class="profile">
      <div class="profile-header">
        <div class="name-row">
          <h1 class="name">{{ profile.name }}</h1>
          <span class="badge">regular</span>
        </div>
        <p class="bio">{{ profile.bio }}</p>
        <div class="stats-row">
          <span class="stat">{{ profile.comments }} comments</span>
          <span class="dot">·</span>
          <span class="stat">{{ profile.votes_cast }} votes cast</span>
        </div>
      </div>

      <section v-if="profile.recent_comments.length" class="section">
        <h2 class="section-title">recent comments</h2>
        <div class="comment-list">
          <div v-for="c in profile.recent_comments" :key="c.id" class="comment-item">
            <div class="comment-meta">
              <router-link :to="`/post/${c.post_slug}`" class="post-link">{{ c.post_title }}</router-link>
              <span class="time">{{ useTimeAgo(c.created_at) }}</span>
            </div>
            <div class="comment-body">{{ c.content }}</div>
          </div>
        </div>
      </section>

      <div v-else class="empty">no comments yet</div>
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

.error-msg,
.empty {
  text-align: center;
  padding: 3rem;
  color: var(--text-muted);
  font-family: var(--font-mono);
  font-size: 0.85rem;
}

.profile-header {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 1.25rem;
  margin-bottom: 1.5rem;
}

.name-row {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 0.5rem;
}

.name {
  font-family: var(--font-mono);
  font-size: 1.3rem;
  font-weight: 700;
}

.badge {
  font-family: var(--font-mono);
  font-size: 0.65rem;
  font-weight: 600;
  color: var(--green);
  background: var(--green-dim);
  padding: 0.1rem 0.4rem;
  border-radius: 3px;
}

.bio {
  font-size: 0.85rem;
  line-height: 1.55;
  color: var(--text-muted);
  margin-bottom: 0.6rem;
}

.stats-row {
  display: flex;
  align-items: center;
  gap: 0.35rem;
  font-family: var(--font-mono);
  font-size: 0.78rem;
  color: var(--text-muted);
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
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.75rem;
  color: var(--text-muted);
  margin-bottom: 0.3rem;
  flex-wrap: wrap;
}

.post-link {
  font-family: var(--font-mono);
  color: var(--accent);
  text-decoration: none;
  font-weight: 500;
}

.post-link:hover {
  text-decoration: underline;
}

.time {
  font-family: var(--font-mono);
  font-size: 0.7rem;
}

.comment-body {
  font-size: 0.85rem;
  line-height: 1.5;
}
</style>
