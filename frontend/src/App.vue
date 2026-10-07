<template>
  <v-app>
    <!-- Sidebar navigation -->
    <v-navigation-drawer v-model="drawer" :rail="rail" permanent>
      <v-list-item
        prepend-icon="mdi-play-circle-outline"
        title="OTT Analytics"
        nav
      >
        <template #append>
          <v-btn
            :icon="rail ? 'mdi-chevron-right' : 'mdi-chevron-left'"
            variant="text"
            @click="rail = !rail"
          />
        </template>
      </v-list-item>

      <v-divider />

      <v-list density="compact" nav>
        <v-list-item
          v-for="item in navItems"
          :key="item.to"
          :prepend-icon="item.icon"
          :title="item.title"
          :to="item.to"
          active-color="primary"
          rounded="lg"
        />
      </v-list>
    </v-navigation-drawer>

    <!-- Top app bar -->
    <v-app-bar elevation="1" color="surface">
      <v-app-bar-title>
        <span class="font-weight-bold">OTT Analytics</span>
        <span class="text-medium-emphasis text-body-2 ml-2">MVP</span>
      </v-app-bar-title>
    </v-app-bar>

    <!-- Main content -->
    <v-main>
      <RouterView />
    </v-main>
  </v-app>
</template>

<script setup>
import { ref } from 'vue'

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
</script>
