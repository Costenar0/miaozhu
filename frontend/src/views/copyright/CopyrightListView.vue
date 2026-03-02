<template>
  <div class="copyright-list-view">
    <div style="display: flex; justify-content: space-between; align-items: center;">
      <h2>软著申请列表</h2>
      <el-button type="primary" @click="$router.push('/copyright/new')">新建申请</el-button>
    </div>
    <el-card style="margin-top: 20px;">
      <el-table v-if="list.length" :data="list" style="width: 100%;">
        <el-table-column prop="software_name" label="软件名称" min-width="180" />
        <el-table-column prop="software_version" label="版本号" width="100" />
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="statusTag(row.status)">{{ statusLabel(row.status) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="创建时间" width="180">
          <template #default="{ row }">
            {{ formatDate(row.created_at) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="150" fixed="right">
          <template #default="{ row }">
            <el-button link type="primary" size="small" @click="$router.push(`/copyright/${row.id}`)">查看</el-button>
            <el-button link type="danger" size="small" @click="handleDelete(row.id)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
      <el-empty v-else-if="!loading" description="暂无申请记录，点击上方按钮创建" />
      <el-pagination
        v-if="total > pageSize"
        style="margin-top: 16px; justify-content: flex-end;"
        background
        layout="total, prev, pager, next"
        :total="total"
        :page-size="pageSize"
        v-model:current-page="currentPage"
        @current-change="fetchList"
      />
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { applicationApi } from '@/api'
import type { ApplicationRecord } from '@/api/application'
import { formatDate } from '@/utils/format'

const list = ref<ApplicationRecord[]>([])
const loading = ref(false)
const currentPage = ref(1)
const pageSize = 20
const total = ref(0)

async function fetchList() {
  loading.value = true
  try {
    const res = await applicationApi.listApplications(currentPage.value, pageSize)
    list.value = res.data.items
    total.value = res.data.total
  } catch {
    // Error shown by global interceptor
  } finally {
    loading.value = false
  }
}

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

async function handleDelete(id: number) {
  try {
    await ElMessageBox.confirm('确定删除该申请？', '确认删除', { type: 'warning' })
    await applicationApi.deleteApplication(id)
    ElMessage.success('已删除')
    fetchList()
  } catch {
    // cancelled or error shown by interceptor
  }
}

onMounted(fetchList)
</script>
