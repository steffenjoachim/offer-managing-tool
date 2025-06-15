<template>
  <div class="home-container">
    <div class="search-container">
      <el-input
        v-model="searchQuery"
        placeholder="Search Listings for Products"
        class="search-input"
        @input="handleSearch"
        size="large"
      >
        <template #prefix>
          <el-icon><Search /></el-icon>
        </template>
      </el-input>
    </div>

    <h1 class="section-title">Recommended Listings for You:</h1>

    <el-row :gutter="10">
      <el-col
        v-for="listing in listings"
        :key="listing.id"
        :xs="12"
        :sm="8"
        :md="6"
        :lg="4"
      >
        <el-card
          class="listing-card"
          :body-style="{ padding: '0px' }"
          @click="goToListingDetail(listing.id)"
        >
          <img
            :src="
              Array.isArray(listing.images) && listing.images.length > 0
                ? listing.images[0].bild
                : typeof listing.images === 'string'
                ? listing.images
                : '/images/placeholder-image.svg'
            "
            class="listing-image"
            @error="handleImageError"
            alt="Listing Image"
          />
          <div class="listing-info">
            <h3 class="listing-title">{{ listing.title }}</h3>
            <p class="listing-price">€{{ listing.price }}</p>
            <p class="listing-date">
              Created at: {{ formatDate(listing.createdAt) }}
            </p>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import { ref, onMounted } from "vue";
import { useStore } from "vuex";
import { useRouter } from "vue-router";
import axios from "axios";
import { Search } from "@element-plus/icons-vue";

export default {
  name: "HomePage",
  components: {
    Search,
  },
  setup() {
    const store = useStore();
    const listings = ref([]);
    const router = useRouter();
    const searchQuery = ref("");
    const originalListings = ref([]);

    const handleImageError = (e) => {
      console.error("Image could not be loaded:", e);
      e.target.src = "/images/placeholder-image.svg";
    };

    const fetchListings = async () => {
      try {
        const response = await axios.get("http://localhost:8000/api/ads/");
        const mappedListings = response.data.map((listing) => ({
          ...listing,
          createdAt: listing.erstellungsdatum || null,
          title: listing.titel,
          price: listing.preis,
          images: listing.bilder,
        }));
        listings.value = mappedListings;
        originalListings.value = mappedListings;
      } catch (error) {
        console.error("Error fetching listings:", error);
      }
    };

    const handleSearch = () => {
      if (!searchQuery.value.trim()) {
        listings.value = originalListings.value;
        return;
      }

      const query = searchQuery.value.toLowerCase();
      listings.value = originalListings.value.filter(
        (listing) =>
          listing.title.toLowerCase().includes(query) ||
          (listing.beschreibung &&
            listing.beschreibung.toLowerCase().includes(query))
      );
    };

    const goToListingDetail = (id) => {
      router.push({ name: "ListingDetail", params: { id: id } });
    };

    // Helper function to format date
    const formatDate = (dateString) => {
      if (!dateString) return "N/A";
      const date = new Date(dateString);
      return isNaN(date.getTime()) ? "N/A" : date.toLocaleDateString();
    };

    onMounted(() => {
      fetchListings();
    });

    return {
      listings,
      handleImageError,
      goToListingDetail,
      formatDate,
      searchQuery,
      handleSearch,
    };
  },
};
</script>

<style scoped>
.home-container {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.search-container {
  margin-bottom: 32px;
}

.search-input {
  width: 100%;
  width: 700px !important;
  display: block;
  margin-left: 0;
  margin-right: auto;
}

.search-input :deep(.el-input__wrapper) {
  padding: 12px 16px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  border-radius: 8px;
  transition: all 0.3s ease;
  width: 250px
}

.search-input :deep(.el-input__wrapper:hover) {
  box-shadow: 0 4px 16px 0 rgba(0, 0, 0, 0.15);
}

.search-input :deep(.el-input__inner) {
  font-size: 16px;
  height: 24px;
  line-height: 24px;
}

.search-input :deep(.el-input__prefix) {
  font-size: 18px;
  color: #909399;
  margin-right: 8px;
}

.section-title {
  margin-bottom: 24px;
  font-size: 24px;
  font-weight: 600;
  color: #303133;
}

.el-row {
  margin: 0 -10px;
}

.el-col {
  padding: 0 10px;
}

.listing-card {
  margin-bottom: 10px;
  transition: transform 0.3s;
}

.listing-card:hover {
  transform: translateY(-5px);
}

.listing-image {
  width: 100%;
  height: 200px;
  object-fit: cover;
  object-position: 50% 30%;
}

.listing-info {
  padding: 14px;
}

.listing-title {
  margin: 0;
  font-size: 16px;
  font-weight: 500;
  color: #303133;
}

.listing-price {
  margin: 8px 0 0;
  font-size: 18px;
  font-weight: 600;
  color: #409eff;
}

.listing-date {
  margin: 5px 0 0;
  font-size: 12px;
  color: #666;
}
</style>
