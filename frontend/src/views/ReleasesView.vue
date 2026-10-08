<template>
  <div class="na-view">
    <div class="na-page-header">
      <div>
        <h1 class="na-page-title">Release Timeline</h1>
        <p class="na-page-sub">Number of titles released per year</p>
      </div>
    </div>

    <div class="na-filters mb-6">
      <div class="na-filter-item">
        <v-select v-model="platform" :items="platformOptions" label="Platform" clearable density="compact" variant="outlined" hide-details class="na-select" />
      </div>
      <div class="na-filter-item">
        <v-select v-model="type" :items="typeOptions" label="Type" clearable density="compact" variant="outlined" hide-details class="na-select" />
      </div>
    </div>

    <div class="na-panel">
      <div class="na-panel__header">
        <span class="na-panel__title">Titles Released Per Year</span>
        <div class="na-panel__dot na-panel__dot--pink" />
      </div>
      <div style="height:380px">
        <LineChart v-if="chartData" :chartData="chartData" :options="chartOptions" />
        <div v-else class="na-loader"><v-progress-circular indeterminate color="primary" size="28" /></div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import LineChart from '../components/LineChart.vue'
import { getReleases } from '../api/index.js'

const platform = ref(null)
const type     = ref(null)
const releases = ref([])
const platformOptions = ['Netflix', 'Prime', 'Disney+']
const typeOptions     = ['Movie', 'TV Show']

async function load() {
  const params = {}
  if (platform.value) params.platform = platform.value
  if (type.value)     params.type     = type.value
  const res = await getReleases(params)
  releases.value = res.data
}
onMounted(load)
watch([platform, type], load)

const chartData = computed(() => {
  if (!releases.value.length) return null
  return {
    labels: releases.value.map(r => String(r.release_year)),
    datasets: [{
      label: 'Titles Released',
      data: releases.value.map(r => r.count),
      borderColor: '#EC4899',
      backgroundColor: 'rgba(236,72,153,0.1)',
      fill: true,
      tension: 0.4,
      pointBackgroundColor: '#EC4899',
      pointRadius: 4,
      pointHoverRadius: 6,
    }],
  }
})
const chartOptions = {
  plugins: { legend: { display: true, labels: { color: '#6B6A8A', font: { size: 11 }, boxWidth: 12 } } },
  scales: { y: { beginAtZero: true } },
}
</script>

<style scoped>
.na-view { padding: 28px 24px; }
.na-page-header { margin-bottom: 24px; }
.na-page-title { font-size: 1.6rem; font-weight: 800; letter-spacing: -0.03em; color: #EDE9FE; margin: 0 0 4px; }
.na-page-sub   { font-size: 0.82rem; color: #6B6A8A; margin: 0; }
.na-filters    { display: flex; gap: 14px; flex-wrap: wrap; }
.na-filter-item { min-width: 180px; }
.na-select :deep(.v-field) { background: rgba(37,35,64,0.7) !important; border-radius: 12px !important; }
.na-panel { background: #1C1A2E; border-radius: 20px; border: 1px solid rgba(168,85,247,0.14); padding: 20px; }
.na-panel__header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 16px; }
.na-panel__title  { font-size: 0.88rem; font-weight: 600; color: #EDE9FE; }
.na-panel__dot    { width: 8px; height: 8px; border-radius: 50%; }
.na-panel__dot--pink { background: #EC4899; box-shadow: 0 0 6px #EC4899; }
.na-loader { height: 100%; display: flex; align-items: center; justify-content: center; }
</style>
