<template>
  <v-container fluid class="pa-6">
    <div class="text-h5 font-weight-bold mb-2">🔍 Search Titles</div>
    <div class="text-body-2 text-medium-emphasis mb-6">
      Find any movie or show by name
    </div>

    <v-row class="mb-4" dense>
      <v-col cols="12" sm="6">
        <v-text-field
          v-model="query"
          label="Search by title"
          prepend-inner-icon="mdi-magnify"
          clearable
          density="compact"
          variant="outlined"
          @click:clear="results = []"
        />
      </v-col>
      <v-col cols="12" sm="3">
        <v-select
          v-model="platform"
          :items="platformOptions"
          label="Platform"
          clearable
          density="compact"
          variant="outlined"
        />
      </v-col>
    </v-row>

    <!-- Loading -->
    <div v-if="loading" class="d-flex justify-center py-8">
      <v-progress-circular indeterminate color="primary" />
    </div>

    <!-- Empty state -->
    <div
      v-else-if="query && !results.length && !loading"
      class="text-center text-medium-emphasis py-8"
    >
      No titles found for "{{ query }}"
    </div>

    <!-- Results -->
    <v-row v-else dense>
      <v-col v-for="title in results" :key="title.id" cols="12" sm="6" md="4" lg="3">
        <TitleCard :title="title" />
      </v-col>
    </v-row>
  </v-container>
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
  if (!query.value || query.value.trim().length < 1) {
    results.value = []
    return
  }
  loading.value = true
  const params = {}
  if (platform.value) params.platform = platform.value
  try {
    const res = await searchTitles(query.value.trim(), params)
    // API returns single object when one result, array otherwise — normalise
    results.value = Array.isArray(res.data) ? res.data : [res.data]
  } catch {
    results.value = []
  } finally {
    loading.value = false
  }
}

watch([query, platform], () => {
  clearTimeout(debounceTimer)
  debounceTimer = setTimeout(search, 350)
})
</script>
