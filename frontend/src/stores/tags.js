import { ref } from 'vue'
import { defineStore } from 'pinia'
import api from '../api.js'

export const useTagsStore = defineStore('tags', () => {
  const tags = ref([])

  async function fetchTags() {
    tags.value = await api.getTags()
  }

  return { tags, fetchTags }
})
