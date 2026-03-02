import client from './client'

export interface GenerateRequest {
  extra_prompt?: string
}

export interface TaskUpdateRequest {
  extra_prompt?: string
}

export interface RegenerateRequest {
  extra_prompt?: string
}

export interface SectionUpdateRequest {
  content: string
}

export interface SectionRecord {
  id: number
  task_id: number
  section_key: string
  title: string
  content: string | null
  section_order: number
  status: string
  error_message: string | null
  created_at: string
  updated_at: string
}

export interface TaskRecord {
  id: number
  application_id: number
  status: string
  extra_prompt: string | null
  generate_source_code: boolean
  generate_db_design: boolean
  total_sections: number
  completed_sections: number
  created_at: string
  updated_at: string
  sections: SectionRecord[]
}

export function startGeneration(appId: number, data: GenerateRequest = {}) {
  return client.post<TaskRecord>(`/applications/${appId}/generate`, data)
}

export function getGeneration(appId: number) {
  return client.get<TaskRecord>(`/applications/${appId}/generation`)
}

export function updateTask(appId: number, data: TaskUpdateRequest) {
  return client.put<TaskRecord>(`/applications/${appId}/generation`, data)
}

export function updateSection(sectionId: number, data: SectionUpdateRequest) {
  return client.put<SectionRecord>(`/generation-sections/${sectionId}`, data)
}

export function regenerateSection(sectionId: number, data: RegenerateRequest = {}) {
  return client.post<SectionRecord>(`/generation-sections/${sectionId}/regenerate`, data)
}

export function generateDiagrams(appId: number) {
  return client.post<TaskRecord>(`/applications/${appId}/generate-diagrams`)
}

const EXPORT_TIMEOUT = 300_000 // 5 minutes for document generation

export function exportManualWord(appId: number) {
  return client.get(`/applications/${appId}/export/manual/word`, { responseType: 'blob', timeout: EXPORT_TIMEOUT })
}

export function exportManualPdf(appId: number) {
  return client.get(`/applications/${appId}/export/manual/pdf`, { responseType: 'blob', timeout: EXPORT_TIMEOUT })
}

export function exportSourceCodeWord(appId: number) {
  return client.get(`/applications/${appId}/export/source-code/word`, { responseType: 'blob', timeout: EXPORT_TIMEOUT })
}

export function exportSourceCodePdf(appId: number) {
  return client.get(`/applications/${appId}/export/source-code/pdf`, { responseType: 'blob', timeout: EXPORT_TIMEOUT })
}

export function exportWord(appId: number) {
  return client.get(`/applications/${appId}/export/word`, { responseType: 'blob', timeout: EXPORT_TIMEOUT })
}

export function exportPdf(appId: number) {
  return client.get(`/applications/${appId}/export/pdf`, { responseType: 'blob', timeout: EXPORT_TIMEOUT })
}
