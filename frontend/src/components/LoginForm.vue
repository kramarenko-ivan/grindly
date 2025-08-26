<template>
  <form @submit.prevent="submitForm" class="login-form">
    <div>
      <label for="username">Username:</label>
      <input id="username" v-model="username" type="text" required />
    </div>

    <div>
      <label for="email">Email:</label>
      <input id="email" v-model="email" type="email" required />
    </div>

    <div>
      <label for="password">Password:</label>
      <input id="password" v-model="password" type="password" required />
    </div>

    <button type="submit" :disabled="loading">
      {{ loading ? 'Registering...' : 'Register' }}
    </button>

    <p v-if="error" class="error">{{ error }}</p>
    <p v-if="success" class="success">Registration successful!</p>
  </form>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue'
import axios, { AxiosError } from 'axios'

export default defineComponent({
  name: 'LoginForm',
  setup() {
    const username = ref('')
    const email = ref('')
    const password = ref('')
    const loading = ref(false)
    const error = ref('')
    const success = ref(false)

    const submitForm = async () => {
      error.value = ''
      success.value = false
      loading.value = true

      try {
        const response = await axios.post('http://localhost:8000/register', {
          username: username.value,
          email: email.value,
          password: password.value,
        })

        if (response.status === 200) {
          success.value = true
          username.value = ''
          email.value = ''
          password.value = ''
        }
      } catch (err: unknown) {
        const axiosError = err as AxiosError<{ detail?: string }>
        error.value = axiosError.response?.data?.detail || 'Registration failed'
      } finally {
        loading.value = false
      }
    }

    return { username, email, password, loading, error, success, submitForm }
  },
})
</script>

<style scoped>
.login-form {
  max-width: 400px;
  margin: 50px auto;
  padding: 2rem;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.login-form label {
  display: block;
  margin-bottom: 0.5rem;
}

.login-form input {
  width: 100%;
  padding: 0.5rem;
  box-sizing: border-box;
}

.login-form button {
  padding: 0.75rem;
  cursor: pointer;
}

.error {
  color: red;
}

.success {
  color: green;
}
</style>
