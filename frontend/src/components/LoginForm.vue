<template>
  <form @submit.prevent="submitForm" class="login-form">
    <h2>{{ isLogin ? 'Login' : 'Register' }}</h2>
    <!-- Username only for registration -->
    <div v-if="!isLogin">
      <label for="username">Username:</label>
      <input id="username" v-model="username" type="text" required />
    </div>

    <!-- Email (always required) -->
    <div>
      <label :for="isLogin ? 'login' : 'email'">
        {{ isLogin ? 'Username or Email:' : 'Email:' }}
      </label>
      <input
        :id="isLogin ? 'login' : 'email'"
        v-model="loginField"
        :type="isLogin ? 'text' : 'email'"
        required
      />
    </div>

    <div>
      <label for="password">Password:</label>
      <input id="password" v-model="password" type="password" required />
    </div>

    <button type="submit" :disabled="loading">
      {{
        loading ? (isLogin ? 'Logging in...' : 'Registering...') : isLogin ? 'Login' : 'Register'
      }}
    </button>

    <p v-if="error" class="error">{{ error }}</p>
    <p v-if="success" class="success">
      {{ isLogin ? 'Login successful!' : 'Registration successful!' }}
    </p>

    <p class="switch-mode">
      {{ isLogin ? "Don't have an account?" : 'Already have an account?' }}
      <a href="#" @click.prevent="toggleMode">{{ isLogin ? 'Register here' : 'Login here' }}</a>
    </p>
  </form>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';
import axios, { AxiosError } from 'axios';
import type { LoginPayload, RegisterPayload, TokenResponse } from '@/types/auth';
import { useRouter } from 'vue-router';
import qs from 'qs';
import { jwtDecode } from 'jwt-decode';

interface JwtPayload {
  sub: string;
}

export default defineComponent({
  name: 'LoginForm',
  setup() {
    const username = ref('');
    const loginField = ref(''); // username or email
    const password = ref('');
    const loading = ref(false);
    const error = ref('');
    const success = ref(false);
    const isLogin = ref(false);

    const router = useRouter();

    const toggleMode = () => {
      isLogin.value = !isLogin.value;
      error.value = '';
      success.value = false;
      username.value = '';
      loginField.value = '';
      password.value = '';
    };

    const submitForm = async () => {
      error.value = '';
      success.value = false;
      loading.value = true;

      try {
        if (isLogin.value) {
          // Login through form-urlencoded
          const payload: LoginPayload = {
            username: loginField.value, // can be username or email
            password: password.value,
          };

          const apiUrl = import.meta.env.VITE_API_URL;
          console.log('VITE_API_URL:', apiUrl); //check
          const response = await axios.post<TokenResponse>(
            `${apiUrl}/login`,
            qs.stringify(payload),
            {
              headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
            },
          );

          if (response.status === 200) {
            const token = response.data.access_token;
            localStorage.setItem('token', token); // save token

            const decoded = jwtDecode<JwtPayload>(token);
            localStorage.setItem('user_id', decoded.sub);

            success.value = true;
            loginField.value = '';
            password.value = '';

            // Move on page HabitsView
            router.push({ name: 'HabitsView' });
          }
        } else {
          // Register through JSON
          const payload: RegisterPayload = {
            username: username.value,
            email: loginField.value, // can be username or email
            password: password.value,
          };

          const apiUrl = import.meta.env.VITE_API_URL;
          console.log('VITE_API_URL:', apiUrl); //check
          const response = await axios.post(`${apiUrl}/register`, payload);
          if (response.status === 200) {
            success.value = true;
            username.value = '';
            loginField.value = '';
            password.value = '';
          }
        }
      } catch (err: unknown) {
        const axiosError = err as AxiosError<{ detail?: string }>;
        error.value = axiosError.response?.data?.detail || 'Registration failed';
      } finally {
        loading.value = false;
      }
    };

    return {
      username,
      loginField,
      password,
      loading,
      error,
      success,
      isLogin,
      toggleMode,
      submitForm,
    };
  },
});
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
