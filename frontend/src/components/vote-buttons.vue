<script setup>
defineProps({
  postId: { type: Number, required: true },
  initialScore: { type: Number, default: 0 },
})
</script>

<template>
  <div class="votes" title="voted on by the regulars">
    <span class="score" :class="{ positive: initialScore > 0, negative: initialScore < 0, zero: initialScore === 0 }">
      {{ initialScore > 0 ? '+' : '' }}{{ initialScore }}
    </span>
    <span class="label">votes</span>
  </div>
</template>

<style scoped>
.votes {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 0.1rem;
  min-width: 40px;
}

.score {
  font-family: var(--font-mono);
  font-size: 0.9rem;
  font-weight: 700;
  line-height: 1;
}

.score.positive {
  color: var(--upvote);
}

.score.negative {
  color: var(--downvote);
}

.score.zero {
  color: var(--text-muted);
}

.label {
  font-family: var(--font-mono);
  font-size: 0.6rem;
  color: var(--text-muted);
  text-transform: lowercase;
  opacity: 0.6;
}
</style>
