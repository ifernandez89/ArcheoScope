/**
 * Get the correct asset path considering basePath in production
 */
export function getAssetPath(path: string): string {
  // Use basePath in production (GitHub Pages)
  const basePath = process.env.NODE_ENV === 'production' ? '/ArcheoScope' : '';
  
  // Ensure path starts with /
  const normalizedPath = path.startsWith('/') ? path : `/${path}`;
  
  return `${basePath}${normalizedPath}`;
}
