"""
Check and validate a nexus file
"""

from check_nexus import check_metadata, validate_nexus, set_logging_level

f = r"C:\Users\grp66007\OneDrive - Diamond Light Source Ltd\DataAnalysis\Nexus\i16_nexus_test_31Oct24\1068436.nxs"

print('\nValidation:')
validate_nexus(f)

print('\n\nSimple check')
set_logging_level('info')
score, missing_paths, missing_attr = check_metadata(f)

print(f"\n\nScore: {score} for Nexus file: {f}")
