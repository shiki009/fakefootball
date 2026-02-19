export function useTimeAgo(dateStr) {
  const date = new Date(dateStr)
  const now = new Date()
  const seconds = Math.floor((now - date) / 1000)

  const intervals = [
    { label: 'y', seconds: 31536000 },
    { label: 'mo', seconds: 2592000 },
    { label: 'd', seconds: 86400 },
    { label: 'h', seconds: 3600 },
    { label: 'm', seconds: 60 },
  ]

  for (const i of intervals) {
    const count = Math.floor(seconds / i.seconds)
    if (count >= 1) return `${count}${i.label} ago`
  }
  return 'just now'
}
