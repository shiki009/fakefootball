const REGULARS = new Set([
  'maroco', 'The real CR7', 'Kolodin', 'kris', 'leo',
  'sass the spurs fan', 'viljandi tann', 'talis chelsea fan', 'shiki',
])

export function authorLink(name) {
  if (REGULARS.has(name)) {
    return `/regulars/${encodeURIComponent(name)}`
  }
  return `/user/${encodeURIComponent(name)}`
}
