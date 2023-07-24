import logging

FMT = "[{levelname}] {name}: {message}"
FORMATS = {
    logging.DEBUG: f"\33[38;2;235;219;178m{FMT}\33[0m",
    logging.INFO: f"\33[38;2;142;192;124m{FMT}\33[0m",
    logging.WARNING: f"\33[38;2;250;189;47m{FMT}\33[0m",
    logging.ERROR: f"\33[38;2;254;128;25m{FMT}\33[0m",
    logging.CRITICAL: f"\33[38;2;249;72;51m{FMT}\33[0m",
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
