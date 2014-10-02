'''
Created on Jan 6, 2014

@author: Arya
'''

import gdata.docs.client, gdata.docs.service

def init():
    
    global firstTime        # If True, user is using app for first time
    global docsclient       # Google Docs client
    global serviceclient    # Google Docs Services client
    global folderContent    # Document Contents of app folder
    global folderName       # Name of folder that file is uploaded to
    global fileName         # File name on personal computer
    global filePath         # Path of the file on computer
    global fileContent      # Encrypted Content of app document
    global allContent       # At any given moment, all content holds all encrypted info in the app document
    global decryptedContent # Decrypted version of all content
    global resources        # App folder resources  
    global queryclient      # Folder search client by name
    global cleanName
    global access_fields
    global access_info
    global first_decryption
    
    first_decryption = False
    access_fields = []
    access_info = []
    firstTime = False
    docsclient = gdata.docs.client.DocsClient()         #source = 'RPi Python-Gdata 2.0.18')
    serviceclient = gdata.docs.service.DocsService()    #source = 'RPi Python-Gdata 2.0.18')
    folderName = 'Cryptfolio'
    fileName = 'CryptoText.txt'
    cleanName = 'CleanUpload.txt'
    fileContent = ""
    allContent = ""
    decryptedContent = ""
    queryclient = gdata.docs.client.DocsQuery(title = folderName, title_exact = 'true', show_collections = 'true')
    docsclient.ssl = True
    