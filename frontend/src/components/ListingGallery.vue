<div class="listing-gallery">
  <div class="main-image">
    <img
      v-if="currentImage"
      :src="currentImage.image"
      :alt="currentImage.alt"
      class="image"
      @error="handleImageError"
    />
    <div v-else class="placeholder">
      <el-icon><Picture /></el-icon>
    </div>
  </div>
  <div class="thumbnails">
    <div
      v-for="(image, index) in images"
      :key="index"
      class="thumbnail"
      :class="{ active: currentIndex === index }"
      @click="selectImage(index)"
    >
      <img
        :src="image.image"
        :alt="image.alt"
        class="image"
        @error="handleImageError"
      />
    </div>
  </div>
</div>

<script setup>
import { ref, computed } from "vue";
import { Picture } from "@element-plus/icons-vue";

const props = defineProps({
  images: {
    type: Array,
    required: true,
  },
});

const emit = defineEmits(["error"]);

const currentIndex = ref(0);

const currentImage = computed(() => {
  return props.images[currentIndex.value];
});

const selectImage = (index) => {
  currentIndex.value = index;
};

const handleImageError = () => {
  emit("error");
};
</script> 