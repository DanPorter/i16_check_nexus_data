"""
Use the punx validator
"""

from punx.validate import Data_File_Validator


def validate_nexus(file: str):
    """Validate nexus file using punx validator"""
    validator = Data_File_Validator()
    try:
        validator.validate(file)
    except Exception as ex:
        print(f"punx validator failed with error:\n{ex}\n")

    print("\n\npunx validator report:")
    validator.print_report()
    validator.close()
