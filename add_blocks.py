#! /usr/bin/python

'''
Convert to nmr pipe format and add blocks of nmr data.

example:

add_blocks.py path/to/fid.com 12 14 66 68 -out <dir_name>

uses the specified fid.com to convert the fids in all
directories to nmr pipe format and afterwards adds them
up. If no output directory is specified, the script will
output a directory called 'added_12_14_66_68'.

If no fid.com is specified, a search through the
directories will be done for a file called 'fid.com'.
If one is found, this will be used to convert all
data in all directories.

If the conversion to nmr pipe format should be skipped
in directories that already contain a fid directory,
the -skip argument can be supplied.

This script completely depends on NMR pipe, so
this should be installed.


Copyright (C) 2015 Joren Retel

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later version.
This program is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program.
If not, see http://www.gnu.org/licenses/.

'''
from parse_arguments import parse_arguments
from add_nmrpipe_blocks import add_experiments
from apply_fid_com import copy_and_run_script
import sys


def convert_and_add_blocks(directories, fid_com=None,
                           scaling_factors=None, out_dir=None,
                           skip=False):
    '''Convert and add fid's'''

    copy_and_run_script(directories, fid_com, skip=skip)
    add_experiments(directories, scaling_factors, out_dir)


if __name__ == '__main__':
    arguments = sys.argv[1:]
    if not arguments:
        print __doc__
    else:
        parsed = parse_arguments(arguments)
        convert_and_add_blocks(directories=parsed['directories'],
                               fid_com=parsed['fid_com'],
                               scaling_factors=parsed['scaling_factors'],
                               out_dir=parsed['out_dir'],
                               skip=parsed['skip'])
