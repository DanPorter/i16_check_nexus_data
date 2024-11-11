"""
NeXus file validation using punx

installation
$ python pip -m install punx
-- also needed --
$ python pip -m install requests pyRestTable
"""

from punx.validate import Data_File_Validator

validator = Data_File_Validator()

f = r"C:\Users\grp66007\OneDrive - Diamond Light Source Ltd\DataAnalysis\Nexus\i16_nexus_test_31Oct24\1068436.nxs"
validator.validate(f)
try:
    validator.validate(f)
except Exception as ex:
    print(f"punx validator failed with error:\n{ex}\n")

print("\n\npunx validator report:")
validator.print_report()
validator.close()
