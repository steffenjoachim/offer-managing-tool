<div class="listing-category">
  <h3 class="title">Category</h3>
<div class="listing-category">
  <el-select
    v-model="selectedCategory"
    placeholder="Select category"
    clearable
    @change="handleCategoryChange"
  >
    <el-option
      v-for="category in categories"
      :key="category"
      :label="category"
      :value="category"
    />
  </el-select>
</div>

<script setup>
import { ref } from "vue";

const emit = defineEmits(["category-change"]);

const selectedCategory = ref("");

const categories = [
  "Electronics",
  "Fashion",
  "Home & Garden",
  "Sports",
  "Toys",
  "Books",
  "Other",
];

const handleCategoryChange = () => {
  emit("category-change", selectedCategory.value);
};
</script>
