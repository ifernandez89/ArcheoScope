/** @type {import('next').NextConfig} */
const isProd = process.env.NODE_ENV === 'production';
const isItch = process.env.NEXT_PUBLIC_DEPLOY_TARGET === 'itch' || process.env.DEPLOY_TARGET === 'itch';

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
  basePath: (isProd && !isItch) ? '/ArcheoScope' : '',
  assetPrefix: (isProd && !isItch) ? '/ArcheoScope' : '',
  reactStrictMode: true,
  images: {
    unoptimized: true,
  },
  
  // Eliminar console.log en producción automáticamente
  compiler: {
    removeConsole: isProd ? { exclude: ['error'] } : false,
  },
  
  // Optimizaciones de performance
  transpilePackages: ['three', '@react-three/fiber', '@react-three/drei', 'scheduler'],
  experimental: {
    optimizePackageImports: ['three'],
  },
  
  webpack: (config, { isServer }) => {
    // Para manejar archivos .glb
    config.module.rules.push({
      test: /\.(glb|gltf)$/,
      type: 'asset/resource',
    });
    
    // FIX CRÍTICO: React Three Fiber + Next.js 14 scheduler resolution
    // El problema: R3F intenta importar 'scheduler' dinámicamente pero webpack
    // no puede resolver la importación en runtime
    // Solución: Agregar scheduler como alias en cliente Y servidor
    
    // Alias para scheduler (requerido por R3F) - aplicar en ambos lados
    config.resolve.alias = {
      ...config.resolve.alias,
      scheduler: require.resolve('scheduler'),
    };
    
    // Optimizaciones de bundle (deshabilitadas temporalmente para debug R3F)
    // NOTA: El chunk splitting de R3F causa problemas con scheduler en desarrollo
    if (!isServer && isProd) {
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
            // React Three Fiber en chunk separado (SOLO EN PRODUCCIÓN)
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

