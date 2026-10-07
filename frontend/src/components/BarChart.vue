<template>
  <Bar :data="chartData" :options="mergedOptions" />
</template>

<script setup>
import { computed } from 'vue'
import { Bar } from 'vue-chartjs'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js'

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend)

const props = defineProps({
  chartData: { type: Object, required: true },
  options:   { type: Object, default: () => ({}) },
})

const defaultOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: { legend: { display: false } },
}

const mergedOptions = computed(() => ({
  ...defaultOptions,
  ...props.options,
  plugins: { ...defaultOptions.plugins, ...(props.options.plugins ?? {}) },
}))
</script>
