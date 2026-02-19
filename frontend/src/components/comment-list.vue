<script setup>
import { ref, watch, onMounted } from 'vue'
import api from '../api.js'
import { useTimeAgo } from '../composables/timeago.js'

const props = defineProps({
  postId: { type: Number, required: true },
})

const comments = ref([])
const authorName = ref('')
const content = ref('')
const submitting = ref(false)

async function loadComments() {
  comments.value = await api.getComments(props.postId)
}

onMounted(loadComments)
watch(() => props.postId, loadComments)

async function submit() {
  if (!content.value.trim()) return
  submitting.value = true
  try {
    const c = await api.addComment(props.postId, authorName.value || 'anonymous', content.value)
    comments.value.unshift(c)
    content.value = ''
    authorName.value = ''
  } finally {
    submitting.value = false
  }
}
</script>

<template>
  <div class="comments-section">
    <h3 class="section-title">comments ({{ comments.length }})</h3>

    <form class="comment-form" @submit.prevent="submit">
      <input
        v-model="authorName"
        class="input"
        placeholder="name (optional)"
      />
      <textarea
        v-model="content"
        class="input textarea"
        placeholder="write something..."
        rows="3"
      ></textarea>
      <button class="submit-btn" :disabled="!content.trim() || submitting">
        {{ submitting ? '...' : 'post comment' }}
      </button>
    </form>

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

.comment-form {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  margin-bottom: 1.5rem;
}

.input {
  background: var(--bg-input);
  border: 1px solid var(--border);
  border-radius: 6px;
  padding: 0.5rem 0.75rem;
  color: var(--text);
  font-size: 0.85rem;
  outline: none;
  transition: border-color 0.15s ease;
}

.input:focus {
  border-color: var(--accent);
}

.textarea {
  resize: vertical;
  min-height: 60px;
  font-family: inherit;
}

.submit-btn {
  align-self: flex-end;
  background: var(--accent);
  color: var(--bg);
  border: none;
  border-radius: 6px;
  padding: 0.45rem 1rem;
  font-family: var(--font-mono);
  font-size: 0.8rem;
  font-weight: 600;
  transition: opacity 0.15s ease;
}

.submit-btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.submit-btn:not(:disabled):hover {
  opacity: 0.85;
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
