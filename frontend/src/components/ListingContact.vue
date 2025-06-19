<div class="listing-contact">
  <h3 class="title">Contact Seller</h3>
  <el-form
    ref="formRef"
    :model="form"
    :rules="rules"
    label-position="top"
    @submit.prevent="handleSubmit"
  >
    <el-form-item label="Message" prop="message">
      <el-input
        v-model="form.message"
        type="textarea"
        :rows="4"
        placeholder="Enter your message"
      />
    </el-form-item>
    <el-form-item>
      <el-button
        type="primary"
        native-type="submit"
        :loading="loading"
      >
        Send Message
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

const emit = defineEmits(["message-sent"]);

const formRef = ref(null);
const loading = ref(false);

const form = ref({
  message: "",
});

const rules = {
  message: [
    { required: true, message: "Please enter a message", trigger: "blur" },
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

    // TODO: Implement message sending logic
    await new Promise((resolve) => setTimeout(resolve, 1000));

    ElMessage.success("Message sent successfully");
    emit("message-sent");
    form.value.message = "";
  } catch (error) {
    console.error("Error sending message:", error);
    ElMessage.error("Failed to send message");
  } finally {
    loading.value = false;
  }
};
</script>
