<template>
  <div class="na-view">
    <div class="na-page-header">
      <div>
        <h1 class="na-page-title">Content Ratings</h1>
        <p class="na-page-sub">Count of titles by content/age rating</p>
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

    <div class="na-panel mb-4">
      <div class="na-panel__header">
        <span class="na-panel__title">Rating Distribution</span>
        <div class="na-panel__dot na-panel__dot--purple" />
      </div>
      <div style="height:340px">
        <BarChart v-if="chartData" :chartData="chartData" :options="chartOptions" />
        <div v-else class="na-loader"><v-progress-circular indeterminate color="primary" size="28" /></div>
      </div>
    </div>

    <div class="na-panel">
      <div class="na-panel__header">
        <span class="na-panel__title">Raw Data</span>
      </div>
      <v-data-table :headers="headers" :items="ratings" :items-per-page="15" density="compact" class="na-table" />
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import BarChart from '../components/BarChart.vue'
import { getRatings } from '../api/index.js'

const platform = ref(null)
const type     = ref(null)
const ratings  = ref([])
const platformOptions = ['Netflix', 'Prime', 'Disney+']
const typeOptions     = ['Movie', 'TV Show']
const headers = [
  { title: 'Rating', key: 'rating' },
  { title: 'Count',  key: 'count'  },
]
const NEON = ['#A855F7','#EC4899','#84CC16','#38BDF8','#F59E0B','#F43F5E','#34D399','#FB923C','#A855F7','#EC4899']

async function load() {
  const params = {}
  if (platform.value) params.platform = platform.value
  if (type.value)     params.type     = type.value
  const res = await getRatings(params)
  ratings.value = res.data
}
onMounted(load)
watch([platform, type], load)

const chartData = computed(() => {
  if (!ratings.value.length) return null
  return {
    labels: ratings.value.map(r => r.rating),
    datasets: [{ label: 'Titles', data: ratings.value.map(r => r.count), backgroundColor: ratings.value.map((_, i) => NEON[i % NEON.length]), borderRadius: 6 }],
  }
})
const chartOptions = { plugins: { legend: { display: false } }, scales: { y: { beginAtZero: true } } }
</script>

<style scoped>
.na-view { padding: 28px 24px; }
.na-page-header { margin-bottom: 24px; }
.na-page-title { font-size: 1.6rem; font-weight: 800; letter-spacing: -0.03em; color: #EDE9FE; margin: 0 0 4px; }
.na-page-sub   { font-size: 0.82rem; color: #6B6A8A; margin: 0; }
.na-filters    { display: flex; gap: 14px; flex-wrap: wrap; }
.na-filter-item { min-width: 180px; }
.na-select :deep(.v-field) { background: rgba(37,35,64,0.7) !important; border-radius: 12px !important; }
.na-panel {
  background: #1C1A2E;
  border-radius: 20px;
  border: 1px solid rgba(168,85,247,0.14);
  padding: 20px;
}
.na-panel__header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 16px; }
.na-panel__title  { font-size: 0.88rem; font-weight: 600; color: #EDE9FE; }
.na-panel__dot    { width: 8px; height: 8px; border-radius: 50%; }
.na-panel__dot--purple { background: #A855F7; box-shadow: 0 0 6px #A855F7; }
.na-loader { height: 100%; display: flex; align-items: center; justify-content: center; }
.na-table :deep(.v-data-table__th) { color: #6B6A8A !important; font-size: 0.78rem !important; font-weight: 600 !important; }
.na-table :deep(.v-data-table__td) { color: #EDE9FE !important; font-size: 0.82rem !important; }
.na-table :deep(tbody tr:hover td) { background: rgba(168,85,247,0.05) !important; }
</style>
