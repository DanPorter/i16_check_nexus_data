"""
Check metadata
"""

import h5py
import logging

from .metadata import METADATA, ATTRIBUTES, NXENTRY_ATTRIBUTES, NXDATA_ATTRIBUTES, NXDETECTOR_DATA, DATASET_ATTRIBUTES

logger = logging.getLogger(__name__)


def set_logging_level(level: str | int):
    """
    Set logging level (how many messages are printed)
    Logging Levels (see builtin module logging)
        'notset'   |  0
        'debug'    |  10
        'info'     |  20
        'warning'  |  30
        'error'    |  40
        'critical' |  50
    :param level: str level name or int level
    :return: None
    """
    if isinstance(level, str):
        level = level.upper()
        # level = logging.getLevelNamesMapping()[level]  # Python >3.11
        level = logging._nameToLevel[level]
    logger.setLevel(int(level))
    logger.info(f"Logging level set to {level}")


def find_nxclass(hdf_file: h5py.File, nxclass: str) -> list[str]:
    """Return NXdata instances"""

    paths = []

    def visit_links(name):
        h5py_obj = hdf_file.get(name)
        if isinstance(h5py_obj, h5py.Group) and h5py_obj.attrs.get('NX_class') == nxclass.encode():
            paths.append(name)

    hdf_file.visit_links(visit_links)
    return paths


def check_metadata(file: str) -> tuple[int, list[str], list[str]]:
    """
    Check metadata of file against expectation
    :param file: NeXus .nxs filename
    :return: score, [missing paths], [missing attributes]
    """

    metadata = METADATA.copy()
    attributes = ATTRIBUTES.copy()

    missing = []
    missing_attributes = []
    logger.info(f"\nFile: {file}")
    with h5py.File(file, 'r') as nxs:

        # --- Update Metadata Spec ---
        # Find NXentry
        nxentry_paths = find_nxclass(nxs, 'NXentry')
        for path in nxentry_paths:
            metadata[path] = 'NXentry'
            attributes[path] = NXENTRY_ATTRIBUTES
            nxentry = nxs[path]
            default = nxentry.attrs.get('default', None)
            if default:
                metadata[f"{path}/{default.decode()}"] = 'NXdata'

        # Find NXdata
        nxdata_paths = find_nxclass(nxs, 'NXdata')
        for path in nxdata_paths:
            metadata[path] = 'NXdata'
            attributes[path] = NXDATA_ATTRIBUTES

            dataset_paths = [
                f"{path}/{name}" for name, dataset in nxs[path].items() if isinstance(dataset, h5py.Dataset)
            ]
            for d_path in dataset_paths:
                metadata[d_path] = 'nd array'
                attributes[d_path] = DATASET_ATTRIBUTES

            # Default plotting
            nxdata = nxs[path]
            default_signal = nxdata.attrs.get('signal')
            if default_signal:
                metadata[f"{path}/{default_signal.decode()}"] = '@signal, nd array'

            default_axes = nxdata.attrs.get('axes', None)
            if default_axes is not None:
                for axes in default_axes:
                    metadata[f"{path}/{axes.decode()}"] = '@axes, nd array'

        # Find detectors
        detector_paths = find_nxclass(nxs, 'NXdetector')
        for path in detector_paths:
            metadata[path] = 'NXdetector'
            for name, example in NXDETECTOR_DATA.items():
                metadata[f"{path}/{name}"] = example

        # --- Find missing metadata ---
        for path, value in metadata.items():
            obj = nxs.get(path)
            if isinstance(obj, h5py.Group):
                nx_class = obj.attrs.get('NX_class', b'none').decode()
                isgood = '' if nx_class == value else f"!Should be {value}!"
                logger.info(f"{path}: NX_class = {nx_class} {isgood}")
            elif isinstance(obj, h5py.Dataset):
                logger.info(f"{path} = {value}")
            else:
                missing.append(f"{path} = {value}")
            if obj and path in attributes:
                for attr, attr_value in attributes[path].items():
                    if attr in obj.attrs:
                        obj_attr = obj.attrs[attr]
                        try:
                            isgood = '' if obj_attr == attr_value else f"(Should be {attr_value})"
                        except ValueError:
                            isgood = f"(Should be {attr_value})"
                        logger.info(f"  @{attr} = {obj_attr} {isgood}")
                    else:
                        logger.info(f"  @{attr} Missing, Should be {attr_value}")
                        missing_attributes.append(f"{path}@{attr} = {attr_value}")

    logger.info('\nMissing fields:')
    logger.info('\n'.join(missing))
    logger.info('\nMissing attributes:')
    logger.info('\n'.join(missing_attributes))

    score = 100 * len(missing) + len(missing_attributes)
    return score, missing, missing_attributes
