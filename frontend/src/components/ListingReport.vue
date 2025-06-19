<div class="listing-report">
  <h3 class="title">Report Listing</h3>
  <el-form
    ref="formRef"
    :model="form"
    :rules="rules"
    label-position="top"
    @submit.prevent="handleSubmit"
  >
    <el-form-item label="Reason" prop="reason">
      <el-select
        v-model="form.reason"
        placeholder="Select a reason"
      >
        <el-option
          v-for="reason in reasons"
          :key="reason.value"
          :label="reason.label"
          :value="reason.value"
        />
      </el-select>
    </el-form-item>
    <el-form-item label="Description" prop="description">
      <el-input
        v-model="form.description"
        type="textarea"
        :rows="4"
        placeholder="Please provide more details"
      />
    </el-form-item>
    <el-form-item>
      <el-button
        type="danger"
        native-type="submit"
        :loading="loading"
      >
        Submit Report
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

const emit = defineEmits(["report-submitted"]);

const formRef = ref(null);
const loading = ref(false);

const form = ref({
  reason: "",
  description: "",
});

const reasons = [
  { value: "inappropriate", label: "Inappropriate Content" },
  { value: "spam", label: "Spam" },
  { value: "fake", label: "Fake Listing" },
  { value: "scam", label: "Scam" },
  { value: "other", label: "Other" },
];

const rules = {
  reason: [
    { required: true, message: "Please select a reason", trigger: "change" },
  ],
  description: [
    {
      required: true,
      message: "Please provide a description",
      trigger: "blur",
    },
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

    // TODO: Implement report submission logic
    await new Promise((resolve) => setTimeout(resolve, 1000));

    ElMessage.success("Report submitted successfully");
    emit("report-submitted");
    form.value = {
      reason: "",
      description: "",
    };
  } catch (error) {
    console.error("Error submitting report:", error);
    ElMessage.error("Failed to submit report");
  } finally {
    loading.value = false;
  }
};
</script>
