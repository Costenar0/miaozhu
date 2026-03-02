<template>
  <div class="download-records-view">
    <el-card>
      <template #header>
        <div style="display: flex; justify-content: space-between; align-items: center;">
          <span>下载记录</span>
          <el-button
            v-if="hasFailedTasks"
            size="small"
            type="danger"
            plain
            @click="handleCleanFailedTasks"
          >清理失败任务</el-button>
        </div>
      </template>
      <el-table :data="records" v-loading="loading" style="width: 100%;" empty-text="暂无导出记录">
        <el-table-column label="文件名" min-width="200">
          <template #default="{ row }">{{ row.file_name || formatExportFormat(row.format) }}</template>
        </el-table-column>
        <el-table-column label="格式" width="200">
          <template #default="{ row }">{{ formatExportFormat(row.format) }}</template>
        </el-table-column>
        <el-table-column label="状态" width="130">
          <template #default="{ row }">
            <el-tag size="small" :type="statusTag(row.status)">
              <span class="status-tag-inner">
                <el-icon v-if="row.status === 'processing'" class="is-loading"><Loading /></el-icon>
                <span>{{ statusLabel(row.status) }}</span>
              </span>
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="大小" width="100">
          <template #default="{ row }">{{ formatFileSize(row.file_size) }}</template>
        </el-table-column>
        <el-table-column label="创建时间" width="170">
          <template #default="{ row }">{{ formatDate(row.created_at) }}</template>
        </el-table-column>
        <el-table-column label="操作" width="130" align="center">
          <template #default="{ row }">
            <div style="display: flex; gap: 8px; justify-content: center;">
              <el-tooltip v-if="row.status === 'completed'" content="下载文件" placement="top">
                <el-button
                  link type="primary" size="small"
                  @click="handleDownload(row.id)"
                >下载</el-button>
              </el-tooltip>
              <el-tooltip v-else-if="row.status === 'failed'" :content="row.error_message || '导出失败'" placement="top">
                <el-button link type="danger" size="small">失败</el-button>
              </el-tooltip>
              <el-popconfirm
                title="确认删除此任务？"
                confirm-button-text="删除"
                cancel-button-text="取消"
                @confirm="handleDelete(row.id)"
              >
                <template #reference>
                  <el-button link type="danger" size="small">删除</el-button>
                </template>
              </el-popconfirm>
            </div>
          </template>
        </el-table-column>
      </el-table>
      <el-pagination
        v-if="total > pageSize"
        style="margin-top: 16px; justify-content: flex-end;"
        background
        layout="total, prev, pager, next"
        :total="total"
        :page-size="pageSize"
        v-model:current-page="currentPage"
        @current-change="fetchRecords"
      />
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Loading } from '@element-plus/icons-vue'
import { exportApi } from '@/api'
import type { ExportTaskRecord } from '@/api/export'
import { createSSE } from '@/utils/sse'
import { formatDate } from '@/utils/format'

const loading = ref(false)
const records = ref<ExportTaskRecord[]>([])
const currentPage = ref(1)
const pageSize = 20
const total = ref(0)
let sse: EventSource | null = null

const hasFailedTasks = computed(() => records.value.some(r => r.status === 'failed'))

function statusTag(s: string) {
  const map: Record<string, string> = { pending: 'info', processing: '', completed: 'success', failed: 'danger' }
  return (map[s] || 'info') as any
}

function statusLabel(s: string) {
  const map: Record<string, string> = { pending: '等待中', processing: '处理中', completed: '已完成', failed: '失败' }
  return map[s] || s
}

function formatExportFormat(f: string) {
  const map: Record<string, string> = {
    'manual-word': '文档鉴别材料（Word）',
    'manual-pdf': '文档鉴别材料（PDF）',
    'source-code-word': '源程序鉴别材料（Word）',
    'source-code-pdf': '源程序鉴别材料（PDF）',
    'all': '全部导出（ZIP）',
  }
  return map[f] || f
}

function formatFileSize(bytes: number | null) {
  if (!bytes) return '-'
  if (bytes < 1024) return bytes + ' B'
  if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB'
  return (bytes / (1024 * 1024)).toFixed(1) + ' MB'
}

async function fetchRecords() {
  try {
    const res = await exportApi.listExportTasks(currentPage.value, pageSize)
    records.value = res.data.items
    total.value = res.data.total
  } catch {
    // handled by interceptor
  }
}

async function handleDownload(taskId: number) {
  window.open(`/api/v1/export-tasks/${taskId}/download`, '_blank')
}

async function handleDelete(taskId: number) {
  try {
    await exportApi.deleteExportTask(taskId)
    ElMessage.success('删除成功')
    await fetchRecords()
  } catch {
    // handled by interceptor
  }
}

async function handleCleanFailedTasks() {
  try {
    await ElMessageBox.confirm('确认删除所有失败的任务？', '批量删除', {
      type: 'warning',
      confirmButtonText: '删除',
      cancelButtonText: '取消',
    })
    const res = await exportApi.deleteFailedExportTasks()
    ElMessage.success(res.data.message)
    await fetchRecords()
  } catch (e) {
    if (e !== 'cancel') {
      // handled by interceptor
    }
  }
}

function startSSE() {
  stopSSE()
  sse = createSSE('/export-tasks', {
    page: String(currentPage.value),
    page_size: String(pageSize),
  })
  sse.onmessage = (e) => {
    try {
      const data = JSON.parse(e.data)
      if (data.items) records.value = data.items
      if (data.total != null) total.value = data.total
      const hasPending = data.items?.some((i: any) => i.status === 'pending' || i.status === 'processing')
      if (!hasPending) stopSSE()
    } catch { /* ignore */ }
  }
  sse.onerror = () => {
    stopSSE()
  }
}

function stopSSE() {
  if (sse) {
    sse.close()
    sse = null
  }
}

onMounted(async () => {
  loading.value = true
  await fetchRecords()
  loading.value = false
  const hasPending = records.value.some(r => r.status === 'pending' || r.status === 'processing')
  if (hasPending) startSSE()
})

onUnmounted(() => {
  stopSSE()
})
</script>

<style scoped>
.download-records-view {
  max-width: 1200px;
}

.status-tag-inner {
  display: inline-flex;
  align-items: center;
  gap: 3px;
  white-space: nowrap;
}
</style>
