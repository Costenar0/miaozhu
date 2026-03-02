/**
 * 创建 SSE 连接
 * @param path SSE 路径，如 "/generation/123" 或 "/export-tasks"
 * @param params 额外 query 参数
 */
export function createSSE(
  path: string,
  params?: Record<string, string | number>,
): EventSource {
  const url = new URL(`/api/v1/sse${path}`, window.location.origin)
  if (params) {
    for (const [k, v] of Object.entries(params)) {
      url.searchParams.set(k, String(v))
    }
  }

  return new EventSource(url.toString())
}
