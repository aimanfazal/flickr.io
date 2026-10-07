<template>
  <v-container fluid class="pa-6">
    <div class="text-h5 font-weight-bold mb-2">📅 Release Timeline</div>
    <div class="text-body-2 text-medium-emphasis mb-6">
      Number of titles released per year
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
      <div style="height:380px">
        <LineChart v-if="chartData" :chartData="chartData" :options="chartOptions" />
        <div v-else class="d-flex align-center justify-center" style="height:100%">
          <v-progress-circular indeterminate color="primary" />
        </div>
      </div>
    </v-card>
  </v-container>
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
      borderColor: '#8b5cf6',
      backgroundColor: 'rgba(139,92,246,0.15)',
      fill: true,
      tension: 0.4,
      pointRadius: 5,
    }],
  }
})

const chartOptions = {
  plugins: { legend: { display: true } },
  scales:  { y: { beginAtZero: true, ticks: { stepSize: 1 } } },
}
</script>
