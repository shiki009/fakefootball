<script setup>
import { ref, onMounted } from 'vue'
import { useTagsStore } from './stores/tags.js'
import { useStatsStore } from './stores/stats.js'
import appHeader from './components/app-header.vue'
import appFooter from './components/app-footer.vue'
import statsWidget from './components/stats-widget.vue'
import tagList from './components/tag-list.vue'
import regularsWidget from './components/regulars-widget.vue'

const tagsStore = useTagsStore()
const statsStore = useStatsStore()
const loading = ref(true)

onMounted(async () => {
  await Promise.all([
    tagsStore.fetchTags(),
    statsStore.fetchStats(),
  ])
  loading.value = false
})
</script>

<template>
  <Transition name="loader-fade">
    <div v-if="loading" class="loader-overlay">
      <div class="loader-content">
        <svg class="ronaldo-face" viewBox="0 0 200 240" fill="none" xmlns="http://www.w3.org/2000/svg">
          <!-- head outline -->
          <ellipse cx="100" cy="120" rx="65" ry="80" stroke="var(--accent)" stroke-width="2.5"/>
          <!-- hair swoosh -->
          <path d="M35 100 Q40 40 100 35 Q140 32 155 50 Q160 58 150 60 Q120 45 80 50 Q50 56 42 95" stroke="var(--accent)" stroke-width="2.5" fill="var(--accent)" fill-opacity="0.15"/>
          <!-- left eyebrow -->
          <path d="M65 95 Q78 85 95 90" stroke="var(--accent)" stroke-width="2.5" stroke-linecap="round"/>
          <!-- right eyebrow -->
          <path d="M110 90 Q125 83 140 92" stroke="var(--accent)" stroke-width="2.5" stroke-linecap="round"/>
          <!-- left eye -->
          <ellipse cx="80" cy="108" rx="10" ry="6" stroke="var(--accent)" stroke-width="2"/>
          <circle cx="80" cy="108" r="3" fill="var(--accent)"/>
          <!-- right eye -->
          <ellipse cx="124" cy="108" rx="10" ry="6" stroke="var(--accent)" stroke-width="2"/>
          <circle cx="124" cy="108" r="3" fill="var(--accent)"/>
          <!-- nose -->
          <path d="M100 105 L96 130 Q100 135 104 130 Z" stroke="var(--accent)" stroke-width="1.5" fill="none"/>
          <!-- smirk -->
          <path d="M78 148 Q90 160 105 158 Q120 156 130 148" stroke="var(--accent)" stroke-width="2.5" stroke-linecap="round" fill="none"/>
          <!-- jawline -->
          <path d="M45 130 Q50 175 100 195 Q150 175 158 130" stroke="var(--accent)" stroke-width="2" fill="none" opacity="0.3"/>
          <!-- left ear -->
          <path d="M36 105 Q25 115 32 130" stroke="var(--accent)" stroke-width="2" fill="none"/>
          <!-- right ear -->
          <path d="M165 105 Q175 115 170 130" stroke="var(--accent)" stroke-width="2" fill="none"/>
        </svg>
        <div class="loader-text">SIUUU</div>
        <div class="loader-dots">
          <span class="dot"></span>
          <span class="dot"></span>
          <span class="dot"></span>
        </div>
      </div>
    </div>
  </Transition>

  <div class="layout" v-show="!loading">
    <appHeader />
    <div class="main-grid container">
      <main class="content">
        <router-view />
      </main>
      <aside class="sidebar">
        <statsWidget />
        <regularsWidget />
        <tagList />
      </aside>
    </div>
    <appFooter />
  </div>
</template>

<style scoped>
.loader-overlay {
  position: fixed;
  inset: 0;
  z-index: 9999;
  background: var(--bg);
  display: flex;
  align-items: center;
  justify-content: center;
}

.loader-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1.5rem;
  animation: pulse-in 0.6s ease-out;
}

.ronaldo-face {
  width: 140px;
  height: 168px;
  animation: face-glow 1.5s ease-in-out infinite alternate;
}

.loader-text {
  font-family: var(--font-mono);
  font-size: 1.8rem;
  font-weight: 700;
  color: var(--accent);
  letter-spacing: 0.3em;
  animation: siuuu 1.5s ease-in-out infinite;
}

.loader-dots {
  display: flex;
  gap: 0.4rem;
}

.dot {
  width: 6px;
  height: 6px;
  background: var(--accent);
  border-radius: 50%;
  animation: bounce 1.2s ease-in-out infinite;
}

.dot:nth-child(2) { animation-delay: 0.15s; }
.dot:nth-child(3) { animation-delay: 0.3s; }

.loader-fade-leave-active {
  transition: opacity 0.4s ease;
}

.loader-fade-leave-to {
  opacity: 0;
}

@keyframes pulse-in {
  from { opacity: 0; transform: scale(0.8); }
  to { opacity: 1; transform: scale(1); }
}

@keyframes face-glow {
  from { filter: drop-shadow(0 0 8px rgba(63, 185, 80, 0.2)); }
  to { filter: drop-shadow(0 0 20px rgba(63, 185, 80, 0.5)); }
}

@keyframes siuuu {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.05); }
}

@keyframes bounce {
  0%, 80%, 100% { transform: translateY(0); opacity: 0.4; }
  40% { transform: translateY(-8px); opacity: 1; }
}

.layout {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.main-grid {
  flex: 1;
  display: grid;
  grid-template-columns: 1fr 260px;
  gap: 1.5rem;
  padding-top: 1.5rem;
  padding-bottom: 3rem;
}

.sidebar {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

@media (max-width: 768px) {
  .main-grid {
    grid-template-columns: 1fr;
  }
  .sidebar {
    order: 1;
  }
}
</style>
