/**
 * Get the correct asset path considering basePath in production
 */
export function getAssetPath(path: string): string {
  // Only use basePath when deploying to GitHub Pages
  const basePath = process.env.NEXT_PUBLIC_GITHUB_PAGES === 'true' ? '/ArcheoScope' : '';
  
  // Ensure path starts with /
  const normalizedPath = path.startsWith('/') ? path : `/${path}`;
  
  return `${basePath}${normalizedPath}`;
}
