#!/usr/bin/env python

import argparse
import sys
import subprocess
import shutil
import os
import re
import zipfile
import glob

folder_tmp="/tmp/navbarenabler_tmp"
folder_decompile=folder_tmp+"/framework-res-edit"
folder_buildapk=folder_decompile+"/build/apk"
folder_extracted=folder_tmp+"/framework-extracted"
file_bools=folder_decompile+"/res/values/bools.xml"
file_dimens=folder_decompile+"/res/values/dimens.xml"
apktool="apktool.jar"

def cleanup():
  print "NAVBARTOOL: Cleanup..."
  try:
    shutil.rmtree(folder_tmp)
    if not os.path.isdir(folder_tmp):
      os.makedirs(folder_tmp)
  except Exception:
    pass

def decompileFramework(pathname):
  print "NAVBARTOOL: Decompile '%s'..." % (pathname,)
  proc = subprocess.Popen(["java", "-jar", apktool, "d", pathname, folder_decompile], stdin=subprocess.PIPE)
  proc.communicate()
  return int(proc.returncode)
  
def showNavigationbar(enable):
  # read data
  f = open(file_bools,"r")
  data=f.read()
  f.close()
  
  # set navbar-value
  if enable:
    print "NAVBARTOOL: Enable NavBar..."
    data=re.sub("<bool name=config_showNavigationBar>false<\/bool>","<bool name=config_showNavigationBar>true</bool>",data)
    data=re.sub("<bool name=\"config_showNavigationBar\">false<\/bool>","<bool name=\"config_showNavigationBar\">true</bool>",data)
  else:
    print "NAVBARTOOL: Disable NavBar..."
    data=re.sub("<bool name=config_showNavigationBar>true<\/bool>","<bool name=config_showNavigationBar>false</bool>",data)
    data=re.sub("<bool name=\"config_showNavigationBar\">true<\/bool>","<bool name=\"config_showNavigationBar\">false</bool>",data)
  
  # write-back to file
  f = open(file_bools,"w")
  f.write(data)
  
  # close file
  f.close()
  
def showNavigationbarWidth(size):
  # read data
  f = open(file_dimens,"r")
  data=f.read()
  f.close()
  
  # set navbar-value
  print "NAVBARTOOL: Set NavBar-width to '%s'..." % (size,)
  data=re.sub("<dimen name=navigation_bar_width>.*<\/dimen>","<dimen name=navigation_bar_width>"+size+"</dimen>",data)
  data=re.sub("<dimen name=\"navigation_bar_width\">.*<\/dimen>","<dimen name=\"navigation_bar_width\">"+size+"</dimen>",data)

  # write-back to file
  f = open(file_dimens,"w")
  f.write(data)
  
  # close file
  f.close()
  
def showNavigationbarHeight(size):
  # read data
  f = open(file_dimens,"r")
  data=f.read()
  f.close()
  
  # set navbar-value
  print "NAVBARTOOL: Set NavBar-height to '%s'..." % (size,)
  data=re.sub("<dimen name=navigation_bar_height>.*<\/dimen>","<dimen name=navigation_bar_height>"+size+"</dimen>",data)
  data=re.sub("<dimen name=\"navigation_bar_height\">.*<\/dimen>","<dimen name=\"navigation_bar_height\">"+size+"</dimen>",data)

  # write-back to file
  f = open(file_dimens,"w")
  f.write(data)
  
  # close file
  f.close()
  
def showNavigationbarHeightLandscape(size):
  # read data
  f = open(file_dimens,"r")
  data=f.read()
  f.close()
  
  # set navbar-value
  print "NAVBARTOOL: Set NavBar-landscape-height to '%s'..." % (size,)
  data=re.sub("<dimen name=navigation_bar_height_landscape>.*<\/dimen>","<dimen name=navigation_bar_height_landscape>"+size+"</dimen>",data)
  data=re.sub("<dimen name=\"navigation_bar_height_landscape\">.*<\/dimen>","<dimen name=\"navigation_bar_height_landscape\">"+size+"</dimen>",data)

  # write-back to file
  f = open(file_dimens,"w")
  f.write(data)
  
  # close file
  f.close()
  
def recompileFramework():
  print "NAVBARTOOL: Recompile..."
  proc = subprocess.Popen(["java", "-jar", apktool, "b", folder_decompile], stdin=subprocess.PIPE)
  proc.communicate()
  return int(proc.returncode)

def addFolderToZip(myZipFile,folder):
  print folder
  folder = folder.encode('ascii') #convert path to ascii for ZipFile Method
  print folder
  rootlen=len(os.path.split(folder)[0])
  print folder
  #print ("/tmp/navbarenabler_tmp/framework-res-edit/build/apk/res/drawable-land-hdpi/jog_tab_bar_right_end_confirm_red.9.png")[rootlen:]
  #return
  for file in glob.glob(folder+"/*"):
    if os.path.isfile(file):
      print "%s -> %s" % (file, os.path.split(folder)[1]+"/"+file[rootlen:])
      #myZipFile.write(file, file, zipfile.ZIP_DEFLATED)
    elif os.path.isdir(file):
      addFolderToZip(myZipFile,file)
      
def zipdir(dirPath=None, zipFilePath=None, includeDirInZip=True):
    """Create a zip archive from a directory.
    
    Note that this function is designed to put files in the zip archive with
    either no parent directory or just one parent directory, so it will trim any
    leading directories in the filesystem paths and not include them inside the
    zip archive paths. This is generally the case when you want to just take a
    directory and make it into a zip file that can be extracted in different
    locations. 
    
    Keyword arguments:
    
    dirPath -- string path to the directory to archive. This is the only
    required argument. It can be absolute or relative, but only one or zero
    leading directories will be included in the zip archive.

    zipFilePath -- string path to the output zip file. This can be an absolute
    or relative path. If the zip file already exists, it will be updated. If
    not, it will be created. If you want to replace it from scratch, delete it
    prior to calling this function. (default is computed as dirPath + ".zip")

    includeDirInZip -- boolean indicating whether the top level directory should
    be included in the archive or omitted. (default True)

"""
    if not zipFilePath:
        zipFilePath = dirPath + ".zip"
    if not os.path.isdir(dirPath):
        raise OSError("dirPath argument must point to a directory. "
            "'%s' does not." % dirPath)
    parentDir, dirToZip = os.path.split(dirPath)
    #Little nested function to prepare the proper archive path
    def trimPath(path):
        archivePath = path.replace(parentDir, "", 1)
        if parentDir:
            archivePath = archivePath.replace(os.path.sep, "", 1)
        if not includeDirInZip:
            archivePath = archivePath.replace(dirToZip + os.path.sep, "", 1)
        return os.path.normcase(archivePath)
        
    outFile = zipfile.ZipFile(zipFilePath, "w",
        compression=zipfile.ZIP_DEFLATED)
    for (archiveDirPath, dirNames, fileNames) in os.walk(dirPath):
        for fileName in fileNames:
            filePath = os.path.join(archiveDirPath, fileName)
            outFile.write(filePath, trimPath(filePath))
        #Make sure we get empty directories as well
        if not fileNames and not dirNames:
            zipInfo = zipfile.ZipInfo(trimPath(archiveDirPath) + "/")
            #some web sites suggest doing
            #zipInfo.external_attr = 16
            #or
            #zipInfo.external_attr = 48
            #Here to allow for inserting an empty directory.  Still TBD/TODO.
            outFile.writestr(zipInfo, "")
    outFile.close()
    

def copy_all(fr, to, overwrite=True):
  fr = os.path.normpath(fr)
  to = os.path.normpath(to)

  if os.path.isdir(fr):
    if (not os.path.exists(to + os.path.basename(fr)) and not
    os.path.basename(fr) == os.path.basename(to)):
      to += "/" + os.path.basename(fr)
      mkdirs(to)
    for file in os.listdir(fr):
      copy_all(fr + "/" + file, to + "/")
  else: #symlink or file
    dest = to
    if os.path.isdir(to):
      dest += "/"
      dest += os.path.basename(fr)

    if overwrite and (os.path.exists(dest) or os.path.islink(dest)):
      rm(dest)

    if os.path.isfile(fr):
      shutil.copy2(fr, dest)
    else: #has to be a symlink
      os.symlink(os.readlink(fr), dest)  


def mkdirs(path):                                                 
  if not os.path.isdir(path):
    os.makedirs(path)


def rm(path):                                                     
  if os.path.isfile(path) or os.path.islink(path):
    os.remove(path)
  elif os.path.isdir(path):
    for file in os.listdir(path):
      fullpath = path+"/"+file
      os.rmdir(fullpath)
                
def packFramework(old_framework, new_framework):
  print "NAVBARTOOL: Pack..."
  
  # extract zip
  f = zipfile.ZipFile( old_framework, "r" )
  f.extractall(folder_extracted)
  f.close()
  
  # copy new resources
  copy_all(folder_buildapk+"/res", folder_extracted);
  
  # delete resources.arsc(we add it in uncompressed mode later)
  rm(folder_extracted+"/resources.arsc")
  
  # zip directory
  rm(new_framework)
  zipdir(folder_extracted, new_framework, False)
  
  # add new resources.arsc
  f = zipfile.ZipFile( new_framework, "a" )
  f.write(folder_buildapk+"/resources.arsc", "/resources.arsc", zipfile.ZIP_STORED)
  f.close()

def main(argv):
  # cleanup
  cleanup()

  # decompile framework
  decompileFramework(argv.framework)
  
  # set NavBar-Status
  showNavigationbar(not argv.disable)
  
  # set Navbar-width
  if argv.width is not None:
    showNavigationbarWidth(argv.width)
    
  # set Navbar-height
  if argv.height is not None:
    showNavigationbarHeight(argv.height)
    
  # set Navbar-height for landscape
  if argv.height_landscape is not None:
    showNavigationbarHeightLandscape(argv.height_landscape)
  
  # recompile framework
  recompileFramework()
  
  # pack final framework
  packFramework(argv.framework, argv.frameworkNew)

  print "NAVBARTOOL: Done."
  return 0

if __name__ == '__main__':
  # buils ArgumentParser
  parser = argparse.ArgumentParser(description='enable/disable NavigationBar and change their size.')
  parser.add_argument('framework', action="store")
  parser.add_argument('frameworkNew', action="store")
  parser.add_argument('-d', action="store_true", dest="disable", help="Disable NavigationBar instead of enabling")
  parser.add_argument('-w', action="store", dest="width", help="Set NavigationBar-width to WIDTH")
  parser.add_argument('-s', action="store", dest="height", help="Set NavigationBar-height to HEIGHT")
  parser.add_argument('-sl', action="store", dest="height_landscape", help="Set NavigationBar-height to HEIGHT_LANDSCAPE")
  
  # parse args
  args=parser.parse_args()
  
  # call main-function
  sys.exit(main(args))