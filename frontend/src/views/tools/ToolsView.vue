<template>
  <div class="tools-view">
    <h2>AI 工具</h2>
    <el-row :gutter="20" style="margin-top: 20px;">
      <el-col :span="8">
        <el-card shadow="hover" class="tool-card">
          <h3>源代码生成</h3>
          <p>AI 自动生成符合要求的源代码文档</p>
          <el-button type="primary" size="small" disabled>即将上线</el-button>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card shadow="hover" class="tool-card">
          <h3>操作手册生成</h3>
          <p>AI 自动生成软件操作说明书</p>
          <el-button type="primary" size="small" disabled>即将上线</el-button>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card shadow="hover" class="tool-card">
          <h3>功能描述优化</h3>
          <p>AI 优化软件功能描述文案</p>
          <el-button type="primary" size="small" disabled>即将上线</el-button>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<style scoped lang="scss">
.tool-card {
  text-align: center;

  h3 {
    margin-bottom: 8px;
    color: $text-primary;
  }

  p {
    font-size: 14px;
    color: $text-secondary;
    margin-bottom: 16px;
  }
}
</style>
