<template>
  <v-container fluid class="pa-6">
    <div class="text-h5 font-weight-bold mb-2">🎭 Genre Breakdown</div>
    <div class="text-body-2 text-medium-emphasis mb-6">
      Distribution of titles across genres
    </div>

    <!-- Filter -->
    <v-row class="mb-6" dense>
      <v-col cols="12" sm="4">
        <v-select
          v-model="platform"
          :items="platformOptions"
          label="Platform"
          clearable
          density="compact"
          variant="outlined"
        />
      </v-col>
      <v-col cols="12" sm="4">
        <v-text-field
          v-model="yearFilter"
          label="Release Year"
          type="number"
          clearable
          density="compact"
          variant="outlined"
        />
      </v-col>
    </v-row>

    <v-row>
      <!-- Pie chart -->
      <v-col cols="12" md="5">
        <v-card rounded="lg" class="pa-4">
          <div class="text-subtitle-1 font-weight-medium mb-3">Genre Share (top 8)</div>
          <div style="height:300px">
            <PieChart v-if="pieData" :chartData="pieData" />
            <div v-else class="d-flex align-center justify-center" style="height:100%">
              <v-progress-circular indeterminate color="primary" />
            </div>
          </div>
        </v-card>
      </v-col>

      <!-- Bar chart -->
      <v-col cols="12" md="7">
        <v-card rounded="lg" class="pa-4">
          <div class="text-subtitle-1 font-weight-medium mb-3">Top Genres by Count</div>
          <div style="height:300px">
            <BarChart v-if="barData" :chartData="barData" />
            <div v-else class="d-flex align-center justify-center" style="height:100%">
              <v-progress-circular indeterminate color="primary" />
            </div>
          </div>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import PieChart from '../components/PieChart.vue'
import BarChart from '../components/BarChart.vue'
import { getGenres } from '../api/index.js'

const platform  = ref(null)
const yearFilter = ref(null)
const genres    = ref([])

const platformOptions = ['Netflix', 'Prime', 'Disney+']

const COLORS = [
  '#3b82f6','#8b5cf6','#ec4899','#f97316',
  '#eab308','#22c55e','#14b8a6','#06b6d4',
]

async function load() {
  const params = {}
  if (platform.value)            params.platform     = platform.value
  if (yearFilter.value)          params.release_year = yearFilter.value
  const res = await getGenres(params)
  genres.value = res.data
}

onMounted(load)
watch([platform, yearFilter], load)

const pieData = computed(() => {
  const top = genres.value.slice(0, 8)
  if (!top.length) return null
  return {
    labels: top.map(g => g.genre),
    datasets: [{ data: top.map(g => g.count), backgroundColor: COLORS }],
  }
})

const barData = computed(() => {
  const top = genres.value.slice(0, 12)
  if (!top.length) return null
  return {
    labels: top.map(g => g.genre),
    datasets: [{
      label: 'Titles',
      data: top.map(g => g.count),
      backgroundColor: '#3b82f6',
    }],
  }
})
</script>
