"""
Check nexus metadata against format specification

NeXus Spec:
"diamond standard nexus structure V2.docx"
https://manual.nexusformat.org/classes/applications/NXmx.html#nxmx

By Dan Porter
2024
"""

import h5py

# from "diamond standard nexus structure V2.docx"
nexus_metadata = {
    '/entry': 'NXentry',
    '/entry/instrument': 'NXinstrument',
    '/entry/instrument/name': 'I16',
    '/entry/instrument/source': 'NXsource',
    '/entry/instrument/source/name': 'Diamond Light Source',
    '/entry/instrument/source/type': 'Synchrotron X-ray Source',
    '/entry/instrument/source/probe': 'x-ray',
    '/entry/instrument/source/current': 'link to ring current',
    '/entry/instrument/insertion_device': 'NXinsertion_device',
    '/entry/instrument/insertion_device/gap': 'link to IDgap',
    '/entry/instrument/monochromator': 'NXmonochromator',
    '/entry/instrument/monochromator/energy': '8 keV',
    '/entry/sample': 'NXsample',
    '/entry/sample/name': 'name',
    '/entry/sample/depends_on': 'name',
    '/entry/sample/chemical_formula': '',
    '/entry/sample/temperature': '10 K',
    '/entry/sample/electric_field': '0 V',
    '/entry/sample/magnetic_field': '0 T',
    '/entry/sample/pressure': '0 Pa',
    'entry/sample/transformations': 'NXtransformations',
    '/entry/sample/beam': 'NXbeam',
    '/entry/sample/beam/incident_energy': '8 keV',
    '/entry/sample/beam/flux': '10^13 ph/s',
    '/entry/sample/beam/extent': '250 x 30 um^2',
    '/entry/sample/beam/incident_beam_divergence': '30 x 10 nm',
    '/entry/sample/beam/incident_polarization': 'vector',
    '/entry/sample/beam/incident_polarization_stokes': 'vector',
    '/entry/sample/surface_hkl': 'vector',
    '/entry/sample/orientation_matrix': '3x3 array',
    '/entry/sample/ub_matrix': '3x3 array',
    '/entry/sample/unit_cell': '6x1 array',
    '/entry/sample/diffcalc': 'NXnote',
    '/entry/sample/diffcalc/description': 'Data used by diffcalc application',
    '/entry/sample/diffcalc/type': 'application/json',
    '/entry/sample/diffcalc/data': '{}',
    '/entry/title': 'scancn x 0.01 3 pil 0.1 roi2',
    '/entry/experiment_identifier': 'mm12345-1',
    '/entry/start_time': '2024-12-24 10:00',
    '/entry/end_time': '2024-12-24 10:01',
    '/entry/end_time_estimated': '2024-12-24 10:01',
    '/entry/program_name': 'GDA',
    '/entry/definition': 'NXmx',
    '/entry/entry_identifier': '123456',
    # '/entry/subentry': 'NXsubentry',
    '/entry/diamond_scan': 'NXCollection',
    '/entry/diamond_scan/keys': 'NXCollection',
    '/entry/diamond_scan/uniqueKeys': 'int',
    '/entry/diamond_scan/point_start_times': '',
    '/entry/diamond_scan/point_end_times': '',
    '/entry/diamond_scan/scan_command': 'scan x 1 10 1 pil3_100k 1',
    '/entry/diamond_scan/scan_dead_time': '',
    '/entry/diamond_scan/scan_dead_time_percent': '',
    '/entry/diamond_scan/scan_estimated_duration': '',
    '/entry/diamond_scan/scan_finished': '1',
    '/entry/diamond_scan/scan_rank': '1',
    '/entry/diamond_scan/scan_shape': '10',
    '/entry/diamond_scan/scan_fields': ['hkl.h', 'hkl.k', 'hkl.l', 'pil3.roi_sum'],
    '/entry/diamond_scan/user_command': '',
    '/entry/diamond_scan/called_by': '',
    '/entry/diamond_scan/script': 'NXnote',
    '/entry/measurement': 'NXdata',
    '/entry/measurement/x': 'link',
    '/entry/measurement/count_time': 'link',
    '/entry/instrument/s5': 'NXslit',
    '/entry/instrument/s5/x_gap': '0.1 mm',
    '/entry/instrument/s5/y_gap': '0.1 mm',
    '/entry/instrument/s5/depends_on': 's5transformations/x_centre',
    '/entry/instrument/s5/s5transformations': 'NXtransformations',
    '/entry/instrument/s5/s5transformations/x_centre': '0.0 mm',
    '/entry/instrument/s5/s5transformations/y_centre': '0.0 mm',
    '/entry/instrument/s5/s5transformations/z_centre': '0.0 mm',
}

nxdetector_metadata = {
    "data": 'nd array',
    "sensor_material": 'char',
    "sensor_thickness": 'float',
    "polarization_analyser_jones_matrix": '',
    "module": 'NXdetector_module',
    "module/data_origin": 'int',
    "module/data_size": 'int',
    "module/fast_pixel_direction": 'int',
    "module/slow_pixel_direction": 'int',
}

nexus_nxdata_attributes = {
    'signal': b'roi2_sum',
    'axes': [b'k',],
    # 'auxiliary_signals': [b'count_time', b'total', b'max_val'],
}

nexus_dataset_attributes = {
    # 'decimals': 8,
    # 'units': b'r.l.u',
    'local_name': b'hkl.h',
}

nexus_attributes = {
    '/entry/measurement': nexus_nxdata_attributes,
    '/entry/measurement/h': nexus_dataset_attributes,
    '/entry/instrument/source/current': {'units': b'mA'},
    '/entry/instrument/insertion_device/gap': {'units': b'mm'},
    '/entry/instrument/monochromator/energy': {'units': b'keV'},
    '/entry/sample/temperature': {'units': b'K'},
    '/entry/sample/electric_field': {'units': b'V'},
    '/entry/sample/magnetic_field': {'units': b'T'},
    '/entry/sample/pressure': {'units': b'Pa'},
    '/entry/sample/beam/incident_energy': {'units': b'keV'},
    '/entry/sample/beam/flux': {'units': b'ph/s'},
    '/entry/sample/beam/incident_beam_size': {'units': b'um'},
    '/entry/sample/beam/incident_beam_divergence': {'units': b'nm'},
}


def find_nxclass(hdf_file: h5py.File, nxclass: str) -> list[str]:
    """Return NXdata instances"""

    paths = []

    def visit_links(name):
        h5py_obj = hdf_file.get(name)
        if isinstance(h5py_obj, h5py.Group) and h5py_obj.attrs.get('NX_class') == nxclass.encode():
            paths.append(name)

    hdf_file.visit_links(visit_links)
    return paths


def check_metadata(file: str):
    missing = []
    missing_attributes = []
    print(f"\nFile: {file}")
    with h5py.File(file, 'r') as nxs:

        # --- Update Metadata Spec ---
        # Find NXdata
        nxdata_paths = find_nxclass(nxs, 'NXdata')
        for path in nxdata_paths:
            nexus_metadata[path] = 'NXdata'
            # nexus_metadata[f"{path}/data"] = 'nd array'
            nexus_attributes[path] = nexus_nxdata_attributes

            dataset_paths = [
                f"{path}/{name}" for name, dataset in nxs[path].items() if isinstance(dataset, h5py.Dataset)
            ]
            for d_path in dataset_paths:
                nexus_metadata[d_path] = 'nd array'
                nexus_attributes[d_path] = nexus_dataset_attributes

            nxdata = nxs[path]
            default_signal = nxdata.attrs.get('signal')
            if default_signal:
                nexus_metadata[f"{path}/{default_signal.decode()}"] = '@signal, nd array'

            default_axes = nxdata.attrs.get('axes', None)
            if default_axes is not None:
                for axes in default_axes:
                    nexus_metadata[f"{path}/{axes.decode()}"] = '@axes, nd array'

        # Find detectors
        detector_paths = find_nxclass(nxs, 'NXdetector')
        for path in detector_paths:
            nexus_metadata[path] = 'NXdetector'
            for name, example in nxdetector_metadata.items():
                nexus_metadata[f"{path}/{name}"] = example

        # --- Find missing metadata ---
        for path, value in nexus_metadata.items():
            obj = nxs.get(path)
            if isinstance(obj, h5py.Group):
                nx_class = obj.attrs.get('NX_class', b'none').decode()
                isgood = '' if nx_class == value else f"!Should be {value}!"
                print(f"{path}: NX_class = {nx_class} {isgood}")
            elif isinstance(obj, h5py.Dataset):
                print(f"{path} = {value}")
            else:
                missing.append(f"{path} = {value}")
            if obj and path in nexus_attributes:
                for attr, value in nexus_attributes[path].items():
                    if attr in obj.attrs:
                        obj_attr = obj.attrs[attr]
                        try:
                            isgood = '' if obj_attr == value else f"(Should be {value})"
                        except ValueError:
                            isgood = f"(Should be {value})"
                        print(f"  @{attr} = {obj_attr} {isgood}")
                    else:
                        print(f"  @{attr} Missing, Should be {value}")
                        missing_attributes.append(f"{path}@{attr} = {value}")

    print('\nMissing fields:')
    print('\n'.join(missing))
    print('\nMissing attributes:')
    print('\n'.join(missing_attributes))


if __name__ == '__main__':
    f = r"C:\Users\grp66007\OneDrive - Diamond Light Source Ltd\DataAnalysis\Nexus\i16_nexus_test_31Oct24\1068436.nxs"
    check_metadata(f)

