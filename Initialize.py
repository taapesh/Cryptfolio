'''
Created on Jan 6, 2014

@author: Arya
'''

import sys, os.path
import globalVars
import gdata.docs.data

global seshID
seshID = ""

# Finds App folder on Google Drive
# Creates the folder if it does not exist
def findFolder(new_user_setup):
    print 'Finding folder...',
    # Get a list of all available resources (GetAllResources() requires >= gdata-2.0.15)
    try:
        
        globalVars.resources = globalVars.docsclient.GetAllResources (
                                                                     
            uri='https://docs.google.com/feeds/default/private/full/-/folder?title=' + globalVars.folderName + '&title-exact=true'
        )
    
    except:
        
        sys.exit('ERROR: Unable to retrieve resources')
    
    # If no matching resources were found, create it and retry
    if not globalVars.resources:
        
        new_user_setup()
        print 'Running first time setup...'
        print 'Creating Cryptfolio Folder in Google Drive...',
        globalVars.serviceclient.CreateFolder('Cryptfolio')
        
        globalVars.resources = globalVars.docsclient.GetAllResources (
            uri='https://docs.google.com/feeds/default/private/full/-/folder?title=' + globalVars.folderName + '&title-exact=true'
        )
        
        print "Done"
    
    print 'Done'
    return globalVars.resources # Returns the found folder as a resource

# Finds the encrypted text file on Google Drive
# Creates the file if it does not exist
# Reads and stores contents of file
def findFile():
    print 'Finding file...',
    # Find app folder
    folder = globalVars.docsclient.GetResources(q=globalVars.queryclient).entry[0]
    
    # Get the resources (file) in the folder
    globalVars.folderContents = globalVars.docsclient.GetResources(uri=folder.content.src)
    
    # If the length of contents list is 0, user is using app for the first time and file needs to be uploaded
    if len(globalVars.folderContents.entry) == 0:
        uploadFile()
    
    # Read and store contents of file
    globalVars.folderContents = globalVars.docsclient.GetResources(uri=folder.content.src)
    globalVars.fileContent = globalVars.docsclient.DownloadResourceToMemory(globalVars.folderContents.entry[0])
    globalVars.allContent = globalVars.fileContent
    
    print 'Done'
    
# Uploads the encrypted file to Google Drive
def uploadFile():
    globalVars.firstTime = True
    CryptoFile = open(globalVars.cleanName)
    globalVars.filePath = str( os.path.abspath(CryptoFile.name) )
    CryptoFile.close()
    
    print 'Uploading file...',
    
    # Create new resource and point media object to it
    newResource = gdata.docs.data.Resource(globalVars.filePath, "CryptoText")
    media = gdata.data.MediaSource()
    media.SetFileHandle(globalVars.filePath, 'mime/type')
    
    # Upload file into folder
    newDoc = globalVars.docsclient.CreateResource(newResource, media=media, collection=globalVars.resources[0])
   
    print 'Done'
    print