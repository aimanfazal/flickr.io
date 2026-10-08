<template>
  <div class="na-title-card">
    <div class="na-title-card__name">{{ title.name }}</div>
    <div class="na-title-card__meta">
      <span class="na-badge na-badge--purple">{{ title.platform }}</span>
      <span class="na-badge">{{ title.type }}</span>
      <span class="na-badge">{{ title.release_year }}</span>
      <span v-if="title.rating" class="na-badge na-badge--lime">{{ title.rating }}</span>
    </div>
    <div class="na-title-card__genres">
      <span
        v-for="genre in title.genres"
        :key="genre"
        class="na-badge na-badge--pink"
      >{{ genre }}</span>
    </div>
  </div>
</template>

<script setup>
defineProps({ title: { type: Object, required: true } })
</script>

<style scoped>
.na-title-card {
  background: #1C1A2E;
  border-radius: 16px;
  border: 1px solid rgba(168, 85, 247, 0.15);
  padding: 16px;
  transition: transform 0.18s, box-shadow 0.18s, border-color 0.18s;
}
.na-title-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 28px rgba(168, 85, 247, 0.18);
  border-color: rgba(168, 85, 247, 0.35);
}

.na-title-card__name {
  font-size: 0.88rem;
  font-weight: 700;
  color: #EDE9FE;
  margin-bottom: 10px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.na-title-card__meta,
.na-title-card__genres {
  display: flex;
  flex-wrap: wrap;
  gap: 5px;
  margin-bottom: 7px;
}

.na-badge {
  display: inline-block;
  font-size: 0.65rem;
  font-weight: 600;
  padding: 3px 8px;
  border-radius: 99px;
  background: rgba(107, 106, 138, 0.2);
  color: #6B6A8A;
}
.na-badge--purple { background: rgba(168,85,247,0.18); color: #C084FC; }
.na-badge--pink   { background: rgba(236,72,153,0.15); color: #F472B6; }
.na-badge--lime   { background: rgba(132,204,22,0.15); color: #A3E635; }
</style>
