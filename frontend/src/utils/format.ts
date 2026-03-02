/**
 * 将后端返回的 UTC 时间字符串格式化为本地时间
 * 后端数据库存储 UTC 时间，但返回的字符串不带时区后缀，
 * 需要手动追加 'Z' 让浏览器正确识别为 UTC 再转为本地时区。
 */
export function formatDate(d: string): string {
  const utc = d.endsWith('Z') ? d : d + 'Z'
  return new Date(utc).toLocaleString('zh-CN')
}
