
def parse_arguments(arguments):
    '''Parses command line arguments for add_blocks.py,
       add_nmrpipe_blocks.py and apply_fid_com.py.
       output:  dict with arguments.

    '''

    directories = []
    out_dir = None
    scaling_factor_tuples = []
    fid_com = None
    skip = False

    while arguments:
        argument = arguments.pop(0)
        if argument == '-out':
            out_dir = arguments.pop(0)
        elif len(argument) > 2 and argument[:2] == '-c':
            dir_index = int(argument[2:])-1
            scaling_factor = arguments.pop(0)
            scaling_factor_tuples.append((dir_index, scaling_factor))
        elif '.com' in argument or '.csh' in argument or '.sh' in argument:
            fid_com = argument
        elif argument == '-skip':
            skip = True
        else:
            directories.append(argument)

    scaling_factors = [1.0]*len(directories)
    for i, scaling_factor in scaling_factor_tuples:
        scaling_factors[i] = scaling_factor

    return {'directories': directories,
            'out_dir': out_dir,
            'scaling_factors': scaling_factors,
            'fid_com': fid_com,
            'skip': skip}
