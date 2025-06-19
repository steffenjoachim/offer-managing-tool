<div class="listing-date">
  <el-tooltip
    :content="formattedDate"
    placement="top"
    :show-after="500"
  >
    <span class="date-text">{{ relativeDate }}</span>
  </el-tooltip>
</div>

<script setup>
import { computed } from "vue";
import { formatDistanceToNow, format } from "date-fns";

const props = defineProps({
  date: {
    type: String,
    required: true,
  },
});

const formattedDate = computed(() => {
  return format(new Date(props.date), "MMMM d, yyyy 'at' h:mm a");
});

const relativeDate = computed(() => {
  return formatDistanceToNow(new Date(props.date), { addSuffix: true });
});
</script>
