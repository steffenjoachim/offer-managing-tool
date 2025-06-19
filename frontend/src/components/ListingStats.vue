<div class="listing-stats">
  <h3 class="title">Listing Statistics</h3>
  <div v-if="loading" class="loading">
    <el-skeleton :rows="3" animated />
  </div>
  <div v-else-if="error" class="error">
    {{ error }}
  </div>
  <div v-else class="stats-grid">
    <div class="stat-item">
      <h4>Views</h4>
      <p>{{ stats.views }}</p>
    </div>
    <div class="stat-item">
      <h4>Favorites</h4>
      <p>{{ stats.favorites }}</p>
    </div>
    <div class="stat-item">
      <h4>Messages</h4>
      <p>{{ stats.messages }}</p>
    </div>
    <div class="stat-item">
      <h4>Reports</h4>
      <p>{{ stats.reports }}</p>
    </div>
  </div>
</div>

<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";

const props = defineProps({
  listingId: {
    type: Number,
    required: true,
  },
});

const stats = ref({
  views: 0,
  favorites: 0,
  messages: 0,
  reports: 0,
});
const loading = ref(true);
const error = ref(null);

const fetchStats = async () => {
  try {
    loading.value = true;
    error.value = null;
    const response = await axios.get(
      `http://localhost:8000/api/listings/${props.listingId}/stats/`
    );
    stats.value = response.data;
  } catch (err) {
    error.value = "Error loading listing statistics";
    console.error("Error loading listing statistics:", err);
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  fetchStats();
});
</script> 