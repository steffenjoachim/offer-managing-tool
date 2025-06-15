<template>
  <div class="listing-detail-container">
    <div v-if="listing" class="listing-content-wrapper">
      <h2 class="listing-title-detail">{{ listing.title }}</h2>

      <div class="main-content-area">
        <!-- Left Section: Main Image -->
        <div class="image-section">
          <img
            v-if="listing.images && listing.images.length > 0"
            :src="listing.images[0].bild"
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
            Description: {{ listing.description }}
          </p>

          <!-- Additional Images Container -->
          <div
            class="additional-images-container"
            v-if="listing.images && listing.images.length > 1"
          >
            <!-- Wrapper for overflow hidden -->
            <div class="additional-images-wrapper">
              <div class="additional-images-list" ref="additionalImagesList">
                <div
                  v-for="(image, index) in listing.images.slice(1)"
                  :key="index"
                  class="thumbnail-container"
                >
                  <img
                    :src="image.bild"
                    alt="Listing Thumbnail"
                    class="thumbnail-image"
                  />
                </div>
              </div>
            </div>
            <!-- Navigation Arrows -->
            <div class="image-navigation">
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
import { ref, onMounted, nextTick } from "vue";
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
          createdAt: response.data.erstellungsdatum || null, // HIER WURDE ES KORRIGIERT
          title: response.data.titel,
          description: response.data.beschreibung,
          price: response.data.preis,
          category: response.data.kategorie,
          images: response.data.bilder,
        };
        nextTick(() => {
          // Check if arrows are needed after images are rendered
          checkScrollArrowsNeeded();
        });
      } catch (error) {
        console.error("Error fetching listing details:", error);
        showError("Failed to load listing details.");
      }
    };

    // Helper function to format date
    const formatDate = (dateString) => {
      if (!dateString) return "N/A";
      const date = new Date(dateString);
      return isNaN(date.getTime()) ? "N/A" : date.toLocaleDateString();
    };

    // Function to check if scroll arrows are needed
    const checkScrollArrowsNeeded = () => {
      if (
        !additionalImagesList.value ||
        !listing.value ||
        !listing.value.images ||
        listing.value.images.length <= 1
      ) {
        showLeftArrow.value = false;
        showRightArrow.value = false;
        return;
      }

      const list = additionalImagesList.value;
      const scrollLeft = Math.round(list.scrollLeft);
      const scrollWidth = Math.round(list.scrollWidth);
      const clientWidth = Math.round(list.clientWidth);

      // Left arrow display, if scrollLeft is greater than 0.
      showLeftArrow.value = scrollLeft > 0;

      // Right arrow display, if scrollLeft is less than the maximum scroll position.
      const maxScrollLeft = scrollWidth - clientWidth;
      showRightArrow.value = scrollLeft < maxScrollLeft;
    };

    // Function to scroll the additional images list
    const scrollAdditionalImages = (direction) => {
      if (additionalImagesList.value) {
        const list = additionalImagesList.value;
        // Calculate scroll amount based on thumbnail width and margin
        const thumbnailElement = list.querySelector(".thumbnail-container");
        if (!thumbnailElement) return; // Should not happen if images are present

        const thumbnailWidth = thumbnailElement.offsetWidth; // includes padding and border if any
        const thumbnailMarginRight = parseInt(
          window.getComputedStyle(thumbnailElement).marginRight,
          10
        );

        const scrollAmount = thumbnailWidth + thumbnailMarginRight;

        if (direction === "left") {
          list.scrollLeft -= scrollAmount;
        } else if (direction === "right") {
          list.scrollLeft += scrollAmount;
        }

        // After scrolling, recheck arrow visibility
        nextTick(() => {
          checkScrollArrowsNeeded();
        });
      }
    };

    const toggleMessageForm = () => {
      showMessageForm.value = !showMessageForm.value;
    };

    const handleMessageSent = async (messageData) => {
      if (!listingId) {
        showError("No listing ID available");
        return;
      }

      try {
        await store.dispatch("messages/sendMessageToListing", {
          listingId: listingId,
          content: messageData.content,
        });
        showSuccess("Message sent successfully!");
        showMessageForm.value = false; // Close form after sending
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
  white-space: pre-wrap; /* Preserves whitespace and line breaks */
}

.additional-images-container {
  position: relative;
  width: 100%;
  margin-top: 20px;
  overflow: hidden; /* Hide scrollbar but allow scrolling */
  padding: 10px 0; /* Padding for arrows */
}

.additional-images-wrapper {
  overflow-x: auto; /* Enable horizontal scrolling */
  -webkit-overflow-scrolling: touch; /* Smooth scrolling on iOS */
  scrollbar-width: none; /* Hide scrollbar for Firefox */
  -ms-overflow-style: none; /* Hide scrollbar for IE/Edge */
}

.additional-images-wrapper::-webkit-scrollbar {
  display: none; /* Hide scrollbar for Chrome, Safari, Opera */
}

.additional-images-list {
  display: flex;
  gap: 15px;
  padding: 5px;
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

.image-navigation {
  position: absolute;
  top: 50%;
  width: 100%;
  display: flex;
  justify-content: space-between;
  transform: translateY(-50%);
  pointer-events: none; /* Allow clicks to pass through */
}

.image-nav-arrow {
  background-color: rgba(0, 0, 0, 0.5);
  color: white;
  padding: 10px 15px;
  border-radius: 50%;
  cursor: pointer;
  font-size: 1.5em;
  z-index: 10;
  pointer-events: all; /* Re-enable clicks for arrows */
  transition: background-color 0.2s ease;
}

.image-nav-arrow:hover {
  background-color: rgba(0, 0, 0, 0.7);
}

.image-nav-arrow.left {
  margin-left: -15px; /* Adjust positioning */
}

.image-nav-arrow.right {
  margin-right: -15px; /* Adjust positioning */
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
