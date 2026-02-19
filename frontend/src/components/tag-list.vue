<script setup>
import { useTagsStore } from '../stores/tags.js'
import { usePostsStore } from '../stores/posts.js'
import { useRouter } from 'vue-router'
import tagBadge from './tag-badge.vue'

const tagsStore = useTagsStore()
const postsStore = usePostsStore()
const router = useRouter()

function selectTag(slug) {
  if (postsStore.activeTag === slug) {
    postsStore.activeTag = null
    router.push('/')
  } else {
    postsStore.setTag(slug)
    router.push(`/tag/${slug}`)
  }
}
</script>

<template>
  <div class="widget" v-if="tagsStore.tags.length">
    <div class="widget-title">tags</div>
    <div class="tag-wrap">
      <tagBadge
        v-for="t in tagsStore.tags"
        :key="t.id"
        :tag="t"
        :active="postsStore.activeTag === t.slug"
        @click="selectTag(t.slug)"
      />
    </div>
  </div>
</template>

<style scoped>
.widget {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 1rem;
}

.widget-title {
  font-family: var(--font-mono);
  font-size: 0.8rem;
  font-weight: 600;
  color: var(--text-muted);
  text-transform: lowercase;
  margin-bottom: 0.75rem;
}

.tag-wrap {
  display: flex;
  flex-wrap: wrap;
  gap: 0.4rem;
}
</style>
