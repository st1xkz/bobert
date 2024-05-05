import logging

FORMATS = {
    logging.DEBUG: (
        "[1;38;2;235;219;178m[{levelname}][0m "
        "[38;2;235;219;178m{name}: {message}[0m"
    ),
    logging.INFO: (
        "[1;38;2;142;192;124m[{levelname}][0m "
        "[38;2;142;192;124m{name}: {message}[0m"
    ),
    logging.WARNING: (
        "[1;38;2;250;189;47m[{levelname}][0m "
        "[38;2;250;189;47m{name}: {message}[0m"
    ),
    logging.ERROR: (
        "[1;38;2;254;128;25m[{levelname}][0m "
        "[38;2;254;128;25m{name}: {message}[0m"
    ),
    logging.CRITICAL: (
        "[1;38;2;249;72;51m[{levelname}][0m " "[38;2;249;72;51m{name}: {message}[0m"
    ),
}


class CustomFormatter(logging.Formatter):
    def format(self, record):
        log_fmt = FORMATS.get(record.levelno, "{levelname} {name}: {message}")
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
