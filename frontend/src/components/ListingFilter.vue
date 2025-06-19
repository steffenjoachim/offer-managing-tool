<div class="listing-filter">
      <el-form :model="filterForm" label-position="top">
        <el-form-item label="Price Range">
          <el-slider
            v-model="filterForm.priceRange"
            range
            :min="0"
            :max="1000"
            :step="10"
            @change="handleFilterChange"
          />
        </el-form-item>

        <el-form-item label="Category">
          <el-select
            v-model="filterForm.category"
            placeholder="Select category"
            clearable
            @change="handleFilterChange"
          >
            <el-option
              v-for="category in categories"
              :key="category"
              :label="category"
              :value="category"
            />
          </el-select>
        </el-form-item>

        <el-form-item label="Sort By">
          <el-select
            v-model="filterForm.sortBy"
            placeholder="Sort by"
            @change="handleFilterChange"
          >
            <el-option label="Newest" value="created_at" />
            <el-option label="Price: Low to High" value="price" />
            <el-option label="Price: High to Low" value="-price" />
          </el-select>
        </el-form-item>

        <el-form-item>
          <el-button type="primary" @click="applyFilters">Apply Filters</el-button>
          <el-button @click="resetFilters">Reset</el-button>
        </el-form-item>
      </el-form>
    </div>

<script setup>
import { ref } from "vue";

const emit = defineEmits(["filter"]);

const filterForm = ref({
  priceRange: [0, 1000],
  category: "",
  sortBy: "created_at",
});

const categories = [
  "Electronics",
  "Fashion",
  "Home & Garden",
  "Sports & Leisure",
  "Toys & Games",
  "Other",
];

const handleFilterChange = () => {
  applyFilters();
};

const applyFilters = () => {
  const filters = {
    minPrice: filterForm.value.priceRange[0],
    maxPrice: filterForm.value.priceRange[1],
    category: filterForm.value.category,
    sortBy: filterForm.value.sortBy,
  };
  emit("filter", filters);
};

const resetFilters = () => {
  filterForm.value = {
    priceRange: [0, 1000],
    category: "",
    sortBy: "created_at",
  };
  applyFilters();
};
</script>
