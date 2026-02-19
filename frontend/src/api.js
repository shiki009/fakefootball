import axios from 'axios'

const http = axios.create({ baseURL: '/api' })

export default {
  getPosts(sort = 'new', tag = null, page = 1) {
    const params = { sort, page }
    if (tag) params.tag = tag
    return http.get('/posts', { params }).then(r => r.data)
  },

  getPost(slug) {
    return http.get(`/posts/${slug}`).then(r => r.data)
  },

  getComments(postId) {
    return http.get(`/posts/${postId}/comments`).then(r => r.data)
  },

  addComment(postId, authorName, content) {
    return http.post(`/posts/${postId}/comments`, {
      author_name: authorName,
      content,
    }).then(r => r.data)
  },

  vote(postId, fingerprint, value) {
    return http.post(`/posts/${postId}/vote`, { fingerprint, value }).then(r => r.data)
  },

  getVote(postId, fingerprint) {
    return http.get(`/posts/${postId}/vote`, { params: { fingerprint } }).then(r => r.data)
  },

  getTags() {
    return http.get('/tags').then(r => r.data)
  },

  getStats() {
    return http.get('/stats').then(r => r.data)
  },

  getRegulars() {
    return http.get('/regulars').then(r => r.data)
  },

  getUserProfile(username) {
    return http.get(`/users/${encodeURIComponent(username)}`).then(r => r.data)
  },
}
