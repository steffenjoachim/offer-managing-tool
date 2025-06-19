<template>
  <div class="content-wrapper">
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

    <div class="listings-container">
      <el-row :gutter="10" justify="center">
        <el-col
          v-for="listing in listings"
          :key="listing.id"
          :xs="24"
          :sm="12"
          :md="8"
          :lg="6"
        >
          <el-card
            class="listing-card"
            :body-style="{ padding: '0px' }"
            @click="goToListingDetail(listing.id)"
          >
            <img
              :src="
                Array.isArray(listing.images) && listing.images.length > 0
                  ? listing.images[0].image
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
                Created at: {{ formatDate(listing.created_at) }}
              </p>
              <p class="listing-description">
                <span class="desc-label">Description:</span>
                {{ listing.description }}
              </p>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from "vue";
import { useStore } from "vuex";
import { useRouter } from "vue-router";
import axios from "axios";
import { Search } from "@element-plus/icons-vue";

const VALIDITY_DAYS = 3; // For testing, listings are valid for 3 days

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
    const loading = ref(false);
    const error = ref(null);

    const handleImageError = (e) => {
      console.error("Image could not be loaded:", e);
      e.target.src = "/images/placeholder-image.svg";
    };

    const fetchListings = async () => {
      try {
        loading.value = true;
        error.value = null;
        const response = await axios.get("http://localhost:8000/api/listings/");
        listings.value = response.data.results.map((listing) => ({
          ...listing,
          created_at: listing.created_at || null,
          title: listing.title,
          description: listing.description,
          price: listing.price,
          category: listing.category,
          images: listing.images,
        }));
        // Filter out listings without creation date
        listings.value = listings.value.filter((listing) => listing.created_at);
        // Filter out expired listings
        listings.value = listings.value.filter(
          (listing) => !isExpired(listing)
        );
      } catch (err) {
        console.error("Error fetching listings:", err);
        error.value = "Failed to load listings";
      } finally {
        loading.value = false;
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
          (listing.description &&
            listing.description.toLowerCase().includes(query))
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

    const isExpired = (listing) => {
      if (!listing.created_at) return true;
      const createdDate = new Date(listing.created_at);
      const expirationDate = new Date(createdDate);
      expirationDate.setDate(createdDate.getDate() + VALIDITY_DAYS);
      const now = new Date();
      return expirationDate.getTime() < now.getTime();
    };

    onMounted(() => {
      fetchListings();
    });

    return {
      listings,
      searchQuery,
      handleSearch,
      loading,
      error,
      formatDate,
      handleImageError,
      goToListingDetail,
    };
  },
};
</script>

<style scoped>
.content-wrapper {
  max-width: 900px;
  margin: 0 auto;
  padding: 20px;
  box-sizing: border-box;
}

.search-container {
  margin-bottom: 30px;
  max-width: 600px;
  margin-left: auto;
  margin-right: auto;
}

.search-input {
  width: 100%;
}

.section-title {
  text-align: center;
  margin-bottom: 30px;
  color: #333;
  font-size: 24px;
}

.listings-container {
  width: 100%;
  margin: 0 auto;
}

.listings-container .el-row {
  row-gap: 16px;
}

.listing-card {
  margin-bottom: 20px;
  cursor: pointer;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  height: 100%;
}

.listing-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.listing-image {
  width: 100%;
  height: 200px;
  object-fit: cover;
  border-radius: 4px 4px 0 0;
}

.listing-info {
  padding: 15px;
}

.listing-title {
  margin: 0;
  font-size: 16px;
  font-weight: bold;
  color: #333;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.listing-price {
  margin: 8px 0;
  font-size: 18px;
  color: #409eff;
  font-weight: bold;
}

.listing-date {
  margin: 0;
  font-size: 12px;
  color: #999;
}

.listing-description {
  font-size: 1.1em;
  color: #555;
  line-height: 1.6;
  white-space: pre-line;
  margin: 0;
}

.desc-label {
  display: inline-block;
  min-width: 100px;
  font-weight: 500;
  color: #222;
}

@media (max-width: 1024px) {
  /* Abstand wird jetzt über :gutter im el-row gesetzt */
}
@media (max-width: 768px) {
  /* Abstand wird jetzt über :gutter im el-row gesetzt */
}
</style>
