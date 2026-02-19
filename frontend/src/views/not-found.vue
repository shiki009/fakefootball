<script setup>
import { useRouter } from 'vue-router'
const router = useRouter()
</script>

<template>
  <div class="notfound">
    <div class="code">404</div>
    <div class="msg">this page got a red card</div>
    <button class="home-btn" @click="router.push('/')">back to pitch</button>
  </div>
</template>

<style scoped>
.notfound {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 5rem 1rem;
  text-align: center;
}

.code {
  font-family: var(--font-mono);
  font-size: 4rem;
  font-weight: 700;
  color: var(--accent);
  line-height: 1;
}

.msg {
  font-family: var(--font-mono);
  font-size: 0.9rem;
  color: var(--text-muted);
  margin: 1rem 0 2rem;
}

.home-btn {
  background: var(--accent);
  color: var(--bg);
  border: none;
  border-radius: 6px;
  padding: 0.5rem 1.25rem;
  font-family: var(--font-mono);
  font-size: 0.85rem;
  font-weight: 600;
  transition: opacity 0.15s ease;
}

.home-btn:hover {
  opacity: 0.85;
}
</style>
