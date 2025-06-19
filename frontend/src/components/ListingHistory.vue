<div class="listing-history">
  <h3 class="title">Listing History</h3>
  <div v-if="loading" class="loading">
    <el-skeleton :rows="3" animated />
  </div>
  <div v-else-if="error" class="error">
    {{ error }}
  </div>
  <div v-else-if="history.length === 0" class="empty">
    No history available.
  </div>
  <div v-else class="history-list">
    <el-timeline>
      <el-timeline-item
        v-for="item in history"
        :key="item.id"
        :timestamp="formatDate(item.timestamp)"
        :type="getTimelineItemType(item.type)"
      >
        {{ item.description }}
      </el-timeline-item>
    </el-timeline>
  </div>
</div>

<script setup>
import { ref, onMounted } from "vue";
import { format } from "date-fns";
import axios from "axios";

const props = defineProps({
  listingId: {
    type: Number,
    required: true,
  },
});

const history = ref([]);
const loading = ref(true);
const error = ref(null);

const fetchHistory = async () => {
  try {
    loading.value = true;
    error.value = null;
    const response = await axios.get(
      `http://localhost:8000/api/listings/${props.listingId}/history/`
    );
    history.value = response.data;
  } catch (err) {
    error.value = "Error loading listing history";
    console.error("Error loading listing history:", err);
  } finally {
    loading.value = false;
  }
};

const formatDate = (date) => {
  return format(new Date(date), "MMMM d, yyyy 'at' h:mm a");
};

const getTimelineItemType = (type) => {
  switch (type) {
    case "created":
      return "success";
    case "updated":
      return "warning";
    case "deleted":
      return "danger";
    default:
      return "info";
  }
};

onMounted(() => {
  fetchHistory();
});
</script> 