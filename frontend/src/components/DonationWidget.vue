<template>
  <div v-if="!dismissed" class="donation-widget">
    <!-- Floating trigger -->
    <div class="donation-trigger" @click="visible = !visible">
      <span class="trigger-icon">&#9749;</span>
      <span v-if="!visible" class="trigger-label">请我喝杯咖啡</span>
    </div>

    <!-- Popup -->
    <transition name="donation-slide">
      <div v-if="visible" class="donation-panel">
        <div class="panel-header">
          <span>请我喝杯美式深烘吧</span>
          <el-icon class="close-btn" @click="visible = false"><Close /></el-icon>
        </div>
        <div class="panel-body">
          <el-image src="/wechat-pay.jpg" alt="微信收款码" class="qr-image" :preview-src-list="['/wechat-pay.jpg']" fit="contain" preview-teleported />
        </div>
        <div class="panel-footer">
          <el-button size="small" text @click="handleDismiss">不再显示</el-button>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { Close } from '@element-plus/icons-vue'

const STORAGE_KEY = 'donation_dismissed'

const visible = ref(false)
const dismissed = ref(false)

onMounted(() => {
  dismissed.value = localStorage.getItem(STORAGE_KEY) === '1'
})

function handleDismiss() {
  localStorage.setItem(STORAGE_KEY, '1')
  dismissed.value = true
  visible.value = false
}
</script>

<style scoped lang="scss">
.donation-widget {
  position: fixed;
  left: 24px;
  bottom: 24px;
  z-index: 2000;
}

.donation-trigger {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 14px;
  background: #ff9500;
  color: #fff;
  border-radius: 20px;
  cursor: pointer;
  box-shadow: 0 4px 12px rgba(255, 149, 0, 0.4);
  transition: all 0.3s;
  user-select: none;
  font-size: 13px;

  &:hover {
    box-shadow: 0 6px 20px rgba(255, 149, 0, 0.5);
    transform: translateY(-2px);
  }
}

.trigger-icon {
  font-size: 18px;
  line-height: 1;
}

.trigger-label {
  font-weight: 500;
  white-space: nowrap;
}

.donation-panel {
  position: absolute;
  left: 0;
  bottom: 48px;
  width: 280px;
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.12);
  overflow: hidden;
}

.panel-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 16px;
  font-size: 15px;
  font-weight: 600;
  color: #303133;
  border-bottom: 1px solid #f0f0f0;
}

.close-btn {
  cursor: pointer;
  color: #909399;
  font-size: 16px;
  transition: color 0.2s;

  &:hover {
    color: #303133;
  }
}

.panel-body {
  padding: 16px;
  display: flex;
  justify-content: center;
}

.qr-image {
  width: 200px;
  height: 200px;
  object-fit: contain;
  border-radius: 8px;
}

.panel-footer {
  padding: 0 16px 12px;
  display: flex;
  justify-content: center;
}

// Transition
.donation-slide-enter-active,
.donation-slide-leave-active {
  transition: all 0.25s ease;
}

.donation-slide-enter-from,
.donation-slide-leave-to {
  opacity: 0;
  transform: translateY(12px);
}
</style>
