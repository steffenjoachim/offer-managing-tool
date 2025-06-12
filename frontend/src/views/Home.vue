<template>
  <div class="home-container">
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

export default {
  name: "HomePage",
  setup() {
    const store = useStore();
    const listings = ref([]);
    const router = useRouter();

    const handleImageError = (e) => {
      console.error("Image could not be loaded:", e);
      e.target.src = "/images/placeholder-image.svg";
    };

    const fetchListings = async () => {
      try {
        const response = await axios.get("http://localhost:8000/api/ads/");
        listings.value = response.data.map((listing) => ({
          ...listing,
          createdAt: listing.erstellungsdatum || null, // Map backend 'erstellungsdatum' to 'createdAt'
          title: listing.titel,
          price: listing.preis,
          images: listing.bilder,
          // Add other mappings if needed
        }));
      } catch (error) {
        console.error("Error fetching listings:", error);
      }
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
    };
  },
};
</script>

<style scoped>
.home-container {
  padding: 20px;
}

.section-title {
  margin-bottom: 24px;
  font-size: 24px;
  font-weight: 600;
  color: #303133;
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
