import logging


FMT = "[{levelname}] {name}: {message}"
FORMATS = {
    logging.DEBUG: f"\33[38;2;153;153;153m{FMT}\33[0m",
    logging.INFO: f"\33[38;2;8;160;69m{FMT}\33[0m",
    logging.WARNING: f"\33[38;2;247;240;82m{FMT}\33[0m",
    logging.ERROR: f"\33[38;2;255;140;66m{FMT}\33[0m",
    logging.CRITICAL: f"\33[38;2;255;60;56m{FMT}\33[0m",
}


class CustomFormatter(logging.Formatter):
    def format(self, record):
        log_fmt = FORMATS[record.levelno]
        formatter = logging.Formatter(log_fmt, style="{")
        return formatter.format(record)


handler = logging.StreamHandler()
handler.setFormatter(CustomFormatter())
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
