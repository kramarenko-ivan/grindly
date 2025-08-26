<template>
  <div class="habits-view">
    <h1>Your Habits</h1>

    <div v-if="loading">Loading habits...</div>
    <div v-if="error" class="error">{{ error }}</div>

    <!-- Habits list -->
    <ul v-if="habits.length > 0">
      <li v-for="habit in habits" :key="habit.id">
        {{ habit.title }}
        {{ habit.description }}
        <button @click="removeHabit(habit.id)">X</button>
      </li>
    </ul>

    <div v-else-if="!loading && !error">No habits yet.</div>

    <!-- Add habit form -->
    <div class="add-habit">
      <input v-model="newTitle" placeholder="Habit title" />
      <input v-model="newDescription" placeholder="Description (optional)" />
      <button @click="addHabit" :disabled="adding">
        {{ adding ? 'Adding...' : 'Add habit' }}
      </button>
    </div>
  </div>
</template>

<script lang="ts">
import axios, { AxiosError } from 'axios';
import { defineComponent, ref, onMounted } from 'vue';

interface Habit {
  id: number;
  title: string;
  description?: string;
}

export default defineComponent({
  name: 'HabitsView',
  setup() {
    const habits = ref<Habit[]>([]);
    const loading = ref(false);
    const error = ref('');
    const adding = ref(false);

    const newTitle = ref('');
    const newDescription = ref('');

    const fetchHabits = async () => {
      loading.value = true;
      error.value = '';
      try {
        const response = await axios.get('http://localhost:8000/habits', {
          params: { user_id: 12 },
        });
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
        await axios.delete(`http://localhost:8000/habits/${habitId}`, {
          params: { user_id: 12 },
        });
        // After remove, we are update list
        habits.value = habits.value.filter((h) => h.id !== habitId);
      } catch (err: unknown) {
        const axiosError = err as AxiosError<{ detail?: string }>;
        error.value = axiosError.response?.data?.detail || 'Failed to load habits';
      }
    };

    const addHabit = async () => {
      if (!newTitle.value.trim()) {
        error.value = 'Title is required';
        return;
      }

      adding.value = true;
      error.value = '';

      try {
        const response = await axios.post('http://localhost:8000/habits', {
          user_id: 12,
          title: newTitle.value,
          description: newDescription.value,
        });
        habits.value.push(response.data);
        newTitle.value = '';
        newDescription.value = '';
      } catch (err: unknown) {
        const axiosError = err as AxiosError<{ detail?: string }>;
        error.value = axiosError.response?.data?.detail || 'Failed to add habit';
      } finally {
        adding.value = false;
      }
    };

    onMounted(() => {
      fetchHabits();
    });

    return { habits, loading, error, newTitle, newDescription, adding, addHabit, removeHabit };
  },
});
</script>

<style scoped>
.habits-view {
  max-width: 600px;
  margin: 50px auto;
  padding: 1rem;
}

.error {
  color: red;
}
</style>
