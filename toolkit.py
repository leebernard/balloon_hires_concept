import numpy as np
import warnings

def open_cross_section(filename, wn_range=None, verbose=False, skiplines=None):
    with open(filename) as file:
        if skiplines:
            if verbose: print('skiping %d lines' % skiplines)
            raw_data = file.readlines()[skiplines:]
        else:
            raw_data = file.readlines()

        wave_numbers = []
        cross_sections = []

        if verbose:
            print('raw')

        for x in raw_data:
            if x == '\n':
                warnings.warn('Cross section read in terminated early due to empty line!', UserWarning)
                break
            else:
                wave_string, cross_string = x.split()
                wave_numbers.append(float(wave_string))
                cross_sections.append(float(cross_string))
        wave_numbers = np.array(wave_numbers)
        cross_sections = np.array(cross_sections)

    if wn_range is None:
        return wave_numbers, cross_sections
    else:
        # wn range needs to be exactly 2 values
        # explicitly pass those two values
        wn_start, wn_end = wn_range
        return spectrum_slicer_old(wn_start, wn_end, wave_numbers, cross_sections)


def spectrum_slicer_old(start_angstrom, end_angstrom, angstrom_data, spectrum_data):

    start_index = (np.abs(angstrom_data - start_angstrom)).argmin()
    end_index = (np.abs(angstrom_data - end_angstrom)).argmin()
    spectrum_slice = spectrum_data[start_index:end_index]
    angstrom_slice = angstrom_data[start_index:end_index]

    return angstrom_slice, spectrum_slice


def spectrum_slicer(start_angstrom, end_angstrom, dataset):

    start_index = (np.abs(dataset[:, 0] - start_angstrom)).argmin()
    end_index = (np.abs(dataset[:, 0] - end_angstrom)).argmin()

    return dataset[start_index:end_index+1]


