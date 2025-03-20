# pybinlock

`binlock` is a python package for programmatically reading and writing Avid bin lock (`.lck`) files in 
multi-user Avid Media Composer projects.

>[!WARNING]
>While the `.lck` lock file format is a very simple one, it is officially undocumented.  Use this library at your own risk --
>I assume no responsibility for any damage to your project, loss of data, or underwhelming box office performance.

## Interesting Uses

- Permanently locking bins
- Temporarily locking bins while programmatically reading/writing to them
- Custom lock names for displaying short messages, such as why the bin is locked
- Removing "stale" locks

## Installation

Install the `pybinlock` package [from PyPI](https://pypi.org/project/pybinlock/) using `pip`:

```bash
pip install pybinlock
```

Or clone from this repo:

```bash
git clone https://github.com/mjiggidy/pybinlock.git
cd pybinlock
pip install .
```

## Usage

See [readthedocs.io](https://pybinlock.readthedocs.io) for general usage and API documentation!

## See Also
- [`pybinhistory`](https://github.com/mjiggidy/pybinhistory) - Programmatcially read and write Avid bin history log (`.log`) files
