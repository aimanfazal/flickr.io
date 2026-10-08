<template>
  <div class="na-view">
    <div class="na-page-header">
      <div>
        <h1 class="na-page-title">Trending Titles</h1>
        <p class="na-page-sub">Most recent releases across platforms</p>
      </div>
    </div>

    <div class="na-filters mb-5">
      <div class="na-filter-item">
        <v-select v-model="platform" :items="platformOptions" label="Platform" clearable density="compact" variant="outlined" hide-details class="na-select" />
      </div>
      <div class="na-filter-item">
        <v-text-field v-model="genreFilter" label="Genre (exact)" clearable density="compact" variant="outlined" hide-details placeholder="e.g. Dramas" class="na-select" />
      </div>
    </div>

    <div class="na-panel">
      <v-data-table
        :headers="headers"
        :items="trends"
        :loading="loading"
        :items-per-page="20"
        density="comfortable"
        class="na-table"
      >
        <template #item.genres="{ item }">
          <span v-for="g in item.genres" :key="g" class="na-chip na-chip--pink">{{ g }}</span>
        </template>
        <template #item.runtime_min="{ item }">
          {{ item.runtime_min ? item.runtime_min + ' min' : '—' }}
        </template>
        <template #item.platform="{ item }">
          <span class="na-chip na-chip--purple">{{ item.platform }}</span>
        </template>
      </v-data-table>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue'
import { getTrends } from '../api/index.js'

const platform    = ref(null)
const genreFilter = ref(null)
const trends      = ref([])
const loading     = ref(false)
const platformOptions = ['Netflix', 'Prime', 'Disney+']
const headers = [
  { title: 'Title',    key: 'name'         },
  { title: 'Type',     key: 'type'         },
  { title: 'Year',     key: 'release_year' },
  { title: 'Rating',   key: 'rating'       },
  { title: 'Runtime',  key: 'runtime_min'  },
  { title: 'Platform', key: 'platform'     },
  { title: 'Genres',   key: 'genres'       },
]

async function load() {
  loading.value = true
  const params = { limit: 20 }
  if (platform.value)    params.platform = platform.value
  if (genreFilter.value) params.genre    = genreFilter.value
  const res = await getTrends(params)
  trends.value  = res.data
  loading.value = false
}
onMounted(load)
watch([platform, genreFilter], load)
</script>

<style scoped>
.na-view { padding: 28px 24px; }
.na-page-header { margin-bottom: 24px; }
.na-page-title { font-size: 1.6rem; font-weight: 800; letter-spacing: -0.03em; color: #EDE9FE; margin: 0 0 4px; }
.na-page-sub   { font-size: 0.82rem; color: #6B6A8A; margin: 0; }
.na-filters    { display: flex; gap: 14px; flex-wrap: wrap; }
.na-filter-item { min-width: 180px; }
.na-select :deep(.v-field) { background: rgba(37,35,64,0.7) !important; border-radius: 12px !important; }
.na-panel { background: #1C1A2E; border-radius: 20px; border: 1px solid rgba(168,85,247,0.14); overflow: hidden; }
.na-table :deep(.v-data-table__th) { color: #6B6A8A !important; font-size: 0.75rem !important; font-weight: 700 !important; letter-spacing: 0.04em !important; }
.na-table :deep(.v-data-table__td) { color: #EDE9FE !important; font-size: 0.83rem !important; }
.na-table :deep(tbody tr:hover td) { background: rgba(168,85,247,0.05) !important; }
.na-chip {
  display: inline-block;
  font-size: 0.65rem;
  font-weight: 600;
  padding: 3px 8px;
  border-radius: 99px;
  margin: 1px 3px 1px 0;
  background: rgba(107,106,138,0.2);
  color: #6B6A8A;
}
.na-chip--purple { background: rgba(168,85,247,0.18); color: #C084FC; }
.na-chip--pink   { background: rgba(236,72,153,0.15); color: #F472B6; }
</style>
