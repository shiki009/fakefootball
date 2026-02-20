import { ref } from 'vue'

const FP_KEY = 'vladfm_fp'
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
    try {
      fp.value = localStorage.getItem(FP_KEY) || generate()
      localStorage.setItem(FP_KEY, fp.value)
    } catch {
      fp.value = generate()
    }
  }
  return fp
}
