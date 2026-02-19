import { ref } from 'vue'

const fp = ref(null)

function generate() {
  const nav = navigator
  const raw = [
    nav.userAgent,
    nav.language,
    screen.width,
    screen.height,
    screen.colorDepth,
    new Date().getTimezoneOffset(),
  ].join('|')

  // simple hash
  let hash = 0
  for (let i = 0; i < raw.length; i++) {
    const char = raw.charCodeAt(i)
    hash = ((hash << 5) - hash) + char
    hash |= 0
  }
  return Math.abs(hash).toString(36)
}

export function useFingerprint() {
  if (!fp.value) {
    fp.value = generate()
  }
  return fp
}
