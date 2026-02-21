<script setup>
defineProps({
  postId: { type: Number, required: true },
  initialScore: { type: Number, default: 0 },
})
</script>

<template>
  <div class="votes">
    <span class="arrow up">▲</span>
    <span class="score" :class="{ positive: initialScore > 0, negative: initialScore < 0 }">{{ initialScore }}</span>
    <span class="arrow down">▼</span>
  </div>
</template>

<style scoped>
.votes {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.15rem;
  min-width: 40px;
}

.arrow {
  font-size: 0.8rem;
  color: var(--border);
  line-height: 1;
  padding: 0.2rem;
}

.score {
  font-family: var(--font-mono);
  font-size: 0.85rem;
  font-weight: 600;
  color: var(--text-muted);
}

.score.positive {
  color: var(--upvote);
}

.score.negative {
  color: var(--downvote);
}
</style>
