<template>
  <div class="dashboard-view">
    <div class="dashboard-header">
      <h2>工作台</h2>
      <el-button type="primary" @click="$router.push('/copyright/new')">
        <el-icon style="margin-right: 6px;"><Plus /></el-icon>新建申请
      </el-button>
    </div>

    <el-row :gutter="20" style="margin-top: 20px;">
      <el-col :span="8">
        <el-card shadow="hover">
          <template #header>申请总数</template>
          <div class="stat-value">{{ stats.total_applications }}</div>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card shadow="hover">
          <template #header>草稿中</template>
          <div class="stat-value">{{ stats.draft_count }}</div>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card shadow="hover">
          <template #header>已完成</template>
          <div class="stat-value">{{ stats.completed_count }}</div>
        </el-card>
      </el-col>
    </el-row>

    <el-card style="margin-top: 20px;">
      <template #header>最近申请</template>
      <el-table v-if="recentList.length" :data="recentList" style="width: 100%;">
        <el-table-column prop="software_name" label="软件名称" min-width="180" />
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="statusTag(row.status)" size="small">{{ statusLabel(row.status) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="创建时间" width="180">
          <template #default="{ row }">
            {{ formatDate(row.created_at) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="100">
          <template #default="{ row }">
            <el-button link type="primary" size="small" @click="$router.push(`/copyright/${row.id}`)">查看</el-button>
          </template>
        </el-table-column>
      </el-table>
      <el-empty v-else description="暂无申请记录" />
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { Plus } from '@element-plus/icons-vue'
import { client } from '@/api'
import { formatDate } from '@/utils/format'

const stats = reactive({
  total_applications: 0,
  draft_count: 0,
  completed_count: 0,
})

const recentList = ref<any[]>([])

function statusLabel(s: string) {
  const map: Record<string, string> = {
    draft: '草稿',
    generating: '生成中',
    generated: '已生成',
    ready: '可导出',
    submitted: '已提交',
    approved: '已通过',
    rejected: '已驳回',
    archived: '已归档',
    completed: '已完成',
  }
  return map[s] || s
}

function statusTag(s: string) {
  const map: Record<string, string> = {
    draft: 'info',
    generating: '',
    generated: 'success',
    ready: 'success',
    submitted: 'warning',
    approved: 'success',
    rejected: 'danger',
    archived: 'info',
    completed: 'success',
  }
  return (map[s] || '') as any
}

onMounted(async () => {
  try {
    const [statsRes, recentRes] = await Promise.all([
      client.get('/dashboard/stats'),
      client.get('/dashboard/recent'),
    ])
    Object.assign(stats, statsRes.data)
    recentList.value = recentRes.data
  } catch {
    // handled by interceptor
  }
})
</script>

<style scoped lang="scss">
.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.stat-value {
  font-size: 32px;
  font-weight: bold;
  color: $primary-color;
  text-align: center;
}
</style>
