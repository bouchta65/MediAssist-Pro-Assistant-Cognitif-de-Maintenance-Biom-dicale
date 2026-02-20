<template>
  <div class="min-h-screen bg-gray-50 flex flex-col justify-center py-12 sm:px-6 lg:px-8">
    <div class="sm:mx-auto sm:w-full sm:max-w-md">
      <div class="flex justify-center">
        <div class="w-12 h-12 bg-indigo-600 rounded-lg flex items-center justify-center">
          <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"></path>
          </svg>
        </div>
      </div>
      <h2 class="mt-6 text-center text-3xl font-extrabold text-gray-900">
        MediAssist Pro
      </h2>
      <p class="mt-2 text-center text-sm text-gray-600">
        Assistant Cognitif de Maintenance Biomédicale
      </p>
    </div>

    <div class="mt-8 sm:mx-auto sm:w-full sm:max-w-md">
      <div class="bg-white py-8 px-4 shadow sm:rounded-lg sm:px-10">
        <!-- Toggle between Login and Register -->
        <div class="flex mb-6">
          <button
            @click="isRegister = false"
            :class="[
              'flex-1 py-2 px-4 text-sm font-medium rounded-l-md border',
              !isRegister ? 'bg-indigo-600 text-white border-indigo-600' : 'bg-white text-gray-700 border-gray-300 hover:bg-gray-50'
            ]"
          >
            Connexion
          </button>
          <button
            @click="isRegister = true"
            :class="[
              'flex-1 py-2 px-4 text-sm font-medium rounded-r-md border-t border-r border-b',
              isRegister ? 'bg-indigo-600 text-white border-indigo-600' : 'bg-white text-gray-700 border-gray-300 hover:bg-gray-50'
            ]"
          >
            Inscription
          </button>
        </div>

        <!-- Login Form -->
        <form v-if="!isRegister" class="space-y-6" @submit.prevent="handleLogin">
          <div>
            <label for="email" class="block text-sm font-medium text-gray-700">
              Adresse email
            </label>
            <div class="mt-1">
              <input
                id="email"
                v-model="email"
                name="email"
                type="email"
                autocomplete="email"
                required
                class="appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                placeholder="votre@email.com"
              />
            </div>
          </div>

          <div>
            <label for="password" class="block text-sm font-medium text-gray-700">
              Mot de passe
            </label>
            <div class="mt-1">
              <input
                id="password"
                v-model="password"
                name="password"
                type="password"
                autocomplete="current-password"
                required
                class="appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                placeholder="••••••••"
              />
            </div>
          </div>

          <div>
            <button
              type="submit"
              :disabled="loading"
              class="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {{ loading ? 'Connexion...' : 'Se connecter' }}
            </button>
          </div>
        </form>

        <!-- Register Form -->
        <form v-else class="space-y-6" @submit.prevent="handleRegister">
          <div>
            <label for="username" class="block text-sm font-medium text-gray-700">
              Nom d'utilisateur
            </label>
            <div class="mt-1">
              <input
                id="username"
                v-model="username"
                name="username"
                type="text"
                required
                class="appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                placeholder="Votre nom"
              />
            </div>
          </div>

          <div>
            <label for="reg-email" class="block text-sm font-medium text-gray-700">
              Adresse email
            </label>
            <div class="mt-1">
              <input
                id="reg-email"
                v-model="email"
                name="email"
                type="email"
                autocomplete="email"
                required
                class="appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                placeholder="votre@email.com"
              />
            </div>
          </div>

          <div>
            <label for="reg-password" class="block text-sm font-medium text-gray-700">
              Mot de passe
            </label>
            <div class="mt-1">
              <input
                id="reg-password"
                v-model="password"
                name="password"
                type="password"
                autocomplete="new-password"
                required
                class="appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                placeholder="••••••••"
              />
            </div>
          </div>

          <div>
            <button
              type="submit"
              :disabled="loading"
              class="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {{ loading ? 'Inscription...' : 'S\'inscrire' }}
            </button>
          </div>
        </form>

        <div v-if="successMessage" class="mt-4 rounded-md bg-green-50 p-4">
          <div class="flex">
            <div class="flex-shrink-0">
              <svg class="h-5 w-5 text-green-400" fill="currentColor" viewBox="0 0 20 20">
                <path
                  fill-rule="evenodd"
                  d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
                  clip-rule="evenodd"
                />
              </svg>
            </div>
            <div class="ml-3">
              <h3 class="text-sm font-medium text-green-800">
                {{ successMessage }}
              </h3>
            </div>
          </div>
        </div>

        <div v-if="error" class="mt-4 rounded-md bg-red-50 p-4">
          <div class="flex">
            <div class="flex-shrink-0">
              <svg class="h-5 w-5 text-red-400" fill="currentColor" viewBox="0 0 20 20">
                <path
                  fill-rule="evenodd"
                  d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"
                  clip-rule="evenodd"
                />
              </svg>
            </div>
            <div class="ml-3">
              <h3 class="text-sm font-medium text-red-800">
                {{ error }}
              </h3>
            </div>
          </div>
        </div>

        <div class="mt-6">
          <div class="relative">
            <div class="absolute inset-0 flex items-center">
              <div class="w-full border-t border-gray-300" />
            </div>
            <div class="relative flex justify-center text-sm">
              <span class="px-2 bg-white text-gray-500">Ou continuer avec</span>
            </div>
          </div>

          <div class="mt-6">
            <button
              @click="handleGoogleLogin"
              class="w-full inline-flex justify-center py-2 px-4 border border-gray-300 rounded-md shadow-sm bg-white text-sm font-medium text-gray-500 hover:bg-gray-50"
            >
              <svg class="w-5 h-5" viewBox="0 0 24 24">
                <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
                <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
                <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/>
                <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/>
              </svg>
              <span class="ml-2">Google</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'Login',
  data() {
    return {
      isRegister: false,
      email: '',
      password: '',
      username: '',
      loading: false,
      error: '',
      successMessage: ''
    }
  },
  methods: {
    async handleLogin() {
      this.loading = true
      this.error = ''
      this.successMessage = ''
      
      try {
        const formData = new FormData()
        formData.append('email', this.email)
        formData.append('password', this.password)
        
        const response = await axios.post('https://devastatingly-nonasbestine-amelie.ngrok-free.dev/api/auth/login', formData, {
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'ngrok-skip-browser-warning': 'true'
          }
        })
        
        localStorage.setItem('token', response.data.access_token)
        this.$router.push('/dashboard')
        
      } catch (error) {
        this.error = error.response?.data?.detail || 'Email ou mot de passe incorrect'
      } finally {
        this.loading = false
      }
    },
    
    async handleRegister() {
      this.loading = true
      this.error = ''
      this.successMessage = ''
      
      try {
        const formData = new FormData()
        formData.append('email', this.email)
        formData.append('password', this.password)
        formData.append('username', this.username)
        
        const response = await axios.post('https://devastatingly-nonasbestine-amelie.ngrok-free.dev/api/auth/register', formData, {
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'ngrok-skip-browser-warning': 'true'
          }
        })
        
        // Show success message and switch to login form
        this.successMessage = response.data.message
        this.isRegister = false
        
        // Pre-fill email in login form
        const registeredEmail = this.email
        this.username = ''
        this.password = ''
        this.email = registeredEmail
        
      } catch (error) {
        this.error = error.response?.data?.detail || 'Erreur lors de l\'inscription'
      } finally {
        this.loading = false
      }
    },
    
    async handleGoogleLogin() {
      try {
        window.location.href = 'https://devastatingly-nonasbestine-amelie.ngrok-free.dev/api/auth/google'
      } catch (error) {
        this.error = 'Erreur lors de la connexion avec Google'
      }
    }
  },
  watch: {
    isRegister() {
      // Clear messages when switching between login and register
      this.error = ''
      this.successMessage = ''
    }
  }
}
</script>