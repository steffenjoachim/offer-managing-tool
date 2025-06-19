<div class="listing-image">
  <img
    v-if="image"
    :src="image"
    :alt="alt"
    class="image"
    @error="handleImageError"
  />
  <div v-else class="placeholder">
    <el-icon><Picture /></el-icon>
  </div>
</div>

<script setup>
import { ref } from "vue";
import { Picture } from "@element-plus/icons-vue";

const props = defineProps({
  image: {
    type: String,
    default: "",
  },
  alt: {
    type: String,
    default: "Listing image",
  },
});

const emit = defineEmits(["error"]);

const handleImageError = () => {
  emit("error");
};
</script> 