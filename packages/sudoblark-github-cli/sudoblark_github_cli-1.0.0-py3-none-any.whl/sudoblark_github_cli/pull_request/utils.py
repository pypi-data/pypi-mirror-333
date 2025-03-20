import copy
from typing import List
from rich.table import Table
from sudoblark_python_core.github.pull_request import PullRequest
from sudoblark_python_core.github.comments import Comment
from sudoblark_github_cli.console import CONSOLE
import logging
from sudoblark_github_cli.utils import LoggingUtils


class PullRequestUtils:

    @staticmethod
    def display_comments(comments: List[Comment]) -> None:  # pragma: no cover
        """
        Simple helper to display n Comment instances on the Command Line

        Args:
            comments (List[Comment]): List of Comment instances to display
        """
        table: Table = Table(title="Comments")
        table.add_column("#", justify="right", style="cyan", no_wrap=True)
        table.add_column("Author", style="green")
        table.add_column("Body", style="white")

        for comment in comments:
            table.add_row(str(comment.identifier), str(comment.author), str(comment.body))
        CONSOLE.print(table)

    @staticmethod
    def display_pull_requests(pull_requests: List[PullRequest]) -> None:  # pragma: no cover
        """
        Simple helper to display n PullRequest instances on the command line

        Args:
            pull_requests (List[PullRequest]): List of PullRequest instances to display
        """

        table: Table = Table(title="Pull Requests")
        table.add_column("#", justify="right", style="cyan", no_wrap=True)
        table.add_column("Title", style="magenta", justify="right")
        table.add_column("State", style="green")

        for pull_request in pull_requests:
            table.add_row(str(pull_request.number), pull_request.title, pull_request.state)
        CONSOLE.print(table)

    @staticmethod
    def return_filtered_comments_list(original_comments: List[Comment], author: str = None, comment_id: int = None) -> List[Comment]:
        """
        Simple helper to filter out a list of comments based on author name or comment_id, retaining the original ordering.

        Args:
            original_comments (List[Comment]): List of Comment instances to filter
            author (str): Case insensitive author name to filter by, defaults to None
            comment_id (int): Comment ID to filter by

        Returns:
                List of comment instances authored by author arg
        """
        def filter_comments():
            for comment in original_comments:
                if author is not None and (comment.author.lower() == author.lower()):
                    new_list.append(comment)
                elif comment_id is not None and (comment.identifier == comment_id):
                    new_list.append(comment)
                else:
                    logger.debug("Filtered out comment '%s' by author '%s' with id '%s'" %
                                 (comment.identifier, comment.author, comment.identifier))
        logger: logging.Logger = LoggingUtils.return_logger(__name__)
        new_list: List[Comment] = []
        if author is not None or comment_id is not None:
            filter_comments()
        else:
            new_list = copy.deepcopy(original_comments)
        return new_list
