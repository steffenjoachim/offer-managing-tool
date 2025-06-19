<div class="listing-status">
  <el-tag
    :type="statusType"
    :effect="statusEffect"
    class="status-tag"
  >
    {{ statusLabel }}
  </el-tag>
</div>

<script setup>
import { computed } from "vue";

const props = defineProps({
  status: {
    type: String,
    required: true,
    validator: (value) => ["active", "sold", "expired"].includes(value),
  },
});

const statusType = computed(() => {
  switch (props.status) {
    case "active":
      return "success";
    case "sold":
      return "warning";
    case "expired":
      return "info";
    default:
      return "default";
  }
});

const statusEffect = computed(() => {
  return "light";
});

const statusLabel = computed(() => {
  switch (props.status) {
    case "active":
      return "Active";
    case "sold":
      return "Sold";
    case "expired":
      return "Expired";
    default:
      return "Unknown";
  }
});
</script>
