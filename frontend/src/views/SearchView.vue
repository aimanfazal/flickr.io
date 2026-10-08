<template>
  <div class="na-view">
    <div class="na-page-header">
      <div>
        <h1 class="na-page-title">Search Titles</h1>
        <p class="na-page-sub">Find any movie or show by name</p>
      </div>
    </div>

    <div class="na-search-row mb-6">
      <div class="na-search-main">
        <v-text-field
          v-model="query"
          label="Search by title…"
          prepend-inner-icon="mdi-magnify"
          clearable
          density="comfortable"
          variant="outlined"
          hide-details
          class="na-select"
          @click:clear="results = []"
        />
      </div>
      <div class="na-filter-item">
        <v-select
          v-model="platform"
          :items="platformOptions"
          label="Platform"
          clearable
          density="comfortable"
          variant="outlined"
          hide-details
          class="na-select"
        />
      </div>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="na-state">
      <v-progress-circular indeterminate color="primary" size="36" />
      <span class="na-state__text">Searching…</span>
    </div>

    <!-- Empty -->
    <div v-else-if="query && !results.length" class="na-state">
      <div class="na-state__icon">🎬</div>
      <span class="na-state__text">No titles found for "<strong>{{ query }}</strong>"</span>
    </div>

    <!-- Results -->
    <v-row v-else dense>
      <v-col v-for="title in results" :key="title.id" cols="12" sm="6" md="4" lg="3">
        <TitleCard :title="title" />
      </v-col>
    </v-row>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import TitleCard from '../components/TitleCard.vue'
import { searchTitles } from '../api/index.js'

const query    = ref('')
const platform = ref(null)
const results  = ref([])
const loading  = ref(false)
const platformOptions = ['Netflix', 'Prime', 'Disney+']
let debounceTimer = null

async function search() {
  if (!query.value || query.value.trim().length < 1) { results.value = []; return }
  loading.value = true
  const params = {}
  if (platform.value) params.platform = platform.value
  try {
    const res = await searchTitles(query.value.trim(), params)
    results.value = Array.isArray(res.data) ? res.data : [res.data]
  } catch { results.value = [] }
  finally { loading.value = false }
}

watch([query, platform], () => { clearTimeout(debounceTimer); debounceTimer = setTimeout(search, 350) })
</script>

<style scoped>
.na-view { padding: 28px 24px; }
.na-page-header { margin-bottom: 24px; }
.na-page-title { font-size: 1.6rem; font-weight: 800; letter-spacing: -0.03em; color: #EDE9FE; margin: 0 0 4px; }
.na-page-sub   { font-size: 0.82rem; color: #6B6A8A; margin: 0; }

.na-search-row { display: flex; gap: 14px; flex-wrap: wrap; align-items: center; }
.na-search-main { flex: 1; min-width: 240px; }
.na-filter-item { min-width: 180px; }
.na-select :deep(.v-field) { background: rgba(37,35,64,0.7) !important; border-radius: 12px !important; }

.na-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 64px 0;
  gap: 14px;
}
.na-state__icon { font-size: 2.5rem; }
.na-state__text {
  font-size: 0.88rem;
  color: #6B6A8A;
}
.na-state__text strong { color: #A855F7; }
</style>
