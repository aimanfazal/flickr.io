<template>
  <Pie :data="chartData" :options="mergedOptions" />
</template>

<script setup>
import { computed } from 'vue'
import { Pie } from 'vue-chartjs'
import {
  Chart as ChartJS,
  ArcElement,
  Tooltip,
  Legend,
} from 'chart.js'

ChartJS.register(ArcElement, Tooltip, Legend)

const props = defineProps({
  chartData: { type: Object, required: true },
  options:   { type: Object, default: () => ({}) },
})

const defaultOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: { legend: { position: 'right' } },
}

const mergedOptions = computed(() => ({
  ...defaultOptions,
  ...props.options,
  plugins: { ...defaultOptions.plugins, ...(props.options.plugins ?? {}) },
}))
</script>
