<script setup>
import { ref, watch, onMounted } from 'vue'
import api from '../api.js'
import { useTimeAgo } from '../composables/timeago.js'

const props = defineProps({
  postId: { type: Number, required: true },
})

const comments = ref([])

async function loadComments() {
  comments.value = await api.getComments(props.postId)
}

onMounted(loadComments)
watch(() => props.postId, loadComments)
</script>

<template>
  <div class="comments-section">
    <h3 class="section-title">comments ({{ comments.length }})</h3>

    <div class="comment-list">
      <div v-for="c in comments" :key="c.id" class="comment">
        <div class="comment-meta">
          <router-link :to="`/user/${encodeURIComponent(c.author_name)}`" class="comment-author" @click.stop>{{ c.author_name }}</router-link>
          <span class="dot">·</span>
          <span class="comment-time">{{ useTimeAgo(c.created_at) }}</span>
        </div>
        <div class="comment-body">{{ c.content }}</div>
      </div>
      <div v-if="!comments.length" class="empty">no comments yet</div>
    </div>
  </div>
</template>

<style scoped>
.section-title {
  font-family: var(--font-mono);
  font-size: 0.85rem;
  font-weight: 600;
  color: var(--text-muted);
  margin-bottom: 1rem;
  text-transform: lowercase;
}

.comment-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.comment {
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
  gap: 0.3rem;
  margin-bottom: 0.3rem;
}

.comment-author {
  font-family: var(--font-mono);
  color: var(--accent);
  font-weight: 500;
  text-decoration: none;
}

.comment-author:hover {
  text-decoration: underline;
}

.dot {
  opacity: 0.4;
}

.comment-body {
  font-size: 0.85rem;
  line-height: 1.5;
}

.empty {
  font-size: 0.85rem;
  color: var(--text-muted);
  font-style: italic;
}
</style>
