<template>
  <v-container class="fill-height" fluid>
    <v-row align="center" justify="center">
      <v-col cols="12" sm="8" md="4">
        <v-card elevation="4" rounded="lg">
          <v-card-title class="pa-6 pb-2">
            <v-icon icon="mdi-play-circle-outline" color="primary" size="32" class="mr-2" />
            <span class="text-h5 font-weight-bold">OTT Analytics</span>
          </v-card-title>

          <v-card-subtitle class="px-6 pb-4 text-medium-emphasis">
            Sign in to access the dashboard
          </v-card-subtitle>

          <v-card-text class="px-6">
            <v-form ref="formRef" @submit.prevent="handleLogin">
              <v-text-field
                v-model="username"
                label="Username"
                prepend-inner-icon="mdi-account-outline"
                variant="outlined"
                density="comfortable"
                :rules="[required]"
                autocomplete="username"
                class="mb-3"
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
                @click:append-inner="showPassword = !showPassword"
              />

              <v-alert
                v-if="error"
                type="error"
                variant="tonal"
                density="compact"
                class="mt-2 mb-4"
              >
                {{ error }}
              </v-alert>

              <v-btn
                type="submit"
                color="primary"
                size="large"
                block
                :loading="loading"
                class="mt-2"
              >
                Sign In
              </v-btn>
            </v-form>
          </v-card-text>

          <v-card-text class="px-6 pb-6 pt-0 text-center text-caption text-medium-emphasis">
            Demo credentials: <strong>admin</strong> / <strong>password</strong>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { login } from '../composables/useAuth.js'

const router = useRouter()

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
