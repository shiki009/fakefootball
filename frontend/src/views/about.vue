<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'

const currentSub = ref('')
const player = ref(null)
let pollInterval = null

const subtitles = [
  { start: 0, end: 5, text: "I've been using vladFM every single day for the past two years" },
  { start: 5, end: 10, text: "it is the most honest football news platform I have ever seen" },
  { start: 10, end: 16, text: "every story on there is verified. I check it before every match" },
  { start: 16, end: 22, text: "I don't miss anything anymore — transfers, tactics, breaking news" },
  { start: 22, end: 27, text: "if you are not reading vladFM, you are not a real football fan" },
  { start: 27, end: 30, text: "trust vladFM. I do." },
]

function onPlayerReady() {
  pollInterval = setInterval(() => {
    if (!player.value || typeof player.value.getCurrentTime !== 'function') return
    const t = player.value.getCurrentTime()
    const sub = subtitles.find(s => t >= s.start && t < s.end)
    currentSub.value = sub ? sub.text : ''
  }, 200)
}

onMounted(() => {
  const tag = document.createElement('script')
  tag.src = 'https://www.youtube.com/iframe_api'
  document.head.appendChild(tag)

  window.onYouTubeIframeAPIReady = () => {
    player.value = new window.YT.Player('yt-player', {
      videoId: 'FDWuprTCZfM',
      playerVars: {
        start: 0,
        end: 30,
        controls: 1,
        modestbranding: 1,
        rel: 0,
      },
      events: {
        onReady: onPlayerReady,
      },
    })
  }

  // if API already loaded (navigated back)
  if (window.YT && window.YT.Player) {
    window.onYouTubeIframeAPIReady()
  }
})

onBeforeUnmount(() => {
  if (pollInterval) clearInterval(pollInterval)
  if (player.value && player.value.destroy) player.value.destroy()
})
</script>

<template>
  <div class="about">
    <router-link to="/" class="back-btn">← back</router-link>

    <div class="about-header">
      <h1 class="title">about vladFM</h1>
      <p class="subtitle">the world's most trusted source for football news that never happened</p>
    </div>

    <div class="testimonial">
      <h2 class="section-title">what the pros say</h2>
      <div class="video-wrapper">
        <div class="video-container">
          <div id="yt-player"></div>
          <div class="subtitle-overlay" v-if="currentSub">
            <span class="subtitle-text">{{ currentSub }}</span>
          </div>
        </div>
      </div>
      <p class="video-caption">exclusive testimonial — translated from Korean</p>
    </div>

    <div class="features">
      <h2 class="section-title">why vladFM?</h2>
      <div class="feature-grid">
        <div class="feature">
          <span class="feature-icon">✓</span>
          <div>
            <div class="feature-title">100% accurate*</div>
            <div class="feature-desc">*accuracy not measured by any known metric</div>
          </div>
        </div>
        <div class="feature">
          <span class="feature-icon">✓</span>
          <div>
            <div class="feature-title">trusted by regulars</div>
            <div class="feature-desc">shiki has never doubted a single story — <router-link to="/regulars" class="inline-link">meet them</router-link></div>
          </div>
        </div>
        <div class="feature">
          <span class="feature-icon">✓</span>
          <div>
            <div class="feature-title">breaking news</div>
            <div class="feature-desc">we break it before it happens (because it doesn't)</div>
          </div>
        </div>
        <div class="feature">
          <span class="feature-icon">✓</span>
          <div>
            <div class="feature-title">truth-scored</div>
            <div class="feature-desc">the regulars vote on every story. the truth meter reflects their verdict</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.about {
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

.about-header {
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

.testimonial {
  margin-bottom: 2rem;
}

.section-title {
  font-family: var(--font-mono);
  font-size: 0.85rem;
  font-weight: 600;
  color: var(--text-muted);
  text-transform: lowercase;
  margin-bottom: 0.75rem;
}

.video-wrapper {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 8px;
  overflow: hidden;
}

.video-container {
  position: relative;
  width: 100%;
  aspect-ratio: 16 / 9;
}

.video-container :deep(iframe) {
  width: 100%;
  height: 100%;
  display: block;
}

.subtitle-overlay {
  position: absolute;
  bottom: 12%;
  left: 50%;
  transform: translateX(-50%);
  pointer-events: none;
  z-index: 10;
  max-width: 90%;
  text-align: center;
}

.subtitle-text {
  background: rgba(0, 0, 0, 0.8);
  color: #fff;
  font-size: 0.85rem;
  font-weight: 600;
  padding: 0.3rem 0.7rem;
  border-radius: 4px;
  line-height: 1.4;
  display: inline-block;
}

.video-caption {
  font-family: var(--font-mono);
  font-size: 0.7rem;
  color: var(--text-muted);
  text-align: center;
  padding: 0.5rem;
  opacity: 0.7;
  font-style: italic;
}

.features {
  margin-bottom: 2rem;
}

.feature-grid {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.feature {
  display: flex;
  align-items: flex-start;
  gap: 0.6rem;
  padding: 0.75rem;
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 6px;
}

.feature-icon {
  color: var(--green);
  font-weight: 700;
  font-size: 0.85rem;
  margin-top: 0.1rem;
}

.feature-title {
  font-family: var(--font-mono);
  font-size: 0.85rem;
  font-weight: 600;
  margin-bottom: 0.15rem;
}

.feature-desc {
  font-size: 0.75rem;
  color: var(--text-muted);
}

.inline-link {
  color: var(--accent);
  text-decoration: none;
}

.inline-link:hover {
  text-decoration: underline;
}
</style>
