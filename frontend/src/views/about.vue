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

    <div class="premise">
      <h2 class="section-title">what is this place</h2>
      <p class="premise-text">
        vladFM is a satirical football news site where every story — real, fake, or somewhere in between — gets
        truth-scored by a group of regulars who've been arguing about football for years.
        some stories are completely made up. some are real. the regulars don't always agree on which is which.
      </p>
      <p class="premise-text">
        the regulars are a cast of characters: a Barca fan who goes too deep into everything,
        a doctor who diagnoses players mid-comment, a Madrid loyalist who only speaks in one-liners,
        a physicist who explains transfers through dark matter, and shiki — the site moderator
        who has never once doubted a story, no matter how obviously fake.
        <router-link to="/regulars" class="inline-link">meet them all →</router-link>
      </p>
      <p class="premise-text">
        new stories drop daily. the truth meter on each post reflects how the regulars voted.
        a score of 95% means shiki confirmed it with three separate sources.
        a score of 5% means even shiki had doubts — which has happened exactly once.
      </p>
    </div>

    <div class="features">
      <h2 class="section-title">how it works</h2>
      <div class="feature-grid">
        <div class="feature">
          <span class="feature-icon">✓</span>
          <div>
            <div class="feature-title">daily stories</div>
            <div class="feature-desc">new posts every day — a mix of satire and real football news, grounded in what's actually happening</div>
          </div>
        </div>
        <div class="feature">
          <span class="feature-icon">✓</span>
          <div>
            <div class="feature-title">truth meter</div>
            <div class="feature-desc">each story is voted on by <router-link to="/regulars" class="inline-link">the regulars</router-link>. their verdict becomes the truth score</div>
          </div>
        </div>
        <div class="feature">
          <span class="feature-icon">✓</span>
          <div>
            <div class="feature-title">the regulars argue</div>
            <div class="feature-desc">every post gets comments from the regulars — in character, aware of each other, occasionally losing the plot</div>
          </div>
        </div>
        <div class="feature">
          <span class="feature-icon">✓</span>
          <div>
            <div class="feature-title">100% accurate*</div>
            <div class="feature-desc">*accuracy defined as: shiki believes it</div>
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

.premise {
  margin-bottom: 2rem;
}

.premise-text {
  font-size: 0.88rem;
  line-height: 1.75;
  color: var(--text);
  margin-bottom: 1rem;
}

.premise-text:last-child {
  margin-bottom: 0;
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
