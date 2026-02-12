/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'export',
  basePath: '/ArcheoScope',
  assetPrefix: '/ArcheoScope/',
  reactStrictMode: true,
  images: {
    unoptimized: true,
  },
  webpack: (config) => {
    // Para manejar archivos .glb
    config.module.rules.push({
      test: /\.(glb|gltf)$/,
      type: 'asset/resource',
    });
    return config;
  },
};

module.exports = nextConfig;
