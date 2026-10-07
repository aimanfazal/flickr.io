<template>
  <Line :data="chartData" :options="mergedOptions" />
</template>

<script setup>
import { computed } from 'vue'
import { Line } from 'vue-chartjs'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler,
} from 'chart.js'

ChartJS.register(
  CategoryScale, LinearScale, PointElement, LineElement,
  Title, Tooltip, Legend, Filler,
)

const props = defineProps({
  chartData: { type: Object, required: true },
  options:   { type: Object, default: () => ({}) },
})

const defaultOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: { legend: { display: false } },
  scales: { y: { beginAtZero: true } },
}

const mergedOptions = computed(() => ({
  ...defaultOptions,
  ...props.options,
  plugins: { ...defaultOptions.plugins, ...(props.options.plugins ?? {}) },
  scales:  { ...defaultOptions.scales,  ...(props.options.scales  ?? {}) },
}))
</script>
