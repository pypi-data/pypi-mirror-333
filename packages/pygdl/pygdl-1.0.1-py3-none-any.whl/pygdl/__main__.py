
# @this file is responsible for running the downloader from
# - commandline.

from pygdl import download
from argpi import PathWays, Definition

definition = Definition()
definition.add('@in', 'file', '@f', 'The argument to specify a file')
definition.add('@git', 'git source', '@g', 'The git source in {username}/{repository} format.')
definition.add('@release', 'release version', '@r', "The github release version to look for. (Optional)")
definition.add('@out', 'outpath', '@o', 'The path where it should be downloaded (must exist)')


class cfg:
    file = ''
    git = ''
    release = 'latest'
    outpath = None
config = cfg()


arguments = PathWays(definition)
arguments.register('@in', lambda f: setattr(config, 'file', f), 'EXEC', what_value_expected='Single')
arguments.register('@git', lambda g: setattr(config, 'git', g), 'EXEC', what_value_expected='Single')
arguments.register('@release', lambda r: setattr(config, 'release', r), 'EXEC', what_value_expected='Single', ignore_if_not_present=True)
arguments.register('@out', lambda o: setattr(config, 'outpath', o), 'EXEC', what_value_expected='Single', ignore_if_not_present=True)
arguments.orchestrate


def main():
    status, e = download(config.file, config.git.split('/')[0], config.git.split('/')[1], config.release, config.outpath)
    if not status:
        raise RuntimeError(e)


if __name__.startswith('__main__'):
    status, e = download(config.file, config.git.split('/')[0], config.git.split('/')[1], config.release, config.outpath)
    if not status:
        raise RuntimeError(e)