import { ref } from 'vue'
import { defineStore } from 'pinia'
import api from '../api.js'

export const usePostsStore = defineStore('posts', () => {
  const posts = ref([])
  const currentPost = ref(null)
  const sort = ref('new')
  const activeTag = ref(null)
  const loading = ref(false)
  const page = ref(1)
  const totalPages = ref(1)

  async function fetchPosts() {
    loading.value = true
    try {
      const data = await api.getPosts(sort.value, activeTag.value, page.value)
      posts.value = data.items
      totalPages.value = data.pages
    } finally {
      loading.value = false
    }
  }

  async function fetchPost(slug) {
    loading.value = true
    try {
      currentPost.value = await api.getPost(slug)
    } finally {
      loading.value = false
    }
  }

  function setSort(s) {
    sort.value = s
    page.value = 1
    fetchPosts()
  }

  function setTag(slug) {
    activeTag.value = slug
    page.value = 1
    fetchPosts()
  }

  function setPage(p) {
    page.value = p
    fetchPosts()
  }

  return { posts, currentPost, sort, activeTag, loading, page, totalPages, fetchPosts, fetchPost, setSort, setTag, setPage }
})
