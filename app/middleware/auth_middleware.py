from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
import httpx
import os

AUTH_SERVICE_URL = os.getenv("AUTH_SERVICE_URL", "http://localhost:8001/api/validate_token")

# Roles permitidos por endpoint 
ACCESS_RULES = {
    "/sync": ["admin", "user"],
    "/predict/occupancy": ["admin", "user"],
    "/predict/occupancy-ranking": ["admin"],
    "/predict/trending-resources": ["admin"],
    "/predict/seasonal-patterns": ["admin"],
}


async def auth_middleware(request: Request, call_next):
    # Permitir acceso libre a la raíz y la documentación (y assets)
    allowed_paths = ["/", "/docs", "/redoc", "/openapi.json", "/openapi", "/docs/oauth2-redirect"]
    if any(request.url.path == p or request.url.path.startswith(p + "/") for p in allowed_paths):
        return await call_next(request)

    # Permitir preflight
    if request.method == "OPTIONS":
        return await call_next(request)

    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return JSONResponse(status_code=401, content={"detail": "Missing or invalid Authorization header"})

    token = auth_header.split("Bearer ")[-1]

    # Validar el token con el servicio externo
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                AUTH_SERVICE_URL,
                headers={"Authorization": f"Bearer {token}"},
                timeout=5.0,
            )
        except httpx.RequestError:
            return JSONResponse(status_code=500, content={"detail": "Authentication service unavailable"})

    if response.status_code != 200:
        return JSONResponse(status_code=401, content={"detail": "Invalid or expired token"})

    user_data = response.json()
    role = user_data.get("role")

    # Comprobar permisos según el endpoint
    allowed_roles = []
    for path, roles in ACCESS_RULES.items():
        if request.url.path.startswith(path):
            allowed_roles = roles
            break

    if allowed_roles and role not in allowed_roles:
        return JSONResponse(status_code=403, content={"detail": "Access forbidden for this role"})

    request.state.user = user_data

    response = await call_next(request)
    return response