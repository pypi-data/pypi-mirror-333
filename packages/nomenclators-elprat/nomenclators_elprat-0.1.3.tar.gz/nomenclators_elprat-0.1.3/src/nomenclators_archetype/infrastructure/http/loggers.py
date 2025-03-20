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

from pythonjsonlogger.json import JsonFormatter

LOGGER_LEVEL_NAME = "LOGGER_LEVEL"
LOGGER_LEVEL_DAFAULT = "INFO"
LOGGER_LEVEL = os.getenv("LOGGER_LEVEL", "INFO").upper()

# Console JSON Logger
logger_console_json = logging.getLogger("logger_console_json")
logger_console_json.setLevel(getattr(logging, LOGGER_LEVEL, logging.INFO))

logger_console_json_handler = logging.StreamHandler(sys.stdout)
logger_console_json_handler.setFormatter(
    JsonFormatter(
        "%(asctime)s %(levelname)s %(name)s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
)

if not logger_console_json.hasHandlers():
    logger_console_json.addHandler(logger_console_json_handler)
    logger_console_json.propagate = False
