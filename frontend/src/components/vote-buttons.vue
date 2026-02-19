<script setup>
import { ref, watch, onMounted } from 'vue'
import api from '../api.js'
import { useFingerprint } from '../composables/fingerprint.js'

const props = defineProps({
  postId: { type: Number, required: true },
  initialScore: { type: Number, default: 0 },
})

const emit = defineEmits(['truth-updated'])

const fp = useFingerprint()
const score = ref(props.initialScore)
const userVote = ref(0)

async function loadVote() {
  score.value = props.initialScore
  const data = await api.getVote(props.postId, fp.value)
  score.value = data.score
  userVote.value = data.user_vote
}

onMounted(loadVote)
watch(() => props.postId, loadVote)

async function castVote(value) {
  const newValue = userVote.value === value ? 0 : value
  const data = await api.vote(props.postId, fp.value, newValue)
  score.value = data.score
  userVote.value = data.user_vote
  emit('truth-updated', data.truth_score)
}
</script>

<template>
  <div class="votes">
    <button
      :class="['vote-btn', 'up', { active: userVote === 1 }]"
      @click.stop="castVote(1)"
    >▲</button>
    <span class="score" :class="{ positive: score > 0, negative: score < 0 }">{{ score }}</span>
    <button
      :class="['vote-btn', 'down', { active: userVote === -1 }]"
      @click.stop="castVote(-1)"
    >▼</button>
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

.vote-btn {
  background: none;
  border: none;
  font-size: 0.8rem;
  color: var(--text-muted);
  padding: 0.2rem;
  border-radius: 4px;
  line-height: 1;
  transition: all 0.15s ease;
}

.vote-btn:hover {
  background: var(--bg-hover);
}

.vote-btn.up.active {
  color: var(--upvote);
}

.vote-btn.down.active {
  color: var(--downvote);
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
