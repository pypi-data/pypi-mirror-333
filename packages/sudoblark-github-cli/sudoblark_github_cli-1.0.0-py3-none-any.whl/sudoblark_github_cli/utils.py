import os
from sudoblark_github_cli.state import STATE
from typing import Optional
from sudoblark_github_cli.constants import LogLevel
from sudoblark_github_cli.constants import DEFAULT_LOG_FORMAT
import logging
import typer
from sudoblark_github_cli import __app_name__, __version__
from sudoblark_github_cli import SUCCESS
from sudoblark_python_core.github.repository import Repository
from sudoblark_python_core.github.pull_request import PullRequest
from typing import Union
from sudoblark_python_core import GitHubClient


class IOUtils:
    @staticmethod
    def read_content_from_file(file_path: str) -> str:
        """
        Reads content of a file and returns it as a string.

        Args:
            file_path (str): The path to the file we wish to read

        Raises:
            IOError if unable to read from file for whatever reason
        """
        logger: logging.Logger = LoggingUtils.return_logger(__name__)
        logger.debug("Attempting to read content from file %s", file_path)
        content = None
        try:
            with open(file_path, "r") as file:
                content = file.read()
            return content
        except Exception as e:
            logger.error("Unable to open content file at path %s" % file_path)
            logger.error("Error as follows: %s", exc_info=e)
            raise IOError("Unable to read content file at path %s" % file_path)


class TyperUtils:
    @staticmethod
    def set_log_level(level: Optional[LogLevel]):
        """Sets the logging level for a single execution of the application

        Args:
            level (Optional[LogLevel]): The log level to use.
        """
        STATE["LOG_LEVEL"] = level.upper()
        if "LOG_LEVEL" in os.environ.keys():
            STATE["LOG_LEVEL"] = os.environ["LOG_LEVEL"].upper()

    @staticmethod
    def set_log_format(log_format: Optional[str]):
        """Sets the log format for a single execution of the application

        Args:
            log_format (Optional[str]): The log format to use.
        """
        STATE["LOG_FORMAT"] = log_format
        if "LOG_FORMAT" in os.environ.keys():
            STATE["LOG_FORMAT"] = os.environ["LOG_FORMAT"]


class LoggingUtils:
    @staticmethod
    def return_logger(name: str) -> logging.Logger:
        """Creates, and returns, a LOGGER given values from STATE

        Args:
            name (str): The name of the logger to return

        Returns:
            Logger with the given name
        """
        new_logger: logging.Logger = logging.getLogger(name)
        new_logger.setLevel(STATE["LOG_LEVEL"])
        stream_handler: logging.StreamHandler = logging.StreamHandler()
        stream_handler.setFormatter(logging.Formatter(STATE["LOG_FORMAT"]))
        new_logger.addHandler(stream_handler)
        return new_logger


class SudoblarkPythonCoreUtils:
    @staticmethod
    def create_github_client() -> GitHubClient:
        """

        Raises:
            ValueError if GITHUB_TOKEN environment variable is not set

        Returns:
            GitHubClient instance
        """
        GITHUB_TOKEN: Union[None, str] = os.getenv("GITHUB_TOKEN")
        if GITHUB_TOKEN is None:
            raise ValueError("GITHUB_TOKEN environment variable is not set")
        return GitHubClient(GITHUB_TOKEN)

    @staticmethod
    def lookup_repository(repository_name: str) -> Repository:
        """

        Raises:
            ValueError if unable to find repository in GitHub

        Returns:
            Repository instance
        """
        logger: logging.Logger = LoggingUtils.return_logger(__name__)
        client: GitHubClient = SudoblarkPythonCoreUtils.create_github_client()
        repo_owner, repo_name = repository_name.split("/")
        repository_object: Repository = client.get_repository(repo_owner, repo_name)
        if repository_object is None:
            logger.error("Unable to find repository with owner '%s' and name '%s'" % (repo_owner, repo_name))
            raise ValueError("Unable to find repository with owner '%s' and name '%s'" % (repo_owner, repo_name))
        logger.debug("Found repository with owner '%s' and name '%s'" % (repo_owner, repo_name))
        return repository_object

    @staticmethod
    def lookup_pull_request(repository_name: str, pull_request_number: int) -> PullRequest:
        """
        Raises:
            ValueError if unable to find pull request in GitHub

        Returns:
            PullRequest instance
        """
        logger: logging.Logger = LoggingUtils.return_logger(__name__)
        repository_object: Repository = SudoblarkPythonCoreUtils.lookup_repository(repository_name)
        pull_request: Union[None, PullRequest] = repository_object.get_pull_request(pull_request_number)
        if pull_request is None:
            logger.error("Unable to find pull request '%s' on repository '%s'" % (str(pull_request_number), repository_name))
            raise ValueError("Unable to find pull request '%s' on repository '%s'" % (str(pull_request_number), repository_name))
        return pull_request


def _version_callback(value: bool) -> None:  # pragma: no cover
    if value:
        typer.echo(f"{__app_name__} v{__version__}")
        raise typer.Exit(SUCCESS)


def main_callback(
    log_level: Optional[LogLevel] = typer.Option(
        LogLevel.INFO,
        "--log-level",
        "-log",
        help="Set the logging level for the application, can also override with LOG_LEVEL environment variable",
        show_default=True,
        show_choices=True,
        case_sensitive=False,
        callback=TyperUtils.set_log_level,
    ),
    log_format: Optional[str] = typer.Option(
        DEFAULT_LOG_FORMAT,
        "--log-format",
        "--format",
        help="Set the logging format for the application, can also override with LOG_FORMAT environment variable",
        show_default=True,
        callback=TyperUtils.set_log_format,
    ),
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        help="Show the application's version and exit.",
        callback=_version_callback,
        is_eager=True,
    ),
) -> None:  # pragma: no cover
    return
