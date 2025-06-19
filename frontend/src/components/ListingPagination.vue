<div class="listing-pagination">
  <el-pagination
    v-model:current-page="currentPage"
    v-model:page-size="pageSize"
    :total="total"
    :page-sizes="[12, 24, 36, 48]"
    layout="total, sizes, prev, pager, next, jumper"
    @size-change="handleSizeChange"
    @current-change="handleCurrentChange"
  />
</div>

<script setup>
import { ref, watch } from "vue";

const props = defineProps({
  total: {
    type: Number,
    required: true,
  },
  initialPage: {
    type: Number,
    default: 1,
  },
  initialPageSize: {
    type: Number,
    default: 12,
  },
});

const emit = defineEmits(["page-change"]);

const currentPage = ref(props.initialPage);
const pageSize = ref(props.initialPageSize);

const handleSizeChange = (size) => {
  pageSize.value = size;
  emit("page-change", { page: currentPage.value, pageSize: size });
};

const handleCurrentChange = (page) => {
  currentPage.value = page;
  emit("page-change", { page, pageSize: pageSize.value });
};

watch(
  () => props.total,
  () => {
    if (currentPage.value > Math.ceil(props.total / pageSize.value)) {
      currentPage.value = 1;
      emit("page-change", { page: 1, pageSize: pageSize.value });
    }
  }
);
</script>
