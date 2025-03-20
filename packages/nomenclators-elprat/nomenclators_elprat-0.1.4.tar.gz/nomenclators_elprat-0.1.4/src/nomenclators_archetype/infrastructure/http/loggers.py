"""
----------------------------------------------------------------------------------------------------
Written by:
  - Yovany Dominico Girón(y.dominico.giron@elprat.cat)

for Ajuntament del Prat de Llobregat
----------------------------------------------------------------------------------------------------

----------------------------------------------------------------------------------------------------
"""
import logging
import sys
import os
import uuid
import time
import socket

from datetime import datetime

from pythonjsonlogger.json import JsonFormatter

from starlette.responses import Response


LOGGER_LEVEL_NAME = "LOGGER_LEVEL"
LOGGER_LEVEL_DAFAULT = "INFO"
LOGGER_LEVEL = os.getenv("LOGGER_LEVEL", "INFO").upper()

# Console JSON Logger
logger_console_json = logging.getLogger("logger_console_json")
logger_console_json.setLevel(getattr(logging, LOGGER_LEVEL, logging.INFO))

logger_console_json_handler = logging.StreamHandler(sys.stdout)
logger_console_json_handler.setFormatter(
    JsonFormatter(
        "%(timestamp)s %(client_request_id)s %(server_request_id)s %(application_id)s "
        "%(request_time)s %(entry_time)s %(user)s %(client_session_id)s "
        "%(client_ip)s %(server_ip)s %(server_port)s %(service)s %(http_method)s "
        "%(module)s %(response_code)s %(response_time)s"
    )
)

if not logger_console_json.hasHandlers():
    logger_console_json.addHandler(logger_console_json_handler)
    logger_console_json.propagate = False


async def log_requests(request, call_next):
    """Log middlewares for the requests router"""

    request_time = datetime.utcnow().isoformat()
    start_time = time.time()
    # ID único de la petición en el servidor
    server_request_id = str(uuid.uuid4())
    # ID de cliente (o generado si no hay)
    client_request_id = request.headers.get(
        "X-Request-ID", str(uuid.uuid4()))
    client_session_id = request.headers.get(
        "Authorization", "Unknown")  # JWT u otro token
    # Nombre de usuario si está disponible
    user = request.headers.get("X-User", "Anonymous")
    client_ip = request.client.host if request.client else "Unknown"
    server_ip = socket.gethostbyname(socket.gethostname())
    server_port = request.url.port or 80
    service = request.url.path  # Ruta del servicio web llamado
    http_method = request.method  # Verbo HTTP (GET, POST, etc.)
    # Intentar obtener el módulo del servicio
    module = request.scope.get("endpoint", "Unknown")

    try:
        # Procesar la petición
        response = await call_next(request)
        response_code = response.status_code
    except Exception as e:
        response_code = 500
        logger_console_json.exception(
            "Exception while processing request %s", server_request_id, exc_info=True)
        response = Response("Internal Server Error", status_code=500)

    # Tiempo de respuesta total
    response_time = round(time.time() - start_time, 4)

    log_data = {
        "timestamp": datetime.utcnow().isoformat(),
        "client_request_id": client_request_id,
        "server_request_id": server_request_id,
        "application_id": APPLICATION_ID,
        "request_time": request_time,
        "entry_time": datetime.utcnow().isoformat(),
        "user": user,
        "client_session_id": client_session_id,
        "client_ip": client_ip,
        "server_ip": server_ip,
        "server_port": server_port,
        "service": service,
        "http_method": http_method,
        "module": module,
        "response_code": response_code,  # Código HTTP de respuesta
        "response_time": response_time  # Tiempo de ejecución en segundos
    }

    logger_console_json.info(log_data)
    return response

    # response = await call_next(request)
    # logger_console_json.info(
    #     f"Request: {request.method} {request.url} - Response: {response.status_code}")
    # return response

    # start_time = time.time()
    # response = await call_next(request)
    # process_time = time.time() - start_time
    # response.headers["X-Process-Time"] = str(process_time)
    # return response
