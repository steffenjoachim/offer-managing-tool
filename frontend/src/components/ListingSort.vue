<div class="listing-sort">
  <el-select
    v-model="sortBy"
    placeholder="Sort by"
    @change="handleSortChange"
  >
    <el-option label="Newest" value="created_at" />
    <el-option label="Price: Low to High" value="price" />
    <el-option label="Price: High to Low" value="-price" />
    <el-option label="Title: A to Z" value="title" />
    <el-option label="Title: Z to A" value="-title" />
  </el-select>
</div>

<script setup>
import { ref } from "vue";

const emit = defineEmits(["sort"]);

const sortBy = ref("created_at");

const handleSortChange = () => {
  emit("sort", sortBy.value);
};
</script>
