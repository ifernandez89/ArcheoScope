---
inclusion: auto
---

# Reglas Estrictas de Performance 3D - React Three Fiber

## REGLAS CRÍTICAS PARA useFrame

1. **NUNCA crear objetos dentro de useFrame**
   ```typescript
   // ❌ MAL - Crea 60 objetos por segundo
   useFrame(() => {
     const pos = new THREE.Vector3()
     mesh.position.copy(pos)
   })
   
   // ✅ BIEN - Reutiliza objeto
   const tempVec = useRef(new THREE.Vector3())
   useFrame(() => {
     mesh.position.copy(tempVec.current.set(x, y, z))
   })
   ```

2. **NUNCA usar setState dentro de useFrame**
   ```typescript
   // ❌ MAL - Causa re-render cada frame
   useFrame(() => {
     setPosition([x, y, z])
   })
   
   // ✅ BIEN - Usar ref
   const posRef = useRef([0, 0, 0])
   useFrame(() => {
     posRef.current = [x, y, z]
     mesh.current.position.set(...posRef.current)
   })
   ```

3. **NUNCA usar .find(), .filter(), .map() dentro de useFrame**
   ```typescript
   // ❌ MAL - O(n) cada frame
   useFrame(() => {
     const planet = planets.find(p => p.name === 'Earth')
   })
   
   // ✅ BIEN - Usar Map para O(1)
   const planetMap = useMemo(() => new Map(planets.map(p => [p.name, p])), [planets])
   useFrame(() => {
     const planet = planetMap.get('Earth')
   })
   ```

4. **NUNCA hacer traverse() dentro de useFrame**
   ```typescript
   // ❌ MAL - Recorre todo el árbol cada frame
   useFrame(() => {
     scene.traverse(child => { ... })
   })
   
   // ✅ BIEN - Cachear meshes una vez
   const cachedMeshes = useRef<THREE.Mesh[]>([])
   useEffect(() => {
     scene.traverse(child => {
       if (child.isMesh) cachedMeshes.current.push(child)
     })
   }, [scene])
   ```

5. **Usar early exit en useFrame**
   ```typescript
   useFrame((state, delta) => {
     if (!isActive || !meshRef.current) return
     // ... lógica
   })
   ```

## REGLAS PARA MODELOS GLB

1. **NUNCA usar .clone() dentro de useFrame o funciones que se llaman frecuentemente**

2. **Usar useMemo para clonar escenas**
   ```typescript
   const clonedScene = useMemo(() => scene.clone(true), [scene])
   ```

3. **NO usar yOffset calculados dinámicamente** - Usar posiciones fijas

## REGLAS PARA RAYCAST

1. **NUNCA hacer raycast contra scene.children completo**
   ```typescript
   // ❌ MAL
   raycaster.intersectObjects(scene.children, true)
   
   // ✅ BIEN - Cachear objetos interactivos
   const interactiveObjects = useRef<THREE.Object3D[]>([])
   // Poblar una vez, usar siempre
   raycaster.intersectObjects(interactiveObjects.current, true)
   ```

## REGLAS PARA VECTORES Y MATRICES

1. **Crear vectores/matrices reutilizables fuera del componente o en useRef**
   ```typescript
   const tempVec3 = new THREE.Vector3()
   const tempMatrix = new THREE.Matrix4()
   
   function MyComponent() {
     useFrame(() => {
       tempVec3.set(x, y, z) // Reutiliza
     })
   }
   ```

## POSICIONES FIJAS IMPORTANTES

- Piramidón en el suelo (Giza): `[100, 0.5, 35]`
- Piramidón en la punta (Giza): `[0, 45.48, 0]`
