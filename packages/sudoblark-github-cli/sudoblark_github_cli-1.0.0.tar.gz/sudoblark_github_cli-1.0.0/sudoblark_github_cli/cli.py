"""
This is the main CLI interface of the application. It is simply an entrypoint,
actual operations are intended to be performed by sub-interfaces. Here we
just map them to high-level namespaces.
"""

import logging

# Our modules
from sudoblark_github_cli.utils import LoggingUtils
from sudoblark_github_cli.utils import main_callback
from sudoblark_github_cli.pull_request.cli import app as PullRequestApp

# Third-party modules
import typer

app = typer.Typer(
    help="CLI tooling intended to automate operations against GitHub within a CI/CD, or other such programmatic. "
    "setting. All commands require a valid GITHUB_TOKEN environment variable to operate.",
    callback=main_callback,
)

app.add_typer(PullRequestApp, name="pull-request")


@app.command("debug-log-config")
def debug_log_config() -> None:
    """
    Outputs log messages at all levels, intended as an easy test for your log config.
    """
    logger: logging.Logger = LoggingUtils.return_logger(__name__)
    logger.debug("debug test message")
    logger.info("info test message")
    logger.warning("warning test message")
    logger.error("error test message")
    logger.critical("critical test message")
