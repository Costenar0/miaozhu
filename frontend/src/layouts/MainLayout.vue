<template>
  <el-container class="main-layout">
    <!-- Sidebar -->
    <el-aside :width="sidebarCollapsed ? '64px' : '240px'" class="sidebar">
      <div class="sidebar-header">
        <a v-if="!sidebarCollapsed" href="https://mz.skyler.uno" target="_blank" class="logo">秒著</a>
        <a v-else href="https://mz.skyler.uno" target="_blank" class="logo logo-mini">软</a>
      </div>

      <el-menu
        :default-active="route.path"
        :collapse="sidebarCollapsed"
        router
        class="sidebar-menu"
      >
        <el-menu-item index="/dashboard">
          <el-icon><DataBoard /></el-icon>
          <template #title>工作台</template>
        </el-menu-item>
        <el-menu-item index="/copyright">
          <el-icon><Document /></el-icon>
          <template #title>软著申请</template>
        </el-menu-item>
        <el-menu-item index="/tools">
          <el-icon><SetUp /></el-icon>
          <template #title>AI 工具</template>
        </el-menu-item>
        <el-menu-item index="/downloads">
          <el-icon><Download /></el-icon>
          <template #title>下载记录</template>
        </el-menu-item>
        <el-menu-item index="/docs">
          <el-icon><Reading /></el-icon>
          <template #title>使用文档</template>
        </el-menu-item>
        <el-menu-item index="/about">
          <el-icon><InfoFilled /></el-icon>
          <template #title>关于我们</template>
        </el-menu-item>
      </el-menu>
    </el-aside>

    <!-- Main content -->
    <el-container>
      <el-header class="main-header">
        <el-icon class="collapse-btn" @click="appStore.toggleSidebar">
          <Fold v-if="!sidebarCollapsed" />
          <Expand v-else />
        </el-icon>
        <el-breadcrumb separator="/">
          <el-breadcrumb-item :to="{ path: '/dashboard' }">首页</el-breadcrumb-item>
          <el-breadcrumb-item v-if="route.meta.title">
            {{ route.meta.title }}
          </el-breadcrumb-item>
        </el-breadcrumb>
      </el-header>

      <el-main class="main-content">
        <router-view />

        <footer class="app-footer">
          <p class="footer-contact">
            <span>邮箱：duhbbx@gmail.com</span>
            <span class="footer-sep">|</span>
            <span>微信：tuhoooo</span>
          </p>
        </footer>
      </el-main>
    </el-container>

    <DonationWidget />
  </el-container>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import {
  DataBoard,
  Document,
  SetUp,
  Fold,
  Expand,
  Download,
  Reading,
  InfoFilled,
} from '@element-plus/icons-vue'
import { useAppStore } from '@/stores/app'
import DonationWidget from '@/components/DonationWidget.vue'

const route = useRoute()
const appStore = useAppStore()

const sidebarCollapsed = computed(() => appStore.sidebarCollapsed)
</script>

<style scoped lang="scss">
.main-layout {
  height: 100vh;
}

.sidebar {
  background: $sidebar-bg;
  border-right: 1px solid $border-color;
  display: flex;
  flex-direction: column;
  transition: width 0.3s;
  overflow: hidden;
}

.sidebar-header {
  height: $header-height;
  display: flex;
  align-items: center;
  justify-content: center;
  border-bottom: 1px solid $border-color;
}

.logo {
  color: $primary-color;
  font-size: 20px;
  font-weight: bold;
  white-space: nowrap;
  text-decoration: none;

  &:hover {
    opacity: 0.8;
  }

  &.logo-mini {
    font-size: 24px;
  }
}

.sidebar-menu {
  flex: 1;
  border-right: none;
  background: transparent;
}

.main-header {
  display: flex;
  align-items: center;
  gap: 16px;
  border-bottom: 1px solid $border-color;
  background: #fff;
}

.collapse-btn {
  cursor: pointer;
  font-size: 20px;
  color: $text-regular;
}

.main-content {
  background: #f5f7fa;
  padding: $content-padding;
}

.app-footer {
  margin-top: 40px;
  padding: 20px 0;
  text-align: center;
  color: #909399;
  font-size: 13px;
  line-height: 1.8;
  border-top: 1px solid #e8e8e8;

  p {
    margin: 0;
  }
}

.footer-contact {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 4px;
  flex-wrap: wrap;
}

.footer-sep {
  color: #dcdfe6;
  margin: 0 4px;
}
</style>
