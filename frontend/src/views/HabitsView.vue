<template>
  <div class="habits-view">
    <h1>Your Habits</h1>

    <div v-if="loading">Loading habits...</div>
    <div v-if="error" class="error">{{ error }}</div>

    <!-- Habits list -->
    <ul v-if="habits.length > 0">
      <li v-for="habit in habits" :key="habit.id">
        <span @click="startEdit(habit)">{{ habit.title }} - {{ habit.description }}</span>
        <button @click="removeHabit(habit.id)">X</button>
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

    const editingHabitId = ref<number | null>(null);
    const titleInput = ref('');
    const descriptionInput = ref('');

    // Unique function for get user_id and error get
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
        if (!user_id) {
          return;
        }
        const response = await axios.get('http://localhost:8000/habits', {
          params: { user_id },
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
        const user_id = getCurrentUserId();
        if (!user_id) {
          return;
        }
        await axios.delete(`http://localhost:8000/habits/${habitId}`, {
          params: { user_id },
        });
        // After remove, we are update list
        habits.value = habits.value.filter((h) => h.id !== habitId);
      } catch (err: unknown) {
        const axiosError = err as AxiosError<{ detail?: string }>;
        error.value = axiosError.response?.data?.detail || 'Failed to load habits';
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
        if (!user_id) {
          return;
        }
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
        if (!user_id) {
          return;
        }
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
        error.value = axiosError.response?.data?.detail || 'Failed to add habit';
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

    onMounted(() => {
      fetchHabits();
    });

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
    };
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
