<div class="listing-rating">
  <h3 class="title">Rating</h3>
  <div v-if="loading" class="loading">
    <el-skeleton :rows="3" animated />
  </div>
  <div v-else-if="error" class="error">
    {{ error }}
  </div>
  <div v-else class="rating-content">
    <div class="rating-overview">
      <el-rate
        v-model="rating.average"
        disabled
        show-score
        text-color="#ff9900"
      />
      <p class="rating-count">{{ rating.count }} reviews</p>
    </div>
    <div class="rating-breakdown">
      <div
        v-for="(count, stars) in rating.breakdown"
        :key="stars"
        class="rating-bar"
      >
        <span class="stars">{{ stars }} stars</span>
        <el-progress
          :percentage="(count / rating.count) * 100"
          :show-text="false"
        />
        <span class="count">{{ count }}</span>
      </div>
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

const rating = ref({
  average: 0,
  count: 0,
  breakdown: {
    5: 0,
    4: 0,
    3: 0,
    2: 0,
    1: 0,
  },
});
const loading = ref(true);
const error = ref(null);

const fetchRating = async () => {
  try {
    loading.value = true;
    error.value = null;
    const response = await axios.get(
      `http://localhost:8000/api/listings/${props.listingId}/rating/`
    );
    rating.value = response.data;
  } catch (err) {
    error.value = "Error loading rating";
    console.error("Error loading rating:", err);
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  fetchRating();
});
</script>
 