#!/usr/bin/env python3
"""
Crear endpoint API para capa de sitios arqueológicos.

Endpoints:
1. GET /api/sites/layer - Obtener todos los sitios para mapa
2. POST /api/sites/candidate - Agregar nuevo candidato
3. GET /api/sites/candidates - Obtener solo candidatos
"""

# Este código debe agregarse a backend/api/scientific_endpoint.py

LAYER_ENDPOINTS_CODE = '''
# ============================================================================
# ENDPOINTS PARA CAPA DE SITIOS ARQUEOLÓGICOS
# ============================================================================

@router.get("/sites/layer")
async def get_sites_layer(
    confidence_level: Optional[str] = None,
    site_type: Optional[str] = None,
    country: Optional[str] = None,
    limit: int = 10000
):
    """
    Obtener sitios para capa de mapa.
    
    Parámetros:
    - confidence_level: HIGH, MODERATE, LOW, CANDIDATE
    - site_type: Filtrar por tipo
    - country: Filtrar por país
    - limit: Máximo de sitios (default 10000)
    
    Returns:
        GeoJSON FeatureCollection
    """
    
    if not db_pool:
        raise HTTPException(status_code=500, detail="Database not available")
    
    try:
        async with db_pool.acquire() as conn:
            # Construir query
            where_clauses = []
            params = []
            param_count = 1
            
            if confidence_level:
                where_clauses.append(f'"confidenceLevel" = ${param_count}')
                params.append(confidence_level)
                param_count += 1
            
            if site_type:
                where_clauses.append(f'"siteType" = ${param_count}')
                params.append(site_type)
                param_count += 1
            
            if country:
                where_clauses.append(f'country = ${param_count}')
                params.append(country)
                param_count += 1
            
            where_sql = " AND ".join(where_clauses) if where_clauses else "TRUE"
            
            query = f"""
                SELECT 
                    id,
                    name,
                    slug,
                    "siteType" as site_type,
                    "environmentType" as environment_type,
                    "confidenceLevel" as confidence_level,
                    latitude,
                    longitude,
                    country,
                    region,
                    description,
                    "createdAt" as created_at
                FROM archaeological_sites
                WHERE {where_sql}
                ORDER BY "confidenceLevel" DESC, "createdAt" DESC
                LIMIT ${param_count}
            """
            params.append(limit)
            
            sites = await conn.fetch(query, *params)
            
            # Convertir a GeoJSON
            features = []
            for site in sites:
                feature = {
                    "type": "Feature",
                    "geometry": {
                        "type": "Point",
                        "coordinates": [site['longitude'], site['latitude']]
                    },
                    "properties": {
                        "id": str(site['id']),
                        "name": site['name'],
                        "slug": site['slug'],
                        "siteType": site['site_type'],
                        "environmentType": site['environment_type'],
                        "confidenceLevel": site['confidence_level'],
                        "country": site['country'],
                        "region": site['region'],
                        "description": site['description'][:200] if site['description'] else "",
                        "createdAt": site['created_at'].isoformat() if site['created_at'] else None
                    }
                }
                features.append(feature)
            
            geojson = {
                "type": "FeatureCollection",
                "features": features,
                "metadata": {
                    "total": len(features),
                    "filters": {
                        "confidence_level": confidence_level,
                        "site_type": site_type,
                        "country": country
                    }
                }
            }
            
            return geojson
            
    except Exception as e:
        print(f"Error getting sites layer: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/sites/candidate")
async def add_candidate_site(request: dict):
    """
    Agregar nuevo sitio candidato a la capa.
    
    Body:
    {
        "name": "Candidato Amazonía 001",
        "latitude": -10.5,
        "longitude": -70.2,
        "country": "Brazil",
        "region": "Acre",
        "origin_probability": 0.85,
        "activity_probability": 0.05,
        "anomaly_probability": 0.02,
        "ess": "high",
        "ess_score": 0.75,
        "description": "Candidato detectado...",
        "analysis_id": "uuid"
    }
    """
    
    if not db_pool:
        raise HTTPException(status_code=500, detail="Database not available")
    
    try:
        # Validar datos requeridos
        required = ['name', 'latitude', 'longitude', 'country']
        for field in required:
            if field not in request:
                raise HTTPException(status_code=400, detail=f"Missing field: {field}")
        
        # Generar slug
        import re
        slug_base = f"{request['name']}-{request['latitude']:.4f}-{request['longitude']:.4f}"
        slug = re.sub(r'[^a-z0-9-]', '', slug_base.lower().replace(' ', '-'))
        
        # Generar descripción con métricas separadas
        origin = request.get('origin_probability', 0)
        activity = request.get('activity_probability', 0)
        anomaly = request.get('anomaly_probability', 0)
        ess = request.get('ess', 'none')
        
        description = (
            f"Candidato arqueológico detectado por ArcheoScope. "
            f"Métricas: Origen {origin:.0%}, Actividad {activity:.0%}, "
            f"Anomalía {anomaly:.0%}. ESS: {ess.upper()}. "
            f"Requiere validación de campo."
        )
        
        if 'description' in request:
            description = request['description']
        
        async with db_pool.acquire() as conn:
            # Insertar sitio
            site_id = await conn.fetchval("""
                INSERT INTO archaeological_sites (
                    name,
                    slug,
                    "siteType",
                    "environmentType",
                    "confidenceLevel",
                    latitude,
                    longitude,
                    country,
                    region,
                    description,
                    "createdAt",
                    "updatedAt"
                ) VALUES (
                    $1, $2, $3, $4, $5, $6, $7, $8, $9, $10, NOW(), NOW()
                )
                RETURNING id
            """,
                request['name'],
                slug,
                'UNKNOWN',  # Tipo por defecto
                request.get('environment_type', 'UNKNOWN'),
                'CANDIDATE',  # Siempre candidato
                request['latitude'],
                request['longitude'],
                request['country'],
                request.get('region', ''),
                description
            )
            
            return {
                "success": True,
                "site_id": str(site_id),
                "message": "Candidato agregado a la capa",
                "slug": slug
            }
            
    except Exception as e:
        print(f"Error adding candidate: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/sites/candidates")
async def get_candidates_only(limit: int = 1000):
    """
    Obtener solo sitios CANDIDATOS para revisión.
    
    Returns:
        Lista de candidatos con métricas
    """
    
    if not db_pool:
        raise HTTPException(status_code=500, detail="Database not available")
    
    try:
        async with db_pool.acquire() as conn:
            candidates = await conn.fetch("""
                SELECT 
                    id,
                    name,
                    slug,
                    "siteType" as site_type,
                    "environmentType" as environment_type,
                    latitude,
                    longitude,
                    country,
                    region,
                    description,
                    "createdAt" as created_at
                FROM archaeological_sites
                WHERE "confidenceLevel" = 'CANDIDATE'
                ORDER BY "createdAt" DESC
                LIMIT $1
            """, limit)
            
            result = []
            for c in candidates:
                # Extraer métricas de la descripción
                import re
                desc = c['description']
                
                origin = 0.0
                activity = 0.0
                anomaly = 0.0
                ess = "none"
                
                # Buscar métricas en descripción
                origin_match = re.search(r'Origen (\d+)%', desc)
                if origin_match:
                    origin = float(origin_match.group(1)) / 100
                
                activity_match = re.search(r'Actividad (\d+)%', desc)
                if activity_match:
                    activity = float(activity_match.group(1)) / 100
                
                anomaly_match = re.search(r'Anomalía (\d+)%', desc)
                if anomaly_match:
                    anomaly = float(anomaly_match.group(1)) / 100
                
                ess_match = re.search(r'ESS: (\w+)', desc)
                if ess_match:
                    ess = ess_match.group(1).lower()
                
                result.append({
                    "id": str(c['id']),
                    "name": c['name'],
                    "slug": c['slug'],
                    "site_type": c['site_type'],
                    "environment_type": c['environment_type'],
                    "latitude": c['latitude'],
                    "longitude": c['longitude'],
                    "country": c['country'],
                    "region": c['region'],
                    "description": c['description'],
                    "created_at": c['created_at'].isoformat() if c['created_at'] else None,
                    "metrics": {
                        "origin": origin,
                        "activity": activity,
                        "anomaly": anomaly,
                        "ess": ess
                    }
                })
            
            return {
                "total": len(result),
                "candidates": result
            }
            
    except Exception as e:
        print(f"Error getting candidates: {e}")
        raise HTTPException(status_code=500, detail=str(e))
'''

print("="*70)
print("📝 CÓDIGO PARA ENDPOINTS DE CAPA DE SITIOS")
print("="*70)
print("\nAgregar este código a: backend/api/scientific_endpoint.py")
print("\nEndpoints creados:")
print("1. GET  /api/scientific/sites/layer - Capa GeoJSON para mapa")
print("2. POST /api/scientific/sites/candidate - Agregar candidato")
print("3. GET  /api/scientific/sites/candidates - Listar candidatos")
print("\n" + "="*70)
print(LAYER_ENDPOINTS_CODE)
