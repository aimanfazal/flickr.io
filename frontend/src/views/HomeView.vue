<template>
  <div class="na-view">
    <!-- Page header -->
    <div class="na-page-header">
      <div>
        <h1 class="na-page-title">Overview</h1>
        <p class="na-page-sub">Your content intelligence at a glance</p>
      </div>
      <div class="na-page-header__badge">
        <v-icon icon="mdi-gamepad-variant-outline" size="14" class="mr-1" />
        Live
      </div>
    </div>

    <!-- KPI Cards -->
    <v-row class="mb-8" dense>
      <v-col v-for="kpi in kpis" :key="kpi.label" cols="12" sm="6" md="3">
        <KpiCard :label="kpi.label" :value="kpi.value" :icon="kpi.icon" />
      </v-col>
    </v-row>

    <!-- Charts -->
    <v-row>
      <v-col cols="12" md="6">
        <div class="na-panel">
          <div class="na-panel__header">
            <span class="na-panel__title">Releases by Year</span>
            <div class="na-panel__dot na-panel__dot--purple" />
          </div>
          <div style="height:220px">
            <LineChart v-if="releaseChart" :chartData="releaseChart" />
            <div v-else class="na-loader"><v-progress-circular indeterminate color="primary" size="28" /></div>
          </div>
        </div>
      </v-col>
      <v-col cols="12" md="6">
        <div class="na-panel">
          <div class="na-panel__header">
            <span class="na-panel__title">Top Genres</span>
            <div class="na-panel__dot na-panel__dot--pink" />
          </div>
          <div style="height:220px">
            <BarChart v-if="genreChart" :chartData="genreChart" />
            <div v-else class="na-loader"><v-progress-circular indeterminate color="primary" size="28" /></div>
          </div>
        </div>
      </v-col>
    </v-row>
  </div>
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
  const totalTitles = releases.value.reduce((s, r) => s + r.count, 0)
  const newestYear  = releases.value.length ? Math.max(...releases.value.map(r => r.release_year)) : '—'
  const totalGenres = genres.value.length
  return [
    { label: 'Total Titles',   value: totalTitles, icon: 'mdi-movie-open'      },
    { label: 'Platforms',      value: 3,           icon: 'mdi-television-play' },
    { label: 'Unique Genres',  value: totalGenres, icon: 'mdi-tag-multiple'    },
    { label: 'Newest Release', value: newestYear,  icon: 'mdi-calendar-star'   },
  ]
})

const NEON = ['#A855F7','#EC4899','#84CC16','#38BDF8','#F59E0B','#F43F5E','#34D399','#FB923C']

const releaseChart = computed(() => {
  if (!releases.value.length) return null
  return {
    labels: releases.value.map(r => String(r.release_year)),
    datasets: [{
      label: 'Titles',
      data: releases.value.map(r => r.count),
      borderColor: '#A855F7',
      backgroundColor: 'rgba(168,85,247,0.12)',
      fill: true,
      tension: 0.4,
      pointBackgroundColor: '#A855F7',
      pointRadius: 4,
      pointHoverRadius: 6,
    }],
  }
})

const genreChart = computed(() => {
  const top = genres.value.slice(0, 8)
  if (!top.length) return null
  return {
    labels: top.map(g => g.genre),
    datasets: [{ label: 'Titles', data: top.map(g => g.count), backgroundColor: NEON, borderRadius: 6 }],
  }
})
</script>

<style scoped>
.na-view { padding: 28px 24px; }

.na-page-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  margin-bottom: 28px;
}
.na-page-title {
  font-size: 1.6rem;
  font-weight: 800;
  letter-spacing: -0.03em;
  color: #EDE9FE;
  margin: 0 0 4px;
}
.na-page-sub {
  font-size: 0.82rem;
  color: #6B6A8A;
  margin: 0;
}
.na-page-header__badge {
  display: flex;
  align-items: center;
  font-size: 0.7rem;
  font-weight: 600;
  color: #84CC16;
  background: rgba(132, 204, 22, 0.12);
  border: 1px solid rgba(132, 204, 22, 0.25);
  padding: 5px 10px;
  border-radius: 99px;
}

.na-panel {
  background: #1C1A2E;
  border-radius: 20px;
  border: 1px solid rgba(168, 85, 247, 0.14);
  padding: 20px;
}
.na-panel__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 16px;
}
.na-panel__title {
  font-size: 0.88rem;
  font-weight: 600;
  color: #EDE9FE;
}
.na-panel__dot {
  width: 8px; height: 8px;
  border-radius: 50%;
}
.na-panel__dot--purple { background: #A855F7; box-shadow: 0 0 6px #A855F7; }
.na-panel__dot--pink   { background: #EC4899; box-shadow: 0 0 6px #EC4899; }

.na-loader { height: 100%; display: flex; align-items: center; justify-content: center; }
</style>
