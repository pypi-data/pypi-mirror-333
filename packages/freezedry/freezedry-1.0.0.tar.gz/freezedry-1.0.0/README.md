# freezedry
A simple method to store a compressed copy of a code repository with customizable filtering of files.

[![PyPI version](https://badge.fury.io/py/freezedry.svg)](https://badge.fury.io/py/freezedry)
[![Documentation Status](https://readthedocs.org/projects/freezedry/badge/?version=latest)](https://freezedry.readthedocs.io/en/latest/?badge=latest)
[![Python Versions](https://img.shields.io/pypi/pyversions/freezedry.svg)](https://pypi.org/project/freezedry/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Tests](https://github.com/landoskape/freezedry/actions/workflows/tests.yml/badge.svg)](https://github.com/landoskape/freezedry/actions/workflows/tests.yml)
[![codecov](https://codecov.io/gh/landoskape/freezedry/branch/main/graph/badge.svg)](https://codecov.io/gh/landoskape/freezedry)

[Full Documentation](https://freezedry.readthedocs.io/) | [GitHub](https://github.com/landoskape/freezedry) | [PyPI](https://pypi.org/project/freezedry/)

Do you ever wish you knew exactly which version of code you used when you made a figure, ran a job
on a HPC cluster, or anything else? Freezedry is the solution! 

With freezedry, you can easily save a compressed copy of an entire file directory that is designed
to focus on _code_. Freezedry is a very simple package-- it only has one method you need to use
(``freezedry``) that takes as input a path to a directory and a path to an output file, along with
a few customizable optional input arguments. 

What does freezedry include? Everything, if you don't specify. However, it's very easy to ignore:
- git related files (i.e. anything with the pattern ``.git`` in the file path)
- anything specified in a ``.gitignore`` file (thank you to [Michael Herrmann](https://github.com/mherrmann))
for the useful [gitignore_parser](https://github.com/mherrmann/gitignore_parser) package.
- anything else you want (including exact string matches and regular expressions).

## Installation
It's on PyPI. If there's any issues, please raise one on this GitHub repo to let me know.
```
pip install freezedry
```

## Usage
Suppose that ``/..dirs../GitHub/your_repo`` contains some code you've been working on. And say you
use the code in ``your_repo`` to do some analyses that are saved to ``/..dirs../results``. Then,
the following block of code will save a copy of your repo to the ``/results`` directory, ignoring
any ``.git`` related files and ignoring anything in your ``.gitignore``. 

```python
from freezedry import freezedry
directory_path = '/..dirs../GitHub/your_repo'
output_path = '/..dirs../results'
freezedry(directory_path, 
          output_path=output_path, 
          ignore_git=True, 
          use_gitignore=True, 
          verbose=True)
```

In addition, you can specify which files to ignore in two other ways:

1. Direct match strings with ``extra_ignore``. This is a list of strings, and if any string in
the list is contained in a file, that file will be ignored. For example, if 
``extra_ignore=['hi', 'world']`` then ``'../hi/test.py'`` and ``'../myworld.py'`` will be ignored.

2. Regular expression strings with ``regexp_ignore``. This is a list of strings used as regular
expressions. The rules are similar to ``extra_ignore``, except that it uses the ``re.search`` 
method to find matches. 

### Setting the .gitignore
If ``.gitignore`` is not provided, then ``freezedry`` will look for it (non-recursively) in 
``directory_path``. Alternatively, you can provide a ``.gitignore`` directly with the optional
argument ``gitignore_path``. Note that you _always_ have to set ``use_gitignore=True`` regardless
of whether you provided a ``gitignore_path``. 

For example:
```python
from freezedry import freezedry
directory_path = '/..dirs../GitHub/your_repo'
output_path = '/..dirs../results'
gitignore_path = '/..dirs../GitHub/my_other_repo/.gitignore'
freezedry(directory_path, 
          output_path=output_path, 
          ignore_git=True, 
          use_gitignore=True, # if False, won't use gitignore_path even if provided!!! 
          gitignore_path=gitignore_path, 
          verbose=True)
```

## Documentation
For full documentation, check it out [here](https://freezedry.readthedocs.io/). You'll find a complete
API reference and more examples of how to use freezedry. 

## Contributing
I'm happy to take issues or pull requests, let me know if you have any ideas on how to make this
better or requests for fixes. 
