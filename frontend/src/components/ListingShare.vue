    <div class="listing-share">
      <h3 class="title">Share Listing</h3>
      <div class="share-buttons">
        <el-button
          type="primary"
          plain
          @click="handleShare('facebook')"
        >
          Facebook
        </el-button>
        <el-button
          type="success"
          plain
          @click="handleShare('twitter')"
        >
          Twitter
        </el-button>
        <el-button
          type="info"
          plain
          @click="handleShare('linkedin')"
        >
          LinkedIn
        </el-button>
        <el-button
          type="warning"
          plain
          @click="handleShare('email')"
        >
          Email
        </el-button>
      </div>
    </div>

<script setup>
import { ElMessage } from "element-plus";

const props = defineProps({
  listingId: {
    type: Number,
    required: true,
  },
  title: {
    type: String,
    required: true,
  },
});

const handleShare = (platform) => {
  const url = `${window.location.origin}/listing/${props.listingId}`;
  const text = `Check out this listing: ${props.title}`;

  switch (platform) {
    case "facebook":
      window.open(`https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(url)}`);
      break;
    case "twitter":
      window.open(`https://twitter.com/intent/tweet?text=${encodeURIComponent(text)}&url=${encodeURIComponent(url)}`);
      break;
    case "linkedin":
      window.open(`https://www.linkedin.com/sharing/share-offsite/?url=${encodeURIComponent(url)}`);
      break;
    case "email":
      window.location.href = `mailto:?subject=${encodeURIComponent(text)}&body=${encodeURIComponent(url)}`;
      break;
  }

  ElMessage.success("Sharing options opened");
};
</script> 