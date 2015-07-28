#! /usr/bin/python

'''
Add up NMR Pipe data from different experiments, example:

add_nmrpipe_blocks.py 12 14 66 68 -c2 2.0 -c3 6.1 -out <dir_name>

to add experiments 12, 14, 66 and 68. Where experiments
14 and 66 are multiplied by 2.0 and 6.1 respectively.

If no output directory is specified, the script will
output a directory called 'added_12_14_66_68'.

This script completely depends on NMR pipe, so
this should be installed. In every experiment
directory there should be a 'fid' directory
produced by a NMR pipe conversion script (fid.com).

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
Foundation, either version 3 of the License, or (at your option) any later version.
This program is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program.
If not, see http://www.gnu.org/licenses/.

'''


from subprocess import call
from os import makedirs, listdir
from shutil import rmtree
from os.path import exists, abspath, join, split, exists
import sys
import re
from parse_arguments import parse_arguments


def add_experiments(exp_dirs, scaling_factors=None, target_dir=None):
    '''This function just calls add_fids, but first makes
       sure the output directory exists and a supplies
       scaling factors (all 1.0) if they are not specified.

    '''

    if not scaling_factors:
        scaling_factors = [1.0]*len(exp_dirs)
    if not target_dir:
        target_dir = create_out_dir_name(exp_dirs)
    target_dir = abspath(target_dir)
    if not exists(target_dir):
        makedirs(target_dir)
    add_fids(exp_dirs, scaling_factors, target_dir)


def add_fids(exp_dirs, scaling_factors, target_dir):
    '''Uses the addNMR command from nmr pipe to add
       up fid's from different experiments. The
       addNMR command only adds up fid's from two
       experiments, therefore this function does it
       in multiple steps.
       arguments:
         expdirs:            the experiment directories,
                             they are supposed to contain
                             a /fid subdirectory with
                             fid's in nmr pipe format.
         scaling_factors:    factor each respective
                             experiment gets multiplied
                             with.
         target_dir:         path to output directory.

    '''

    # making temporary directories
    temp_dir_names = ['temp' + str(i) for i in range(len(exp_dirs)-2)]

    # this is the directory the fids reside in
    pattern = None
    fid_dirs = None
    for filename in listdir(exp_dirs[0]):
        if filename.endswith('.fid'):
            fid_dirs = [abspath(exp_dir) for exp_dir in exp_dirs]
            pattern = filename
            temp_dir_names.append(None)
            break
    else:
        fid_dirs = [join(abspath(exp_dir), 'fid') for exp_dir in exp_dirs]
        pattern = file_pattern_from_dir(fid_dirs[0])
        temp_dir_names.append('fid')

    if not pattern or not fid_dirs:
        raise IOError('Could not find a .fid file or fid directory in experiment directories.')

    temp_dirs = []
    for name in temp_dir_names:
        if not name:
            full_path = target_dir
        else:
            full_path = join(target_dir, name)
            if not exists(full_path):
                makedirs(full_path)
        temp_dirs.append(full_path)

    in1 = fid_dirs[0]
    c1 = scaling_factors[0]
    com = 'addNMR -in1 {in1}/{pattern} -in2 {in2}/{pattern} -out {out}/{pattern} -c1 {c1} -c2 {c2} -verb'

    for fid_dir, scaling_factor, temp_dir in zip(fid_dirs[1:], scaling_factors[1:], temp_dirs):

        in2 = fid_dir
        c2 = scaling_factor
        out = temp_dir
        final_com = com.format(in1=in1,
                               in2=in2,
                               out=out,
                               pattern=pattern,
                               c1=c1,
                               c2=c2)
        in1 = temp_dir
        c1 = 1.0
        print ''
        print final_com
        print ''
        call_in_csh(final_com)

    # Removing all temporary directories, the last one is
    # is actually the final one, so we don't throw that one
    # out.
    for temp_dir in temp_dirs[:-1]:
        print 'removing ', temp_dir
        rmtree(temp_dir)


def create_out_dir_name(directories):
    '''Simple way to generate a directory
       name from the original experiments
       that are added up.

    '''
    return 'added_' + '_'.join(directories)


def file_pattern_from_dir(directory):
    '''Takes a directory and creates
       the naming pattern nmrpipe expects
       for the files it contains.

    '''
    files = listdir(directory)
    if files:
        one_file_name = split(files[0])[-1]
        return create_file_pattern(one_file_name)


def create_file_pattern(filename):
    '''Given a file name, create the naming
       pattern nmr pipe expects.

    '''

    m = re.match('(\w*[a-zA-Z_])([0-9]*)(\.\w*)', filename)
    base, counter, extension = m.groups()
    pattern = base + r'%0' + str(len(counter)) + 'd' + extension
    return pattern


def call_in_csh(command_list):
    '''Call a command in c-shell.'''

    command_list = ['csh', '-c'] + [command_list]
    call(command_list)


if __name__ == '__main__':
    arguments = sys.argv[1:]
    if not arguments:
        print __doc__.format(script_path=sys.argv[0])
    else:
        parsed = parse_arguments(arguments)
        add_experiments(directories=parsed['directories'],
                        scaling_factors=parsed['scaling_factors'],
                        out_dir=parsed['out_dir'])
