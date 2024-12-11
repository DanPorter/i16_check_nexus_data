"""
Use nexus2srs and compare dat files
"""

import os
import numpy as np
import nexus2srs


class Dict2Obj(dict):
    """Convert dictionary object to class instance"""

    def __init__(self, dictvals):
        super().__init__(**dictvals)

        for name, values in dictvals.items():
            setattr(self, name, values)
            self.update({name: dictvals[name]})


def read_dat_file(filename):
    """
    Reads #####.dat files from instrument, returns class instance containing all data
    Input:
      filename = string filename of data file
    Output:
      d = class instance with parameters associated to scanned values in the data file, plus:
         d.metadata - class containing all metadata from datafile
         d.keys() - returns all parameter names
         d.values() - returns all parameter values
         d.items() - returns parameter (name,value) tuples
    """
    with open(filename, 'r') as f:
        lines = f.readlines()

    # Read metadata
    meta = {}
    lineno = 0
    for ln in lines:
        lineno += 1
        if '&END' in ln: break
        ln = ln.strip(' ,\n')
        neq = ln.count('=')
        if neq == 1:
            'e.g. cmd = "scan x 1 10 1"'
            inlines = [ln]
        elif neq > 1 and '{' not in ln:
            'e.g. SRSRUN=571664,SRSDAT=201624,SRSTIM=183757'
            ' but not ubMeta={"name": "crystal=big", ...}'
            inlines = ln.split(',')
        else:
            'e.g. <MetaDataAtStart>'
            continue

        for inln in inlines:
            vals = inln.split('=')
            if len(vals) != 2: continue
            try:
                meta[vals[0]] = eval(vals[1])
            except:
                meta[vals[0]] = vals[1]

    # Read Main data
    # previous loop ended at &END, now starting on list of names
    names = lines[lineno].split()

    # Load 2D arrays of scanned values
    # vals = np.loadtxt(lines[lineno+1:],ndmin=2)
    try:
        vals = np.genfromtxt(lines[lineno + 1:],
                             ndmin=2)  # changed 31/10/24 to handle 'true'/'false' in file (returns nan)
    except TypeError:  # numpy < 1.2
        vals = np.genfromtxt(lines[lineno + 1:])
        if np.ndim(vals) < 2:  # single point scans
            vals = np.reshape(vals, (1, -1))

    # Assign arrays to a dictionary
    main = {
        name: value for name, value in zip(names, vals.T)
    }

    # Convert to class instance
    obj = Dict2Obj(main)
    obj.metadata = Dict2Obj(meta)
    return obj


def compare_dat_objects(old_dat_obj: Dict2Obj, new_dat_obj: Dict2Obj):
    """
    Compare data objects
    :param old_dat_obj:
    :param new_dat_obj:
    :return:
    """

    old_metadata = old_dat_obj.metadata
    new_metadata = new_dat_obj.metadata
    len_old_data = len(old_dat_obj[next(iter(old_dat_obj))])
    len_new_data = len(new_dat_obj[next(iter(new_dat_obj))])

    # Compare number of data
    print(f"{'':20}  Original  :  Converted")
    print(f"{'Scannables':20} {len(old_dat_obj):9}  :  {len(new_dat_obj)}")
    print(f"{'Metadata':20} {len(old_metadata):9}  :  {len(new_metadata)}")
    print(f"{'Scan length':20} {len_old_data:9}  :  {len_new_data}")

    # Check for differences in data
    if len_old_data == len_new_data:
        different_scannables = "\n ".join(
            f"{name}: {diff}" for name, value in old_dat_obj.items()
            if name in new_dat_obj and (
                diff := np.sqrt(np.sum(np.square(np.subtract(value, new_dat_obj[name]))))
            ) > 0.1
        )
        print(f"\n\nDifferent scan data:\n  {different_scannables}")

    def compare_metadata(val1, val2):
        """Return true if match"""
        try:
            _diff = val1 - val2
            return np.sqrt(np.sum(np.square(np.subtract(val1, val2)))) < 0.1
        except:
            return str(val1) == str(val2)

    different_metadata = "\n ".join(
        f"{name} : {value}  : {new_metadata[name]}" for name, value in old_metadata.items()
        if name in new_metadata and not compare_metadata(value, new_metadata[name])
    )
    print(f"\nDifferent metadata:\n  {different_metadata}")

    # List missing data
    missing_scannables = "\n  ".join(
        f"{name}: {np.shape(value)}"
        for name, value in old_dat_obj.items() if name not in new_dat_obj
    )
    new_scannables = '\n  '.join(
        f"{name}: {np.shape(value)}"
        for name, value in new_dat_obj.items() if name not in old_dat_obj
    )
    mising_metadata = "\n  ".join(
        f"{name}: {value}"
        for name, value in old_metadata.items() if name not in new_metadata
    )
    print(f"\n\nMissing scannables:\n  {missing_scannables}")
    print(f"\nNew scannables:\n  {new_scannables}")
    print(f"\nMissing metadata:\n  {mising_metadata}")


def convert_and_compare_dat(old_dat_file: str):
    """
    Compare old dat file to one generated using nexus2srs
    :param old_dat_file: '123456.dat'
    :return:
    """
    nexus_filename = old_dat_file.replace('.dat', '.nxs')
    new_dat_filename = old_dat_file.replace('.dat', '.nexus2srs.dat')

    if os.path.isfile(new_dat_filename):
        os.remove(new_dat_filename)

    # Generate new file
    nexus2srs.nxs2dat(
        nexus_file=nexus_filename,
        dat_file=new_dat_filename,
        write_tiff=False
    )
    # Load files
    old_dat_obj = read_dat_file(old_dat_file)
    new_dat_obj = read_dat_file(new_dat_filename)

    print(f"---{os.path.basename(old_dat_file)}---")
    print("Nexus2SRS DAT file Comparison")
    print(f"Old file: {old_dat_file}")
    print(f"Converted file: {new_dat_filename}")
    compare_dat_objects(old_dat_obj, new_dat_obj)
