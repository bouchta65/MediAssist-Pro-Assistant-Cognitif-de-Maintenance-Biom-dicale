<template>
  <div class="min-h-screen bg-gray-50 flex flex-col justify-center py-12 sm:px-6 lg:px-8">
    <div class="sm:mx-auto sm:w-full sm:max-w-md">
      <div class="bg-white py-8 px-4 shadow sm:rounded-lg sm:px-10">
        <div class="text-center">
          <div v-if="loading" class="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600 mx-auto"></div>
          <div v-else-if="error" class="text-red-600">
            <h3 class="text-lg font-medium">Erreur d'authentification</h3>
            <p class="mt-2">{{ error }}</p>
            <router-link to="/" class="mt-4 inline-block text-indigo-600 hover:text-indigo-500">
              Retour à la connexion
            </router-link>
          </div>
          <div v-else class="text-green-600">
            <h3 class="text-lg font-medium">Connexion réussie</h3>
            <p class="mt-2">Redirection en cours...</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AuthCallback',
  data() {
    return {
      loading: true,
      error: null
    }
  },
  mounted() {
    this.handleCallback()
  },
  methods: {
    handleCallback() {
      const urlParams = new URLSearchParams(window.location.search)
      const token = urlParams.get('token')
      
      if (token) {
        localStorage.setItem('token', token)
        this.$router.push('/dashboard')
      } else {
        this.error = 'Token non reçu'
        this.loading = false
      }
    }
  }
}
</script>