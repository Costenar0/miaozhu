<template>
  <div class="about-page">
    <el-card shadow="never" class="about-card">
      <template #header>
        <span class="card-title">关于我们</span>
      </template>

      <div class="about-section">
        <h3>秒著 - AI 软著材料生成工具</h3>
        <p>这是一个开源的单机版工具，开箱即用，无需部署数据库和 Redis，完全免费，随便使用。</p>
        <p>如果觉得好用，欢迎 Star 和分享给更多人。</p>
      </div>

      <el-divider />

      <div class="about-section">
        <h3>联系作者</h3>
        <el-descriptions :column="1" border>
          <el-descriptions-item label="邮箱">duhbbx@gmail.com</el-descriptions-item>
          <el-descriptions-item label="微信">tuhoooo</el-descriptions-item>
        </el-descriptions>
      </div>

      <el-divider />

      <div class="about-section">
        <h3>项目合作</h3>
        <p>如果您有合作意向，欢迎通过邮箱或微信联系我，可以提供丰厚的分成。</p>
      </div>
    </el-card>
  </div>
</template>

<style scoped lang="scss">
.about-page {
  max-width: 640px;
}

.about-card {
  border-radius: 8px;
}

.card-title {
  font-size: 18px;
  font-weight: 600;
}

.about-section {
  h3 {
    margin: 0 0 12px;
    font-size: 15px;
    color: #303133;
  }

  p {
    margin: 0 0 8px;
    color: #606266;
    font-size: 14px;
    line-height: 1.8;

    &:last-child {
      margin-bottom: 0;
    }
  }
}
</style>
