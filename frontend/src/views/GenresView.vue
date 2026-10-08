<template>
  <div class="na-view">
    <div class="na-page-header">
      <div>
        <h1 class="na-page-title">Genre Breakdown</h1>
        <p class="na-page-sub">Distribution of titles across genres</p>
      </div>
    </div>

    <div class="na-filters mb-6">
      <div class="na-filter-item">
        <v-select v-model="platform" :items="platformOptions" label="Platform" clearable density="compact" variant="outlined" hide-details class="na-select" />
      </div>
      <div class="na-filter-item">
        <v-text-field v-model="yearFilter" label="Release Year" type="number" clearable density="compact" variant="outlined" hide-details class="na-select" />
      </div>
    </div>

    <v-row>
      <v-col cols="12" md="5">
        <div class="na-panel">
          <div class="na-panel__header">
            <span class="na-panel__title">Genre Share — Top 8</span>
            <div class="na-panel__dot na-panel__dot--pink" />
          </div>
          <div style="height:300px">
            <PieChart v-if="pieData" :chartData="pieData" />
            <div v-else class="na-loader"><v-progress-circular indeterminate color="primary" size="28" /></div>
          </div>
        </div>
      </v-col>
      <v-col cols="12" md="7">
        <div class="na-panel">
          <div class="na-panel__header">
            <span class="na-panel__title">Top Genres by Count</span>
            <div class="na-panel__dot na-panel__dot--purple" />
          </div>
          <div style="height:300px">
            <BarChart v-if="barData" :chartData="barData" />
            <div v-else class="na-loader"><v-progress-circular indeterminate color="primary" size="28" /></div>
          </div>
        </div>
      </v-col>
    </v-row>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import PieChart from '../components/PieChart.vue'
import BarChart from '../components/BarChart.vue'
import { getGenres } from '../api/index.js'

const platform   = ref(null)
const yearFilter = ref(null)
const genres     = ref([])
const platformOptions = ['Netflix', 'Prime', 'Disney+']
const NEON = ['#A855F7','#EC4899','#84CC16','#38BDF8','#F59E0B','#F43F5E','#34D399','#FB923C']

async function load() {
  const params = {}
  if (platform.value)   params.platform     = platform.value
  if (yearFilter.value) params.release_year = yearFilter.value
  const res = await getGenres(params)
  genres.value = res.data
}
onMounted(load)
watch([platform, yearFilter], load)

const pieData = computed(() => {
  const top = genres.value.slice(0, 8)
  if (!top.length) return null
  return { labels: top.map(g => g.genre), datasets: [{ data: top.map(g => g.count), backgroundColor: NEON, borderWidth: 0 }] }
})
const barData = computed(() => {
  const top = genres.value.slice(0, 12)
  if (!top.length) return null
  return { labels: top.map(g => g.genre), datasets: [{ label: 'Titles', data: top.map(g => g.count), backgroundColor: '#A855F7', borderRadius: 6 }] }
})
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
.na-panel__dot--purple { background: #A855F7; box-shadow: 0 0 6px #A855F7; }
.na-panel__dot--pink   { background: #EC4899; box-shadow: 0 0 6px #EC4899; }
.na-loader { height: 100%; display: flex; align-items: center; justify-content: center; }
</style>
