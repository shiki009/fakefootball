<script setup>
import { useRouter } from 'vue-router'
import { usePostsStore } from '../stores/posts.js'

const router = useRouter()
const postsStore = usePostsStore()

const siteName = 'vladFM'

function goHome() {
  postsStore.activeTag = null
  router.push('/')
}
</script>

<template>
  <header class="header">
    <div class="container header-inner">
      <div class="logo" @click="goHome">
        <svg class="logo-icon" viewBox="0 0 200 240" fill="none">
          <ellipse cx="100" cy="120" rx="65" ry="80" stroke="currentColor" stroke-width="2.5"/>
          <path d="M35 100 Q40 40 100 35 Q140 32 155 50 Q160 58 150 60 Q120 45 80 50 Q50 56 42 95" stroke="currentColor" stroke-width="2.5" fill="currentColor" fill-opacity="0.15"/>
          <path d="M65 95 Q78 85 95 90" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"/>
          <path d="M110 90 Q125 83 140 92" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"/>
          <ellipse cx="80" cy="108" rx="10" ry="6" stroke="currentColor" stroke-width="2"/>
          <circle cx="80" cy="108" r="3" fill="currentColor"/>
          <ellipse cx="124" cy="108" rx="10" ry="6" stroke="currentColor" stroke-width="2"/>
          <circle cx="124" cy="108" r="3" fill="currentColor"/>
          <path d="M100 105 L96 130 Q100 135 104 130 Z" stroke="currentColor" stroke-width="1.5" fill="none"/>
          <path d="M78 148 Q90 160 105 158 Q120 156 130 148" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" fill="none"/>
          <path d="M36 105 Q25 115 32 130" stroke="currentColor" stroke-width="2" fill="none"/>
          <path d="M165 105 Q175 115 170 130" stroke="currentColor" stroke-width="2" fill="none"/>
        </svg>
        <span class="logo-text">{{ siteName }}</span>
      </div>
      <div class="header-right">
        <router-link to="/sponsor" class="about-link">sponsor</router-link>
        <router-link to="/about" class="about-link">about</router-link>
        <div class="tagline">the news that never happened</div>
      </div>
    </div>
  </header>
</template>

<style scoped>
.header {
  border-bottom: 1px solid var(--border);
  background: var(--bg-card);
}

.header-inner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-top: 0.75rem;
  padding-bottom: 0.75rem;
}

.logo {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
  user-select: none;
}

.logo-icon {
  width: 28px;
  height: 32px;
  color: var(--accent);
}

.logo-text {
  font-family: var(--font-mono);
  font-weight: 700;
  font-size: 1.2rem;
  color: var(--accent);
}

.header-right {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.about-link {
  font-family: var(--font-mono);
  font-size: 0.75rem;
  color: var(--accent);
  text-decoration: none;
  font-weight: 600;
  transition: opacity 0.15s ease;
}

.about-link:hover {
  opacity: 0.8;
  text-decoration: none;
}

.tagline {
  font-family: var(--font-mono);
  font-size: 0.75rem;
  color: var(--text-muted);
}

@media (max-width: 500px) {
  .tagline {
    display: none;
  }
}
</style>
