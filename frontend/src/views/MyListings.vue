<template>
  <div class="my-listings-container">
    <el-card class="my-listings-card">
      <template #header>
        <div class="card-header">
          <el-icon><Tickets /></el-icon>
          <span>My Listings</span>
        </div>
      </template>

      <div v-if="loading" class="loading-container">
        <el-skeleton :rows="3" animated />
      </div>

      <div v-else-if="error" class="error-container">
        <el-alert :title="error" type="error" :closable="false" show-icon />
      </div>

      <div v-else class="my-listings-content">
        <div v-if="listings && listings.length === 0" class="no-listings">
          <el-empty description="You haven't created any listings yet." />
          <el-button type="primary" @click="navigateToCreateListing">
            Create a new listing
          </el-button>
        </div>

        <div v-else-if="listings && listings.length > 0" class="listings-grid">
          <el-row :gutter="20">
            <el-col
              v-for="listing in listings"
              :key="listing.id"
              :xs="24"
              :sm="12"
              :md="8"
              :lg="6"
            >
              <el-card class="listing-card" shadow="hover">
                <img
                  v-if="listing.images && listing.images.length > 0"
                  :src="listing.images[0].bild"
                  class="listing-image"
                  alt="Listing Image"
                />
                <img
                  v-else
                  src="/images/placeholder-image.svg"
                  class="listing-image"
                  alt="No Image Available"
                />
                <div class="listing-info">
                  <h3 class="listing-title">{{ listing.title }}</h3>
                  <p class="listing-price">€{{ listing.price }}</p>
                  <p class="listing-date">
                    Created at:
                    {{ formatDate(listing.createdAt) }}
                  </p>
                  <p class="listing-validity">
                    Validity: {{ getValidityStatus(listing.createdAt) }}
                  </p>
                  <div class="listing-actions">
                    <el-button
                      type="primary"
                      size="small"
                      @click="viewListing(listing.id)"
                    >
                      View
                    </el-button>
                    <el-button
                      type="danger"
                      size="small"
                      @click="deleteListing(listing.id)"
                    >
                      Delete
                    </el-button>
                  </div>
                </div>
              </el-card>
            </el-col>
          </el-row>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script>
import { ref, watch } from "vue";
import { useRouter } from "vue-router";
import { useStore } from "vuex";
import axios from "axios";
import { Tickets } from "@element-plus/icons-vue";
import { ElMessage, ElMessageBox } from "element-plus";

const VALIDITY_DAYS = 3; // For testing, listings are valid for 3 days

export default {
  name: "MyListings",
  components: {
    Tickets,
  },
  setup() {
    const router = useRouter();
    const store = useStore();
    const loading = ref(true);
    const error = ref(null);
    const listings = ref([]);

    const fetchMyListings = async (userId) => {
      try {
        loading.value = true;
        error.value = null; // Clear any previous errors
        if (!userId) {
          loading.value = false;
          return;
        }
        const response = await axios.get(
          `http://localhost:8000/api/listings/?user_id=${userId}`
        );
        const now = new Date();
        listings.value = response.data
          .map((listing) => ({
            ...listing,
            createdAt: listing.erstellungsdatum || null, // Map backend 'erstellungsdatum' to 'createdAt'
            title: listing.titel,
            price: listing.preis,
            images: listing.bilder,
          }))
          .filter((listing) => {
            if (!listing.createdAt) return false; // Listings without a creation date are invalid
            const createdDate = new Date(listing.createdAt);
            const expirationDate = new Date(createdDate);
            expirationDate.setDate(createdDate.getDate() + VALIDITY_DAYS);
            return expirationDate.getTime() > now.getTime(); // Keep only listings that have not expired
          });
        console.log("MyListings: Fetched listing data:", listings.value);
      } catch (err) {
        error.value = err.message || "Error loading your listings";
        console.error("Error loading my listings:", err);
        ElMessage.error(error.value);
      } finally {
        loading.value = false;
      }
    };

    // Helper function to format date
    const formatDate = (dateString) => {
      if (!dateString) return "N/A";
      const date = new Date(dateString);
      return isNaN(date.getTime()) ? "N/A" : date.toLocaleDateString();
    };

    // Helper function to get validity status
    const getValidityStatus = (createdAtString) => {
      if (!createdAtString) return "N/A";

      // Setze die Zeit auf Mitternacht für beide Daten
      const createdDate = new Date(createdAtString);
      createdDate.setHours(0, 0, 0, 0);

      const now = new Date();
      now.setHours(0, 0, 0, 0);

      const expirationDate = new Date(createdDate);
      expirationDate.setDate(createdDate.getDate() + VALIDITY_DAYS);

      // Berechne die Differenz in Tagen
      const diffTime = expirationDate.getTime() - now.getTime();
      const diffDays = Math.floor(diffTime / (1000 * 60 * 60 * 24));

      if (diffDays > 0) {
        return `Expires in ${diffDays} day${diffDays === 1 ? "" : "s"}`;
      } else if (diffDays === 0) {
        return "Expires today";
      } else {
        return `Expired ${Math.abs(diffDays)} day${
          Math.abs(diffDays) === 1 ? "" : "s"
        } ago`;
      }
    };

    // Watch for changes in the authenticated user object
    watch(
      () => store.getters["auth/currentUser"],
      (currentUser) => {
        if (currentUser && currentUser.id) {
          fetchMyListings(currentUser.id); // Pass userId directly
        } else {
          // User is not logged in or user data is not complete
          listings.value = [];
          error.value = "User not logged in or user ID not available.";
          loading.value = false;
        }
      },
      { immediate: true } // Run immediately on component mount
    );

    const viewListing = (id) => {
      router.push(`/listing/${id}`);
    };

    const deleteListing = async (id) => {
      try {
        await ElMessageBox.confirm(
          "This will permanently delete the listing. Continue?",
          "Warning",
          {
            confirmButtonText: "OK",
            cancelButtonText: "Cancel",
            type: "warning",
          }
        );
        await axios.delete(`http://localhost:8000/api/listings/${id}/`);
        ElMessage.success("Listing deleted successfully");
        await fetchMyListings(store.getters["auth/currentUser"]?.id); // Refresh with current userId
      } catch (err) {
        if (err !== "cancel") {
          // User cancelled the deletion
          ElMessage.error("Error deleting listing");
          console.error("Error deleting listing:", err);
        }
      }
    };

    const navigateToCreateListing = () => {
      router.push("/create-listing");
    };

    return {
      loading,
      error,
      listings,
      viewListing,
      deleteListing,
      navigateToCreateListing,
      formatDate,
      getValidityStatus,
    };
  },
};
</script>

<style scoped>
.my-listings-container {
  padding: 20px;
}

.my-listings-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 20px;
  font-weight: bold;
}

.loading-container,
.error-container,
.no-listings {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  min-height: 200px;
}

.no-listings .el-button {
  margin-top: 20px;
}

.listings-grid {
  margin-top: 20px;
}

.listing-card {
  margin-bottom: 20px;
  transition: transform 0.2s;
}

.listing-card:hover {
  transform: translateY(-5px);
}

.listing-image {
  width: 100%;
  height: 200px;
  object-fit: cover;
  border-radius: 4px;
}

.listing-info {
  padding: 10px 0;
}

.listing-title {
  margin: 0;
  font-size: 16px;
  font-weight: bold;
  color: #333;
}

.listing-price {
  margin: 0 0 10px 0;
  font-size: 18px;
  color: #409eff;
  font-weight: bold;
}

.listing-date {
  margin: 5px 0 0;
  font-size: 12px;
  color: #666;
}

.listing-validity {
  margin: 5px 0 0;
  font-size: 14px;
  color: #606266;
}

.listing-actions {
  display: flex;
  gap: 10px;
  margin-top: 10px;
}
</style>
