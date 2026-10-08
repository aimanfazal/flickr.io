<template>
  <v-app class="na-app">
    <!-- ── Sidebar ── -->
    <v-navigation-drawer
      v-if="isAuthenticated"
      v-model="drawer"
      :rail="rail"
      permanent
      class="na-drawer"
    >
      <!-- Brand -->
      <div class="na-brand" :class="{ 'na-brand--rail': rail }">
        <div class="na-brand__icon">
          <v-icon icon="mdi-television-play" size="20" />
        </div>
        <span v-if="!rail" class="na-brand__name">OTT<span class="na-brand__accent">analytics</span></span>
        <v-btn
          v-if="!rail"
          :icon="'mdi-chevron-left'"
          variant="text"
          size="x-small"
          color="primary"
          class="ml-auto"
          @click="rail = true"
        />
        <v-btn
          v-else
          icon="mdi-chevron-right"
          variant="text"
          size="x-small"
          color="primary"
          @click="rail = false"
        />
      </div>

      <v-divider class="na-divider" />

      <v-list density="compact" nav class="na-nav pt-2">
        <v-list-item
          v-for="item in navItems"
          :key="item.to"
          :prepend-icon="item.icon"
          :title="item.title"
          :to="item.to"
          rounded="xl"
          class="na-nav__item mb-1"
        />
      </v-list>

      <template #append>
        <div v-if="!rail" class="na-drawer__footer">
          <v-icon icon="mdi-gamepad-variant-outline" size="14" class="mr-1" />
          Neon Arcade v1.0
        </div>
      </template>
    </v-navigation-drawer>

    <!-- ── App Bar ── -->
    <v-app-bar elevation="0" class="na-bar">
      <v-app-bar-title class="na-bar__title">
        <span class="na-bar__text">OTT Analytics</span>
      </v-app-bar-title>
      <template v-if="isAuthenticated" #append>
        <v-avatar size="30" class="na-avatar mr-2">
          <v-icon icon="mdi-account" size="18" />
        </v-avatar>
        <v-btn
          icon="mdi-logout-variant"
          variant="text"
          color="secondary"
          size="small"
          title="Sign out"
          @click="handleLogout"
        />
      </template>
    </v-app-bar>

    <!-- ── Main ── -->
    <v-main class="na-main">
      <RouterView />
    </v-main>
  </v-app>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { isAuthenticated, logout } from './composables/useAuth.js'

const router = useRouter()
const drawer = ref(true)
const rail   = ref(false)

const navItems = [
  { to: '/',         title: 'Overview',  icon: 'mdi-view-dashboard-outline' },
  { to: '/ratings',  title: 'Ratings',   icon: 'mdi-star-outline'           },
  { to: '/genres',   title: 'Genres',    icon: 'mdi-tag-multiple-outline'   },
  { to: '/releases', title: 'Releases',  icon: 'mdi-calendar-month-outline' },
  { to: '/trends',   title: 'Trends',    icon: 'mdi-trending-up'            },
  { to: '/search',   title: 'Search',    icon: 'mdi-magnify'                },
]

function handleLogout() {
  logout()
  router.push('/login')
}
</script>

<style>
/* ── Global base ── */
:root {
  --na-bg:        #12111A;
  --na-surface:   #1C1A2E;
  --na-surface2:  #252340;
  --na-purple:    #A855F7;
  --na-pink:      #EC4899;
  --na-lime:      #84CC16;
  --na-sky:       #38BDF8;
  --na-text:      #EDE9FE;
  --na-muted:     #6B6A8A;
  --na-grad:      linear-gradient(135deg, #A855F7, #EC4899);
  --na-grad-lime: linear-gradient(135deg, #84CC16, #38BDF8);
  --na-radius:    16px;
}

html, body, #app {
  background: var(--na-bg) !important;
}

* {
  scrollbar-width: thin;
  scrollbar-color: var(--na-purple) var(--na-surface);
}
::-webkit-scrollbar       { width: 5px; }
::-webkit-scrollbar-track { background: var(--na-surface); }
::-webkit-scrollbar-thumb { background: var(--na-purple); border-radius: 99px; }
</style>

<style scoped>
.na-app { font-family: 'Inter', system-ui, sans-serif; }

/* ── Drawer ── */
.na-drawer {
  background: var(--na-surface) !important;
  border-right: 1px solid rgba(168, 85, 247, 0.15) !important;
}

.na-brand {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 20px 16px 16px;
}
.na-brand--rail {
  justify-content: center;
  padding: 20px 8px 16px;
}

.na-brand__icon {
  width: 34px;
  height: 34px;
  border-radius: 10px;
  background: var(--na-grad);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  box-shadow: 0 4px 14px rgba(168, 85, 247, 0.45);
}

.na-brand__name {
  font-size: 1rem;
  font-weight: 800;
  letter-spacing: -0.02em;
  color: var(--na-text);
}
.na-brand__accent {
  background: var(--na-grad);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  font-weight: 900;
}

.na-divider { border-color: rgba(168, 85, 247, 0.12) !important; }

.na-nav :deep(.v-list-item) {
  color: var(--na-muted) !important;
  font-size: 0.85rem !important;
  font-weight: 500;
  transition: all 0.18s;
}
.na-nav :deep(.v-list-item--active) {
  background: linear-gradient(90deg, rgba(168,85,247,0.2), rgba(236,72,153,0.1)) !important;
  color: var(--na-text) !important;
}
.na-nav :deep(.v-list-item--active .v-icon) {
  background: var(--na-grad);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}
.na-nav :deep(.v-list-item:hover:not(.v-list-item--active)) {
  background: rgba(168, 85, 247, 0.07) !important;
  color: var(--na-text) !important;
}

.na-drawer__footer {
  font-size: 0.68rem;
  color: var(--na-muted);
  padding: 12px 16px;
  border-top: 1px solid rgba(168, 85, 247, 0.1);
  display: flex;
  align-items: center;
}

/* ── App Bar ── */
.na-bar {
  background: rgba(18, 17, 26, 0.85) !important;
  border-bottom: 1px solid rgba(168, 85, 247, 0.12) !important;
  backdrop-filter: blur(12px);
}
.na-bar__title { padding-left: 4px; }
.na-bar__text {
  font-size: 1rem;
  font-weight: 800;
  letter-spacing: -0.02em;
  background: var(--na-grad);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.na-avatar {
  background: var(--na-grad);
  box-shadow: 0 0 12px rgba(168, 85, 247, 0.4);
}

/* ── Main ── */
.na-main { background: var(--na-bg) !important; }
</style>
