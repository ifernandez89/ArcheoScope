/**
 * Get the correct asset path considering basePath in production
 */
export function getAssetPath(path: string): string {
  // In production, prepend the basePath
  const basePath = process.env.NODE_ENV === 'production' ? '/ArcheoScope' : '';
  
  // Ensure path starts with /
  const normalizedPath = path.startsWith('/') ? path : `/${path}`;
  
  return `${basePath}${normalizedPath}`;
}
