# Diamond I16 NeXus Validation
Check and validate NeXus files against Diamond specifications


**Version 0.1**

| By Dan Porter        | 
|----------------------|
| Diamond Light Source |
| 2024                 |


### TL;DR - Usage

```bash
$ check_nexus 12345.nxs
```

### Description
The `check_metadata` function compares HDF paths and attributes against the standard NeXus structure of i16 at
Diamond Light Source:

 - `"diamond standard nexus structure V2.docx"`

In addition, the nexus file is compared to the NXmx application definition:

 - [NXmx](https://manual.nexusformat.org/classes/applications/NXmx.html#nxmx)


The `validate_nexus` function uses the [punx](https://github.com/prjemian/punx) package to valiate the nexus file against the current standard spec.

More info here:
 - https://manual.nexusformat.org/validation.html
 - https://manual.nexusformat.org/datarules.html#version-3