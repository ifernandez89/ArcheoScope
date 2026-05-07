/** @type {import('next').NextConfig} */
const isProd = process.env.NODE_ENV === 'production';

// Bundle Analyzer (solo si está instalado)
let withBundleAnalyzer = (config) => config
try {
  if (process.env.ANALYZE === 'true') {
    withBundleAnalyzer = require('@next/bundle-analyzer')({
      enabled: true,
    })
  }
} catch (e) {
  console.log('ℹ️ @next/bundle-analyzer not installed. Run: npm install --save-dev @next/bundle-analyzer')
}

const nextConfig = {
  output: 'export',
  basePath: isProd ? '/ArcheoScope' : '',
  assetPrefix: isProd ? '/ArcheoScope' : '',
  reactStrictMode: true,
  images: {
    unoptimized: true,
  },
  
  // Eliminar console.log en producción automáticamente
  compiler: {
    removeConsole: isProd ? { exclude: ['error'] } : false,
  },
  
  // Optimizaciones de performance
  experimental: {
    optimizePackageImports: ['three', '@react-three/fiber', '@react-three/drei'],
  },
  
  webpack: (config, { isServer }) => {
    // Para manejar archivos .glb
    config.module.rules.push({
      test: /\.(glb|gltf)$/,
      type: 'asset/resource',
    });
    
    // Optimizaciones de bundle
    if (!isServer) {
      config.optimization = {
        ...config.optimization,
        splitChunks: {
          chunks: 'all',
          cacheGroups: {
            // Three.js en chunk separado
            three: {
              test: /[\\/]node_modules[\\/](three)[\\/]/,
              name: 'three',
              priority: 10,
            },
            // React Three Fiber en chunk separado
            r3f: {
              test: /[\\/]node_modules[\\/](@react-three)[\\/]/,
              name: 'react-three',
              priority: 9,
            },
            // Engines en chunk separado
            engines: {
              test: /[\\/]engines[\\/]/,
              name: 'engines',
              priority: 8,
            },
            // Vendors comunes
            vendor: {
              test: /[\\/]node_modules[\\/]/,
              name: 'vendor',
              priority: 5,
            },
          },
        },
      };
    }
    
    return config;
  },
};

module.exports = withBundleAnalyzer(nextConfig);

