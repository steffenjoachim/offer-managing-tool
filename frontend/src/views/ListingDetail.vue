<template>
  <div class="listing-detail-container">
    <div v-if="listing" class="listing-content-wrapper">
      <h2 class="listing-title-detail">{{ listing.title }}</h2>

      <div class="main-content-area">
        <!-- Left Section: Main Image -->
        <div class="image-section">
          <img
            v-if="listing.images && listing.images.length > 0"
            :src="listing.images[0].image"
            alt="Main Listing Image"
            class="main-detail-image"
          />
          <img
            v-else
            src="/images/placeholder-image.svg"
            alt="No Image Available"
            class="main-detail-image"
          />
        </div>

        <!-- Right Section: Details -->
        <div class="details-section">
          <div class="price-and-actions">
            <p class="listing-price-detail">Price: € {{ listing.price }}</p>
          </div>

          <p class="listing-description">
            <span class="desc-label">Description:</span>
            {{ listing.description }}
          </p>

          <div class="seller-info">
            <p>Seller: {{ listing.user ? listing.user.username : "N/A" }}</p>
            <p
              v-if="listing.user && listing.user.date_joined"
              class="member-since-info"
            >
              Member since: {{ formatDate(listing.user.date_joined) }}
            </p>
            <p>
              Created at:
              {{ formatDate(listing.createdAt) }}
            </p>
          </div>
        </div>
      </div>

      <!-- Additional Images Section -->
      <div class="additional-images-section" v-if="additionalImages.length > 0">
        <div class="additional-images-wrapper" ref="additionalImagesList">
          <div class="additional-images-list">
            <div
              v-for="(image, index) in additionalImages"
              :key="index"
              class="thumbnail-container"
            >
              <img
                :src="image.image"
                alt="Listing Thumbnail"
                class="thumbnail-image"
              />
            </div>
          </div>
        </div>

        <!-- Navigation Arrows BELOW images -->
        <div class="image-navigation-controls">
          <div
            class="image-nav-arrow left"
            v-if="showLeftArrow"
            @click="scrollAdditionalImages('left')"
          >
            ❮
          </div>
          <div
            class="image-nav-arrow right"
            v-if="showRightArrow"
            @click="scrollAdditionalImages('right')"
          >
            ❯
          </div>
        </div>
      </div>

      <!-- Bottom Section: Message Form -->
      <div class="message-section">
        <div class="action-buttons">
          <el-button type="primary" @click="toggleMessageForm"
            >Send Message</el-button
          >
          <el-button @click="addToWatchlist">Add to Watchlist</el-button>
        </div>
        <MessageForm
          v-if="showMessageForm"
          :recipient="listing.user"
          @message-sent="handleMessageSent"
        />
      </div>
    </div>
    <div v-else class="loading-or-error">
      <p>Loading listing details...</p>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, nextTick, computed } from "vue";
import { useRoute } from "vue-router";
import axios from "axios";
import { ElButton, ElMessage } from "element-plus";
import MessageForm from "@/components/MessageForm.vue";
import { useStore } from "vuex";

export default {
  name: "ListingDetail",
  components: {
    ElButton,
    MessageForm,
  },
  setup() {
    const listing = ref(null);
    const route = useRoute();
    const listingId = route.params.id;
    const additionalImagesList = ref(null);
    const showLeftArrow = ref(false);
    const showRightArrow = ref(false);
    const showMessageForm = ref(false);
    const store = useStore();

    const showError = (message) => {
      try {
        ElMessage({
          message: message,
          type: "error",
          duration: 3000,
        });
      } catch (e) {
        console.error("Error showing message:", e);
      }
    };

    const showSuccess = (message) => {
      try {
        ElMessage({
          message: message,
          type: "success",
          duration: 3000,
        });
      } catch (e) {
        console.error("Error showing message:", e);
      }
    };

    const fetchListing = async () => {
      try {
        const response = await axios.get(
          `http://localhost:8000/api/listings/${listingId}/`
        );
        listing.value = {
          ...response.data,
          createdAt: response.data.created_at || null,
          title: response.data.title,
          description: response.data.description,
          price: response.data.price,
          category: response.data.category,
          images: response.data.images,
        };
        console.log("Fetched listing images:", listing.value.images); // Debug-Log
        nextTick(() => {
          checkScrollArrowsNeeded();
        });
      } catch (error) {
        console.error("Error fetching listing details:", error);
        showError("Failed to load listing details.");
      }
    };

    const formatDate = (dateString) => {
      if (!dateString) return "N/A";
      const date = new Date(dateString);
      return isNaN(date.getTime()) ? "N/A" : date.toLocaleDateString();
    };

    const checkScrollArrowsNeeded = () => {
      if (additionalImagesList.value) {
        const { scrollWidth, clientWidth } = additionalImagesList.value;
        showLeftArrow.value = additionalImagesList.value.scrollLeft > 0;
        showRightArrow.value = scrollWidth > clientWidth;
      }
    };

    const scrollAdditionalImages = (direction) => {
      const scrollAmount = 200; // Adjust as needed
      if (additionalImagesList.value) {
        if (direction === "left") {
          additionalImagesList.value.scrollLeft -= scrollAmount;
        } else {
          additionalImagesList.value.scrollLeft += scrollAmount;
        }
        nextTick(() => {
          checkScrollArrowsNeeded();
        });
      }
    };

    const toggleMessageForm = () => {
      showMessageForm.value = !showMessageForm.value;
    };

    const handleMessageSent = async (messageData) => {
      try {
        await store.dispatch("messages/sendMessageToListing", {
          listingId: listingId,
          content: messageData.content,
        });
        showSuccess("Message sent successfully!");
        showMessageForm.value = false;
      } catch (error) {
        console.error("Error sending message:", error);
        showError("Failed to send message.");
      }
    };

    const addToWatchlist = async () => {
      if (!listingId) {
        showError("No listing ID available.");
        return;
      }
      try {
        await store.dispatch("watchlist/addListingToWatchlist", listingId);
        showSuccess("Listing added to watchlist!");
      } catch (error) {
        console.error("Error adding to watchlist:", error);
        showError("Failed to add listing to watchlist or already added.");
      }
    };

    const additionalImages = computed(() => {
      if (
        listing.value &&
        Array.isArray(listing.value.images) &&
        listing.value.images.length > 1
      ) {
        return listing.value.images.slice(1);
      }
      return [];
    });

    onMounted(() => {
      fetchListing();
    });

    return {
      listing,
      additionalImagesList,
      showLeftArrow,
      showRightArrow,
      scrollAdditionalImages,
      formatDate,
      showMessageForm,
      toggleMessageForm,
      handleMessageSent,
      addToWatchlist,
      additionalImages,
    };
  },
};
</script>

<style scoped>
.listing-detail-container {
  max-width: 1200px;
  margin: 20px auto;
  padding: 20px;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.listing-title-detail {
  font-size: 2.5em;
  color: #333;
  margin-bottom: 20px;
  text-align: center;
}

.main-content-area {
  display: flex;
  flex-wrap: wrap; /* Allows wrapping on smaller screens */
  gap: 30px;
  margin-bottom: 30px;
}

.image-section {
  flex: 2; /* Takes more space */
  min-width: 300px; /* Minimum width before wrapping */
}

.main-detail-image {
  width: 100%;
  height: auto;
  max-height: 500px;
  object-fit: contain; /* Ensures the whole image is visible */
  border-radius: 6px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.details-section {
  flex: 1; /* Takes remaining space */
  min-width: 280px; /* Minimum width before wrapping */
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.price-and-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.listing-price-detail {
  font-size: 1.5rem;
  color: #409eff;
  font-weight: bold;
  margin: 0;
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

.seller-info {
  margin-top: 20px;
  border-top: 1px solid #eee;
  padding-top: 15px;
  font-size: 0.95em;
  color: #666;
}

.seller-info p {
  margin-bottom: 5px;
}

.member-since-info {
  font-size: 0.85em; /* Slightly smaller than seller info */
  margin-top: -3px; /* Move closer to seller info */
  margin-bottom: 8px; /* Maintain some spacing to next element */
  color: #777;
}

.additional-images-section {
  width: 100%;
  margin-top: 20px;
  display: flex;
  flex-direction: column; /* Stack image wrapper and controls vertically */
  align-items: center; /* Center the image wrapper and controls */
}

.additional-images-wrapper {
  overflow-x: auto; /* Enable horizontal scrolling */
  -webkit-overflow-scrolling: touch; /* Smooth scrolling on iOS */
  scrollbar-width: none; /* Hide scrollbar for Firefox */
  -ms-overflow-style: none; /* Hide scrollbar for IE/Edge */
  width: 100%; /* Ensure it takes full width for scrolling */
}

.additional-images-wrapper::-webkit-scrollbar {
  display: none; /* Hide scrollbar for Chrome, Safari, Opera */
}

.additional-images-list {
  display: flex;
  flex-wrap: nowrap; /* CRUCIAL: Prevent wrapping to enable horizontal scrolling */
  gap: 15px;
  padding: 5px; /* Keep padding for aesthetic around thumbnails */
  scroll-behavior: smooth; /* Smooth scroll on arrow click */
}

.thumbnail-container {
  flex: 0 0 auto; /* Prevent stretching */
  width: 100px;
  height: 100px;
  border-radius: 4px;
  overflow: hidden;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s ease;
}

.thumbnail-container:hover {
  transform: scale(1.05);
  cursor: pointer;
}

.thumbnail-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.image-navigation-controls {
  display: flex;
  justify-content: center; /* Center arrows below images */
  gap: 30px; /* Space between left and right arrows */
  margin-top: 15px; /* Space between images and arrows */
  width: 100%; /* Take full width to allow centering */
}

.image-nav-arrow {
  background-color: rgba(0, 0, 0, 0.5);
  color: white;
  padding: 10px 15px;
  border-radius: 50%;
  cursor: pointer;
  font-size: 1.5em;
  z-index: 10; /* Ensure arrows are above other content if overlapping */
  transition: background-color 0.2s ease;
  position: static; /* Reset from previous absolute positioning */
}

.message-section {
  margin-top: 30px;
  padding-top: 20px;
  border-top: 1px solid #eee;
}

.action-buttons {
  display: flex;
  gap: 15px;
  margin-bottom: 20px;
  justify-content: center;
}

.loading-or-error {
  text-align: center;
  padding: 50px;
  font-size: 1.2em;
  color: #888;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .main-content-area {
    flex-direction: column;
  }

  .image-section,
  .details-section {
    min-width: unset;
    width: 100%;
  }

  .listing-title-detail {
    font-size: 2em;
  }

  .listing-price-detail {
    font-size: 1.2rem;
  }

  .action-buttons {
    flex-direction: column;
  }
}
</style>
