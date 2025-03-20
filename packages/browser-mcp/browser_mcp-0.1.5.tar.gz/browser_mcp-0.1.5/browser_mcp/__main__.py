"""
Main entry point for browser-mcp that checks dependencies before starting the server
"""

# Import sys first to set up stdout redirection before any other imports
import sys
import os
import logging
import logging.config
import io
from pathlib import Path

# Now import the rest of our dependencies
from browser_mcp.server import mcp
from browser_mcp.check_playwright import check_playwright_browsers

# Set up logs directory in user's home directory
LOG_DIR = os.path.join(str(Path.home()), ".browser-mcp", "logs")
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, "browser-mcp.log")

# Configure logging before any imports
logging.config.dictConfig(
    {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "standard": {
                "format": "%(asctime)s [%(name)s] [%(levelname)s] %(message)s"
            },
        },
        "handlers": {
            "file": {
                "class": "logging.FileHandler",
                "filename": LOG_FILE,
                "mode": "a",
                "formatter": "standard",
            }
        },
        "loggers": {
            "": {  # Root logger
                "handlers": ["file"],
                "level": "WARNING",
                "propagate": True,
            },
            "browser_use": {
                "handlers": ["file"],
                "level": "WARNING",
                "propagate": False,
            },
        },
    }
)

# Set environment variables before any other imports
os.environ["ANONYMIZED_TELEMETRY"] = "false"
os.environ["BROWSER_USE_LOG_LEVEL"] = "WARNING"  # Add this line to suppress INFO logs


os.environ["ANONYMIZED_TELEMETRY"] = "false"

# Set up stdout redirection immediately, before any other imports
# Create a minimal file handler for early logging
early_handler = logging.FileHandler(LOG_FILE, mode="a")
early_handler.setFormatter(
    logging.Formatter("%(asctime)s [%(name)s] [%(levelname)s] %(message)s")
)

# Set up a minimal logger for the StdoutSuppressor
early_logger = logging.getLogger("stdout-suppressor")
early_logger.setLevel(logging.DEBUG)
early_logger.addHandler(early_handler)
early_logger.propagate = False


class StdoutSuppressor:
    def __init__(self):
        self.buffer = io.BytesIO()
        self._original_stdout = sys.stdout

    def write(self, message):
        if message and message.strip():  # If the message isn't just whitespace
            early_logger.debug(f"Suppressed stdout: {message.strip()}")
        if isinstance(message, str):
            self.buffer.write(message.encode("utf-8"))
        else:
            self.buffer.write(message)
        return len(message) if message else 0

    def flush(self):
        self.buffer.flush()

    def fileno(self):
        return self._original_stdout.fileno()

    def isatty(self):
        return self._original_stdout.isatty()


# Save the original stdout before replacing it
original_stdout = sys.stdout
# Replace stdout with our suppressor before any other imports
sys.stdout = StdoutSuppressor()

# Suppress Playwright's logging immediately
os.environ["PLAYWRIGHT_BROWSER_PATH"] = ""  # Suppress browser download messages
os.environ["PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD"] = "1"  # Skip automatic downloads
os.environ["DEBUG"] = ""  # Disable debug logging
os.environ["PWDEBUG"] = "0"  # Disable debug mode

# Now set up our complete logging configuration
# Configure root logger to suppress all output and set to highest level
root_logger = logging.getLogger()
root_logger.setLevel(logging.CRITICAL)  # Only show critical errors

# Make sure no handlers are attached to the root logger
for handler in root_logger.handlers[:]:
    root_logger.removeHandler(handler)

# Set up file handler for all loggers
file_handler = logging.FileHandler(LOG_FILE, mode="a")
file_handler.setFormatter(
    logging.Formatter("%(asctime)s [%(name)s] [%(levelname)s] %(message)s")
)

# Configure our app's logging to go to file
app_logger = logging.getLogger("browser-mcp")
app_logger.setLevel(logging.INFO)
app_logger.addHandler(file_handler)
app_logger.propagate = False  # Don't propagate to parent loggers

# Capture all third-party library logs and send to file instead of stdout
# Add more logger names that might be used by dependencies
for logger_name in [
    "playwright",
    "langchain",
    "mcp",
    "browser_use",
    "root",
    "uvicorn",
    "fastapi",
    "starlette",
]:
    logger = logging.getLogger(logger_name)

    # Remove any existing handlers
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    logger.setLevel(logging.WARNING)
    logger.addHandler(file_handler)
    logger.propagate = False  # Don't propagate to parent loggers


def check_playwright_installed():
    """
    Check if playwright and its browsers are installed by attempting to launch a browser.
    This is more reliable than checking command line tools.
    """
    success, browsers = check_playwright_browsers()
    if success:
        app_logger.info(f"Playwright is installed with browsers: {', '.join(browsers)}")
    return success


def install_playwright_browsers():
    """Install Chromium browser using the Python API"""
    app_logger.info("Installing Chromium browser...")
    try:
        from playwright.sync_api import sync_playwright
        import sys
        import subprocess

        # Install only Chromium browser
        subprocess.run(
            [sys.executable, "-m", "playwright", "install", "chromium"], check=True
        )

        # Verify installation by attempting to create a playwright instance
        with sync_playwright() as p:
            try:
                browser = p.chromium.launch()
                browser.close()
            except Exception as e:
                app_logger.error(f"Failed to verify Chromium installation: {e}")
                return False

        app_logger.info("Chromium browser installed and verified successfully.")
        return True
    except Exception as e:
        app_logger.error(f"Error installing Chromium browser: {e}")
        return False


def main():
    """
    Main entry point for browser-mcp.
    This is used when running the package directly.
    """
    # Restore original stdout before running MCP
    sys.stdout = original_stdout

    if not check_playwright_installed():
        app_logger.info("Attempting to install Playwright browsers...")
        if not install_playwright_browsers():
            app_logger.error(
                "Failed to install playwright browsers. Please run 'playwright install' manually."
            )
            sys.exit(1)

        if not check_playwright_installed():
            app_logger.error(
                "Playwright browsers installation verification failed. Please check your installation."
            )
            sys.exit(1)

    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
