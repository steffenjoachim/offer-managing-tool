<template>
  <div class="listing-detail-container">
    <div v-if="listing">
      <h2 class="listing-title-detail">{{ listing.titel }}</h2>

      <div class="content-container">
        <div class="image-section">
          <!-- Main Image (first image) -->
          <img
            v-if="listing.bilder && listing.bilder.length > 0"
            :src="listing.bilder[0].bild"
            alt="Main Listing Image"
            class="main-detail-image"
          />
          <!-- Placeholder if no images -->
          <img
            v-else
            src="/images/placeholder-image.svg"
            alt="No Image Available"
            class="main-detail-image"
          />
        </div>

        <div class="details-section">
          <div class="price-and-actions">
            <p class="listing-price-detail">€{{ listing.preis }}</p>
            <div class="action-buttons">
              <el-button type="primary">Send Message</el-button>
              <el-button>Add to Watchlist</el-button>
            </div>
          </div>

          <p class="listing-description">{{ listing.beschreibung }}</p>

          <!-- Additional Images Container -->
          <div
            class="additional-images-container"
            v-if="listing.bilder && listing.bilder.length > 1"
          >
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
            <!-- Navigation Arrows below images -->
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

export default {
  name: "ListingDetail",
  components: {
    ElButton,
  },
  setup() {
    const listing = ref(null);
    const route = useRoute();
    const listingId = route.params.id;
    const additionalImagesList = ref(null);
    const showScrollArrows = ref(false); // State to control arrow visibility

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
        const scrollAmount = 200; // Adjust scroll amount as needed
        if (direction === "left") {
          list.scrollLeft -= scrollAmount;
        } else if (direction === "right") {
          list.scrollLeft += scrollAmount;
        }
      }
    };

    onMounted(() => {
      fetchListing();
    });

    return {
      listing,
      additionalImagesList,
      showScrollArrows,
      scrollAdditionalImages,
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
  gap: 30px; /* Space between image section and details section */
  flex-wrap: wrap; /* Allow wrapping on smaller screens */
}

.image-section {
  flex: 1; /* Allow image section to grow */
  min-width: 300px; /* Minimum width to prevent shrinking too much */
}

.main-image-container {
  flex: 3; /* Main image takes more space */
  max-width: 600px;
}

.main-detail-image {
  width: 100%;
  height: auto;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.details-section {
  flex: 1; /* Allow details section to grow */
  min-width: 300px; /* Minimum width */
}

.price-and-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  flex-wrap: wrap; /* Allow buttons to wrap */
  gap: 10px; /* Add gap between wrapped items */
}

.listing-price-detail {
  font-size: 24px;
  font-weight: bold;
  color: #409eff;
  margin: 0;
}

.action-buttons {
  display: flex;
  gap: 10px; /* Consistent gap between buttons */
  flex-wrap: wrap; /* Allow buttons to wrap */
}

.action-buttons .el-button {
  margin-left: 0; /* Remove default margin */
  min-width: 120px; /* Ensure minimum width for buttons */
  height: 40px; /* Set consistent height */
  white-space: nowrap; /* Prevent text wrapping */
}

.listing-description {
  margin-top: 20px;
  margin-bottom: 20px;
  color: #555;
  line-height: 1.6;
  word-wrap: break-word; /* Added to prevent overflow */
}

.seller-info {
  margin-top: 20px; /* Add space above seller info */
}

.seller-info p {
  margin-bottom: 5px;
  color: #777;
  font-size: 14px;
}

.additional-images-container {
  margin-top: 20px; /* Add space above the thumbnail container */
  border: 1px solid #ddd; /* Add border to the container */
  border-radius: 8px; /* Match border radius with main image */
  padding: 10px; /* Add padding inside the border */
  /* Removed position: relative */
  display: flex; /* Use flexbox for column layout */
  flex-direction: column; /* Stack images and navigation vertically */
  align-items: center; /* Center items horizontally */
}

.additional-images-list {
  display: flex;
  flex-direction: row;
  gap: 10px;
  overflow-x: auto;
  overflow-y: hidden; /* Hide vertical scrollbar */
  /* Hide scrollbar for IE, Edge and Firefox */
  -ms-overflow-style: none; /* IE and Edge */
  scrollbar-width: none; /* Firefox */
  padding-bottom: 10px; /* Add padding for scrollbar space if needed */
  width: 100%; /* Ensure list takes full width for scrolling */
}

/* Hide scrollbar for Chrome, Safari and Opera */
.additional-images-list::-webkit-scrollbar {
  display: none;
}

.thumbnail-container {
  flex-shrink: 0; /* Prevent thumbnails from shrinking */
  width: 100px; /* Example thumbnail size */
  /* Removed individual border and padding */
  cursor: pointer;
}

.thumbnail-image {
  width: 100%; /* Thumbnails take full width of their container */
  height: auto;
  display: block;
  border-radius: 4px; /* Add border radius to images */
}

.image-navigation {
  display: flex;
  justify-content: center; /* Center arrows horizontally */
  width: 100%;
  margin-top: 10px; /* Space above navigation */
  gap: 20px; /* Space between arrows */
}

.image-nav-arrow {
  /* Removed absolute positioning */
  background-color: rgba(255, 255, 255, 0.7);
  border: 1px solid #ccc;
  border-radius: 50%;
  width: 25px; /* Smaller size */
  height: 25px; /* Smaller size */
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  user-select: none; /* Prevent text selection */
  z-index: 10; /* Ensure arrows are above images */
  font-size: 14px; /* Smaller font size */
  color: #333;
  transition: background-color 0.2s ease;
}

.image-nav-arrow:hover {
  background-color: rgba(255, 255, 255, 1);
}

/* Removed specific left/right positioning */

/* Responsive adjustments */
@media (max-width: 768px) {
  .content-container {
    flex-direction: column;
    gap: 20px;
  }

  .image-section {
    flex-direction: column;
  }

  .additional-images-container {
    margin-top: 20px; /* Keep margin on smaller screens */
    /* Adjust layout for stacking */
  }

  .additional-images-list {
    overflow-y: hidden;
    overflow-x: auto;
  }

  .thumbnail-container {
    width: 100px;
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
    width: 100%; /* Full width on small screens */
    margin-top: 10px; /* Add space between price and buttons */
  }

  .action-buttons .el-button {
    flex: 1; /* Equal width for buttons when stacked */
    min-width: 0; /* Allow buttons to shrink if needed */
  }
}
</style>
