<template>
  <div class="na-kpi">
    <div class="na-kpi__icon-wrap">
      <v-icon :icon="icon" size="22" color="white" />
    </div>
    <div class="na-kpi__value">{{ value }}</div>
    <div class="na-kpi__label">{{ label }}</div>
  </div>
</template>

<script setup>
defineProps({
  label: { type: String, required: true },
  value: { type: [String, Number], required: true },
  icon:  { type: String, default: 'mdi-chart-bar' },
})
</script>

<style scoped>
.na-kpi {
  background: #1C1A2E;
  border-radius: 20px;
  border: 1px solid rgba(168, 85, 247, 0.18);
  padding: 24px 20px;
  text-align: center;
  position: relative;
  overflow: hidden;
  transition: transform 0.2s, box-shadow 0.2s, border-color 0.2s;
}
.na-kpi::before {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, rgba(168,85,247,0.05), rgba(236,72,153,0.04));
  pointer-events: none;
}
.na-kpi:hover {
  transform: translateY(-3px);
  box-shadow: 0 12px 32px rgba(168, 85, 247, 0.2);
  border-color: rgba(168, 85, 247, 0.4);
}

.na-kpi__icon-wrap {
  width: 44px;
  height: 44px;
  border-radius: 12px;
  background: linear-gradient(135deg, #A855F7, #EC4899);
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 14px;
  box-shadow: 0 4px 16px rgba(168, 85, 247, 0.4);
}

.na-kpi__value {
  font-size: 2rem;
  font-weight: 800;
  letter-spacing: -0.03em;
  color: #EDE9FE;
  line-height: 1;
}

.na-kpi__label {
  font-size: 0.72rem;
  font-weight: 500;
  color: #6B6A8A;
  margin-top: 8px;
  text-transform: uppercase;
  letter-spacing: 0.06em;
}
</style>
