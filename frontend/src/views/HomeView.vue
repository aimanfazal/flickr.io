<template>
  <v-container fluid class="pa-6">
    <div class="text-h5 font-weight-bold mb-6">🎬 OTT Analytics — Overview</div>

    <!-- KPI Cards -->
    <v-row class="mb-8" dense>
      <v-col v-for="kpi in kpis" :key="kpi.label" cols="12" sm="6" md="3">
        <KpiCard :label="kpi.label" :value="kpi.value" :icon="kpi.icon" />
      </v-col>
    </v-row>

    <!-- Mini charts side by side -->
    <v-row>
      <v-col cols="12" md="6">
        <v-card rounded="lg" class="pa-4">
          <div class="text-subtitle-1 font-weight-medium mb-3">Releases by Year</div>
          <div style="height:220px">
            <LineChart v-if="releaseChart" :chartData="releaseChart" />
          </div>
        </v-card>
      </v-col>
      <v-col cols="12" md="6">
        <v-card rounded="lg" class="pa-4">
          <div class="text-subtitle-1 font-weight-medium mb-3">Top Genres</div>
          <div style="height:220px">
            <BarChart v-if="genreChart" :chartData="genreChart" />
          </div>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import KpiCard   from '../components/KpiCard.vue'
import LineChart from '../components/LineChart.vue'
import BarChart  from '../components/BarChart.vue'
import { getReleases, getGenres } from '../api/index.js'

const releases = ref([])
const genres   = ref([])

onMounted(async () => {
  const [relRes, genRes] = await Promise.all([getReleases(), getGenres()])
  releases.value = relRes.data
  genres.value   = genRes.data
})

const kpis = computed(() => {
  const totalTitles    = releases.value.reduce((s, r) => s + r.count, 0)
  const newestYear     = releases.value.length ? Math.max(...releases.value.map(r => r.release_year)) : '—'
  const totalGenres    = genres.value.length
  return [
    { label: 'Total Titles',    value: totalTitles, icon: 'mdi-movie-open'       },
    { label: 'Platforms',       value: 3,           icon: 'mdi-television-play'  },
    { label: 'Unique Genres',   value: totalGenres, icon: 'mdi-tag-multiple'     },
    { label: 'Newest Release',  value: newestYear,  icon: 'mdi-calendar-star'    },
  ]
})

const COLORS = [
  '#3b82f6','#8b5cf6','#ec4899','#f97316',
  '#eab308','#22c55e','#14b8a6','#06b6d4',
]

const releaseChart = computed(() => {
  if (!releases.value.length) return null
  return {
    labels: releases.value.map(r => String(r.release_year)),
    datasets: [{
      label: 'Titles',
      data: releases.value.map(r => r.count),
      borderColor: '#3b82f6',
      backgroundColor: 'rgba(59,130,246,0.15)',
      fill: true,
      tension: 0.4,
    }],
  }
})

const genreChart = computed(() => {
  const top = genres.value.slice(0, 8)
  if (!top.length) return null
  return {
    labels: top.map(g => g.genre),
    datasets: [{
      label: 'Titles',
      data: top.map(g => g.count),
      backgroundColor: COLORS,
    }],
  }
})
</script>
