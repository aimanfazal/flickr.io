<template>
  <div class="na-title-card" @click="open = true">
    <div class="na-title-card__name">{{ title.name }}</div>
    <div class="na-title-card__meta">
      <span class="na-badge na-badge--purple">{{ title.platform }}</span>
      <span class="na-badge">{{ title.type }}</span>
      <span class="na-badge">{{ title.release_year }}</span>
      <span v-if="title.rating" class="na-badge na-badge--lime">{{ title.rating }}</span>
    </div>
    <div class="na-title-card__genres">
      <span v-for="genre in title.genres" :key="genre" class="na-badge na-badge--pink">{{ genre }}</span>
    </div>

    <!-- ── detail modal ── -->
    <Teleport to="body">
      <Transition name="na-modal">
        <div v-if="open" class="na-modal-backdrop" @click.self="open = false">
          <div class="na-modal-card" role="dialog" :aria-label="title.name">
            <div class="na-modal-card__topbar" />

            <div class="na-modal-card__body">
              <!-- header row -->
              <div class="na-modal-card__header">
                <p class="na-modal-card__title">{{ title.name }}</p>
                <button class="na-modal-card__close" @click="open = false" aria-label="Close">✕</button>
              </div>

              <!-- badges -->
              <div class="na-modal-card__badges">
                <span class="na-badge na-badge--purple">{{ title.platform }}</span>
                <span class="na-badge">{{ title.type }}</span>
                <span v-if="title.rating" class="na-badge na-badge--lime">{{ title.rating }}</span>
              </div>

              <!-- genre pills -->
              <div v-if="title.genres?.length" class="na-modal-card__badges" style="margin-top:6px">
                <span v-for="genre in title.genres" :key="genre" class="na-badge na-badge--pink">{{ genre }}</span>
              </div>

              <div class="na-modal-card__divider" />

              <!-- metadata rows -->
              <div class="na-modal-card__rows">
                <div v-if="title.release_year" class="na-modal-card__row">
                  <span class="na-modal-card__label">Year</span>
                  <span class="na-modal-card__value">{{ title.release_year }}</span>
                </div>
                <div v-if="title.runtime_min" class="na-modal-card__row">
                  <span class="na-modal-card__label">Runtime</span>
                  <span class="na-modal-card__value">{{ title.runtime_min }} min</span>
                </div>
                <div v-if="title.language" class="na-modal-card__row">
                  <span class="na-modal-card__label">Language</span>
                  <span class="na-modal-card__value">{{ title.language }}</span>
                </div>
                <div v-if="title.country" class="na-modal-card__row">
                  <span class="na-modal-card__label">Country</span>
                  <span class="na-modal-card__value">{{ title.country }}</span>
                </div>
                <div v-if="title.vote_count" class="na-modal-card__row">
                  <span class="na-modal-card__label">Votes</span>
                  <span class="na-modal-card__value">{{ title.vote_count.toLocaleString() }}</span>
                </div>
              </div>

              <!-- description -->
              <div v-if="title.description" class="na-modal-card__desc">
                {{ title.description }}
              </div>
            </div>
          </div>
        </div>
      </Transition>
    </Teleport>
  </div>
</template>

<script setup>
import { ref } from 'vue'

defineProps({ title: { type: Object, required: true } })
const open = ref(false)
</script>

<style scoped>
/* ── card ── */
.na-title-card {
  background: #1C1A2E;
  border-radius: 16px;
  border: 1px solid rgba(168, 85, 247, 0.15);
  padding: 16px;
  cursor: pointer;
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

/* ── backdrop ── */
.na-modal-backdrop {
  position: fixed;
  inset: 0;
  z-index: 9999;
  background: rgba(10, 9, 20, 0.75);
  backdrop-filter: blur(6px);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 24px;
}

/* ── modal card ── */
.na-modal-card {
  width: 100%;
  max-width: 400px;
  background: #1C1A2E;
  border-radius: 20px;
  border: 1px solid rgba(168, 85, 247, 0.3);
  box-shadow: 0 32px 80px rgba(0, 0, 0, 0.7), 0 0 0 1px rgba(168,85,247,0.1);
  overflow: hidden;
}

.na-modal-card__topbar {
  height: 3px;
  background: linear-gradient(90deg, #A855F7, #EC4899, #84CC16);
}

.na-modal-card__body { padding: 22px 24px 24px; }

.na-modal-card__header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 12px;
}

.na-modal-card__title {
  font-size: 1rem;
  font-weight: 800;
  color: #EDE9FE;
  margin: 0;
  line-height: 1.35;
  flex: 1;
}

.na-modal-card__close {
  background: rgba(107,106,138,0.2);
  border: none;
  color: #6B6A8A;
  font-size: 0.75rem;
  line-height: 1;
  width: 26px;
  height: 26px;
  border-radius: 99px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  transition: background 0.15s, color 0.15s;
}
.na-modal-card__close:hover { background: rgba(168,85,247,0.25); color: #C084FC; }

.na-modal-card__badges {
  display: flex;
  flex-wrap: wrap;
  gap: 5px;
}

.na-modal-card__divider {
  height: 1px;
  background: rgba(168,85,247,0.12);
  margin: 14px 0;
}

.na-modal-card__rows {
  display: flex;
  flex-direction: column;
  gap: 6px;
  margin-bottom: 12px;
}
.na-modal-card__row {
  display: flex;
  justify-content: space-between;
  gap: 8px;
}
.na-modal-card__label {
  font-size: 0.7rem;
  color: #6B6A8A;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.04em;
}
.na-modal-card__value {
  font-size: 0.75rem;
  color: #C4B5FD;
  font-weight: 600;
  text-align: right;
}

.na-modal-card__desc {
  font-size: 0.75rem;
  color: #7C7A9A;
  line-height: 1.6;
}

/* ── transition ── */
.na-modal-enter-active { transition: opacity 0.2s ease, transform 0.2s ease; }
.na-modal-leave-active { transition: opacity 0.15s ease, transform 0.15s ease; }
.na-modal-enter-from  { opacity: 0; transform: scale(0.95) translateY(8px); }
.na-modal-leave-to    { opacity: 0; transform: scale(0.95) translateY(8px); }

/* ── badges ── */
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
.na-badge--lime   { background: rgba(132,204,22,0.15);  color: #A3E635; }
</style>
