<template>
  <div class="watchlist-container">
    <el-card class="watchlist-card">
      <template #header>
        <div class="card-header">
          <el-icon><Star /></el-icon>
          <span>My Watchlist</span>
        </div>
      </template>

      <div v-if="loading" class="loading-container">
        <el-skeleton :rows="3" animated />
      </div>

      <div v-else-if="error" class="error-container">
        <el-alert :title="error" type="error" :closable="false" show-icon />
      </div>

      <div v-else class="watchlist-content">
        <div v-if="watchlist.length === 0" class="no-items">
          <el-empty description="No items in watchlist, yet." />
        </div>

        <div v-else class="watchlist-items">
          <el-row :gutter="20">
            <el-col
              v-for="item in watchlist"
              :key="item.id"
              :xs="24"
              :sm="12"
              :md="8"
              :lg="6"
            >
              <el-card class="listing-card" shadow="hover">
                <img
                  v-if="item.images && item.images.length > 0"
                  :src="item.images[0].image"
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
                  <h3 class="listing-title">{{ item.title }}</h3>
                  <p class="listing-price">€{{ item.price }}</p>
                  <div class="listing-actions">
                    <el-button
                      type="primary"
                      size="small"
                      @click="viewListing(item.id)"
                    >
                      View
                    </el-button>
                    <el-button
                      type="danger"
                      size="small"
                      @click="removeFromWatchlist(item.id)"
                    >
                      Remove
                    </el-button>
                  </div>
                </div>
              </el-card>
            </el-col>
          </el-row>
        </div>
        <div class="watchlist-actions-bottom">
          <el-button type="primary" @click="navigateToHome">
            Go to Homepage
          </el-button>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import { useStore } from "vuex";
import { Star } from "@element-plus/icons-vue";
import { ElMessage } from "element-plus";
import axios from "axios";

export default {
  name: "WatchlistView",
  components: {
    Star,
  },
  setup() {
    const router = useRouter();
    const store = useStore();
    const loading = ref(true);
    const error = ref(null);
    const watchlist = ref([]);

    const fetchWatchlist = async () => {
      try {
        const response = await axios.get(
          "http://localhost:8000/api/watchlist/"
        );
        watchlist.value = response.data.map((listing) => ({
          ...listing,
          createdAt: listing.created_at || null,
          title: listing.title,
          description: listing.description,
          price: listing.price,
          category: listing.category,
          images: listing.images,
        }));
      } catch (error) {
        console.error("Error fetching watchlist:", error);
        showError("Failed to load your watchlist.");
      }
    };

    const viewListing = (id) => {
      router.push(`/listing/${id}`);
    };

    const removeFromWatchlist = async (id) => {
      try {
        await store.dispatch("watchlist/removeListingFromWatchlist", id);
        ElMessage.success("Item removed from watchlist");
        await fetchWatchlist();
      } catch (err) {
        ElMessage.error("Error removing item from watchlist");
        console.error("Error removing item from watchlist:", err);
      }
    };

    const navigateToHome = () => {
      router.push("/");
    };

    onMounted(() => {
      fetchWatchlist();
    });

    return {
      loading,
      error,
      watchlist,
      viewListing,
      removeFromWatchlist,
      navigateToHome,
    };
  },
};
</script>

<style scoped>
.watchlist-container {
  padding: 20px;
}

.watchlist-card {
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
.no-items {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 200px;
}

.watchlist-items {
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
  margin: 0 0 10px 0;
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

.listing-actions {
  display: flex;
  gap: 10px;
  margin-top: 10px;
}

.watchlist-actions-bottom {
  margin-top: 30px;
  text-align: center;
}
</style>
