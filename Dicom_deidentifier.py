#The following script takes a DICOM medical image data set (ie CT as an example) and deidentifies it.
#It also removes any secondary captures or snapshots that may contain sensitive patient identifiers.
#All DICOM deidentifers I've used in the past aren't good enough and they don't remove
#secondary screen captures or snapshots that contain sensitive personal health information about patients.
#This script preserves the original dataset and places the new de-identifed dataset in a separate folder.
#The user is given the option to de-identify either a CT or an MRI dataset.

#The following libraries are imported to do this work, including the pydicom library.
#The numeric, scientific and plotting libraries and operating system libraries are
#also included.  The operating system module is also used to manipulate directories
#more easily and efficiently.
import pydicom
import os
import sys
from pydicom.uid import generate_uid

#Change the working directory to the directory of this script file that invoked the Python interpreter.
os.chdir(sys.path[0])

#Set the current working directory as a variable.
wd = os.getcwd()

#Create a list of files and other directories in the current working directory
dir_list = os.listdir(wd)

#Set the desired name of the original image dataset directory.
CT_dir = 'CT original dataset'
MRI_dir = 'MRI original dataset'

#Define the directory with the original DICOM data.
original_dir_CT = os.path.join(wd,CT_dir)
original_dir_MRI = os.path.join(wd, MRI_dir)

#Generate a unique random study UID before looping through all the images in
#the study.  These are needed for specific tags in the MRI and CT datasets.
StudyID = generate_uid()
EquipmentID = generate_uid()

#Change the working directory to the directory containing the original DICOM data.
#There are two datasets, a CT dataset and an MRI dataset.  Let the user pick which
#dataset of the two they want to deidentify.

#Initialize the original data directory to anonymize with an empty string.
original_directory = ' '

#Keep asking the user to enter either CT or MRI if they keep entering the
#directory they want to de-identify incorrectly (ie. something other than CT
#or MRI).
while original_directory != 'CT' and original_directory != 'MRI':

   #Get the user input for which dataset they want to de-identify.  Should be CT or MRI.
   original_directory = input("Choose which dataset you want to deidentify (CT or MRI): ")

   #If the user wants to deidentify the CT dataset
   if original_directory == 'CT':

      #Create a new directory path to store anonymized CT dataset.
      new_dir_CT = os.path.join(wd, r'CT anonymized dataset')

      #If the new directory for the deidentified data doesn't exist yet, then create the directory.
      if not os.path.exists(new_dir_CT):
         os.makedirs(new_dir_CT)
      
      #Change directory to the original CT data
      os.chdir(original_dir_CT)

      #Get the list of file names in the original data directory.
      orig_filelist = os.listdir(original_dir_CT)

      #Start iterating through the file list in the original DICOM dataset.
      for num, file in enumerate(orig_filelist):

         #Check to make sure that the file being interrogated is an actual DICOM file in the folder.
         if file.endswith('.dcm'):
            
            #Read the first DICOM file in the original data directory.
            ds = pydicom.dcmread(file)

            #Check if the SOPClassUID tag says that the images are
            #from a CT dataset.  Since we are only looking for CT images
            #with this command, it will also ignore all secondary captures
            #and snapshots, so that these won't be part of the de-identified dataset.
            #These secondary captures can also contain sensitive, identifying patient
            #information.
            if ds[0x0008,0x0016].repval == 'CT Image Storage':
                
                #Begin the deidentification of all relevant tags.
                ds.PatientName = 'CT_Patient'
                ds.AccessionNumber = ' '
                ds.Manufacturer = ' '
                ds.InstitutionName = ' '
                ds.InstitutionAddress = ' '
                ds.ReferringPhysicianName = ' '
                ds.StationName = ' '
                ds.InstitutionalDepartmentName = ' '
                ds.OperatorsName = ' '
                ds.ManufacturerModelName = ' '
                ds.PatientID = ' '
                ds.PatientBirthDate = ' '
                ds.PatientSex = ' '
                ds.PatientAge = ' '
                ds.DeviceSerialNumber = ' '
                ds.SoftwareVersions = ' '
                ds.StudyID = ' '
                ds.AcquisitionDate = ' '
                ds.AcquisitionTime = ' '
                ds.SeriesDate = ' '
                ds.StudyDate = ' '
                ds.SeriesTime = ' '
                ds.StudyTime = ' '
                ds.ContentDate = ' '
                ds.ContentTime = ' '
                ds.ScheduledProcedureStepEndDate = ' '
                ds.ScheduledProcedureStepEndTime = ' '
                ds.ScheduledProcedureStepStartDate = ' '
                ds.ScheduledProcedureStepStartTime = ' '
                ds.PerformedProcedureStepID = ' '
                ds.PerformedProcedureStepStartDate = ' '
                ds.PerformedProcedureStepStartTime = ' '
            
                #The request attributes tag is a nested tag, so additional steps
                #are needed to de-identify the internal tags.
                ds.RequestAttributesSequence[0].ScheduledProcedureStepID = ' '
                ds.RequestAttributesSequence[0].RequestedProcedureID = ' '

                #Can also remove sensitive tags from the file header metadata.
                ds.file_meta.SourceApplicationEntityTitle = ' '

                #Generate random UIDs for instances (slices), image series
                #and the entire imaging study.
                SOPUID = generate_uid()
                ds.file_meta.MediaStorageSOPInstanceUID = SOPUID
                ds.SOPInstanceUID = SOPUID
                ds.StudyInstanceUID = StudyID
                ds.SeriesInstanceUID = ' '    #Don't need this.
                ds.FrameOfReferenceUID = generate_uid()
            
                #Remove all private tags.
                ds.remove_private_tags()
    
                #Change to the new directory, save the image in sequence and then
                #go back to the directory with the original DICOM data.
                os.chdir(new_dir_CT)
                ds.save_as('Image_{:05d}.dcm'.format(num))
                os.chdir(original_dir_CT)


   #If the user wants to deidentify the MRI dataset instead
   elif original_directory == 'MRI':

      #Create a new directory path to store the deidentified image dataset, for
      #the MRI dataset
      new_dir_MRI = os.path.join(wd, r'MRI anonymized dataset')

      #If the new directory for the deidentified data doesn't exist yet, then create the directory.
      if not os.path.exists(new_dir_MRI):
         os.makedirs(new_dir_MRI)
      
      #Change directory to the original CT data
      os.chdir(original_dir_MRI)

      #Get the list of file names in the original data directory.
      orig_filelist = os.listdir(original_dir_MRI)

      #Start iterating through the file list in the original DICOM dataset.
      for num, file in enumerate(orig_filelist):

         #Check to make sure that the file being interrogated is an actual DICOM file in the folder.
         if file.endswith('.dcm'):
            
            #Read the first DICOM file in the original data directory.
            ds = pydicom.dcmread(file)
   
            #If the images are from an MRI dataset, then use these deidentification
            #steps instead.  Also ignore secondary captures, which can have additional identifiers.
            if ds[0x0008,0x0016].repval == 'MR Image Storage':
                
                #Begin the deidentification of all relevant tags from the MRI data.
                ds.InstanceCreationDate = ' '
                ds.InstanceCreationTime = ' '
                ds.StudyDate= ' '
                ds.SeriesDate=' '
                ds.AcquisitionDate=' '
                ds.ContentDate = ' '
                ds.StudyTime=' '
                ds.SeriesTime=' '
                ds.AcquisitionTime=' '
                ds.ContentTime=' '
                ds.AccessionNumber=' '
                ds.Manufacturer=' '
                ds.InstitutionName=' '
                ds.ReferringPhysicianName =' '
                ds.StationName=' '
                ds.NameOfPhysiciansReadingStudy=' '
                ds.OperatorsName=' '
                ds.ManufacturersModelName=' '
                ds.PatientName='MRI_patient'
                ds.PatientID=' '
                ds.PatientBirthDate=' '
                ds.PatientSex=' '
                ds.PatientAge=' '
                ds.PatientWeight=' '
                ds.AdditionalPatientHistory=' '
                ds.ManufacturerModelName = ' '

                #Get rid of the Performed Procedure Step ID if it exists.  Unfortunately with the
                #MRI data, different image series for the same exam can have a different number
                #of tags, so this needs to be taken into account for the entire imaging exam.
                if (0x0040,0x0253) in ds:
                    ds.PerformedProcedureStepID =' '

                #Get rid to the Attribute IDs, as these contain sensitive patient info.
                if (0x0040,0x0275) in ds:
                    ds.RequestAttributesSequence[0].ScheduledProcedureStepID = ' '
                    ds.RequestAttributesSequence[0].RequestedProcedureID = ' '

                #Get rid of the scanner serial number so it can't be traced.
                if (0x0018,0x1000) in ds:
                    ds.DeviceSerialNumber = ' '

                #Removereference image sequence UIDs.
                if(0x0008,0x1140) in ds:
                    del ds[0x0008,0x1140]
                                         
                #Can also remove sensitive tags from the file header metadata.
                ds.file_meta.SourceApplicationEntityTitle = ' '

                #Generate random UIDs for instances (slices), image series
                #and the entire imaging study.
                SOPUID = generate_uid()
                ds.file_meta.MediaStorageSOPInstanceUID = SOPUID
                ds.SOPInstanceUID = SOPUID
                ds.StudyInstanceUID = StudyID
                ds.SeriesInstanceUID = ' '    #Don't need this.
                ds.FrameOfReferenceUID = generate_uid()
                ds.EquipmentUID =  EquipmentID

                #Remove all private tags.
                ds.remove_private_tags()

                #Change to the new directory, save the image in sequence and then
                #go back to the directory with the original DICOM data.
                os.chdir(new_dir_MRI)
                ds.save_as('Image_{:05d}.dcm'.format(num))
                os.chdir(original_dir_MRI)         
                                           
   #Condition if the user didn't enter either CT or MRI dataset to de-identify.
   else:
      print("You didn't enter either CT or MRI.  Please try again.\n")

                
