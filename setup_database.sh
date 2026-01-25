#!/bin/bash

# ArcheoScope Database Setup Script
# ==================================

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                                                              ║"
echo "║   ArcheoScope - Setup de Base de Datos PostgreSQL           ║"
echo "║                                                              ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# Colores
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Verificar Node.js
echo "🔍 Verificando Node.js..."
if ! command -v node &> /dev/null; then
    echo -e "${RED}❌ Node.js no está instalado${NC}"
    echo "   Instala Node.js desde: https://nodejs.org/"
    exit 1
fi
echo -e "${GREEN}✅ Node.js $(node --version)${NC}"

# Verificar npm
if ! command -v npm &> /dev/null; then
    echo -e "${RED}❌ npm no está instalado${NC}"
    exit 1
fi
echo -e "${GREEN}✅ npm $(npm --version)${NC}"

# Instalar dependencias
echo ""
echo "📦 Instalando dependencias de Node.js..."
npm install

# Verificar .env
echo ""
echo "🔧 Verificando configuración..."
if [ ! -f .env ]; then
    echo -e "${YELLOW}⚠️  Archivo .env no encontrado${NC}"
    echo "   Copiando .env.example a .env..."
    cp .env.example .env
    echo -e "${YELLOW}⚠️  IMPORTANTE: Edita .env y configura tu DATABASE_URL${NC}"
    echo ""
    echo "   Opciones:"
    echo "   1. PostgreSQL local: postgresql://postgres:postgres@localhost:5432/archeoscope_db"
    echo "   2. Supabase: https://supabase.com (gratis)"
    echo "   3. Railway: https://railway.app (gratis)"
    echo ""
    read -p "   Presiona Enter después de configurar .env..."
fi

# Verificar DATABASE_URL
if ! grep -q "DATABASE_URL=" .env || grep -q "DATABASE_URL=\"postgresql://archeoscope:password@localhost:5432/archeoscope_db" .env; then
    echo -e "${RED}❌ DATABASE_URL no configurada correctamente en .env${NC}"
    echo "   Edita .env y configura tu DATABASE_URL"
    exit 1
fi

echo -e "${GREEN}✅ DATABASE_URL configurada${NC}"

# Generar cliente Prisma
echo ""
echo "🔨 Generando cliente Prisma..."
npx prisma generate

# Ejecutar migraciones
echo ""
echo "🗄️  Ejecutando migraciones de base de datos..."
npx prisma migrate dev --name init

# Ejecutar seed
echo ""
echo "🌱 Poblando base de datos con datos iniciales..."
npx prisma db seed

# Migrar JSON a PostgreSQL
echo ""
echo "📂 Migrando datos del JSON a PostgreSQL..."
python scripts/migrate_json_to_postgres.py

# Resumen
echo ""
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                                                              ║"
echo "║   ✅ Setup Completado Exitosamente                           ║"
echo "║                                                              ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""
echo "🎉 La base de datos está lista para usar!"
echo ""
echo "📊 Próximos pasos:"
echo "   1. Abre Prisma Studio: npm run db:studio"
echo "   2. Explora los datos en: http://localhost:5555"
echo "   3. Integra con el backend Python"
echo ""
echo "📚 Documentación:"
echo "   - DATABASE_SETUP.md: Guía completa"
echo "   - DATABASE_SUMMARY.md: Resumen ejecutivo"
echo ""
