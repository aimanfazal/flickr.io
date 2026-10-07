<template>
  <v-card variant="elevated" rounded="lg" class="kpi-card">
    <v-card-text class="d-flex flex-column align-center pa-6">
      <v-icon :icon="icon" size="36" color="primary" class="mb-3" />
      <div class="text-h4 font-weight-bold">{{ value }}</div>
      <div class="text-body-2 text-medium-emphasis mt-1">{{ label }}</div>
    </v-card-text>
  </v-card>
</template>

<script setup>
defineProps({
  label: { type: String, required: true },
  value: { type: [String, Number], required: true },
  icon:  { type: String, default: 'mdi-chart-bar' },
})
</script>

<style scoped>
.kpi-card { min-width: 160px; }
</style>
