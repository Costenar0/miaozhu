<template>
  <div class="copyright-new-view">
    <div class="page-header">
      <h2>新建软著申请</h2>
      <p class="page-desc">请填写软件的基本信息，未填写的可选项将由 AI 自动生成</p>
    </div>

    <el-form :model="form" label-width="130px" label-position="right" style="margin-top: 20px;">
      <!-- Required fields -->
      <el-card>
        <template #header>
          <span class="section-title">必填信息</span>
        </template>
        <el-row :gutter="24">
          <el-col :span="12">
            <el-form-item label="软件全称" required>
              <el-input v-model="form.software_name" placeholder="例如：企业管理系统软件" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="软件简称" required>
              <el-input v-model="form.software_short_name" placeholder="例如：企业管理系统" />
            </el-form-item>
          </el-col>
          <el-col :span="24">
            <el-form-item label="软件主要功能" required>
              <el-input v-model="form.main_features" type="textarea" :rows="4" placeholder="请描述软件的核心功能" />
            </el-form-item>
          </el-col>
        </el-row>
      </el-card>

      <!-- Optional fields in collapsible sections -->
      <el-collapse v-model="activeCollapse" style="margin-top: 20px;">
        <!-- Basic optional -->
        <el-collapse-item title="基本可选信息" name="basic">
          <div class="collapse-form">
            <el-row :gutter="24">
              <el-col :span="12">
                <el-form-item label="版本号">
                  <el-input v-model="form.software_version" placeholder="例如：V1.0" />
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item label="软件分类">
                  <el-select v-model="form.software_category" placeholder="请选择" style="width: 100%;">
                    <el-option label="应用软件" value="应用软件" />
                    <el-option label="系统软件" value="系统软件" />
                    <el-option label="嵌入式软件" value="嵌入式软件" />
                    <el-option label="中间件" value="中间件" />
                    <el-option label="游戏软件" value="游戏软件" />
                  </el-select>
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item label="运行平台">
                  <el-input v-model="form.runtime_platform" placeholder="例如：Windows、Linux、iOS 等" />
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item label="开发完成日期">
                  <el-date-picker v-model="form.completion_date" type="date" placeholder="选择日期" value-format="YYYY-MM-DD" style="width: 100%;" />
                </el-form-item>
              </el-col>
              <el-col :span="24">
                <el-form-item label="软件简介">
                  <el-input v-model="form.software_description" type="textarea" :rows="3" placeholder="简要描述软件的功能和特点..." />
                </el-form-item>
              </el-col>
            </el-row>
          </div>
        </el-collapse-item>

        <!-- Development info -->
        <el-collapse-item title="开发信息" name="dev">
          <div class="collapse-form">
            <el-row :gutter="24">
              <el-col :span="12">
                <el-form-item label="编程语言">
                  <el-select v-model="form.programming_languages" multiple placeholder="可多选" style="width: 100%;">
                    <el-option label="Java" value="Java" />
                    <el-option label="Python" value="Python" />
                    <el-option label="C/C++" value="C/C++" />
                    <el-option label="JavaScript" value="JavaScript" />
                    <el-option label="TypeScript" value="TypeScript" />
                    <el-option label="Go" value="Go" />
                    <el-option label="Rust" value="Rust" />
                    <el-option label="C#" value="C#" />
                    <el-option label="PHP" value="PHP" />
                    <el-option label="Swift" value="Swift" />
                    <el-option label="Kotlin" value="Kotlin" />
                    <el-option label="Ruby" value="Ruby" />
                  </el-select>
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item label="代码行数">
                  <el-input v-model="form.code_line_count" placeholder="例如：10000" type="number" />
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item label="开发方式">
                  <el-select v-model="form.development_method" placeholder="请选择" style="width: 100%;">
                    <el-option label="独立开发" value="独立开发" />
                    <el-option label="合作开发" value="合作开发" />
                    <el-option label="委托开发" value="委托开发" />
                  </el-select>
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item label="开发的硬件环境">
                  <el-input v-model="form.dev_hardware" placeholder="例如：PC/服务器" />
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item label="开发的操作系统">
                  <el-input v-model="form.dev_os" placeholder="例如：Windows 11、macOS" />
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item label="开发环境/工具">
                  <el-input v-model="form.dev_tools" placeholder="例如：VS Code、IntelliJ IDEA" />
                </el-form-item>
              </el-col>
            </el-row>
          </div>
        </el-collapse-item>

        <!-- Runtime info -->
        <el-collapse-item title="运行环境" name="runtime">
          <div class="collapse-form">
            <el-row :gutter="24">
              <el-col :span="12">
                <el-form-item label="运行的硬件环境">
                  <el-input v-model="form.runtime_hardware" placeholder="例如：PC/手机/服务器" />
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item label="运行支撑环境">
                  <el-input v-model="form.runtime_software" placeholder="例如：MySQL、Redis、Nginx" />
                </el-form-item>
              </el-col>
            </el-row>
          </div>
        </el-collapse-item>

        <!-- Technical features -->
        <el-collapse-item title="技术特点" name="tech">
          <div class="collapse-form">
            <el-row :gutter="24">
              <el-col :span="24">
                <el-form-item label="技术特点">
                  <el-checkbox-group v-model="form.tech_features_list">
                    <el-checkbox label="数据库技术" value="数据库技术" />
                    <el-checkbox label="网络技术" value="网络技术" />
                    <el-checkbox label="人工智能" value="人工智能" />
                    <el-checkbox label="安全技术" value="安全技术" />
                    <el-checkbox label="多媒体技术" value="多媒体技术" />
                    <el-checkbox label="面向对象技术" value="面向对象技术" />
                    <el-checkbox label="中间件技术" value="中间件技术" />
                    <el-checkbox label="云计算" value="云计算" />
                    <el-checkbox label="大数据" value="大数据" />
                  </el-checkbox-group>
                  <div v-if="form.tech_features_list.length > 3" class="field-tip warning">最多选择 3 项</div>
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item label="面向领域/行业">
                  <el-input v-model="form.target_industry" placeholder="例如：企业管理、电子商务" />
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item label="开发目的">
                  <el-input v-model="form.development_purpose" placeholder="例如：为了提高企业管理效率..." />
                </el-form-item>
              </el-col>
              <el-col :span="24">
                <el-form-item label="功能模块设计">
                  <el-input v-model="form.module_design" type="textarea" :rows="3" placeholder="描述主要功能模块..." />
                </el-form-item>
              </el-col>
            </el-row>
          </div>
        </el-collapse-item>

        <!-- Rights info -->
        <el-collapse-item title="权利信息" name="rights">
          <div class="collapse-form">
            <el-row :gutter="24">
              <el-col :span="12">
                <el-form-item label="软件作品说明">
                  <el-select v-model="form.work_type" placeholder="请选择" style="width: 100%;">
                    <el-option label="原创" value="原创" />
                    <el-option label="修改" value="修改" />
                    <el-option label="翻译" value="翻译" />
                    <el-option label="汇编" value="汇编" />
                  </el-select>
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item label="权利取得方式">
                  <el-select v-model="form.rights_acquisition" placeholder="请选择" style="width: 100%;">
                    <el-option label="原始取得" value="原始取得" />
                    <el-option label="继承取得" value="继承取得" />
                    <el-option label="受让取得" value="受让取得" />
                  </el-select>
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item label="权利范围">
                  <el-select v-model="form.rights_scope" placeholder="请选择" style="width: 100%;">
                    <el-option label="全部权利" value="全部权利" />
                    <el-option label="部分权利" value="部分权利" />
                  </el-select>
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item label="发表状态">
                  <el-select v-model="form.publish_status" placeholder="请选择" style="width: 100%;">
                    <el-option label="已发表" value="已发表" />
                    <el-option label="未发表" value="未发表" />
                  </el-select>
                </el-form-item>
              </el-col>
              <el-col v-if="form.publish_status === '已发表'" :span="12">
                <el-form-item label="首次发表日期">
                  <el-date-picker v-model="form.first_publish_date" type="date" placeholder="选择日期" value-format="YYYY-MM-DD" style="width: 100%;" />
                </el-form-item>
              </el-col>
              <el-col v-if="form.publish_status === '已发表'" :span="12">
                <el-form-item label="首次发表地点">
                  <el-input v-model="form.first_publish_location" placeholder="例如：中国北京市" />
                </el-form-item>
              </el-col>
            </el-row>
          </div>
        </el-collapse-item>
      </el-collapse>

      <!-- Actions -->
      <div class="form-actions">
        <el-button @click="$router.back()">取消</el-button>
        <el-button :loading="submitting" @click="handleSaveDraft">保存草稿</el-button>
        <el-button type="primary" :loading="submitting" @click="handleSubmit">提交申请</el-button>
      </div>
    </el-form>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { applicationApi } from '@/api'

const router = useRouter()
const activeCollapse = ref<string[]>([])
const submitting = ref(false)

const form = reactive({
  // Required
  software_name: '',
  software_short_name: '',
  main_features: '',
  // Basic optional
  software_version: '',
  software_category: '',
  runtime_platform: '',
  completion_date: '',
  software_description: '',
  // Dev info
  programming_languages: [] as string[],
  code_line_count: '',
  development_method: '',
  dev_hardware: '',
  dev_os: '',
  dev_tools: '',
  // Runtime
  runtime_hardware: '',
  runtime_software: '',
  // Tech
  tech_features_list: [] as string[],
  module_design: '',
  development_purpose: '',
  target_industry: '',
  // Rights
  work_type: '',
  rights_acquisition: '',
  rights_scope: '',
  publish_status: '',
  first_publish_date: '',
  first_publish_location: '',
})

function buildPayload() {
  const { programming_languages, tech_features_list, ...rest } = form
  return {
    ...rest,
    development_language: programming_languages.join(';') || undefined,
    technical_features: tech_features_list.join(';') || undefined,
  }
}

function validate(): boolean {
  if (!form.software_name.trim()) {
    ElMessage.warning('请输入软件全称')
    return false
  }
  if (!form.software_short_name.trim()) {
    ElMessage.warning('请输入软件简称')
    return false
  }
  if (!form.main_features.trim()) {
    ElMessage.warning('请描述软件主要功能')
    return false
  }
  if (form.tech_features_list.length > 3) {
    ElMessage.warning('技术特点最多选择 3 项')
    return false
  }
  return true
}

async function handleSaveDraft() {
  if (!form.software_name.trim()) {
    ElMessage.warning('至少填写软件全称')
    return
  }
  submitting.value = true
  try {
    await applicationApi.createApplication(buildPayload())
    ElMessage.success('草稿已保存')
    router.push('/copyright')
  } catch {
    // Error shown by global interceptor
  } finally {
    submitting.value = false
  }
}

async function handleSubmit() {
  if (!validate()) return
  submitting.value = true
  try {
    await applicationApi.createApplication(buildPayload())
    ElMessage.success('申请已提交')
    router.push('/copyright')
  } catch {
    // Error shown by global interceptor
  } finally {
    submitting.value = false
  }
}
</script>

<style scoped lang="scss">
.page-header {
  margin-bottom: 4px;
}

.page-desc {
  font-size: 14px;
  color: $text-secondary;
  margin-top: 8px;
}

.section-title {
  font-weight: 600;
}

.collapse-form {
  padding: 16px 0 0 0;
}

.field-tip {
  font-size: 12px;
  margin-top: 4px;

  &.warning {
    color: $danger-color;
  }
}

.form-actions {
  margin-top: 24px;
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  padding-bottom: 40px;
}

:deep(.el-collapse) {
  border: none;
}

:deep(.el-collapse-item__header) {
  font-size: 15px;
  font-weight: 600;
  background: #fff;
  padding: 0 20px;
  height: 52px;
  border-radius: $border-radius;
}

:deep(.el-collapse-item__wrap) {
  background: #fff;
  padding: 0 20px;
}

:deep(.el-collapse-item) {
  margin-bottom: 4px;
  border: 1px solid $border-color;
  border-radius: $border-radius;
  overflow: hidden;
}

:deep(.el-checkbox) {
  margin-bottom: 8px;
}
</style>
