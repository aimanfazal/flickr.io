<template>
  <Bar :data="chartData" :options="mergedOptions" />
</template>

<script setup>
import { computed } from 'vue'
import { Bar } from 'vue-chartjs'
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend } from 'chart.js'

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend)

const props = defineProps({
  chartData: { type: Object, required: true },
  options:   { type: Object, default: () => ({}) },
})

const defaultOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: { display: false },
    tooltip: {
      backgroundColor: '#1C1A2E',
      borderColor: 'rgba(168,85,247,0.4)',
      borderWidth: 1,
      titleColor: '#EDE9FE',
      bodyColor: '#6B6A8A',
      padding: 10,
      cornerRadius: 10,
    },
  },
  scales: {
    x: {
      ticks: { color: '#6B6A8A', font: { size: 11 } },
      grid:  { color: 'rgba(168,85,247,0.06)', drawBorder: false },
    },
    y: {
      beginAtZero: true,
      ticks: { color: '#6B6A8A', font: { size: 11 } },
      grid:  { color: 'rgba(168,85,247,0.08)', drawBorder: false },
    },
  },
}

const mergedOptions = computed(() => ({
  ...defaultOptions,
  ...props.options,
  plugins: { ...defaultOptions.plugins, ...(props.options.plugins ?? {}) },
  scales:  { ...defaultOptions.scales,  ...(props.options.scales  ?? {}) },
}))
</script>
