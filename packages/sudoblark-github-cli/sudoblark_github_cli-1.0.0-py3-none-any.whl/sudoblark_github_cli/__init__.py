"""Top-level package for app"""

__app_name__ = "sudoblark-github-cli"
__version__ = "1.0.0"

# Below maps error codes to human-readable output
(SUCCESS, PARAMETER_ERROR, FILE_ERROR) = range(3)

ERRORS = {
    PARAMETER_ERROR: "Incorrect parameter(s) provided to command",
    FILE_ERROR: "Error with i/o for file",
}
