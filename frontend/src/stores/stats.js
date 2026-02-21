import { ref } from 'vue'
import { defineStore } from 'pinia'
import api from '../api.js'

export const useStatsStore = defineStore('stats', () => {
  const stats = ref(null)
  const error = ref(false)

  async function fetchStats() {
    try {
      stats.value = await api.getStats()
    } catch {
      error.value = true
    }
  }

  return { stats, error, fetchStats }
})
