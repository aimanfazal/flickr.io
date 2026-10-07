<template>
  <v-container fluid class="pa-6">
    <div class="text-h5 font-weight-bold mb-2">📈 Trending Titles</div>
    <div class="text-body-2 text-medium-emphasis mb-6">
      Most recent releases across platforms
    </div>

    <!-- Filters -->
    <v-row class="mb-4" dense>
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
          v-model="genreFilter"
          label="Genre (exact)"
          clearable
          density="compact"
          variant="outlined"
          placeholder="e.g. Dramas"
        />
      </v-col>
    </v-row>

    <v-card rounded="lg">
      <v-data-table
        :headers="headers"
        :items="trends"
        :loading="loading"
        :items-per-page="20"
        density="comfortable"
      >
        <template #item.genres="{ item }">
          <v-chip
            v-for="g in item.genres"
            :key="g"
            size="x-small"
            class="mr-1"
            color="secondary"
            variant="tonal"
          >{{ g }}</v-chip>
        </template>
        <template #item.runtime_min="{ item }">
          {{ item.runtime_min ? item.runtime_min + ' min' : '—' }}
        </template>
      </v-data-table>
    </v-card>
  </v-container>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue'
import { getTrends } from '../api/index.js'

const platform   = ref(null)
const genreFilter = ref(null)
const trends     = ref([])
const loading    = ref(false)

const platformOptions = ['Netflix', 'Prime', 'Disney+']

const headers = [
  { title: 'Title',        key: 'name'        },
  { title: 'Type',         key: 'type'        },
  { title: 'Year',         key: 'release_year'},
  { title: 'Rating',       key: 'rating'      },
  { title: 'Runtime',      key: 'runtime_min' },
  { title: 'Platform',     key: 'platform'    },
  { title: 'Genres',       key: 'genres'      },
]

async function load() {
  loading.value = true
  const params = { limit: 20 }
  if (platform.value)    params.platform = platform.value
  if (genreFilter.value) params.genre    = genreFilter.value
  const res = await getTrends(params)
  trends.value = res.data
  loading.value = false
}

onMounted(load)
watch([platform, genreFilter], load)
</script>
