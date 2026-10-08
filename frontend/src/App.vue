<template>
  <v-app class="na-app">

    <!-- ── Top Navigation Bar ── -->
    <v-app-bar elevation="0" class="na-bar" :height="56">

      <!-- Logo -->
      <div class="na-bar__logo ml-4">
        <div class="na-bar__logo-icon">
          <v-icon icon="mdi-television-play" size="18" />
        </div>
        <span class="na-bar__logo-name">OTT<span class="na-bar__logo-accent">analytics</span></span>
      </div>

      <!-- Nav links -->
      <nav v-if="isAuthenticated" class="na-bar__nav">
        <RouterLink
          v-for="item in navItems"
          :key="item.to"
          :to="item.to"
          class="na-bar__link"
          active-class="na-bar__link--active"
          exact-active-class="na-bar__link--active"
        >{{ item.title }}</RouterLink>
      </nav>

      <!-- Right: logout -->
      <template v-if="isAuthenticated" #append>
        <v-btn
          icon="mdi-logout-variant"
          variant="text"
          color="secondary"
          size="small"
          title="Sign out"
          class="mr-2"
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
import { useRouter } from 'vue-router'
import { isAuthenticated, logout } from './composables/useAuth.js'

const router = useRouter()

const navItems = [
  { to: '/',         title: 'Overview'  },
  { to: '/ratings',  title: 'Ratings'   },
  { to: '/genres',   title: 'Genres'    },
  { to: '/releases', title: 'Releases'  },
  { to: '/trends',   title: 'Trends'    },
  { to: '/search',   title: 'Search'    },
]

function handleLogout() {
  logout()
  router.push('/login')
}
</script>

<style>
/* ── Global base ── */
:root {
  --na-bg:      #12111A;
  --na-surface: #1C1A2E;
  --na-purple:  #A855F7;
  --na-pink:    #EC4899;
  --na-lime:    #84CC16;
  --na-text:    #EDE9FE;
  --na-muted:   #6B6A8A;
  --na-grad:    linear-gradient(135deg, #A855F7, #EC4899);
}

html, body, #app { background: var(--na-bg) !important; }

/* Let v-main pass its full available height to child views */
.v-main__scroller { height: 100% !important; }
.v-main__scroller > * { height: 100%; }

* { scrollbar-width: thin; scrollbar-color: var(--na-purple) var(--na-surface); }
::-webkit-scrollbar       { width: 5px; }
::-webkit-scrollbar-track { background: var(--na-surface); }
::-webkit-scrollbar-thumb { background: var(--na-purple); border-radius: 99px; }
</style>

<style scoped>
.na-app { font-family: 'Inter', system-ui, sans-serif; }

/* ── App Bar ── */
.na-bar {
  background: rgba(18, 17, 26, 0.92) !important;
  border-bottom: 1px solid rgba(168, 85, 247, 0.14) !important;
  backdrop-filter: blur(12px);
}

/* Logo */
.na-bar__logo {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-shrink: 0;
  margin-right: 32px;
}
.na-bar__logo-icon {
  width: 30px;
  height: 30px;
  border-radius: 8px;
  background: var(--na-grad);
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 3px 10px rgba(168, 85, 247, 0.4);
}
.na-bar__logo-name {
  font-size: 0.95rem;
  font-weight: 800;
  letter-spacing: -0.02em;
  color: var(--na-text);
}
.na-bar__logo-accent {
  background: var(--na-grad);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

/* Nav links */
.na-bar__nav {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 4px;
  flex: 1;
}
.na-bar__link {
  display: inline-block;
  padding: 6px 12px;
  border-radius: 8px;
  font-size: 0.83rem;
  font-weight: 500;
  color: var(--na-muted);
  text-decoration: none;
  transition: color 0.15s;
  white-space: nowrap;
}
.na-bar__link:hover {
  color: var(--na-text);
}
.na-bar__link--active {
  font-weight: 700;
  background: linear-gradient(135deg, #A855F7, #EC4899);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

/* Avatar */
.na-avatar {
  background: var(--na-grad);
  box-shadow: 0 0 10px rgba(168, 85, 247, 0.4);
}

/* ── Main ── */
.na-main { background: var(--na-bg) !important; }
</style>
