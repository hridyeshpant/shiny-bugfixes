"""
    FILE:			UploadBitsToStageServer.py
    Purpose:    	Tool for querying the codex and get the information
    Prereq.:        Python should be present on the machine.
   
                    
  
"""

import sys, os.path, shutil, time, traceback, subprocess,datetime

import shutil
import getpass
from codexPythonClient import codex
from xml.dom import minidom
from xml.dom.minidom import Document
from ZSI import ServiceProxy, FaultException
from codexPythonClient import codexdatatypes as datatypes
from codexPythonClient import smb, codexlocation

# Global variables
exit_message="FAIL"
unksed="none"
user="none"


  
# Global variables
gLogger            = None
gComponent_file_dict      = []
gP4_file_dict = []
# Function definitions.

def exitWithMessage(exitMsg):
    #printLog(exitMsg)
    deleteLogger(exitMsg)
    sys.exit(0)
    
def createLogger(logFilePath):
    global  gLogger
    if os.path.exists(os.path.dirname(logFilePath)) is True:     
        gLogger =   open(logFilePath,"w")

    now = time.localtime(time.time())
    printLog('#############################################################################')
    printLog(time.strftime("Start Time-   %m/%d/%y  %H:%M:%S\n", now))


def deleteLogger(exitMsg):
    if (gLogger):
        now = time.localtime(time.time())
        printLog('\n\n############################################################################################################')
        printLog('                   Status : '+ exitMsg)
        printLog('                   End Time- '+time.strftime("%m/%d/%y  %H:%M:%S", now))
        printLog('################################################################################################################')
        gLogger.close()
        gTrace.close()

def printLog(str):
    gLogger.write(str+'\n')
    print str

        
def printStacktrace(traceback):
    printLog("\n\n")
    funcnames = traceback.split('\n')
    for func in funcnames:
        if (gLogger):
            printLog(func)
        else:
            print func

def _handleFaultException(exception):
   "takes a ZSI.FaultException and reraises a more specific type of exception if possible, based on the string"
   s = exception.__str__()
   if 'does not exist' in s: raise KeyError, s
   elif 'No entity found for query' in s: raise KeyError, s
   elif 'already exists' in s: raise NameError, s
   elif 'InvalidNameException' in s: raise NameError, s
   else: raise FaultException, s

   
def runCmd(cmd, logOutput):
	'''
	execute a command
	'''

	status = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	(output,error) = status.communicate()
	returncode = status.returncode

	if (returncode != 0 or logOutput == True ): 
		#printLog(("  cmd: %s") %(cmd))
		printLog(("  cmdRetCode [%d],  cmdErrMsg [%s], cmdOutput [%s]") %(returncode, error.strip() , output.strip()))

	return (output,error,returncode)

def read_file(p4client) :
     global unksed
     #filepath =  os.environ.get('FILE_PATH')
     filepath = '/home/alsvm1/setup/.p' 
     #print (filepath)
     f = open(filepath , 'r')
     items = []
     for row in f.readlines():
         items = row.split(':')
         unksed=items[0]
     f.close()
     match_data =p4client.find('1670')
     #print (p4client)
     if (match_data > 0):
        print ('inside 1670 ')
        return items[1]
     if (p4client.find('1740') > 0) :
        print ('inside 1740')
        return items[2]
     if (p4client.find('alsvm1') > 0) :
        print ('alsvm1')
        return items[0]
    
def create_p4_files_list (sync_path,P4ComponentList,num_component,assetTargetLocation) :
    try:
      global gP4_file_dict
      printLog("\n    *** copying p4 files ***" )
      printLog("\n    *** source p4 files ***" + sync_path)
      printLog("\n    *** destination p4 files ***" + assetTargetLocation)
      print "num_component : %d " % (num_component)
      itemIndex = 0
      index = 0
      while index < num_component :
        component = P4ComponentList[index]
        webPath    = component.getAttribute("webPath")
        description= component.getAttribute("description")
        gP4_file_dict.append({'webPath':webPath})
        index=index+1

      num_items = len (gP4_file_dict)
      while itemIndex < num_items :
        _webPath            = gP4_file_dict[itemIndex]['webPath']

        relativePath = _webPath.replace("http://xyz.com", "")
        relativePath = relativePath.replace("http://xyz.com", "")
        relativePath = relativePath.replace("http://xyzmf.com", "")
        releaseFilePath = assetTargetLocation + relativePath
        source_path     = sync_path + relativePath
        #relativePath = relativePath.replace("/", "\\")
        if os.path.exists( source_path ) is False:
           print "sync file not present : " + source_path
           raise Exception("FileNotFound")
        print "p4 source path : " + source_path
        print "p4 Dest path : " + releaseFilePath
        itemIndex   = itemIndex + 1;
        update_p4File(source_path, releaseFilePath)
    except:
      printLog ("Fail to generate the p4_filelist")
      printStacktrace(traceback.format_exc())
      raise


def update_p4File(cacheFilePath, releaseFilePath):
   try:
      printLog("      -------- Updating P4 file : " + releaseFilePath)

      releaseFileDir = os.path.dirname(releaseFilePath)
      if os.path.exists( releaseFileDir ) is False:
         os.makedirs(releaseFileDir)

      #if os.path.exists( releaseFilePath ) is True:
         #os.rename(releaseFilePath, backupFile)

      # Now copy the file to release location
      shutil.copyfile(cacheFilePath, releaseFilePath)

      # No exception, our operation was successful
      return True

   except OSError:
      printLog ("Fail to update the file, some file operation failed.")
      printStacktrace(traceback.format_exc())
      return False
   except:
      printLog ("Fail to update the file.")
      printStacktrace(traceback.format_exc())
      raise

def getComponentInformation(acroComponentList, num_component, version, build):
   try:
      global gComponent_file_dict
      printLog("\n    *** Fetching information form the installerspec file ***")
      index = 0
      while index < num_component :
         component = acroComponentList[index]

         codexName      = component.getAttribute("codexname")
         webPath    = component.getAttribute("webPath")
         product        = component.getAttribute("product")
         subProduct     = component.getAttribute("subProduct")
         description= component.getAttribute("description")
         format     = component.getAttribute("format")
         filename       = component.getAttribute("filename")

         metadata = "codexname=" + codexName
         if (build == "0"):
            build = ''

         result = codex.getLatestBuild(product, version, subProduct, build, '', '', '', '', format, '', '', '', metadata)

         printLog ("      Getting information for file : " + filename  + " [" + codexName + "]  --- " + result._build + "   " + result._product + "   "  + result._version + "    " + result._status)

         myFileIndex = 0
         while myFileIndex < len(result._fileinfo) :
            if (filename == result._fileinfo[myFileIndex]['filename']):
               break
            myFileIndex = myFileIndex + 1

         fileIndex = myFileIndex
         if ( not (myFileIndex < len(result._fileinfo)) ) :
            printLog("ERROR: Fail to get the information from codex for file : " + filename  )
            printLog("Error: Skipping the operation requested.")
            raise Exception("CodexError")

         gComponent_file_dict.append({
                                      'filename':filename,
                                      'webPath':webPath,
                                      'codexName':codexName,
                                      'build':result._build,
                                      'product':product,
                                      'status':result._status,
                                      'size':result._fileinfo[fileIndex]['size'],
                                      'md5':result._fileinfo[fileIndex]['md5'],
                                      'postingInfo':result._location
                                      })

         index= index + 1;

         #### start: hpant for debug/trial run uncomment following two lines ##
         #if index == 2:
            #break
         #### end: hpant for debug/trial run uncomment above two lines ##

      #print the data information we have collected
      #print gComponent_file_dict

   except:
      printLog ("Fail to get the component information.")
      printStacktrace(traceback.format_exc())
      raise

def checkComponentAvailablity():
   try:
     printLog("\n    *** Check the availability of assets at sjstore file server ***")
     num_items = len (gComponent_file_dict)
     itemIndex = 0
     while itemIndex < num_items :

        _fileName           = gComponent_file_dict[itemIndex]['filename']
        _fileLocationURI    = "%s://%s%s%s" % (gComponent_file_dict[itemIndex]['postingInfo']['protocol'], gComponent_file_dict[itemIndex]['postingInfo']['server'], gComponent_file_dict[itemIndex]['postingInfo']['path'], gComponent_file_dict[itemIndex]['postingInfo']['query'])

        if (gComponent_file_dict[itemIndex]['status'] != "Available" ):
           printLog ("ERROR: The file [" + gComponent_file_dict[itemIndex]['filename'] + "] is not present on server : " + gComponent_file_dict[itemIndex]['postingInfo']['server'] + gComponent_file_dict[itemIndex]['postingInfo']['path'] )
           return False

        # Actually go to the path and check for the file
        try:
           locationObj = codexlocation.CodexLocation(_fileLocationURI, mode="r", username=user, password=unksed)
        except codexlocation.BadPathError:
           print "Build doesn't exist at location %s" % (_fileLocationURI)
        except:
           raise

        printLog( "      File : " + _fileName + "  at server  [" + gComponent_file_dict[itemIndex]['postingInfo']['server'] + "]")
        filelist = locationObj.listdir()
        filePresentflag = 0
        for f in filelist:
           if f.lower() == _fileName.lower():
              filePresentflag = 1

        if not filePresentflag:
           print "Build Location does not have file : " + gComponent_file_dict[itemIndex]['postingInfo']['server'] + gComponent_file_dict[itemIndex]['postingInfo']['path'] + _fileName
           return False

        locationObj.close()


        itemIndex   = itemIndex + 1;

     return True

   except:
      printLog ("Fail to get the component information.")
      printStacktrace(traceback.format_exc())
      raise


def getComponentLocally(assetTmpLocation):
   try:
     printLog("\n    *** Downloading the files at local cache folder ***")
     num_items = len (gComponent_file_dict)
     itemIndex = 0
     while itemIndex < num_items :

        _webPath            = gComponent_file_dict[itemIndex]['webPath']
        _fileName           = gComponent_file_dict[itemIndex]['filename']
        _fileLocationURI    = "%s://%s%s%s" % (gComponent_file_dict[itemIndex]['postingInfo']['protocol'], gComponent_file_dict[itemIndex]['postingInfo']['server'], gComponent_file_dict[itemIndex]['postingInfo']['path'], gComponent_file_dict[itemIndex]['postingInfo']['query'])

        ##
        ##### Windows specific path implementation
        ##
        relativePath = _webPath.replace("http://xyz.com", "")
        relativePath = relativePath.replace("http://xyzmf.com", "")
        #relativePath = relativePath.replace("/", "\\")

        fileRemotePath  = gComponent_file_dict[itemIndex]['postingInfo']['path'] + _fileName
        fileLocalPath   = assetTmpLocation + relativePath

        fileDir         = os.path.dirname(fileLocalPath)

        if os.path.exists( fileDir ) is False:
           os.makedirs(fileDir)


        # If we are here, we need to download this file
        # Actually download the file
        try:
           locationObj = codexlocation.CodexLocation(_fileLocationURI, mode="r", username=user, password=unksed)
        except codexlocation.BadPathError:
           print "Build doesn't exist at location %s" % (_fileLocationURI)
        except:
           raise

        printLog( "      -------- Downloading file : " + _fileName)
        printLog( "      --------      " + gComponent_file_dict[itemIndex]['postingInfo']['server'] + fileRemotePath )

        locationObj.download(fileRemotePath, fileLocalPath)
        os.chmod(fileLocalPath,0777)

        locationObj.close()

        itemIndex   = itemIndex + 1;

   except:
      printLog ("Fail to download the component.")
      printStacktrace(traceback.format_exc())
      raise

def read_file(p4client) :
     global unksed
     #filepath =  os.environ.get('FILE_PATH')
     filepath = '/home/alsvm1/setup/.p'
     print (filepath)
     f = open(filepath , 'r')
     items = []
     for row in f.readlines():
         items = row.split(':')
         unksed=items[0]
     f.close()
     match_data =p4client.find('1670')
     print (p4client)
     if (match_data > 0):
        print ('inside 1670 ')
        return items[1]
     if (p4client.find('1740') > 0) :
        print ('inside 1740')
        return items[2]
     if (p4client.find('alsvm1') >= 0) :
        print ('alsvm1')
        return items[0]
     else :
        print "Not found anythings"


def checkPushSpecIntegrrity(assetTmpLocation,pushSpecFile,pushSpecPath) :
    printLog("\n\n")
    printLog("  ***Integrity verified with push_spec ")
    lines = []
    push_spec_files=pushSpecFile.split(',')
    for file in push_spec_files :
         stage_filepath=os.path.join (pushSpecPath,file)
         printLog("\n")
         printLog("        ** checking push_spec file : "+stage_filepath)
         push_spec_file= open (stage_filepath,"r")
         lines = push_spec_file.readlines()
         push_spec_file.close()
         for content in lines:
             if not content.strip():
                 continue
             if content.startswith('#') :
                 continue
             if (content.find('worm_aL7') >= 0) :
                 continue
             content=content.replace('\n', '')
             stage_filepath=os.path.join (assetTmpLocation,content)
             printLog("        ** checking file : "+content)
             if os.path.exists( stage_filepath ) is False:
                  printLog("\n\n")
                  printLog("*************************************************************************************************************************************")
                  printLog("          ** Error  : Downloaded file not present : " + content)
                  printLog("**************************************************************************************************************************************")
                  raise Exception("FileNotFound")
             else :
                  printLog ("              **Found : " + stage_filepath)


def calculateMD5(filePath):
   try:
      #f=open("1.txt", mode='rb')
      commandStr = "/usr/bin/md5sum " + filePath
      (val,error,returncode)=runCmd (commandStr, False)
      #p = os.popen(commandStr)
      #val = p.readline()
      output=val.split(" ")
      md5 = output[0]
      #print ("@@@@ md5 : "+md5[0])
      return md5
   except:
      printLog ("Fail to calulate MD5 checksum.")
      printStacktrace(traceback.format_exc())
      raise



def refreshWithUpdatedComponents(assetTmpLocation,assetFinalLocation,pushSpecFile,pushSpecPath) :
    lines = []
    fileUpdate_dict        = []
    checksumReleaseFile    = ""
    sizeReleaseFile        = ""
    errorInFileUpdateOp    = False
    fileUpdateRequire      = False
    push_spec_files=pushSpecFile.split(',')
    for file in push_spec_files :
        stage_filepath=os.path.join (pushSpecPath,file)
        printLog("     ** checking push_spec file : "+stage_filepath)
        push_spec_file= open (stage_filepath,"r")
        lines = push_spec_file.readlines()
        for content in lines:
             if not content.strip():
                 continue
             if content.startswith('#') :
                 continue
             if (content.find('worm_aL7') >= 0) :
                 continue
             content=content.replace('\n', '')
             cacheFilePath=os.path.join (assetTmpLocation,content)
             releaseFilePath=os.path.join (assetFinalLocation,content)
             fileUpdateRequire = False
             if os.path.exists( cacheFilePath ) is False:
                 print "Downloaded file not present : " + cacheFilePath
                 raise Exception("FileNotFound")

             if os.path.exists( releaseFilePath ) is False:
                print "      file not present in assetFinalLocation : " + releaseFilePath
                fileUpdateRequire = True
            
             checksumCacheFile = calculateMD5(cacheFilePath)
             sizeCacheFile     = os.path.getsize(cacheFilePath)

             if fileUpdateRequire is False:
                checksumReleaseFile  = calculateMD5(releaseFilePath)
                sizeReleaseFile        = os.path.getsize(releaseFilePath)

             if ( checksumCacheFile != checksumReleaseFile):
                 print "      File checksum mismatched for file : " + releaseFilePath
                 print "      Checksum of downloaded file : " + checksumCacheFile
                 print "      Checksum of Release file : " + checksumReleaseFile
                 print "      The file needs to be updated, Adding this to file update dictionary."
                 fileUpdateRequire = True
             else :
                  print "      File checksum same for file : " + releaseFilePath
             if ((fileUpdateRequire is True)):
                 if updateFile(cacheFilePath, releaseFilePath) is True:
                      print "           -------- File updated successfully : " + releaseFilePath 
                      print "\n"
                 else:
                      print "      -------- Fail to update file : " + releaseFilePath
                      print "           -------- Source file : " + cacheFilePath 
                      sys.exit(-1)

              

def updateFile(cacheFilePath, releaseFilePath):
   try:
      #printLog("      -------- Updating file : " + releaseFilePath)
      # first take backup of the

      releaseFileDir = os.path.dirname(releaseFilePath)
      if os.path.exists( releaseFileDir ) is False:
         os.makedirs(releaseFileDir)

      # Now copy the file to release location
      shutil.copyfile(cacheFilePath, releaseFilePath)
      os.chmod(releaseFilePath,0777)
      printLog("      -------- Copying : "+cacheFilePath)
      printLog("                      ->"+ releaseFilePath )
      return True

   except OSError:
      printLog ("Fail to update the file, some file operation failed.")
      printStacktrace(traceback.format_exc())
      return False
   except:
      printLog ("Fail to update the file.")
      printStacktrace(traceback.format_exc())
      raise



if __name__ == "__main__":
   global gTrace,logFile,push_spec,installerSpecFile,buildNumber,trackname

   try:
      
      gToolDir          = "/disks/netapp2/acrobat/webserver/test/worm_aL7/pubs_bkp"
      stage_location    = "/disks/netapp2/acrobat/webserver/test/worm_aL7"
      dynamic_files_location=  "/disks/netapp2/acrobat/webserver/build/acroweb_content"
      webdir_unix_root = "/disks/netapp2/acrobat/webserver/build/acroweb_content/pubs/"
      push_spec_location = "/disks/netapp2/acrobat/acrorel/acro_build/web/pushspecs"
      
      track=os.environ['Track_Name']
      pushSpecFile=os.environ['Push_Spec']
      buildNumber=os.environ['Build']
      user='alsvm1'
      unksed=read_file(user)
      
      if ((not track) and (pushSpecFile) and (buildNumber) ) :
         print "Wrong number of argument"
         print "Usage: some of the input paramter are empty, please provide all values ..."
         raise Exception("InvalidArgument")

      installerSpecFile = webdir_unix_root + track +"/installer_spec/installerSpec.xml"      
      if os.path.exists( installerSpecFile ) is False:
           print "installerSpecFile file not present : " + installerSpecFile
           raise Exception("FileNotFound")
        
      push_spec_files=pushSpecFile.split(',')
      for file in push_spec_files :
          pushSpecFile_list              = os.path.join (push_spec_location,file)
          #pushSpecFile              = "1111a_RDC.txt"
          if os.path.exists(pushSpecFile_list) is False:
              print "****** Error : pushSpecFile file not present : " + pushSpecFile_list
              raise Exception("FileNotFound")

      if (( buildNumber.isdigit() is False ) or (not ( int(buildNumber) > 0)) ):
         print "Usage: python <installer_spec>  <buildNumber>"
         print "Wrong buildNumber, must be a positive number"
         raise Exception("InvalidArgument")
      
      gRootDir            = os.path.join(gToolDir,buildNumber)
      
      if os.path.exists(gRootDir) is False:
         os.makedirs(gRootDir)
                  
      log_location = gRootDir + "/logs/"
      if os.path.exists(log_location) is False:
         os.makedirs(log_location)
      assetTmpLocation      = os.path.join(gRootDir,'downloaded')
      if os.path.exists(assetTmpLocation) is False:     
         os.makedirs(assetTmpLocation) 
      #sys.exit(0);
      currStatusServerTrackPath = log_location
      gTrace        = open( os.path.join(log_location, 'Codex_UploadBitsToStageServer.log') ,    "w")
      logFilePath  = os.path.join(log_location, 'UploadBitsToStageServer.log')
      createLogger(logFilePath)
 
   except  IOError:
      print ('Error: Failed to create logfile [' + logFilePath + '].')
      sys.exit("Unable to open log file : 501")   
   except FaultException, e:
      _handleFaultException(e)
      sys.exit("Unable to open log file : 501")   

      printStacktrace(traceback.format_exc())
      printLog ('Error: Failed to read the input file. The file is not well formed. [' + installerSpecFile + ']')
      raise Exception("InvalidXMLFile")
 
   try:
      xmldoc = minidom.parse(installerSpecFile)
   except FaultException, e:
      printStacktrace(traceback.format_exc())
      printLog ('Error: Failed to read the input file. The file is not well formed. [' + installerSpecFile + ']')
      raise Exception("InvalidXMLFile")
   try:
      docElements = xmldoc.documentElement
      if docElements.tagName != "InstallerSpecData" :
         printLog( 'Imput xml file is not valid it does not have [InstallerSpecData] root tag')
         raise Exception("InvalidXMLFile")

      P4Configs   = xmldoc.getElementsByTagName('P4Config')
      P4Config = P4Configs[0]
      web_dir      = P4Config.getAttribute("web_dir")
      email=P4Config.getAttribute("ids")
      dynamic_files_location = os.path.join(dynamic_files_location,web_dir)
      P4Components   = xmldoc.getElementsByTagName('P4list');
      p4_num_elements      = len (P4Components);

      codex = codex.CodexService(gTrace)
      printLog ("== Dynamic server location : " +dynamic_files_location)
      printLog ("== assetTmpLocation location : " +assetTmpLocation)
      printLog ("== stage_location location : " +stage_location)

      # Now we have the appropriate Acrobat Track Element for the required trackID
      printLog( '\n*****************  Going to process ----- ')
      printLog("\n    *** Uploading files to Static Server ***")
      printLog("\n    *** Source Location : " +assetTmpLocation)
      printLog("\n    *** Stage Location : " + stage_location)
      #sys.exit(0)
      refreshDone = refreshWithUpdatedComponents(assetTmpLocation,stage_location,pushSpecFile,push_spec_location)

      printLog ("\n\n************************* Download Successful **********************************")
      printLog (" *** installerSpecFile : " + installerSpecFile)
      printLog (" *** pushSpecFile      : " + pushSpecFile)
      printLog (" *** buildNumber       : " + buildNumber)
      printLog (" *** logFilePath       : " + logFilePath)
      printLog (" *** download path     : " + assetTmpLocation)
      printLog (" *** Dynamic server location : " +dynamic_files_location)
      printLog (" *** Staging Server path      : " + stage_location) 
      printLog ("******************************************************************************\n\n") 
   except Exception , err:
      #printLog ('Error: Failed to Process the Acrobat Track.' + acroTrackID)
      printStacktrace(traceback.format_exc())
      sys.exit(-1)

