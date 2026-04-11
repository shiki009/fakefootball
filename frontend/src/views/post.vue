<script setup>
import { onMounted, onUnmounted, watch, ref, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { usePostsStore } from '../stores/posts.js'
import { useTimeAgo } from '../composables/timeago.js'
import { authorLink } from '../composables/authorlink.js'
import voteButtons from '../components/vote-buttons.vue'
import tagBadge from '../components/tag-badge.vue'
import commentList from '../components/comment-list.vue'
import loadingSpinner from '../components/loading-spinner.vue'

const route = useRoute()
const router = useRouter()
const postsStore = usePostsStore()
const copied = ref(false)

const isTrueStory = computed(() => postsStore.currentPost?.truth_score >= 60)

const truthLabel = computed(() => {
  const s = postsStore.currentPost?.truth_score ?? 0
  if (s >= 100) return 'confirmed true'
  if (s >= 60) return 'true story'
  if (s >= 40) return 'unverified'
  if (s >= 20) return 'doubtful'
  return 'fake'
})

const truthColor = computed(() => {
  const s = postsStore.currentPost?.truth_score ?? 0
  if (s >= 60) return 'var(--green)'
  if (s >= 40) return '#f59e0b'
  return 'var(--text-muted)'
})

function setMeta(post) {
  if (!post) return
  const title = `${post.title} — vladFM`
  const desc = post.content.slice(0, 160).replace(/\n/g, ' ')
  const ogImage = `${window.location.origin}/api/og/${post.slug}`
  const postUrl = `${window.location.origin}/post/${post.slug}`
  document.title = title
  const setTag = (sel, attr, val) => {
    let el = document.querySelector(sel)
    if (!el) { el = document.createElement('meta'); document.head.appendChild(el) }
    el.setAttribute(attr, val)
  }
  setTag('meta[name="description"]', 'content', desc)
  setTag('meta[property="og:title"]', 'content', title)
  setTag('meta[property="og:description"]', 'content', desc)
  setTag('meta[property="og:image"]', 'content', ogImage)
  setTag('meta[property="og:url"]', 'content', postUrl)
  setTag('meta[property="og:type"]', 'content', 'article')
  setTag('meta[name="twitter:card"]', 'content', 'summary_large_image')
  setTag('meta[name="twitter:title"]', 'content', title)
  setTag('meta[name="twitter:description"]', 'content', desc)
  setTag('meta[name="twitter:image"]', 'content', ogImage)
}

function resetMeta() {
  document.title = 'vladFM — the news that never happened'
  const orig = 'the news that never happened — fake football news you can believe in'
  const setTag = (sel, attr, val) => { const el = document.querySelector(sel); if (el) el.setAttribute(attr, val) }
  setTag('meta[name="description"]', 'content', orig)
  setTag('meta[property="og:title"]', 'content', 'vladFM')
  setTag('meta[property="og:description"]', 'content', orig)
  setTag('meta[property="og:image"]', 'content', '/favicon.svg')
  setTag('meta[property="og:url"]', 'content', window.location.origin)
  setTag('meta[property="og:type"]', 'content', 'website')
  setTag('meta[name="twitter:card"]', 'content', 'summary')
  setTag('meta[name="twitter:title"]', 'content', 'vladFM')
  setTag('meta[name="twitter:description"]', 'content', orig)
  setTag('meta[name="twitter:image"]', 'content', '/favicon.svg')
}

async function load() {
  await postsStore.fetchPost(route.params.slug)
  setMeta(postsStore.currentPost)
}

onMounted(load)
watch(() => route.params.slug, load)
onUnmounted(resetMeta)

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
            <router-link v-if="authorLink(postsStore.currentPost.author_name)" :to="authorLink(postsStore.currentPost.author_name)" class="author">{{ postsStore.currentPost.author_name }}</router-link>
            <span v-else class="author author-plain">{{ postsStore.currentPost.author_name }}</span>
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
          <div class="truth-meter">
            <div class="truth-bar">
              <div class="truth-fill" :style="{ width: postsStore.currentPost.truth_score + '%', background: truthColor }"></div>
            </div>
            <span class="truth-label" :style="{ color: truthColor }">{{ truthLabel }} {{ postsStore.currentPost.truth_score }}%</span>
          </div>
        </div>
      </div>

      <div class="post-content">
        <p v-for="(para, i) in postsStore.currentPost.content.split(/\n\n+/)" :key="i">{{ para }}</p>
      </div>
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
  min-width: 0;
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
  flex-wrap: wrap;
}

.author {
  font-family: var(--font-mono);
  color: var(--accent);
  text-decoration: none;
}

.author:hover {
  text-decoration: underline;
}

.author-plain {
  cursor: default;
  color: var(--text-muted);
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
  margin-bottom: 0.5rem;
}

.truth-meter {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-top: 0.5rem;
}

.truth-bar {
  flex: 1;
  height: 4px;
  background: var(--border);
  border-radius: 2px;
  max-width: 80px;
  overflow: hidden;
}

.truth-fill {
  height: 100%;
  border-radius: 2px;
  transition: width 0.3s ease;
}

.truth-label {
  font-family: var(--font-mono);
  font-size: 0.65rem;
  font-weight: 500;
}

.post-content {
  font-size: 0.9rem;
  line-height: 1.7;
  color: var(--text);
  padding-top: 1rem;
  border-top: 1px solid var(--border);
  display: flex;
  flex-direction: column;
  gap: 0.9rem;
}

.post-content p {
  margin: 0;
}

.comments-block {
  margin-top: 1.5rem;
}
</style>
