<el-form
  ref="formRef"
  :model="form"
  :rules="rules"
  label-position="top"
  class="listing-form"
>
  <el-form-item label="Title" prop="title">
    <el-input v-model="form.title" placeholder="Enter listing title" />
  </el-form-item>

  <el-form-item label="Description" prop="description">
    <el-input
      v-model="form.description"
      type="textarea"
      :rows="4"
      placeholder="Enter listing description"
    />
  </el-form-item>

  <el-form-item label="Price" prop="price">
    <el-input-number
      v-model="form.price"
      :min="0"
      :precision="2"
      :step="0.01"
      placeholder="Enter price"
    />
  </el-form-item>

  <el-form-item label="Category" prop="category">
    <el-select v-model="form.category" placeholder="Select category">
      <el-option
        v-for="category in categories"
        :key="category"
        :label="category"
        :value="category"
      />
    </el-select>
  </el-form-item>

  <el-form-item label="Images" prop="images">
    <el-upload
      v-model:file-list="fileList"
      action="#"
      :auto-upload="false"
      :on-change="handleFileChange"
      :on-remove="handleFileRemove"
      multiple
      list-type="picture-card"
    >
      <el-icon><Plus /></el-icon>
    </el-upload>
  </el-form-item>

  <el-form-item>
    <el-button type="primary" @click="submitForm">Submit</el-button>
    <el-button @click="resetForm">Reset</el-button>
  </el-form-item>
</el-form>

<script setup>
import { ref, defineProps, defineEmits } from "vue";
import { Plus } from "@element-plus/icons-vue";

const props = defineProps({
  initialData: {
    type: Object,
    default: () => ({
      title: "",
      description: "",
      price: 0,
      category: "",
      images: [],
    }),
  },
});

const emit = defineEmits(["submit", "reset"]);

const formRef = ref(null);
const fileList = ref([]);

const form = ref({
  title: props.initialData.title,
  description: props.initialData.description,
  price: props.initialData.price,
  category: props.initialData.category,
  images: props.initialData.images,
});

const categories = [
  "Electronics",
  "Fashion",
  "Home & Garden",
  "Sports",
  "Toys",
  "Books",
  "Other",
];

const rules = {
  title: [
    { required: true, message: "Please enter a title", trigger: "blur" },
    {
      min: 3,
      max: 100,
      message: "Length should be 3 to 100 characters",
      trigger: "blur",
    },
  ],
  description: [
    { required: true, message: "Please enter a description", trigger: "blur" },
    {
      min: 10,
      max: 1000,
      message: "Length should be 10 to 1000 characters",
      trigger: "blur",
    },
  ],
  price: [
    { required: true, message: "Please enter a price", trigger: "blur" },
    {
      type: "number",
      min: 0,
      message: "Price must be greater than 0",
      trigger: "blur",
    },
  ],
  category: [
    { required: true, message: "Please select a category", trigger: "change" },
  ],
  images: [
    {
      required: true,
      message: "Please upload at least one image",
      trigger: "change",
    },
  ],
};

const handleFileChange = (file) => {
  form.value.images.push(file.raw);
};

const handleFileRemove = (file) => {
  const index = form.value.images.indexOf(file.raw);
  if (index !== -1) {
    form.value.images.splice(index, 1);
  }
};

const submitForm = async () => {
  if (!formRef.value) return;

  await formRef.value.validate((valid) => {
    if (valid) {
      emit("submit", form.value);
    }
  });
};

const resetForm = () => {
  if (!formRef.value) return;

  formRef.value.resetFields();
  fileList.value = [];
  form.value.images = [];
  emit("reset");
};
</script>
