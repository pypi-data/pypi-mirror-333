import os
import re
import zipfile
from pathlib import Path
from typing import List, Optional, Union, Dict, Any
from gitignore_parser import parse_gitignore

__version__ = "1.0.0"


def match_git(path: str) -> bool:
    """Check if a path is a git-related file or directory.

    Parameters
    ----------
    path : str
        File or directory path to check.

    Returns
    -------
    bool
        True if the path contains '.git', False otherwise.
    """
    return ".git" in path


def match_extra(path: str, extra_ignore: List[str]):
    """Check if any strings in extra_ignore are contained in the given path.

    Parameters
    ----------
    path : str
        File or directory path to check.
    extra_ignore : List[str]
        List of strings to check against the path.

    Returns
    -------
    bool
        True if any string in extra_ignore is found in path, False otherwise.

    Raises
    ------
    ValueError
        If extra_ignore is not a list or contains non-string elements.
    """
    if not type(extra_ignore) == list:
        raise ValueError(f"extra_ignore should be a list of strings, but it is a {type(extra_ignore)}")
    if not all([isinstance(pattern, str) for pattern in extra_ignore]):
        types = list(set([type(pattern).__name__ for pattern in extra_ignore]))
        types_formatted = ", ".join(types)
        raise ValueError(f"extra_ignore should be a list of strings, but it contains the following types: {types_formatted}")
    return any([pattern in path for pattern in extra_ignore])


def match_regexp(path: str, regexp_ignore: List[str]):
    """Check if any regular expressions in regexp_ignore match the given path.

    Parameters
    ----------
    path : str
        File or directory path to check.
    regexp_ignore : List[str]
        List of regular expression patterns to match against the path.

    Returns
    -------
    bool
        True if any pattern in regexp_ignore matches the path, False otherwise.

    Raises
    ------
    ValueError
        If regexp_ignore is not a list or contains non-string elements.
    """
    if not type(regexp_ignore) == list:
        raise ValueError(f"extra_ignore should be a list of strings, but it is a {type(regexp_ignore)}")
    if not all([isinstance(pattern, str) for pattern in regexp_ignore]):
        types = list(set([type(pattern).__name__ for pattern in regexp_ignore]))
        types_formatted = ", ".join(types)
        raise ValueError(f"regexp_ignore should be a list of strings, but it contains the following types: {types_formatted}")
    matches = [re.search(pattern, path) for pattern in regexp_ignore]
    return any(matches)


def check_ignore(
    path: str,
    ignore_git: bool = False,
    gitparser: Optional[object] = None,
    extra_ignore: Optional[List[str]] = None,
    regexp_ignore: Optional[List[str]] = None,
) -> bool:
    """Check if a path should be ignored based on multiple filtering criteria.

    Parameters
    ----------
    path : str
        File or directory path to check.
    ignore_git : bool, default=False
        If True, checks for git-related paths.
    gitparser : Optional[object], default=None
        Gitignore parser object that implements a callable interface.
    extra_ignore : Optional[List[str]], default=None
        List of strings to check against the path.
    regexp_ignore : Optional[List[str]], default=None
        List of regular expression patterns to match against the path.

    Returns
    -------
    bool
        True if any of the ignore conditions are met, False otherwise.
    """
    if ignore_git:
        if match_git(path):
            return True
    if gitparser is not None:
        if gitparser(path):
            return True
    if extra_ignore is not None:
        if match_extra(path, extra_ignore):
            return True
    if regexp_ignore is not None:
        if match_regexp(path, regexp_ignore):
            return True
    return False


def freezedry(
    directory_path: Union[str, Path, os.PathLike],
    output_path: Optional[Union[str, Path, os.PathLike]] = None,
    ignore_git: bool = False,
    use_gitignore: bool = False,
    gitignore_path: Optional[Union[str, bytes, os.PathLike]] = None,
    extra_ignore: Optional[List[str]] = None,
    regexp_ignore: Optional[List[str]] = None,
    ignore_by_directory: bool = True,
    verbose: bool = True,
    zipfile_arguments: Optional[Dict[str, Any]] = {},
):
    """Create a zip file of the contents of a directory, with filtering options.

    This function creates a compressed zip archive of a directory's contents while
    providing various filtering options to exclude unwanted files and directories.

    Parameters
    ----------
    directory_path : Union[str, Path, os.PathLike]
        Path to the directory to compress
    output_path : Union[str, Path, os.PathLike]
        Path where the output zip file should be created. If not provided, defaults to
        '<directory_path>/compressed_directory.zip'.
    ignore_git : bool, default=False
        If True, ignores any files with '.git' in their path.
    use_gitignore : bool, default=False
        If True, ignores files based on .gitignore rules.
    gitignore_path : str or os.PathLike, optional
        Path to .gitignore file. If not provided but use_gitignore=True,
        looks for .gitignore in directory_path.
    extra_ignore : list of str, optional
        List of strings - files containing any of these strings will be ignored.
    regexp_ignore : list of str, optional
        List of regular expressions - files matching any of these will be ignored.
    ignore_by_directory : bool, default=True
        If True, ignores all files in a directory that meets ignore criteria.
        If False, checks each file individually.
    verbose : bool, default=True
        If True, prints names of files as they are added to the zip.
    zipfile_arguments : dict, optional
        Additional keyword arguments passed to zipfile.ZipFile constructor.

    Returns
    -------
    None
        Creates a zip file at the specified output_path.

    Raises
    ------
    AssertionError
        If directory_path is not a directory or if gitignore file is not found
        when use_gitignore=True.
    ValueError
        If the input parameters are invalid
    RuntimeError
        If there are issues creating the zip file

    Examples
    --------
    >>> # Basic usage
    >>> freezedry("my_project")

    >>> # Ignore git files and use .gitignore rules
    >>> freezedry("my_project", ignore_git=True, use_gitignore=True)

    >>> # Custom ignore patterns
    >>> freezedry("my_project", extra_ignore=["__pycache__", ".pyc"])
    """
    assert "r" != zipfile_arguments.get("mode")  # cannot be in read mode for writing a new zipfile
    assert os.path.isdir(directory_path), f"{directory_path} is not a directory"

    if output_path is None:
        output_path = os.path.join(directory_path, "compressed_directory.zip")

    if use_gitignore:
        if gitignore_path is None:
            gitignore_path = os.path.join(directory_path, ".gitignore")
        assert os.path.exists(gitignore_path), f".gitignore file not found at {gitignore_path}"
        gitparser = parse_gitignore(gitignore_path)
    else:
        gitparser = None

    check_arguments = dict(
        ignore_git=ignore_git,
        gitparser=gitparser,
        extra_ignore=extra_ignore,
        regexp_ignore=regexp_ignore,
    )

    # Prepare list for copying files
    files_to_copy = []
    archive_names = []
    for dirpath, dirnames, files in os.walk(directory_path):
        if check_ignore(dirpath, **check_arguments):
            if ignore_by_directory:
                # clear any files from within this path using in-place method
                # to ignore any children files of an ignored directory
                dirnames[:] = []
        else:
            # Filter files based on specified rules
            path_to_files = [os.path.normpath(os.path.join(dirpath, f)).replace(os.sep, "/") for f in files]
            keep_files = [f for f in path_to_files if not check_ignore(f, **check_arguments)]

            for file in keep_files:
                # Add file to the copy list
                files_to_copy.append(file)
                archive_names.append(os.path.relpath(file, directory_path))

    # create zip file
    zipfile_arguments = zipfile_arguments or dict(compression=zipfile.ZIP_DEFLATED)
    with zipfile.ZipFile(output_path, mode="w", **zipfile_arguments) as zipf:
        if verbose:
            print(f"Writing the following files to {output_path}")
        # go through directory and write any files
        for file, name in zip(files_to_copy, archive_names):
            zipf.write(file, arcname=name)
            if verbose:
                print(": ", name, "<--", file)
