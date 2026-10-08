<template>
  <Pie :data="chartData" :options="mergedOptions" />
</template>

<script setup>
import { computed } from 'vue'
import { Pie } from 'vue-chartjs'
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js'

ChartJS.register(ArcElement, Tooltip, Legend)

const props = defineProps({
  chartData: { type: Object, required: true },
  options:   { type: Object, default: () => ({}) },
})

const defaultOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      position: 'right',
      labels: {
        color: '#6B6A8A',
        font: { size: 11 },
        boxWidth: 12,
        padding: 14,
        borderRadius: 4,
      },
    },
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
}

const mergedOptions = computed(() => ({
  ...defaultOptions,
  ...props.options,
  plugins: { ...defaultOptions.plugins, ...(props.options.plugins ?? {}) },
}))
</script>
