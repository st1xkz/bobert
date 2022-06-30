import logging

import hikari
import lightbulb

logs_plugin = lightbulb.Plugin("color-logs")


FMT = "[{levelname}] {name}: {message}"
FORMATS = {
    logging.DEBUG: f"\33[38;2;190;0;254m{FMT}\33[0m",
    logging.INFO: f"\33[38;2;0;111;249m{FMT}\33[0m",
    logging.WARNING: f"\33[38;2;102;255;0m{FMT}\33[0m",
    logging.ERROR: f"\33[38;2;255;255;0m{FMT}\33[0m",
    logging.CRITICAL: f"\33[38;2;255;0;127m{FMT}\33[0m",
}


class CustomFormatter(logging.Formatter):
    def format(self, record):
        log_fmt = FORMATS[record.levelno]
        formatter = logging.Formatter(log_fmt, style="{")
        return formatter.format(record)


@logs_plugin.listener()
async def started_logs(event: hikari.StartedEvent):
    handler.setFormatter(CustomFormatter())


handler = logging.StreamHandler()
logging.basicConfig(
    level=logging.DEBUG,
    handlers=[handler],
)

log = logging.getLogger("colored-logger")
log.debug("DEBUG MESSAGE")
log.info("INFO MESSAGE")
log.warning("WARNING MESSAGE")
log.error("ERROR MESSAGE")
log.critical("CRITICAL MESSAGE")
