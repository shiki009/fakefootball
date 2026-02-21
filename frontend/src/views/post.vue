<script setup>
import { onMounted, watch, ref, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { usePostsStore } from '../stores/posts.js'
import { useTimeAgo } from '../composables/timeago.js'
import voteButtons from '../components/vote-buttons.vue'
import tagBadge from '../components/tag-badge.vue'
import commentList from '../components/comment-list.vue'
import loadingSpinner from '../components/loading-spinner.vue'

const route = useRoute()
const router = useRouter()
const postsStore = usePostsStore()
const copied = ref(false)

const isTrueStory = computed(() => postsStore.currentPost?.truth_score >= 60)

function load() {
  postsStore.fetchPost(route.params.slug)
}

onMounted(load)
watch(() => route.params.slug, load)

function goToTag(slug) {
  router.push(`/tag/${slug}`)
}

function share() {
  navigator.clipboard.writeText(window.location.href)
  copied.value = true
  setTimeout(() => { copied.value = false }, 1500)
}
</script>

<template>
  <div>
    <button class="back-btn" @click="router.push('/')">← back</button>

    <loadingSpinner v-if="postsStore.loading" />

    <article v-else-if="postsStore.currentPost" class="post-detail" :class="{ 'true-story-glow': isTrueStory }">
      <div class="post-header">
        <voteButtons
          :postId="postsStore.currentPost.id"
          :initialScore="postsStore.currentPost.score"
        />
        <div class="post-info">
          <h1 class="post-title">
            {{ postsStore.currentPost.title }}
            <span v-if="isTrueStory" class="true-badge">✓ true story</span>
          </h1>
          <div class="post-meta">
            <router-link :to="`/user/${encodeURIComponent(postsStore.currentPost.author_name)}`" class="author">{{ postsStore.currentPost.author_name }}</router-link>
            <span class="dot">·</span>
            <span>{{ useTimeAgo(postsStore.currentPost.created_at) }}</span>
            <span class="dot">·</span>
            <span class="share-btn" @click="share">{{ copied ? 'copied!' : 'share' }}</span>
          </div>
          <div class="post-tags" v-if="postsStore.currentPost.tags.length">
            <tagBadge
              v-for="t in postsStore.currentPost.tags"
              :key="t.id"
              :tag="t"
              @click="goToTag(t.slug)"
            />
          </div>
        </div>
      </div>

      <div class="post-content">{{ postsStore.currentPost.content }}</div>
    </article>

    <commentList
      v-if="postsStore.currentPost"
      :postId="postsStore.currentPost.id"
      class="comments-block"
    />
  </div>
</template>

<style scoped>
.back-btn {
  background: none;
  border: none;
  color: var(--text-muted);
  font-family: var(--font-mono);
  font-size: 0.8rem;
  padding: 0.3rem 0;
  margin-bottom: 1rem;
  transition: color 0.15s ease;
}

.back-btn:hover {
  color: var(--accent);
}

.post-detail {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 1.25rem;
}

.post-header {
  display: flex;
  gap: 0.75rem;
  margin-bottom: 1rem;
}

.post-info {
  flex: 1;
}

.post-title {
  font-size: 1.2rem;
  font-weight: 700;
  line-height: 1.4;
  margin-bottom: 0.4rem;
}

.true-badge {
  font-family: var(--font-mono);
  font-size: 0.65rem;
  font-weight: 600;
  color: var(--green);
  background: var(--green-dim);
  padding: 0.1rem 0.4rem;
  border-radius: 3px;
  margin-left: 0.4rem;
  vertical-align: middle;
}

.post-meta {
  font-size: 0.8rem;
  color: var(--text-muted);
  display: flex;
  align-items: center;
  gap: 0.35rem;
  margin-bottom: 0.5rem;
}

.author {
  font-family: var(--font-mono);
  color: var(--accent);
  text-decoration: none;
}

.author:hover {
  text-decoration: underline;
}

.dot {
  opacity: 0.4;
}

.share-btn {
  font-family: var(--font-mono);
  color: var(--text-muted);
  cursor: pointer;
  transition: color 0.15s ease;
}

.share-btn:hover {
  color: var(--accent);
}

.post-tags {
  display: flex;
  gap: 0.3rem;
  flex-wrap: wrap;
}

.post-content {
  font-size: 0.9rem;
  line-height: 1.7;
  color: var(--text);
  padding-top: 1rem;
  border-top: 1px solid var(--border);
}

.comments-block {
  margin-top: 1.5rem;
}
</style>
