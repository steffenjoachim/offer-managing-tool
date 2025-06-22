<template>
  <div class="edit-listing-container">
    <el-card class="edit-listing-card">
      <template #header>
        <div class="card-header">
          <el-icon><Edit /></el-icon>
          <span>Edit Listing</span>
        </div>
      </template>
      <el-form
        ref="formRef"
        :model="form"
        :rules="rules"
        label-position="top"
        @submit.prevent="handleSubmit"
      >
        <el-form-item label="Title" prop="title">
          <el-input v-model="form.title" placeholder="Enter listing title" />
        </el-form-item>
        <el-form-item label="Description" prop="description">
          <el-input
            v-model="form.description"
            type="textarea"
            :rows="4"
            placeholder="Describe your item"
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
            <el-option label="Electronics" value="electronics" />
            <el-option label="Fashion" value="fashion" />
            <el-option label="Home & Garden" value="home" />
            <el-option label="Sports & Leisure" value="sports" />
            <el-option label="Toys & Games" value="toys" />
            <el-option label="Other" value="other" />
          </el-select>
        </el-form-item>
        <el-form-item label="Images">
          <el-upload
            :file-list="fileList"
            action="#"
            list-type="picture-card"
            :auto-upload="false"
            :on-change="handleFileChange"
            multiple
          >
            <el-icon><Edit /></el-icon>
          </el-upload>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" native-type="submit" :loading="loading">
            Save Changes
          </el-button>
          <el-button @click="goBack">Cancel</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script>
import { ref, reactive, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import { ElMessage } from "element-plus";
import { Edit } from "@element-plus/icons-vue";
import axios from "axios";

export default {
  name: "EditListing",
  components: {
    Edit,
  },
  setup() {
    const route = useRoute();
    const router = useRouter();
    const formRef = ref(null);
    const loading = ref(false);
    const fileList = ref([]);
    const listingId = route.params.id;

    const form = reactive({
      title: "",
      description: "",
      price: 0,
      category: "",
      images: [],
    });

    const rules = {
      title: [
        { required: true, message: "Please enter a title", trigger: "blur" },
        {
          min: 3,
          max: 200,
          message: "Length should be 3 to 200 characters",
          trigger: "blur",
        },
      ],
      description: [
        {
          required: true,
          message: "Please enter a description",
          trigger: "blur",
        },
      ],
      price: [
        { required: true, message: "Please enter a price", trigger: "blur" },
      ],
      category: [
        {
          required: true,
          message: "Please select a category",
          trigger: "change",
        },
      ],
    };

    const fetchListing = async () => {
      try {
        loading.value = true;
        const response = await axios.get(
          `http://localhost:8000/api/listings/${listingId}/`
        );
        Object.assign(form, {
          title: response.data.title,
          description: response.data.description,
          price: response.data.price,
          category: response.data.category,
          images: response.data.images || [],
        });
        // Bilder für Upload-Komponente vorbereiten
        fileList.value = (response.data.images || []).map((img, idx) => ({
          name: `Image ${idx + 1}`,
          url: img.image,
        }));
      } catch (error) {
        ElMessage.error("Failed to load listing data");
      } finally {
        loading.value = false;
      }
    };

    onMounted(() => {
      fetchListing();
    });

    const handleFileChange = (file) => {
      form.images.push(file.raw);
    };

    const handleSubmit = async () => {
      if (!formRef.value) return;
      try {
        await formRef.value.validate();
        loading.value = true;
        const formData = new FormData();
        formData.append("title", form.title);
        formData.append("description", form.description);
        formData.append("price", form.price);
        formData.append("category", form.category);
        form.images.forEach((file) => {
          formData.append("images", file);
        });
        await axios.patch(
          `http://localhost:8000/api/listings/${listingId}/`,
          formData,
          {
            headers: {
              "Content-Type": "multipart/form-data",
            },
          }
        );
        ElMessage.success("Listing updated successfully!");
        router.push("/my-listings");
      } catch (error) {
        ElMessage.error(
          error.response?.data?.detail || "Failed to update listing"
        );
      } finally {
        loading.value = false;
      }
    };

    const goBack = () => {
      router.push("/my-listings");
    };

    return {
      formRef,
      form,
      rules,
      loading,
      fileList,
      handleFileChange,
      handleSubmit,
      goBack,
    };
  },
};
</script>

<style scoped>
.edit-listing-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.edit-listing-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  align-items: center;
  gap: 8px;
}
</style>
