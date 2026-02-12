# 🔄 CÓMO VER LOS CAMBIOS EN EL NAVEGADOR

## El servidor está corriendo correctamente en http://localhost:3000

### Para ver los cambios nuevos:

1. **Abre el navegador en http://localhost:3000**

2. **Haz un HARD REFRESH (limpia la caché):**
   - **Windows/Linux:** `Ctrl + Shift + R` o `Ctrl + F5`
   - **Mac:** `Cmd + Shift + R`

3. **O abre el DevTools y desactiva caché:**
   - Presiona `F12` para abrir DevTools
   - Ve a la pestaña "Network"
   - Marca la casilla "Disable cache"
   - Refresca la página con `F5`

4. **Si aún no ves cambios:**
   - Cierra completamente el navegador
   - Ábrelo de nuevo
   - Ve a http://localhost:3000

## ✅ Qué deberías ver ahora:

- **Botón 🗿 más grande (70px)** en la esquina inferior derecha
- **Indicador de conexión** (punto verde/rojo) en el botón
- **Conexión automática a Ollama** (sin necesidad de hacer clic en "Conectar")
- **Estado "Ollama Activo"** en verde si Ollama está corriendo
- **Botón de voz 🔊/🔇** en el header del chat
- **Indicador de voz** (🔊 amarillo) cuando el Moai habla

## 🔊 Para que el Moai hable:

1. Asegúrate de que Ollama esté corriendo: `ollama serve`
2. El botón 🗿 debe estar verde (conectado)
3. Abre el chat haciendo clic en 🗿
4. El botón 🔊 debe estar activado (no 🔇)
5. Escribe un mensaje y envíalo
6. El Moai responderá con texto Y voz

## 🐛 Si hay errores:

Abre la consola del navegador (F12 → Console) y comparte el error.
