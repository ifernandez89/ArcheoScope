# Guías de Seguridad - ArcheoScope

## 🔐 Protección de API Keys y Datos Sensibles

### ⚠️ CRÍTICO: Nunca Exponer API Keys

**API Keys que NUNCA deben estar en el código:**
- OpenRouter API Keys (`sk-or-v1-...`)
- TestSprite MCP API Keys
- Cualquier clave de servicio externo
- Credenciales de base de datos
- Tokens de autenticación

### ✅ Configuración Segura

#### 1. **Usar Variables de Entorno**
```bash
# ✅ CORRECTO - En .env.local (protegido por .gitignore)
OPENROUTER_API_KEY=sk-or-v1-tu_key_real_aqui

# ❌ INCORRECTO - En código fuente
api_key = "sk-or-v1-tu_key_real_aqui"
```

#### 2. **Archivos de Configuración**
```bash
# ✅ Archivos seguros (en .gitignore)
.env.local          # Variables de entorno reales
mcp.json.local      # Configuración MCP real

# ✅ Archivos de ejemplo (seguros para Git)
.env.local.example  # Plantilla sin valores reales
mcp.json.example    # Plantilla MCP sin keys reales
```

#### 3. **En el Código**
```python
# ✅ CORRECTO - Leer desde variables de entorno
import os
from dotenv import load_dotenv

load_dotenv('.env.local')
api_key = os.getenv('OPENROUTER_API_KEY', 'CONFIGURE_YOUR_KEY')

# ❌ INCORRECTO - Hardcoded
api_key = "sk-or-v1-real-key-here"
```

### 🛡️ Configuración del .gitignore

El archivo `.gitignore` está configurado para proteger:

```gitignore
# Environment variables
.env
.env.local
.env.*.local

# MCP Configuration (puede contener API keys)
mcp.json.local

# API Keys y configuración sensible
*api_key*
*API_KEY*
*.key
*.pem
```

### 🔧 Setup Seguro

#### 1. **Primera Configuración**
```bash
# 1. Copiar plantillas
cp .env.local.example .env.local
cp mcp.json.example mcp.json.local

# 2. Editar con valores reales
nano .env.local
nano mcp.json.local

# 3. Verificar que están en .gitignore
git status  # No deben aparecer .env.local ni mcp.json.local
```

#### 2. **Verificar Seguridad**
```bash
# Verificar que no hay API keys en el código
grep -r "sk-or-v1-" --exclude-dir=.git .
grep -r "API_KEY.*=" --exclude-dir=.git .

# Solo deben aparecer en archivos .example o con valores placeholder
```

### 🚨 Qué Hacer Si Se Expone una API Key

#### 1. **Inmediatamente**
- Revocar la API key expuesta en el servicio (OpenRouter, etc.)
- Generar una nueva API key
- Actualizar la configuración local

#### 2. **Limpiar el Repositorio**
```bash
# Si la key está en commits anteriores
git filter-branch --force --index-filter \
  'git rm --cached --ignore-unmatch archivo_con_key.py' \
  --prune-empty --tag-name-filter cat -- --all

# Forzar push (CUIDADO: reescribe historia)
git push origin --force --all
```

#### 3. **Prevenir Futuras Exposiciones**
- Usar pre-commit hooks para detectar keys
- Revisar todos los commits antes de push
- Usar herramientas como `git-secrets`

### 📋 Checklist de Seguridad

Antes de cada commit:

- [ ] ✅ No hay API keys reales en el código
- [ ] ✅ Variables sensibles están en .env.local
- [ ] ✅ .env.local está en .gitignore
- [ ] ✅ Solo archivos .example tienen placeholders
- [ ] ✅ Documentación usa valores de ejemplo
- [ ] ✅ Tests usan variables de entorno

### 🔍 Herramientas de Verificación

#### 1. **Script de Verificación**
```bash
#!/bin/bash
# check_security.sh

echo "🔍 Verificando seguridad..."

# Buscar posibles API keys expuestas
if grep -r "sk-or-v1-[a-zA-Z0-9]" --exclude-dir=.git --exclude="*.example" .; then
    echo "❌ PELIGRO: API keys encontradas en el código"
    exit 1
fi

echo "✅ No se encontraron API keys expuestas"
```

#### 2. **Pre-commit Hook**
```bash
#!/bin/sh
# .git/hooks/pre-commit

# Verificar API keys antes de commit
if grep -r "sk-or-v1-[a-zA-Z0-9]" --exclude-dir=.git --exclude="*.example" .; then
    echo "❌ COMMIT BLOQUEADO: API keys detectadas"
    echo "   Mueve las keys a .env.local"
    exit 1
fi
```

### 🌐 Configuración para Producción

#### 1. **Variables de Entorno del Sistema**
```bash
# En el servidor de producción
export OPENROUTER_API_KEY="sk-or-v1-production-key"
export DATABASE_URL="postgresql://..."
```

#### 2. **Docker Secrets**
```yaml
# docker-compose.yml
services:
  archeoscope:
    environment:
      - OPENROUTER_API_KEY_FILE=/run/secrets/openrouter_key
    secrets:
      - openrouter_key

secrets:
  openrouter_key:
    file: ./secrets/openrouter_key.txt
```

#### 3. **Kubernetes Secrets**
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: archeoscope-secrets
type: Opaque
data:
  openrouter-api-key: <base64-encoded-key>
```

### 📞 Contacto de Seguridad

Si encuentras una vulnerabilidad de seguridad:

1. **NO** la reportes públicamente
2. Contacta directamente al equipo de desarrollo
3. Proporciona detalles específicos
4. Permite tiempo para la corrección antes de divulgación

### 🔄 Rotación de API Keys

**Frecuencia recomendada:**
- Desarrollo: Cada 3 meses
- Producción: Cada mes
- Si hay sospecha de compromiso: Inmediatamente

**Proceso:**
1. Generar nueva key
2. Actualizar configuración
3. Probar funcionamiento
4. Revocar key anterior
5. Documentar el cambio

---

## ✅ Resumen

**La seguridad es responsabilidad de todos:**
- Nunca hardcodear API keys
- Usar variables de entorno
- Verificar antes de cada commit
- Mantener .gitignore actualizado
- Rotar keys regularmente

**Recuerda: Una API key expuesta puede comprometer todo el sistema.**