<div class="listing-search">
      <el-input
        v-model="searchQuery"
        placeholder="Search listings..."
        class="search-input"
        @input="handleSearch"
      >
        <template #prefix>
          <el-icon><Search /></el-icon>
        </template>
      </el-input>

      <el-select
        v-model="selectedCategory"
        placeholder="Category"
        class="category-select"
        @change="handleSearch"
      >
        <el-option
          v-for="category in categories"
          :key="category"
          :label="category"
          :value="category"
        />
      </el-select>

      <el-select
        v-model="sortBy"
        placeholder="Sort by"
        class="sort-select"
        @change="handleSearch"
      >
        <el-option label="Newest" value="created_at" />
        <el-option label="Price: Low to High" value="price" />
        <el-option label="Price: High to Low" value="-price" />
      </el-select>
    </div>

<script setup>
import { ref, watch } from "vue";
import { Search } from "@element-plus/icons-vue";

const emit = defineEmits(["search"]);

const searchQuery = ref("");
const selectedCategory = ref("");
const sortBy = ref("created_at");

const categories = [
  "Electronics",
  "Fashion",
  "Home & Garden",
  "Sports & Leisure",
  "Toys & Games",
  "Other",
];

const handleSearch = () => {
  const searchParams = {
    query: searchQuery.value,
    category: selectedCategory.value,
    sort: sortBy.value,
  };
  emit("search", searchParams);
};

watch([searchQuery, selectedCategory, sortBy], () => {
  handleSearch();
});
</script>
