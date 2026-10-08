<template>
  <div class="na-login">
    <!-- Blurred orbs background -->
    <div class="na-orb na-orb--purple" aria-hidden="true" />
    <div class="na-orb na-orb--pink"   aria-hidden="true" />

    <div class="na-card">
      <!-- Gradient top bar -->
      <div class="na-card__topbar" />

      <div class="na-card__body">
        <!-- Logo -->
        <div class="na-logo">
          <div class="na-logo__icon">
            <v-icon icon="mdi-filmstrip" size="28" color="white" />
          </div>
          <div>
            <div class="na-logo__name"><em>Flickr</em><span class="na-logo__accent">.io</span></div>
            <div class="na-logo__sub">Content Intelligence Dashboard</div>
          </div>
        </div>

        <div class="na-card__divider" />

        <p class="na-card__headline">Welcome Back 👾</p>
        <p class="na-card__sub">Sign in to access your dashboard</p>

        <v-form ref="formRef" @submit.prevent="handleLogin" class="mt-5">
          <v-text-field
            v-model="username"
            label="Username"
            prepend-inner-icon="mdi-account-outline"
            variant="outlined"
            density="comfortable"
            :rules="[required]"
            autocomplete="username"
            class="na-field mb-3"
          />

          <v-text-field
            v-model="password"
            label="Password"
            prepend-inner-icon="mdi-lock-outline"
            :append-inner-icon="showPassword ? 'mdi-eye-off-outline' : 'mdi-eye-outline'"
            :type="showPassword ? 'text' : 'password'"
            variant="outlined"
            density="comfortable"
            :rules="[required]"
            autocomplete="current-password"
            class="na-field"
            @click:append-inner="showPassword = !showPassword"
          />

          <v-alert
            v-if="error"
            type="error"
            variant="tonal"
            density="compact"
            rounded="lg"
            class="mt-3 mb-1"
          >{{ error }}</v-alert>

          <button
            type="submit"
            class="na-btn-submit mt-5"
            :disabled="loading"
          >
            <v-progress-circular v-if="loading" indeterminate size="18" width="2" color="white" class="mr-2" />
            <span>{{ loading ? 'Signing in…' : 'Sign In' }}</span>
            <v-icon v-if="!loading" icon="mdi-arrow-right" size="18" class="ml-2" />
          </button>
        </v-form>

        <p class="na-hint mt-5">
          Demo: <strong>admin</strong> / <strong>password</strong>
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { login } from '../composables/useAuth.js'

const router       = useRouter()
const formRef      = ref(null)
const username     = ref('')
const password     = ref('')
const showPassword = ref(false)
const loading      = ref(false)
const error        = ref('')

const required = (v) => !!v || 'This field is required'

async function handleLogin() {
  error.value = ''
  const { valid } = await formRef.value.validate()
  if (!valid) return
  loading.value = true
  try {
    await login(username.value, password.value)
    router.push('/')
  } catch (err) {
    error.value = err?.response?.data?.detail ?? 'Login failed. Please try again.'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
/* ── page ── */
.na-login {
  height: 100%;
  min-height: 0;
  background: #12111A;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: hidden;
  padding: 24px;
}

/* soft blurred orbs */
.na-orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(80px);
  pointer-events: none;
}
.na-orb--purple {
  width: 480px; height: 480px;
  background: rgba(168, 85, 247, 0.22);
  top: -120px; left: -100px;
}
.na-orb--pink {
  width: 400px; height: 400px;
  background: rgba(236, 72, 153, 0.18);
  bottom: -100px; right: -80px;
}

/* ── card ── */
.na-card {
  position: relative;
  z-index: 1;
  width: 100%;
  max-width: 420px;
  background: #1C1A2E;
  border-radius: 24px;
  border: 1px solid rgba(168, 85, 247, 0.2);
  overflow: hidden;
  box-shadow: 0 24px 60px rgba(0, 0, 0, 0.5), 0 0 0 1px rgba(168,85,247,0.08);
}

.na-card__topbar {
  height: 4px;
  background: linear-gradient(90deg, #A855F7, #EC4899, #84CC16);
}

.na-card__body { padding: 32px; }

.na-card__divider {
  height: 1px;
  background: rgba(168, 85, 247, 0.12);
  margin: 20px 0;
}

/* ── logo ── */
.na-logo {
  display: flex;
  align-items: center;
  gap: 14px;
}
.na-logo__icon {
  width: 48px; height: 48px;
  border-radius: 14px;
  background: linear-gradient(135deg, #A855F7, #EC4899);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  box-shadow: 0 6px 20px rgba(168, 85, 247, 0.5);
}
.na-logo__name {
  font-size: 1.25rem;
  font-weight: 800;
  letter-spacing: -0.02em;
  color: #EDE9FE;
}
.na-logo__accent {
  background: linear-gradient(135deg, #A855F7, #EC4899);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}
.na-logo__sub {
  font-size: 0.72rem;
  color: #6B6A8A;
  margin-top: 2px;
}

/* ── headlines ── */
.na-card__headline {
  font-size: 1.4rem;
  font-weight: 700;
  color: #EDE9FE;
  margin: 0 0 4px;
}
.na-card__sub {
  font-size: 0.82rem;
  color: #6B6A8A;
  margin: 0;
}

/* ── fields ── */
.na-field :deep(.v-field) { background: rgba(37, 35, 64, 0.8) !important; }
.na-field :deep(.v-field__outline) { --v-field-border-opacity: 0.4 !important; }

/* ── submit button ── */
.na-btn-submit {
  width: 100%;
  padding: 14px 24px;
  border-radius: 12px;
  background: linear-gradient(135deg, #A855F7, #EC4899);
  color: #fff;
  font-size: 0.95rem;
  font-weight: 700;
  letter-spacing: 0.01em;
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: opacity 0.2s, transform 0.15s, box-shadow 0.2s;
  box-shadow: 0 6px 24px rgba(168, 85, 247, 0.4);
}
.na-btn-submit:hover:not(:disabled) {
  opacity: 0.92;
  transform: translateY(-1px);
  box-shadow: 0 10px 32px rgba(168, 85, 247, 0.55);
}
.na-btn-submit:active:not(:disabled) { transform: translateY(0); }
.na-btn-submit:disabled { opacity: 0.6; cursor: not-allowed; }

/* ── hint ── */
.na-hint {
  text-align: center;
  font-size: 0.75rem;
  color: #6B6A8A;
}
.na-hint strong { color: #A855F7; }
</style>
