The following Python script is a de-identification tool for DICOM medical images.
This tool is designed to remove sensitive, private information about patients.
The focus here is mainly on de-identification of CT and MRI image datasets, but
it could be adapted to other types of DICOM image data.  This tool also gets rid
of secondary captures such as movies, snapshots or scan summaries, which can also
contain sensitive, personal patient info.  DICOM anonymization tools I've worked with
in the past don't remove these secondary captures, so the data still wasn't
fully de-identified.  This script addresses this problem.  In the script, the user
is given the option to de-identify either a CT or an MRI dataset.