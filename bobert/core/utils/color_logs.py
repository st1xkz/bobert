import logging

RESET = "\033[0m"
BOLD = "\033[1m"

FORMATS = {
    logging.DEBUG: (
        f"{BOLD}\033[38;2;235;219;178m[DEBUG]{RESET} \033[38;2;235;219;178m{{name}}: {{message}}{RESET}"
    ),
    logging.INFO: (
        f"{BOLD}\033[38;2;142;192;124m[INFO]{RESET} \033[38;2;142;192;124m{{name}}: {{message}}{RESET}"
    ),
    logging.WARNING: (
        f"{BOLD}\033[38;2;250;189;47m[WARNING]{RESET} \033[38;2;250;189;47m{{name}}: {{message}}{RESET}"
    ),
    logging.ERROR: (
        f"{BOLD}\033[38;2;254;128;25m[ERROR]{RESET} \033[38;2;254;128;25m{{name}}: {{message}}{RESET}"
    ),
    logging.CRITICAL: (
        f"{BOLD}\033[38;2;249;72;51m[CRITICAL]{RESET} \033[38;2;249;72;51m{{name}}: {{message}}{RESET}"
    ),
}


class CustomFormatter(logging.Formatter):
    def format(self, record):
        log_fmt = FORMATS.get(record.levelno, "{levelname} {name}: {message}")
        formatter = logging.Formatter(log_fmt, style="{")
        return formatter.format(record)


handler = logging.StreamHandler()
handler.setFormatter(CustomFormatter())

logging.basicConfig(level=logging.DEBUG, handlers=[handler], force=True)

log = logging.getLogger("colored-logger")

# Test logs
log.debug("DEBUG MESSAGE")
log.info("INFO MESSAGE")
log.warning("WARNING MESSAGE")
log.error("ERROR MESSAGE")
log.critical("CRITICAL MESSAGE")
