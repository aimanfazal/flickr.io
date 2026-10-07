<template>
  <v-card variant="outlined" rounded="lg" class="title-card">
    <v-card-title class="text-body-1 font-weight-bold pb-1">{{ title.name }}</v-card-title>
    <v-card-subtitle class="pt-0">
      <v-chip size="x-small" class="mr-1" color="primary" variant="tonal">{{ title.platform }}</v-chip>
      <v-chip size="x-small" class="mr-1" variant="tonal">{{ title.type }}</v-chip>
      <v-chip size="x-small" class="mr-1" variant="tonal">{{ title.release_year }}</v-chip>
      <v-chip v-if="title.rating" size="x-small" variant="tonal">{{ title.rating }}</v-chip>
    </v-card-subtitle>
    <v-card-text class="pt-2">
      <v-chip
        v-for="genre in title.genres"
        :key="genre"
        size="x-small"
        class="mr-1 mb-1"
        color="secondary"
        variant="tonal"
      >{{ genre }}</v-chip>
    </v-card-text>
  </v-card>
</template>

<script setup>
defineProps({
  title: { type: Object, required: true },
})
</script>

<style scoped>
.title-card { transition: box-shadow 0.2s; }
.title-card:hover { box-shadow: 0 2px 12px rgba(0,0,0,0.12); }
</style>
