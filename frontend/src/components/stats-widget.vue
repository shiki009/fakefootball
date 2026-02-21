<script setup>
import { useStatsStore } from '../stores/stats.js'
import { useTimeAgo } from '../composables/timeago.js'

const statsStore = useStatsStore()
</script>

<template>
  <div class="widget" v-if="statsStore.stats">
    <div class="widget-title">stats</div>
    <div class="stat-grid">
      <div class="stat">
        <span class="stat-val">{{ statsStore.stats.total_posts }}</span>
        <span class="stat-label">posts</span>
      </div>
      <div class="stat">
        <span class="stat-val">{{ statsStore.stats.total_comments }}</span>
        <span class="stat-label">comments</span>
      </div>
      <div class="stat">
        <span class="stat-val">{{ statsStore.stats.total_votes }}</span>
        <span class="stat-label">votes</span>
      </div>
      <div class="stat">
        <span class="stat-val">{{ statsStore.stats.total_tags }}</span>
        <span class="stat-label">tags</span>
      </div>
    </div>
    <div class="last-updated" v-if="statsStore.stats.last_post_at">
      last post {{ useTimeAgo(statsStore.stats.last_post_at) }}
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

.stat-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.75rem;
}

.stat {
  display: flex;
  flex-direction: column;
}

.stat-val {
  font-family: var(--font-mono);
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--accent);
}

.stat-label {
  font-size: 0.75rem;
  color: var(--text-muted);
}

.last-updated {
  margin-top: 0.75rem;
  padding-top: 0.6rem;
  border-top: 1px solid var(--border);
  font-family: var(--font-mono);
  font-size: 0.7rem;
  color: var(--text-muted);
  opacity: 0.7;
}
</style>
