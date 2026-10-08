import { createApp } from 'vue'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
import '@mdi/font/css/materialdesignicons.css'
import 'vuetify/styles'

import App from './App.vue'
import router from './router/index.js'

const neonArcade = {
  dark: true,
  colors: {
    background:        '#12111A',
    surface:           '#1C1A2E',
    'surface-variant': '#252340',
    primary:           '#A855F7',   // purple
    secondary:         '#EC4899',   // hot pink
    accent:            '#84CC16',   // lime
    error:             '#F43F5E',
    warning:           '#F59E0B',
    info:              '#38BDF8',
    success:           '#84CC16',
    'on-background':   '#EDE9FE',
    'on-surface':      '#EDE9FE',
    'on-primary':      '#FFFFFF',
    'on-secondary':    '#FFFFFF',
  },
}

const vuetify = createVuetify({
  components,
  directives,
  theme: {
    defaultTheme: 'neonArcade',
    themes: { neonArcade },
  },
  icons: { defaultSet: 'mdi' },
  defaults: {
    VCard:      { rounded: 'xl' },
    VBtn:       { rounded: 'lg' },
    VTextField: { color: 'primary', rounded: 'lg' },
    VSelect:    { color: 'primary', rounded: 'lg' },
    VChip:      { rounded: 'lg' },
  },
})

createApp(App).use(router).use(vuetify).mount('#app')
