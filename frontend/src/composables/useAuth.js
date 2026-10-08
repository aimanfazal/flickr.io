import { ref, computed } from 'vue'
import { login as apiLogin } from '../api/index.js'

const TOKEN_KEY = 'ott_auth_token'

const token = ref(localStorage.getItem(TOKEN_KEY) ?? null)

export const isAuthenticated = computed(() => token.value !== null)

export async function login(username, password) {
  const data = await apiLogin(username, password)
  token.value = data.access_token
  localStorage.setItem(TOKEN_KEY, data.access_token)
}

export function logout() {
  token.value = null
  localStorage.removeItem(TOKEN_KEY)
}

export function getToken() {
  return token.value
}
