<template>
  <div class="create-listing-container">
    <el-card class="create-listing-card">
      <template #header>
        <div class="card-header">
          <el-icon><Plus /></el-icon>
          <span>Create New Listing</span>
        </div>
      </template>

      <el-form
        ref="formRef"
        :model="form"
        :rules="rules"
        label-position="top"
        @submit.prevent="handleSubmit"
      >
        <el-form-item label="Title" prop="titel">
          <el-input v-model="form.titel" placeholder="Enter listing title" />
        </el-form-item>

        <el-form-item label="Description" prop="beschreibung">
          <el-input
            v-model="form.beschreibung"
            type="textarea"
            :rows="4"
            placeholder="Describe your item"
          />
        </el-form-item>

        <el-form-item label="Price" prop="preis">
          <el-input-number
            v-model="form.preis"
            :min="0"
            :precision="2"
            :step="0.01"
            placeholder="Enter price"
          />
        </el-form-item>

        <el-form-item label="Category" prop="kategorie">
          <el-select v-model="form.kategorie" placeholder="Select category">
            <el-option label="Electronics" value="electronics" />
            <el-option label="Furniture" value="furniture" />
            <el-option label="Clothing" value="clothing" />
            <el-option label="Books" value="books" />
            <el-option label="Other" value="other" />
          </el-select>
        </el-form-item>

        <el-form-item label="Images" prop="bilder">
          <el-upload
            v-model:file-list="fileList"
            action="#"
            list-type="picture-card"
            :auto-upload="false"
            :on-change="handleFileChange"
            multiple
          >
            <el-icon><Plus /></el-icon>
          </el-upload>
        </el-form-item>

        <el-form-item>
          <el-button type="primary" native-type="submit" :loading="loading">
            Create Listing
          </el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script>
import { ref, reactive } from "vue";
import { useStore } from "vuex";
import { useRouter } from "vue-router";
import { ElMessage } from "element-plus";
import { Plus } from "@element-plus/icons-vue";

export default {
  name: "CreateListing",
  components: {
    Plus,
  },
  setup() {
    const store = useStore();
    const router = useRouter();
    const formRef = ref(null);
    const loading = ref(false);
    const fileList = ref([]);

    const form = reactive({
      titel: "",
      beschreibung: "",
      preis: 0,
      kategorie: "",
      bilder: [],
    });

    const rules = {
      titel: [
        { required: true, message: "Please enter a title", trigger: "blur" },
        {
          min: 3,
          max: 200,
          message: "Length should be 3 to 200 characters",
          trigger: "blur",
        },
      ],
      beschreibung: [
        {
          required: true,
          message: "Please enter a description",
          trigger: "blur",
        },
      ],
      preis: [
        { required: true, message: "Please enter a price", trigger: "blur" },
      ],
      kategorie: [
        {
          required: true,
          message: "Please select a category",
          trigger: "change",
        },
      ],
    };

    const handleFileChange = (file) => {
      form.bilder.push(file.raw);
    };

    const handleSubmit = async () => {
      if (!formRef.value) return;

      try {
        await formRef.value.validate();
        loading.value = true;

        const formData = new FormData();
        formData.append("titel", form.titel);
        formData.append("beschreibung", form.beschreibung);
        formData.append("preis", form.preis);
        formData.append("kategorie", form.kategorie);
        form.bilder.forEach((file) => {
          formData.append("bilder", file);
        });

        await store.dispatch("listings/createListing", formData);
        ElMessage.success("Listing created successfully!");
        router.push("/");
      } catch (error) {
        console.error("Error creating listing:", error);
        ElMessage.error(
          error.response?.data?.detail || "Failed to create listing"
        );
      } finally {
        loading.value = false;
      }
    };

    return {
      formRef,
      form,
      rules,
      loading,
      fileList,
      handleFileChange,
      handleSubmit,
    };
  },
};
</script>

<style scoped>
.create-listing-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.create-listing-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  align-items: center;
  gap: 8px;
}

.el-upload--picture-card {
  width: 148px;
  height: 148px;
  line-height: 146px;
}
</style>
