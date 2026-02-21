<script setup>
import { useRouter } from 'vue-router'
const router = useRouter()

const quotes = [
  "my source confirmed this page existed — I just can't find it right now",
  "I've seen this URL before on a vladFM telegram group. it was real. something happened to it",
  "the page was here. I have screenshots. someone removed it and I think I know why",
  "this is exactly what they want you to think. the page is there, you just can't see it",
  "I watched this page load three times last week. the 404 is part of the story",
]
const quote = quotes[Math.floor(Math.random() * quotes.length)]
</script>

<template>
  <div class="notfound">
    <div class="code">404</div>
    <div class="msg">this page got a red card</div>
    <div class="shiki-block">
      <div class="shiki-header">
        <router-link to="/regulars/shiki" class="shiki-name">shiki</router-link>
        <span class="shiki-label">vladFM moderator · my source confirmed</span>
      </div>
      <div class="shiki-quote">"{{ quote }}"</div>
    </div>
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
  margin: 1rem 0 1.5rem;
}

.shiki-block {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-left: 3px solid var(--accent);
  border-radius: 8px;
  padding: 0.85rem 1rem;
  margin-bottom: 2rem;
  max-width: 420px;
  text-align: left;
}

.shiki-header {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 0.4rem;
}

.shiki-name {
  font-family: var(--font-mono);
  font-size: 0.78rem;
  font-weight: 700;
  color: var(--accent);
  text-decoration: none;
}

.shiki-name:hover {
  text-decoration: underline;
}

.shiki-label {
  font-family: var(--font-mono);
  font-size: 0.68rem;
  color: var(--text-muted);
  opacity: 0.7;
}

.shiki-quote {
  font-size: 0.83rem;
  line-height: 1.5;
  color: var(--text);
  font-style: italic;
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
