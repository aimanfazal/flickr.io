<template>
  <v-container fluid class="pa-6">
    <div class="text-h5 font-weight-bold mb-2">⭐ Content Rating Distribution</div>
    <div class="text-body-2 text-medium-emphasis mb-6">
      Count of titles by content/age rating (PG, TV-MA, R, …)
    </div>

    <!-- Filters -->
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
        <v-select
          v-model="type"
          :items="typeOptions"
          label="Type"
          clearable
          density="compact"
          variant="outlined"
        />
      </v-col>
    </v-row>

    <v-card rounded="lg" class="pa-4">
      <div style="height:360px">
        <BarChart v-if="chartData" :chartData="chartData" :options="chartOptions" />
        <div v-else class="d-flex align-center justify-center" style="height:100%">
          <v-progress-circular indeterminate color="primary" />
        </div>
      </div>
    </v-card>

    <!-- Data table -->
    <v-card rounded="lg" class="mt-4">
      <v-data-table
        :headers="headers"
        :items="ratings"
        :items-per-page="15"
        density="compact"
      />
    </v-card>
  </v-container>
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

const COLORS = [
  '#3b82f6','#8b5cf6','#ec4899','#f97316',
  '#eab308','#22c55e','#14b8a6','#06b6d4',
  '#f43f5e','#a855f7',
]

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
    datasets: [{
      label: 'Titles',
      data: ratings.value.map(r => r.count),
      backgroundColor: ratings.value.map((_, i) => COLORS[i % COLORS.length]),
    }],
  }
})

const chartOptions = {
  plugins: { legend: { display: false } },
  scales:  { y: { beginAtZero: true, ticks: { stepSize: 1 } } },
}
</script>
