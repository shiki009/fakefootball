<script setup>
import { computed, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useTimeAgo } from '../composables/timeago.js'
import voteButtons from './vote-buttons.vue'
import tagBadge from './tag-badge.vue'

const props = defineProps({
  post: { type: Object, required: true },
})

const router = useRouter()
const truthScore = ref(props.post.truth_score)
const copied = ref(false)

function onTruthUpdated(newScore) {
  truthScore.value = newScore
}

function share() {
  const url = `${window.location.origin}/post/${props.post.slug}`
  navigator.clipboard.writeText(url)
  copied.value = true
  setTimeout(() => { copied.value = false }, 1500)
}

const isTrueStory = computed(() => truthScore.value >= 60)

const truthLabel = computed(() => {
  const s = truthScore.value
  if (s >= 100) return 'confirmed true'
  if (s >= 60) return 'true story'
  if (s >= 40) return 'unverified'
  if (s >= 20) return 'doubtful'
  return 'fake'
})

const truthColor = computed(() => {
  const s = truthScore.value
  if (s >= 60) return 'var(--green)'
  if (s >= 40) return '#f59e0b'
  return 'var(--text-muted)'
})

function goToPost() {
  router.push(`/post/${props.post.slug}`)
}

function goToTag(slug) {
  router.push(`/tag/${slug}`)
}
</script>

<template>
  <div
    :class="['card', { 'true-story-glow': isTrueStory }]"
    @click="goToPost"
  >
    <voteButtons :postId="post.id" :initialScore="post.score" @truth-updated="onTruthUpdated" />
    <div class="card-body">
      <div class="card-title">
        {{ post.title }}
        <span v-if="isTrueStory" class="true-badge">✓ true story</span>
      </div>
      <div class="card-meta">
        <router-link :to="`/user/${encodeURIComponent(post.author_name)}`" class="author" @click.stop>{{ post.author_name }}</router-link>
        <span class="dot">·</span>
        <span class="time">{{ useTimeAgo(post.created_at) }}</span>
        <span class="dot">·</span>
        <span class="comments">{{ post.comment_count }} comments</span>
        <span class="dot">·</span>
        <span class="share-btn" @click.stop="share">{{ copied ? 'copied!' : 'share' }}</span>
      </div>
      <div class="truth-meter">
        <div class="truth-bar">
          <div class="truth-fill" :style="{ width: truthScore + '%', background: truthColor }"></div>
        </div>
        <span class="truth-label" :style="{ color: truthColor }">{{ truthLabel }} {{ truthScore }}%</span>
      </div>
      <div class="card-tags" v-if="post.tags.length">
        <tagBadge
          v-for="t in post.tags"
          :key="t.id"
          :tag="t"
          @click.stop="goToTag(t.slug)"
        />
      </div>
    </div>
  </div>
</template>

<style scoped>
.card {
  display: flex;
  gap: 0.75rem;
  padding: 0.75rem;
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.15s ease;
}

.card:hover {
  background: var(--bg-hover);
  border-color: var(--text-muted);
}

.card-body {
  flex: 1;
  min-width: 0;
}

.card-title {
  font-size: 0.95rem;
  font-weight: 600;
  line-height: 1.4;
  margin-bottom: 0.35rem;
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

.card-meta {
  font-size: 0.75rem;
  color: var(--text-muted);
  display: flex;
  align-items: center;
  gap: 0.35rem;
  margin-bottom: 0.35rem;
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

.dot {
  opacity: 0.4;
}

.truth-meter {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 0.35rem;
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
  white-space: nowrap;
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

.card-tags {
  display: flex;
  gap: 0.3rem;
  flex-wrap: wrap;
}
</style>
