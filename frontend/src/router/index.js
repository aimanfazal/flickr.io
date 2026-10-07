import { createRouter, createWebHistory } from 'vue-router'

import HomeView from '../views/HomeView.vue'
import RatingsView from '../views/RatingsView.vue'
import GenresView from '../views/GenresView.vue'
import ReleasesView from '../views/ReleasesView.vue'
import TrendsView from '../views/TrendsView.vue'
import SearchView from '../views/SearchView.vue'

const routes = [
  { path: '/',         name: 'Home',     component: HomeView     },
  { path: '/ratings',  name: 'Ratings',  component: RatingsView  },
  { path: '/genres',   name: 'Genres',   component: GenresView   },
  { path: '/releases', name: 'Releases', component: ReleasesView },
  { path: '/trends',   name: 'Trends',   component: TrendsView   },
  { path: '/search',   name: 'Search',   component: SearchView   },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
