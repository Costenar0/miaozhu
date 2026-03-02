import client from './client'

export interface ApplicationPayload {
  software_name: string
  software_short_name: string
  main_features: string
  software_version?: string
  software_category?: string
  runtime_platform?: string
  completion_date?: string
  software_description?: string
  development_language?: string
  code_line_count?: string
  development_method?: string
  dev_hardware?: string
  dev_os?: string
  dev_tools?: string
  runtime_hardware?: string
  runtime_software?: string
  technical_features?: string
  module_design?: string
  development_purpose?: string
  target_industry?: string
  work_type?: string
  rights_acquisition?: string
  rights_scope?: string
  publish_status?: string
  first_publish_date?: string
  first_publish_location?: string
  generate_source_code?: boolean
  generate_db_design?: boolean
  generate_diagrams?: boolean
}

export const ApplicationStatus = {
  DRAFT: 'draft',
  GENERATING: 'generating',
  GENERATED: 'generated',
  READY: 'ready',
  SUBMITTED: 'submitted',
  APPROVED: 'approved',
  REJECTED: 'rejected',
  ARCHIVED: 'archived',
} as const
export type ApplicationStatus = typeof ApplicationStatus[keyof typeof ApplicationStatus]

export interface ApplicationRecord extends ApplicationPayload {
  id: number
  status: ApplicationStatus | string
  generate_source_code: boolean
  generate_db_design: boolean
  generate_diagrams: boolean
  created_at: string
  updated_at: string
  applicant_name?: string
  applicant_type?: string
  nationality?: string
  province?: string
  city?: string
}

export function createApplication(data: ApplicationPayload) {
  return client.post<ApplicationRecord>('/applications', data)
}

export interface PaginatedResult<T> {
  items: T[]
  total: number
}

export function listApplications(page = 1, pageSize = 20) {
  return client.get<PaginatedResult<ApplicationRecord>>('/applications', { params: { page, page_size: pageSize } })
}

export function getApplication(id: number) {
  return client.get<ApplicationRecord>(`/applications/${id}`)
}

export function updateApplication(id: number, data: Partial<ApplicationPayload>) {
  return client.put<ApplicationRecord>(`/applications/${id}`, data)
}

export function deleteApplication(id: number) {
  return client.delete(`/applications/${id}`)
}

export interface StatusTransitionRequest {
  target_status: ApplicationStatus
  comment?: string
}

export function transitionApplicationStatus(id: number, data: StatusTransitionRequest) {
  return client.post<ApplicationRecord>(`/applications/${id}/status`, data)
}

export interface StatusFlowNode {
  label: string
  targets: Array<{ value: string; label: string }>
}

export function getStatusFlow() {
  return client.get<Record<string, StatusFlowNode>>('/applications/status/flow')
}
