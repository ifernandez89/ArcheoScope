/**
 * package-itch.js
 * Script de build, auditoría y empaquetado para itch.io (HTML5 Web)
 * 
 * Verifica los límites de itch.io:
 * - index.html en la raíz del ZIP
 * - <= 1000 archivos descomprimidos
 * - <= 500 MB descomprimidos
 * - <= 200 MB por archivo individual
 * - <= 240 caracteres por ruta
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

console.log('\n🌌 ===================================================');
console.log('🛸  ARCHEOSCOPE — EMPAQUETADOR PARA ITCH.IO (HTML5)');
console.log('===================================================\n');

const ROOT_DIR = path.resolve(__dirname, '..');
const OUT_DIR = path.join(ROOT_DIR, 'out');
const RELEASES_DIR = path.join(ROOT_DIR, 'releases');
const ZIP_OUTPUT = path.join(RELEASES_DIR, 'ArcheoScope_Web.zip');

// 1. Compilación con DEPLOY_TARGET=itch
console.log('📦 1. Compilando Next.js para itch.io (basePath: "")...');
try {
  execSync('npx next build', {
    cwd: ROOT_DIR,
    stdio: 'inherit',
    env: {
      ...process.env,
      NODE_ENV: 'production',
      NEXT_PUBLIC_DEPLOY_TARGET: 'itch',
      DEPLOY_TARGET: 'itch',
    },
  });
} catch (err) {
  console.error('\n❌ Error durante el build de Next.js');
  process.exit(1);
}

// 2. Verificar existencia de out/ y out/index.html
console.log('\n🔍 2. Auditando contenido de out/...');
if (!fs.existsSync(OUT_DIR)) {
  console.error('❌ Error: El directorio out/ no fue generado.');
  process.exit(1);
}

const indexHtmlPath = path.join(OUT_DIR, 'index.html');
if (!fs.existsSync(indexHtmlPath)) {
  console.error('❌ Error crítico: index.html no existe en la raíz de out/.');
  process.exit(1);
}
console.log('  ✅ index.html verificado en la raíz.');

// Función para recolectar archivos recursivamente
function getFiles(dir) {
  let results = [];
  const entries = fs.readdirSync(dir, { withFileTypes: true });
  for (const entry of entries) {
    const fullPath = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      results = results.concat(getFiles(fullPath));
    } else {
      results.push(fullPath);
    }
  }
  return results;
}

const allFiles = getFiles(OUT_DIR);
const fileCount = allFiles.length;
let totalSizeBytes = 0;
let largestFile = { path: '', sizeBytes: 0 };
let longestPath = { path: '', length: 0 };

for (const filePath of allFiles) {
  const stats = fs.statSync(filePath);
  totalSizeBytes += stats.size;
  const relPath = path.relative(OUT_DIR, filePath);

  if (stats.size > largestFile.sizeBytes) {
    largestFile = { path: relPath, sizeBytes: stats.size };
  }

  if (relPath.length > longestPath.length) {
    longestPath = { path: relPath, length: relPath.length };
  }
}

const totalMB = (totalSizeBytes / (1024 * 1024)).toFixed(2);
const largestMB = (largestFile.sizeBytes / (1024 * 1024)).toFixed(2);

console.log(`\n📊 Métricas del Build de itch.io:`);
console.log(`  • Cantidad de archivos: ${fileCount} / 1000 ${fileCount <= 1000 ? '✅' : '❌ (SUPERA EL LÍMITE)'}`);
console.log(`  • Peso descomprimido:   ${totalMB} MB / 500 MB ${totalSizeBytes <= 500 * 1024 * 1024 ? '✅' : '❌ (SUPERA EL LÍMITE)'}`);
console.log(`  • Archivo más pesado:   ${largestFile.path} (${largestMB} MB) ${largestFile.sizeBytes <= 200 * 1024 * 1024 ? '✅' : '❌ (SUPERA 200 MB)'}`);
console.log(`  • Ruta más larga:       ${longestPath.length} caracteres ${longestPath.length <= 240 ? '✅' : '❌ (SUPERA 240 CHARS)'}`);

if (fileCount > 1000 || totalSizeBytes > 500 * 1024 * 1024 || largestFile.sizeBytes > 200 * 1024 * 1024 || longestPath.length > 240) {
  console.error('\n❌ Uno o más límites de itch.io fueron excedidos.');
  process.exit(1);
}

// 3. Crear ZIP
console.log('\n🗜️  3. Creando ArcheoScope_Web.zip...');
if (!fs.existsSync(RELEASES_DIR)) {
  fs.mkdirSync(RELEASES_DIR, { recursive: true });
}

if (fs.existsSync(ZIP_OUTPUT)) {
  fs.unlinkSync(ZIP_OUTPUT);
}

try {
  // Usar tar nativo de Windows / BSD tar para crear zip con index.html en la raíz
  execSync(`tar -a -c -f "${ZIP_OUTPUT}" *`, {
    cwd: OUT_DIR,
    stdio: 'inherit',
  });
} catch (err) {
  console.log('  ⚠️ tar falló, intentando con PowerShell Compress-Archive...');
  try {
    execSync(`powershell -NoProfile -Command "Compress-Archive -Path '${OUT_DIR}\\*' -DestinationPath '${ZIP_OUTPUT}' -Force"`, {
      stdio: 'inherit',
    });
  } catch (psErr) {
    console.error('❌ Error creando el archivo ZIP:', psErr);
    process.exit(1);
  }
}

if (fs.existsSync(ZIP_OUTPUT)) {
  const zipStats = fs.statSync(ZIP_OUTPUT);
  const zipMB = (zipStats.size / (1024 * 1024)).toFixed(2);
  console.log(`\n🎉 ¡ZIP creado exitosamente!`);
  console.log(`  📁 Ubicación: ${ZIP_OUTPUT}`);
  console.log(`  ⚖️  Peso del ZIP comprimido: ${zipMB} MB`);
  console.log(`\n📋 Próximos pasos para publicar en itch.io:`);
  console.log(`  1. Ir al panel de itch.io -> Create new project`);
  console.log(`  2. Kind of project: 'HTML'`);
  console.log(`  3. Subir '${path.basename(ZIP_OUTPUT)}'`);
  console.log(`  4. Marcar: [x] 'This file will be played in the browser'`);
  console.log(`  5. Configurar viewport: 1280x720 (o Fullscreen)`);
} else {
  console.error('❌ Error: El archivo ZIP no fue generado.');
  process.exit(1);
}
