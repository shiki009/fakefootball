import { ref } from 'vue'
import { defineStore } from 'pinia'
import api from '../api.js'

export const useStatsStore = defineStore('stats', () => {
  const stats = ref(null)

  async function fetchStats() {
    stats.value = await api.getStats()
  }

  return { stats, fetchStats }
})
