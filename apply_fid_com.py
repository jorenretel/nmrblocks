#! /usr/bin/python

'''
Copy and apply a csh script to a set of directories.
The usecase that I had in mind writing this script
was using the same fid.com csh script for the conversion
of nmr data to NMR pipe format in multiple directories:

apply_fid_com.py path/to/fid.com 12 14 66 68

to copy and run the script fid.com in 'path/to' in
the directories 12, 14, 66 and 68. The script does
not have to be called 'fid.com'. However, if no fid.com
is specified, a search through the directories will be
done for a file called 'fid.com'. If one is found, this
will be used to convert all data in all directories.

If directories that already contain a fid directory
should be skipped the -skip argument can be supplied.

To use this script with NMR pipe conversion scripts,
NMR pipe should of course be installed. When used
with a typical NMR pipe converion script (fid.com),
in every directory a 'fid' sub-directory will be added.

To run this script wherever you want, you have
to add the directory this script recides in to
your path.
If you are using bash, you can do that by adding this line
to your .bashrc file (in your home folder):

export PATH="{script_path}:$PATH"

or if you are using csh this line to your .cshrc file
(also in your home folder):

set path = ($path {script_path})

If you don't know whether you are using bash or csh
type:

echo $SHELL

in your terminal.

Also don't forget to make this file executable by
typing:

chmod +x apply_fid_com.py

in the directory this file recides in.



Copyright (C) 2015 Joren Retel

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version. This program is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
more details.

You should have received a copy of the GNU General Public License along with
this program. If not, see http://www.gnu.org/licenses/.

'''

from subprocess import call
from shutil import copy
from os.path import abspath, join, split, exists
import sys
from parse_arguments import parse_arguments


def copy_and_run_script(directories, fid_com=None, skip=False):
    '''Copies the fid_com script to all directories and
       runs it in csh. If no fid_com is defined, the
       directories are searched for a file that is literally
       called 'fid.com'. The first one that is encountered is
       used to convert all datasets. If skip is set to True
       the conversion is skipped for directories that already
       contain a directory called 'fid'.

    '''

    directories = [abspath(directory) for directory in directories]

    if not fid_com:
        fid_com = find_fid_com(directories)
    if not fid_com:
        print 'No fid.com file defined or found.'
        return
    fid_com = abspath(fid_com)
    filename = split(fid_com)[-1]
    for directory in directories:

        if skip is True and exists(join(directory, 'fid')):
            continue

        destination = join(directory, filename)
        if not fid_com == destination:
            copy(fid_com, destination)
        print 'Running {filename} in {directory}'.format(filename=filename,
                                                         directory=directory)
        call_in_csh(destination, cwd=directory)


def find_fid_com(directories):
    '''Searches directories for a file called 'fid.com'.'''

    for directory in directories:
        fid_com = join(directory, 'fid.com')
        if exists(fid_com):
            return fid_com


def call_in_csh(command_list, cwd=None):
    '''Call command in csh.'''

    command_list = ['csh', '-c'] + [command_list]
    call(command_list, cwd=cwd)

if __name__ == '__main__':
    arguments = sys.argv[1:]
    if not arguments:
        print __doc__.format(script_path=sys.argv[0])
    else:
        parsed = parse_arguments(arguments)
        copy_and_run_script(directories=parsed['directories'],
                            fid_com=parsed['fid_com'],
                            skip=parsed['skip'])

