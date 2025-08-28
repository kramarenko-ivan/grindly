<template>
  <div class="habits-view">
    <div class="habits-header">
      <h1>Your Habits</h1>
      <button class="logout-btn" @click="logout">Logout</button>
    </div>

    <div v-if="loading">Loading habits...</div>
    <div v-if="error" class="error">{{ error }}</div>

    <!-- Habits list -->
    <ul v-if="habits.length > 0">
      <li v-for="habit in habits" :key="habit.id" class="habit-item">
        <span @click="startEdit(habit)">{{ habit.title }} - {{ habit.description }}</span>
        <button class="remove-btn" @click="removeHabit(habit.id)">X</button>
      </li>
    </ul>

    <div v-else-if="!loading && !error">No habits yet.</div>

    <!-- Add habit form -->
    <div class="habit-form">
      <input v-model="titleInput" placeholder="Habit title" />
      <input v-model="descriptionInput" placeholder="Description (optional)" />
      <button @click="editingHabitId ? saveHabit() : addHabit()" :disabled="adding">
        {{ editingHabitId ? 'Save habit' : adding ? 'Adding...' : 'Add habit' }}
      </button>
      <button v-if="editingHabitId" @click="cancelEdit()">Cancel</button>
    </div>
  </div>
</template>

<script lang="ts">
import { getUserId } from '@/utils/auth';
import axios, { AxiosError } from 'axios';
import { defineComponent, ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';

interface Habit {
  id: number;
  title: string;
  description?: string;
}

export default defineComponent({
  name: 'HabitsView',
  setup() {
    const router = useRouter();
    const habits = ref<Habit[]>([]);
    const loading = ref(false);
    const error = ref('');
    const adding = ref(false);

    const editingHabitId = ref<number | null>(null);
    const titleInput = ref('');
    const descriptionInput = ref('');

    const getCurrentUserId = (): string | null => {
      const user_id = getUserId();
      if (!user_id) {
        error.value = 'User not logged in';
        loading.value = false;
        return null;
      }
      return user_id;
    };

    const fetchHabits = async () => {
      loading.value = true;
      error.value = '';
      try {
        const user_id = getCurrentUserId();
        if (!user_id) return;
        const response = await axios.get('http://localhost:8000/habits', { params: { user_id } });
        habits.value = response.data;
      } catch (err: unknown) {
        const axiosError = err as AxiosError<{ detail?: string }>;
        error.value = axiosError.response?.data?.detail || 'Failed to load habits';
      } finally {
        loading.value = false;
      }
    };

    const removeHabit = async (habitId: number) => {
      try {
        const user_id = getCurrentUserId();
        if (!user_id) return;
        await axios.delete(`http://localhost:8000/habits/${habitId}`, { params: { user_id } });
        habits.value = habits.value.filter((h) => h.id !== habitId);
      } catch (err: unknown) {
        const axiosError = err as AxiosError<{ detail?: string }>;
        error.value = axiosError.response?.data?.detail || 'Failed to remove habit';
      }
    };

    const addHabit = async () => {
      if (!titleInput.value.trim()) {
        error.value = 'Title is required';
        return;
      }
      adding.value = true;
      error.value = '';
      try {
        const user_id = getCurrentUserId();
        if (!user_id) return;
        const response = await axios.post('http://localhost:8000/habits', {
          user_id,
          title: titleInput.value,
          description: descriptionInput.value,
        });
        habits.value.push(response.data);
        titleInput.value = '';
        descriptionInput.value = '';
      } catch (err: unknown) {
        const axiosError = err as AxiosError<{ detail?: string }>;
        error.value = axiosError.response?.data?.detail || 'Failed to add habit';
      } finally {
        adding.value = false;
      }
    };

    const saveHabit = async () => {
      if (!titleInput.value.trim()) {
        error.value = 'Title is required';
        return;
      }
      try {
        const user_id = getCurrentUserId();
        if (!user_id) return;
        const response = await axios.put(`http://localhost:8000/habits/${editingHabitId.value}`, {
          user_id,
          title: titleInput.value,
          description: descriptionInput.value,
        });
        const index = habits.value.findIndex((h) => h.id === editingHabitId.value);
        if (index !== -1) habits.value[index] = response.data;
        cancelEdit();
      } catch (err: unknown) {
        const axiosError = err as AxiosError<{ detail?: string }>;
        error.value = axiosError.response?.data?.detail || 'Failed to update habit';
      }
    };

    const cancelEdit = () => {
      editingHabitId.value = null;
      titleInput.value = '';
      descriptionInput.value = '';
    };

    const startEdit = (habit: Habit) => {
      editingHabitId.value = habit.id;
      titleInput.value = habit.title;
      descriptionInput.value = habit.description || '';
    };

    const logout = () => {
      localStorage.removeItem('token');
      localStorage.removeItem('user_id');
      router.push('/');
    };

    onMounted(fetchHabits);

    return {
      habits,
      loading,
      error,
      editingHabitId,
      titleInput,
      descriptionInput,
      adding,
      addHabit,
      removeHabit,
      startEdit,
      saveHabit,
      cancelEdit,
      logout,
    };
  },
});
</script>

<style scoped>
.habits-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.logout-btn {
  padding: 0.5rem 1rem;
  cursor: pointer;
  background-color: #39a6ff;
  color: #fff;
  border: none;
  border-radius: 5px;
}
.logout-btn:hover {
  background-color: #359cf0;
}

.habits-view {
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

.habits-view h1 {
  text-align: center;
  margin-bottom: 1rem;
}

.habit-form input {
  width: 100%;
  padding: 0.5rem;
  margin-bottom: 0.5rem;
  box-sizing: border-box;
}

.habit-form button {
  padding: 0.75rem;
  cursor: pointer;
  width: 100%;
  margin-top: 0.5rem;
}

.habit-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.5rem;
  border-bottom: 1px solid #eee;
}

.remove-btn {
  background-color: #ff4d4d;
  color: white;
  border: none;
  border-radius: 4px;
  padding: 0.25rem 0.5rem;
  cursor: pointer;
}

.error {
  color: red;
  text-align: center;
}

.habit-form {
  display: flex;
  flex-direction: column;
}
</style>
