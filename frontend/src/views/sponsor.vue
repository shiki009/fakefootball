<script setup>
import { ref, computed } from 'vue'
import { useTimeAgo } from '../composables/timeago.js'

const STORAGE_KEY = 'vladfm_supporters'

const beerOptions = [
  { count: 1, price: 3, label: '1 beer' },
  { count: 3, price: 9, label: '3 beers' },
  { count: 6, price: 18, label: '6-pack' },
]

const selectedOption = ref(0)
const customAmount = ref('')
const isCustom = ref(false)
const name = ref('')
const message = ref('')
const showThankYou = ref(false)

const defaultSupporters = [
  { name: 'shiki', beers: 12, message: 'keep the scoops coming, editor', time: '2 days ago' },
  { name: 'neymar_truther', beers: 6, message: 'vladFM is the only source I trust for PSG news', time: '4 days ago' },
  { name: 'anonymous', beers: 1, message: 'I lost a bet because of this site. worth it', time: '1 week ago' },
  { name: 'carlo_ansen', beers: 3, message: 'the editor works harder than my entire midfield', time: '1 week ago' },
  { name: 'corner_flag_enthusiast', beers: 18, message: 'vladFM got me through a rough transfer window', time: '2 weeks ago' },
  { name: 'tactics_board_42', beers: 1, message: '', time: '3 weeks ago' },
]

function loadUserSupporters() {
  try {
    return JSON.parse(localStorage.getItem(STORAGE_KEY)) || []
  } catch {
    return []
  }
}

function saveUserSupporters(list) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(list))
}

const userSupporters = ref(loadUserSupporters())

const allSupporters = computed(() => {
  const mapped = userSupporters.value.map(s => ({
    ...s,
    time: useTimeAgo(s.createdAt),
  }))
  return [...mapped, ...defaultSupporters]
})

const totalPrice = computed(() => {
  if (isCustom.value && customAmount.value) {
    return Number(customAmount.value)
  }
  return beerOptions[selectedOption.value].price
})

const beerCount = computed(() => {
  if (isCustom.value && customAmount.value) {
    return Math.floor(Number(customAmount.value) / 3) || 1
  }
  return beerOptions[selectedOption.value].count
})

function selectOption(index) {
  selectedOption.value = index
  isCustom.value = false
  customAmount.value = ''
}

function selectCustom() {
  isCustom.value = true
}

function buy() {
  const entry = {
    name: name.value.trim() || 'anonymous',
    beers: beerCount.value,
    message: message.value.trim(),
    createdAt: new Date().toISOString(),
  }
  userSupporters.value = [entry, ...userSupporters.value]
  saveUserSupporters(userSupporters.value)
  showThankYou.value = true
}

function reset() {
  showThankYou.value = false
  name.value = ''
  message.value = ''
  selectedOption.value = 0
  isCustom.value = false
  customAmount.value = ''
}

const perPage = 3
const supportersPage = ref(1)

const visibleSupporters = computed(() => {
  return allSupporters.value.slice(0, supportersPage.value * perPage)
})

const hasMoreSupporters = computed(() => {
  return allSupporters.value.length > supportersPage.value * perPage
})

const remainingSupporters = computed(() => {
  return allSupporters.value.length - supportersPage.value * perPage
})

const thankYouLines = [
  "the editor raises a cold one in your honor.",
  "this will fuel at least 2 more fabricated transfer rumors.",
  "your generosity will be remembered (and slightly exaggerated).",
  "the vladFM newsroom morale just went up by 400%.",
]

const thankYouLine = computed(() => {
  return thankYouLines[Math.floor(Math.random() * thankYouLines.length)]
})
</script>

<template>
  <div class="sponsor">
    <router-link to="/" class="back-btn">&larr; back</router-link>

    <div class="sponsor-header">
      <h1 class="title">buy the editor a beer</h1>
      <p class="subtitle">running vladFM is thirsty work. every beer fuels another completely fabricated headline.</p>
    </div>

    <div v-if="!showThankYou">
      <div class="section">
        <h2 class="section-title">choose your round</h2>
        <div class="beer-options">
          <button
            v-for="(opt, i) in beerOptions"
            :key="i"
            class="beer-btn"
            :class="{ active: !isCustom && selectedOption === i }"
            @click="selectOption(i)"
          >
            <span class="beer-emoji">&#x1F37A;</span>
            <span class="beer-label">{{ opt.label }}</span>
            <span class="beer-price">&euro;{{ opt.price }}</span>
          </button>
        </div>
        <div class="custom-row">
          <button
            class="beer-btn custom-toggle"
            :class="{ active: isCustom }"
            @click="selectCustom"
          >custom</button>
          <input
            v-if="isCustom"
            v-model="customAmount"
            type="number"
            min="1"
            class="custom-input"
            placeholder="&euro;"
          />
        </div>
      </div>

      <div class="section">
        <h2 class="section-title">say something (optional)</h2>
        <input
          v-model="name"
          type="text"
          class="field"
          placeholder="your name or alias"
        />
        <textarea
          v-model="message"
          class="field textarea"
          placeholder="leave a message for the editor..."
          rows="3"
        ></textarea>
      </div>

      <button class="buy-btn" @click="buy">
        buy {{ isCustom && customAmount ? customAmount : beerOptions[selectedOption].count }} beer{{ (isCustom ? Number(customAmount) : beerOptions[selectedOption].count) === 1 ? '' : 's' }} &mdash; &euro;{{ totalPrice }}
      </button>
    </div>

    <div v-else class="thank-you">
      <div class="thank-you-card">
        <span class="thank-you-icon">&#x1F37B;</span>
        <h2 class="thank-you-title">cheers{{ name ? ', ' + name : '' }}!</h2>
        <p class="thank-you-text">{{ thankYouLine }}</p>
        <p class="thank-you-note">no money was actually charged. this is vladFM after all.</p>
        <button class="reset-btn" @click="reset">buy another round</button>
      </div>
    </div>

    <div class="section supporters">
      <h2 class="section-title">recent supporters</h2>
      <div class="supporter-list">
        <div v-for="(s, i) in visibleSupporters" :key="i" class="supporter">
          <div class="supporter-top">
            <span class="supporter-name">{{ s.name }}</span>
            <span class="supporter-beers">&#x1F37A; &times;{{ s.beers }}</span>
          </div>
          <p v-if="s.message" class="supporter-msg">"{{ s.message }}"</p>
          <span class="supporter-time">{{ s.time }}</span>
        </div>
        <button v-if="hasMoreSupporters" class="show-more" @click="supportersPage++">
          show more supporters ({{ remainingSupporters }} remaining)
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.sponsor {
  max-width: 640px;
}

.back-btn {
  display: inline-block;
  color: var(--text-muted);
  font-family: var(--font-mono);
  font-size: 0.8rem;
  padding: 0.3rem 0;
  margin-bottom: 1rem;
  text-decoration: none;
  transition: color 0.15s ease;
}

.back-btn:hover {
  color: var(--accent);
}

.sponsor-header {
  margin-bottom: 2rem;
}

.title {
  font-family: var(--font-mono);
  font-size: 1.4rem;
  font-weight: 700;
  margin-bottom: 0.3rem;
}

.subtitle {
  font-size: 0.85rem;
  color: var(--text-muted);
}

.section {
  margin-bottom: 1.5rem;
}

.section-title {
  font-family: var(--font-mono);
  font-size: 0.85rem;
  font-weight: 600;
  color: var(--text-muted);
  text-transform: lowercase;
  margin-bottom: 0.75rem;
}

.beer-options {
  display: flex;
  gap: 0.5rem;
}

.beer-btn {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.3rem;
  padding: 0.75rem 0.5rem;
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 6px;
  cursor: pointer;
  font-family: var(--font-mono);
  color: var(--text);
  transition: border-color 0.15s ease, background 0.15s ease;
}

.beer-btn:hover {
  border-color: var(--accent);
}

.beer-btn.active {
  border-color: var(--accent);
  background: rgba(74, 222, 128, 0.08);
}

.beer-emoji {
  font-size: 1.5rem;
}

.beer-label {
  font-size: 0.8rem;
  font-weight: 600;
}

.beer-price {
  font-size: 0.75rem;
  color: var(--text-muted);
}

.custom-row {
  display: flex;
  gap: 0.5rem;
  margin-top: 0.5rem;
}

.custom-toggle {
  flex: none;
  padding: 0.5rem 1rem;
  font-size: 0.8rem;
}

.custom-input {
  flex: 1;
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 6px;
  padding: 0.5rem 0.75rem;
  color: var(--text);
  font-family: var(--font-mono);
  font-size: 0.85rem;
  outline: none;
}

.custom-input:focus {
  border-color: var(--accent);
}

.field {
  display: block;
  width: 100%;
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 6px;
  padding: 0.6rem 0.75rem;
  color: var(--text);
  font-family: var(--font-mono);
  font-size: 0.85rem;
  outline: none;
  margin-bottom: 0.5rem;
  box-sizing: border-box;
}

.field:focus {
  border-color: var(--accent);
}

.textarea {
  resize: vertical;
  min-height: 60px;
}

.buy-btn {
  display: block;
  width: 100%;
  padding: 0.75rem;
  background: var(--accent);
  color: var(--bg);
  border: none;
  border-radius: 6px;
  font-family: var(--font-mono);
  font-size: 0.9rem;
  font-weight: 700;
  cursor: pointer;
  transition: opacity 0.15s ease;
  margin-bottom: 2rem;
}

.buy-btn:hover {
  opacity: 0.85;
}

.thank-you {
  margin-bottom: 2rem;
}

.thank-you-card {
  background: var(--bg-card);
  border: 1px solid var(--accent);
  border-radius: 8px;
  padding: 2rem;
  text-align: center;
}

.thank-you-icon {
  font-size: 2.5rem;
  display: block;
  margin-bottom: 0.75rem;
}

.thank-you-title {
  font-family: var(--font-mono);
  font-size: 1.2rem;
  font-weight: 700;
  margin-bottom: 0.5rem;
}

.thank-you-text {
  font-size: 0.85rem;
  color: var(--text-muted);
  margin-bottom: 0.75rem;
}

.thank-you-note {
  font-family: var(--font-mono);
  font-size: 0.7rem;
  color: var(--text-muted);
  opacity: 0.6;
  font-style: italic;
  margin-bottom: 1rem;
}

.reset-btn {
  background: transparent;
  border: 1px solid var(--border);
  border-radius: 6px;
  padding: 0.5rem 1rem;
  color: var(--accent);
  font-family: var(--font-mono);
  font-size: 0.8rem;
  font-weight: 600;
  cursor: pointer;
  transition: border-color 0.15s ease;
}

.reset-btn:hover {
  border-color: var(--accent);
}

.supporters {
  margin-bottom: 2rem;
}

.supporter-list {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.supporter {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 6px;
  padding: 0.75rem;
}

.supporter-top {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.25rem;
}

.supporter-name {
  font-family: var(--font-mono);
  font-size: 0.85rem;
  font-weight: 600;
}

.supporter-beers {
  font-family: var(--font-mono);
  font-size: 0.75rem;
  color: var(--text-muted);
}

.supporter-msg {
  font-size: 0.8rem;
  color: var(--text-muted);
  font-style: italic;
  margin-bottom: 0.25rem;
}

.supporter-time {
  font-family: var(--font-mono);
  font-size: 0.65rem;
  color: var(--text-muted);
  opacity: 0.6;
}

.show-more {
  margin-top: 0.75rem;
  background: none;
  border: 1px solid var(--border);
  border-radius: 6px;
  padding: 0.45rem 1rem;
  font-family: var(--font-mono);
  font-size: 0.75rem;
  color: var(--text-muted);
  width: 100%;
  cursor: pointer;
  transition: all 0.15s ease;
}

.show-more:hover {
  border-color: var(--accent);
  color: var(--accent);
}
</style>
