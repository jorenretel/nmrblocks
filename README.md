
nmrblocks
=========

NMR spectra are often recorded in several blocks to cope with magnetic field drift. These scripts can help add up blocks of nmr data. They completely rely on nmr pipe (http://spin.niddk.nih.gov/NMRPipe/), so that should be installed in order to use these scripts. Most users might just want to use the script 'add_blocks.py', since it combines the functionality from both add_nmrpipe_blocks.py and apply_fid.com. Notice that even if you only want to use this script, still the other scripts should be available to it and should therefor be downloaded aswell.

Quick example:

```shell

add_blocks.py path/to/fid.com 12 14 66 68 -out /path/to/output/directory

```

to add up experiments 12 14 66 and 68. add_blocks.py uses the specified fid.com to convert the fids in all directories to nmr pipe format and afterwards adds them up. If no output directory is specified, the script will output a directory called something like 'added_12_14_66_68'.

If no fid.com is specified, a search through the directories will be done for a file called 'fid.com'. If one is found, this will be used to convert all data in all directories. If the conversion to nmr pipe format should be skipped in directories that already contain a fid directory, the -skip argument can be supplied.

If you want to apply a scaling factor to the different experiments this is possible like this:

```shell

add_blocks.py path/to/fid.com 12 14 66 68 -out /path/to/output/directory -c2 1.6 -c4 20.38

```

to multiply experiment 14 and 68 with factors of 1.6 and 20.38 respectively.


## 'installation'

There is no real installation required except adding the directory these scripts are located in to your path and making the scripts executable. Adding the directory to your allows your operating system to find the scripts so that you can execute them in any directory you want.
On linux or osx you can do this as follows: If you are using bash as your shell language, you can do it by adding this line to your .bashrc file (in your home folder):

```bash

export PATH="/path/to/nmrblocks:$PATH"

```
or if you are using csh, add this line to your .cshrc file (also in your home folder):

```csh

set path = ($path /path/to/nmrblocks)

```

If you don't know whether you are using bash or csh
type:

echo $SHELL

in your terminal.

Notice that in order to make these changes become active you have to (re-)initialize your shell. The easiest way to do this is by just opening a new one.

To make for instance the add_blocks.py script executable, navigate in the terminal to the directory these scripts are located in and type:

```shell

chmod +x add_blocks.py

```


## Copyright Notice

Copyright (C) 2015 Joren Retel

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later version.
This program is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program.
If not, see http://www.gnu.org/licenses/.