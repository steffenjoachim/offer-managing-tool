<div class="listing-review-form">
  <h3 class="title">Write a Review</h3>
  <el-form
    ref="formRef"
    :model="form"
    :rules="rules"
    label-position="top"
    @submit.prevent="handleSubmit"
  >
    <el-form-item label="Rating" prop="rating">
      <el-rate
        v-model="form.rating"
        :colors="colors"
        show-score
      />
    </el-form-item>
    <el-form-item label="Comment" prop="comment">
      <el-input
        v-model="form.comment"
        type="textarea"
        :rows="4"
        placeholder="Write your review"
      />
    </el-form-item>
    <el-form-item>
      <el-button
        type="primary"
        native-type="submit"
        :loading="loading"
      >
        Submit Review
      </el-button>
    </el-form-item>
  </el-form>
</div>

<script setup>
import { ref } from "vue";
import { ElMessage } from "element-plus";

const props = defineProps({
  listingId: {
    type: Number,
    required: true,
  },
});

const emit = defineEmits(["review-submitted"]);

const formRef = ref(null);
const loading = ref(false);

const form = ref({
  rating: 0,
  comment: "",
});

const colors = {
  1: "#F56C6C",
  2: "#E6A23C",
  3: "#909399",
  4: "#67C23A",
  5: "#409EFF",
};

const rules = {
  rating: [
    { required: true, message: "Please select a rating", trigger: "change" },
    {
      type: "number",
      min: 1,
      max: 5,
      message: "Rating must be between 1 and 5",
      trigger: "change",
    },
  ],
  comment: [
    { required: true, message: "Please write a comment", trigger: "blur" },
    {
      min: 10,
      max: 1000,
      message: "Length should be 10 to 1000 characters",
      trigger: "blur",
    },
  ],
};

const handleSubmit = async () => {
  if (!formRef.value) return;

  try {
    await formRef.value.validate();
    loading.value = true;

    // TODO: Implement review submission logic
    await new Promise((resolve) => setTimeout(resolve, 1000));

    ElMessage.success("Review submitted successfully");
    emit("review-submitted");
    form.value = {
      rating: 0,
      comment: "",
    };
  } catch (error) {
    console.error("Error submitting review:", error);
    ElMessage.error("Failed to submit review");
  } finally {
    loading.value = false;
  }
};
</script>
