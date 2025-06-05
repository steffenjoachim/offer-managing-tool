<template>
  <div class="listing-detail-container">
    <div v-if="listing">
      <h2 class="listing-title-detail">{{ listing.titel }}</h2>

      <div class="content-container">
        <!-- Left Section: Main Image -->
        <div class="image-section">
          <img
            v-if="listing.bilder && listing.bilder.length > 0"
            :src="listing.bilder[0].bild"
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
            <p class="listing-price-detail">€{{ listing.preis }}</p>
          </div>

          <p class="listing-description">{{ listing.beschreibung }}</p>

          <!-- Additional Images Container -->
          <div
            class="additional-images-container"
            v-if="listing.bilder && listing.bilder.length > 1"
          >
            <!-- Wrapper for overflow hidden -->
            <div class="additional-images-wrapper">
              <div class="additional-images-list" ref="additionalImagesList">
                <div
                  v-for="(image, index) in listing.bilder.slice(1)"
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
            <div class="image-navigation" v-if="showScrollArrows">
              <div
                class="image-nav-arrow left"
                @click="scrollAdditionalImages('left')"
              >
                ❮
              </div>
              <div
                class="image-nav-arrow right"
                @click="scrollAdditionalImages('right')"
              >
                ❯
              </div>
            </div>
          </div>

          <div class="seller-info">
            <p>Seller: {{ listing.user }}</p>
            <p>
              Created:
              {{ new Date(listing.erstellungsdatum).toLocaleDateString() }}
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
          <el-button>Add to Watchlist</el-button>
        </div>
        <MessageForm
          v-if="showMessageForm"
          :recipient="listing.user"
          @message-sent="handleMessageSent"
        />
      </div>
    </div>
    <div v-else>
      <p>Loading listing details...</p>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, nextTick } from "vue";
import { useRoute } from "vue-router";
import axios from "axios";
import { ElButton } from "element-plus";
import MessageForm from "@/components/MessageForm.vue";

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
    const showScrollArrows = ref(false); // State to control arrow visibility
    const showMessageForm = ref(false);

    const fetchListing = async () => {
      try {
        const response = await axios.get(
          `http://localhost:8000/api/listings/${listingId}/`
        );
        listing.value = response.data;
        nextTick(() => {
          // Check if arrows are needed after images are rendered
          checkScrollArrowsNeeded();
        });
      } catch (error) {
        console.error("Error fetching listing details:", error);
      }
    };

    // Function to check if scroll arrows are needed
    const checkScrollArrowsNeeded = () => {
      if (additionalImagesList.value) {
        const list = additionalImagesList.value;
        // Check if the content width is greater than the container width
        if (list.scrollWidth > list.clientWidth) {
          showScrollArrows.value = true;
        } else {
          showScrollArrows.value = false;
        }
      }
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
      }
    };

    const toggleMessageForm = () => {
      showMessageForm.value = !showMessageForm.value;
    };

    const handleMessageSent = async (messageData) => {
      // console.log("Message Data:", {
      //   sender: "current_user", // This will be replaced with actual user data
      //   recipient: listing.value.user,
      //   content: messageData.content,
      //   timestamp: new Date().toISOString(),
      //   listingId: listingId,
      //   listingTitle: listing.value.titel,
      // });

      try {
        const response = await axios.post(
          "http://localhost:8000/api/messages/messages/send_message/",
          {
            listingId: listingId,
            content: messageData.content,
            // recipient wird im Backend basierend auf listingId ermittelt
          }
        );
        console.log("Message sent successfully:", response.data);
        // Optional: Erfolgsmeldung anzeigen
        // ElMessage.success("Nachricht erfolgreich gesendet!"); // Benötigt ElMessage Import
      } catch (error) {
        console.error("Error sending message:", error);
        // Optional: Fehlermeldung anzeigen
        // ElMessage.error("Fehler beim Senden der Nachricht."); // Benötigt ElMessage Import
      }

      showMessageForm.value = false;
    };

    onMounted(() => {
      fetchListing();
    });

    return {
      listing,
      additionalImagesList,
      showScrollArrows,
      scrollAdditionalImages,
      showMessageForm,
      toggleMessageForm,
      handleMessageSent,
    };
  },
};
</script>

<style scoped>
.listing-detail-container {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.listing-title-detail {
  margin-bottom: 20px;
  font-size: 28px;
  color: #333;
}

.content-container {
  display: flex;
  gap: 30px;
  margin-bottom: 30px;
}

.image-section {
  flex: 1;
  min-width: 300px;
}

.details-section {
  flex: 1;
  min-width: 300px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.message-section {
  width: 100%;
  margin-top: 20px;
  padding: 20px;
  border-top: 1px solid #eee;
}

.action-buttons {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
  justify-content: center;
}

.action-buttons .el-button {
  margin-left: 0;
  min-width: 120px;
  height: 40px;
  white-space: nowrap;
}

.main-detail-image {
  width: 100%;
  height: auto;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.listing-price-detail {
  font-size: 24px;
  font-weight: bold;
  color: #409eff;
  margin: 0;
}

.listing-description {
  margin: 0;
  color: #555;
  line-height: 1.6;
  word-wrap: break-word;
}

.seller-info {
  margin: 0;
}

.seller-info p {
  margin-bottom: 5px;
  color: #777;
  font-size: 14px;
}

.additional-images-container {
  margin: 0;
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 10px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.additional-images-wrapper {
  overflow: hidden;
  width: 100%;
}

.additional-images-list {
  display: flex;
  flex-direction: row;
  gap: 10px;
  overflow-y: hidden;
  -ms-overflow-style: none;
  scrollbar-width: none;
  padding-bottom: 10px;
  width: 100%;
}

.additional-images-list::-webkit-scrollbar {
  display: none;
}

.thumbnail-container {
  flex-shrink: 0;
  width: 100px;
  cursor: pointer;
  margin-right: 15px;
  display: inline-block;
}

.thumbnail-image {
  width: 100%;
  height: auto;
  display: block;
  border-radius: 4px;
}

.image-navigation {
  display: flex;
  justify-content: center;
  width: 100%;
  margin-top: 10px;
  gap: 20px;
}

.image-nav-arrow {
  background-color: rgba(255, 255, 255, 0.7);
  border: 1px solid #ccc;
  border-radius: 50%;
  width: 25px;
  height: 25px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  user-select: none;
  z-index: 10;
  font-size: 14px;
  color: #333;
  transition: background-color 0.2s ease;
}

.image-nav-arrow:hover {
  background-color: rgba(255, 255, 255, 1);
}

@media (max-width: 768px) {
  .content-container {
    flex-direction: column;
    gap: 20px;
  }

  .image-section {
    flex-direction: column;
  }

  .additional-images-container {
    margin-top: 20px;
  }

  .additional-images-list {
    overflow-y: hidden;
    gap: 15px;
  }

  .thumbnail-container {
    width: 100px;
    margin-right: 50px;
  }

  .thumbnail-image {
    width: auto;
    height: 100px;
  }
}

@media (max-width: 850px) {
  .price-and-actions {
    flex-direction: column;
    align-items: flex-start;
  }

  .action-buttons {
    width: 100%;
    margin-top: 10px;
  }

  .action-buttons .el-button {
    flex: 1;
    min-width: 0;
  }
}
</style>
