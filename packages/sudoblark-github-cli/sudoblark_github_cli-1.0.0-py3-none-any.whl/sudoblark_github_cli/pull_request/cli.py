"""
This CLI interface is expected to interaction with pull requests.

It is simply the entrypoint for such commands, actual operations are performed by
underlying nested callback functions or nested CLI interfaces.

It is expected to operate as a nested sub-interface of the overall CLI application.
"""

import logging

# Third-party modules
import typer
from typing import List

# Our modules
from sudoblark_github_cli.utils import SudoblarkPythonCoreUtils
from sudoblark_github_cli.utils import LoggingUtils
from sudoblark_github_cli.utils import IOUtils
from sudoblark_github_cli.pull_request.constants import PermissiblePullRequestStates
from sudoblark_github_cli.utils import main_callback
from sudoblark_github_cli.pull_request.utils import PullRequestUtils
from sudoblark_python_core.github.repository import Repository
from sudoblark_python_core.github.pull_request import PullRequest
from sudoblark_python_core.github.comments import Comment
from sudoblark_github_cli import PARAMETER_ERROR

app = typer.Typer(help="Interact with pull requests", callback=main_callback)


@app.command("create-comment")
def create_comment(
        repository_name: str = typer.Option(..., "--repository", "-re",
                                            help="Repository to query in form of " "owner/repository."),
        pull_request_number: int = typer.Option(
            ..., "--pull-request-number", "-pr", help="Number of the pull request we wish to create a comment on"
        ),
        content_file_path: str = typer.Option(
            ...,
            "--content-file-path",
            "-cf",
            help="Path to a file containing the content of the comment we wish to " "create, should be either HTML or markdown format.",
        ),
):
    """
    Create a new comment on a given pull request on a given repository.

    Examples: \n
        Create a new comment on a pull request:\n
        create-comment --repository sudoblark/sudoblark.python.core --pull-request-number 3 --content-file-path test.md
    """
    logger = LoggingUtils.return_logger(__name__)
    logger.debug(
        "Starting execution for \n%s"
        % (
                "create-comment --repository %s --pull-request-number %s "
                "--content-file-path %s" % (repository_name, pull_request_number, content_file_path)
        )
    )
    pull_request: PullRequest = SudoblarkPythonCoreUtils.lookup_pull_request(
        repository_name=repository_name, pull_request_number=pull_request_number
    )
    pull_request.post_comment(body=IOUtils.read_content_from_file(content_file_path))
    logger.info("Created comment on pull request '%s' in repository '%s'.", pull_request_number, repository_name)


@app.command("read-comment")
def read_comment(
        repository_name: str = typer.Option(..., "--repository", "-re",
                                            help="Repository to query in form of owner/repository."),
        pull_request_number: int = typer.Option(
            ..., "--pull-request-number", "-pr", help="Number of the pull request we wish to create a comment on"
        ),
        author: str = typer.Option("NA", "--author", "-au", help="Author to filter comments for."),
):
    """
    Read comments on a given pull request on a given repository, optionally
    filtered by user, and output in a verbose table.

    Examples: \n
    Get all comments regardless of user: \n
    read-comment --repository vexx32/pskoans --pull-request-number 241 \n\n

    Get all comments, filtered by user:
    read-comment --repository vexx32/pskoans --pull-request-number 241 --author benjaminlukeclark \n\n
    """
    logger = LoggingUtils.return_logger(__name__)
    logger.debug(
        "Starting execution for \n%s"
        % ("read-comment --repository %s --pull-request-number %s " "--author %s" % (
        repository_name, pull_request_number, author))
    )
    pull_request: PullRequest = SudoblarkPythonCoreUtils.lookup_pull_request(
        repository_name=repository_name, pull_request_number=pull_request_number
    )
    comments: List[Comment] = PullRequestUtils.return_filtered_comments_list(
        original_comments=pull_request.get_comments(),
        author=None if author == "NA" else author,
        comment_id=None
    )
    PullRequestUtils.display_comments(comments)


@app.command("update-comment")
def update_comment(
        repository_name: str = typer.Option(..., "--repository", "-re",
                                            help="Repository to query in form of owner/repository."),
        pull_request_number: int = typer.Option(
            ..., "--pull-request-number", "-pr", help="Number of the pull request we wish to create a comment on"
        ),
        author: str = typer.Option("NA", "--author", "-au", help="Author to filter comments for."),
        comment_id: int = typer.Option(-1, "--comment-id", "-cid", help="Specific comment ID to update"),
        content_file_path: str = typer.Option(
            ...,
            "--content-file-path",
            "-cf",
            help="Path to a file containing the content of the comment we wish to " "create, should be either HTML or markdown format.",
        ),
        overwrite: bool = typer.Option(False, "--overwrite", "-o",
                                       help="Overwrite existing comment rather than appending."),
):
    """
    Update an explicit comment, or the last comment by a given user, on a given
    pull request on a given repository.

    Examples: \n
        Update last comment by a given user: \n
        update-comment --repository sudoblark.python.core --pull-request-number 3 --author sudoblark-bot --content-file-path update.md \n\n

        Update an explicit comment ID: \n
        update-comment --repository sudoblark.python.core --pull-request-number 3 --comment-id 2679890418 --content-file-path update.md \n\n
    """
    logger = LoggingUtils.return_logger(__name__)
    logger.debug(
        "Starting execution for \n%s"
        % (
                "update-comment --repository %s --pull-request-number %s "
                "--author %s --comment-id %s --content-file-path %s --overwrite %s"
                % (repository_name, pull_request_number, author, str(comment_id), content_file_path, str(overwrite))
        )
    )
    if author.upper() != "NA" and comment_id != -1:
        logger.error("--author and --comment-id are mutually exclusive, only provide one or the other.")
        return PARAMETER_ERROR

    pull_request: PullRequest = SudoblarkPythonCoreUtils.lookup_pull_request(
        repository_name=repository_name, pull_request_number=pull_request_number
    )
    content: str = IOUtils.read_content_from_file(content_file_path)
    comments: List[Comment] = PullRequestUtils.return_filtered_comments_list(
        original_comments=pull_request.get_comments(),
        author=None if author == "NA" else author,
        comment_id=None if comment_id == -1 else comment_id
    )
    if len(comments) == 0:
        logger.error("Unable to find comment on pull request '%s' in repository '%s' with author '%s' or id '%s'",
                     pull_request_number, repository_name, author, comment_id
                     )
    elif overwrite:
        comments[-1].overwrite(content)
        logger.info("Overwritten comment on pull request '%s' in repository '%s'.", pull_request_number,
                    repository_name)
    else:
        comments[-1].update(content)
        logger.info("Updated comment on pull request '%s' in repository '%s'.", pull_request_number,
                    repository_name)


@app.command("delete-comment")
def delete_comment(
        repository_name: str = typer.Option(..., "--repository", "-re",
                                            help="Repository to query in form of owner/repository."),
        pull_request_number: int = typer.Option(
            ..., "--pull-request-number", "-pr", help="Number of the pull request we wish to delete a comment on"
        ),
        author: str = typer.Option("NA", "--author", "-au", help="Author to filter comments for."),
        comment_id: int = typer.Option(-1, "--comment-id", "-cid", help="Specific comment ID to delete"),
):
    """
    Delete an explicit comment, or the last comment by a given user, on a given
    pull request on a given repository.

    Examples: \n
        Delete last comment by a given user: \n
        delete-comment --repository sudoblark.python.core --pull-request-number 3 --author sudoblark-bot

        Delete an explicit comment ID: \n
        delete-comment --repository sudoblark.python.core --pull-request-number 3 --comment-id 2679890418
    """
    logger = LoggingUtils.return_logger(__name__)
    logger.debug(
        "Starting execution for \n%s"
        % (
                "delete-comment --repository %s --pull-request-number %s "
                "--author %s --comment-id %s"
                % (repository_name, pull_request_number, author, str(comment_id))
        )
    )
    if author.upper() != "NA" and comment_id != -1:
        logger.error("--author and --comment-id are mutually exclusive, only provide one or the other.")
        return PARAMETER_ERROR

    pull_request: PullRequest = SudoblarkPythonCoreUtils.lookup_pull_request(
        repository_name=repository_name, pull_request_number=pull_request_number
    )
    comments: List[Comment] = PullRequestUtils.return_filtered_comments_list(
        original_comments=pull_request.get_comments(),
        author=None if author == "NA" else author,
        comment_id=None if comment_id == -1 else comment_id
    )
    if len(comments) == 0:
        logger.error("Unable to find comment on pull request '%s' in repository '%s' with author '%s' or id '%s'",
                     pull_request_number, repository_name, author, comment_id
                     )
    else:
        comments[-1].delete()
        logger.info("Deleted comment on pull request '%s' in repository '%s'.", pull_request_number,
                    repository_name)


@app.command("list")
def list_pull_requests(
        repository: str = typer.Option(..., "--repository", "-r",
                                       help="Repository to query in form of owner/repository."),
        state: PermissiblePullRequestStates = typer.Option("ALL", "--state", "-s",
                                                           help="State of pull requests to query for"),
) -> None:
    """
    Output a concise table of pull requests for the given repository.

    Examples: \n
        list --repository sudoblark/sudoblark.python.core --state ALL
    """
    logger: logging.Logger = LoggingUtils.return_logger(__name__)
    logger.debug("Starting execution for \n%s" % ("list --repository %s --state %s" % (repository, state)))
    repository: Repository = SudoblarkPythonCoreUtils.lookup_repository(repository)
    pull_requests: List[PullRequest] = repository.get_pull_requests(state=state.value.lower())
    logger.debug(
        "Found '%s' pull requests of state '%s' for repo '%s'" % (len(pull_requests), state.value.lower(), repository))
    PullRequestUtils.display_pull_requests(pull_requests)
