import { createRouter, createWebHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    redirect: '/dashboard',
  },
  {
    path: '/',
    component: () => import('@/layouts/MainLayout.vue'),
    children: [
      {
        path: 'dashboard',
        name: 'Dashboard',
        component: () => import('@/views/dashboard/DashboardView.vue'),
        meta: { title: '工作台' },
      },
      {
        path: 'copyright',
        name: 'CopyrightList',
        component: () => import('@/views/copyright/CopyrightListView.vue'),
        meta: { title: '软著申请' },
      },
      {
        path: 'copyright/new',
        name: 'CopyrightNew',
        component: () => import('@/views/copyright/CopyrightNewView.vue'),
        meta: { title: '新建申请' },
      },
      {
        path: 'copyright/:id',
        name: 'CopyrightGenerate',
        component: () => import('@/views/copyright/CopyrightGenerateView.vue'),
        meta: { title: 'AI 生成' },
      },
      {
        path: 'copyright/:id/edit',
        name: 'CopyrightEdit',
        component: () => import('@/views/copyright/CopyrightEditView.vue'),
        meta: { title: '编辑申请信息' },
      },
      {
        path: 'tools',
        name: 'Tools',
        component: () => import('@/views/tools/ToolsView.vue'),
        meta: { title: 'AI 工具' },
      },
      {
        path: 'downloads',
        name: 'Downloads',
        component: () => import('@/views/downloads/DownloadRecordsView.vue'),
        meta: { title: '下载记录' },
      },
      {
        path: 'docs',
        name: 'Docs',
        component: () => import('@/views/docs/DocsView.vue'),
        meta: { title: '使用文档' },
      },
      {
        path: 'about',
        name: 'About',
        component: () => import('@/views/about/AboutView.vue'),
        meta: { title: '关于我们' },
      },
    ],
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
