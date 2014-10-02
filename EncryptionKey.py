'''
Created on Jan 6, 2014

@author: Arya
'''

import random
import gdata.docs.data
import globalVars
import os.path

allGib = []

# All characters used to encrypt text
allChars = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z",
            "A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z",
            "1","2","3","4","5","6","7","8","9","0","1","2","3","4","5","6","7","8","9","0","1","2","3","4","5","6","7","8","9","0"]
lengthChars = len(allChars)

# Randomize above list to improve overall randomness
randomChars = []

for i in range (len(allChars)):
    
    randNum = random.randint(0,len(allChars)-1)
    randomChars.append(allChars.pop(randNum))

# All possible characters used in passwords, if a new character is seen, add it to list and make change to key file
allPasswordChars = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z",
                    "A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z",
                    "1","2","3","4","5","6","7","8","9","0","!","@","#","$","%","^","&","*","(",")","<",">","?"," ",".",",", '_']

# All hash representations of each password character
stringReps = [ [],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],
               [],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],
               [],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[], [] ]

# All hashes used for character replacement or for gibberish
# Prevents any hash from being reused
allHashes = []

global processedLines
processedLines = []

# A key does not exist until you input information for the first time
# Then, every time new information is added, the key is expanded
def get_key_history():
    global processedLines
    
    encryptKey = open("key.txt", "r")
    allLines = encryptKey.readlines()
    processedLines = []
    
    # Get all past hash representations of characters
    # Hash reps file contains the character followed by a line of all of its possible hash representations, separated by a commas
    charIndex = 0
    for line in allLines:

        line = line.rstrip('\n')
        if line == "end": 
            break
        
        processedLines.append(line)
      
        if len(line) == 1:
            continue
        
        else:
            
            if len(line) == 0:
                charIndex += 1
                continue
            
            else:
                hashReps = line.split(",")
                del hashReps[0]
                
                for hashRep in hashReps:
                    
                    allHashes.append(hashRep)
                    stringReps[charIndex].append(hashRep)
            
            charIndex += 1

    # Get all past gibberish inserted into encryption
    gibFile = open("gib.txt", "r")
    gibLines = gibFile.readlines()
    
    for gib in gibLines:
        
        gib = gib.strip()
        allGib.append(gib)

# Encrypt new information and update key file
def expandKey(info, finished_encrypting):
    
    # Delete the file on Drive before reuploading it with new changes
    folder = globalVars.docsclient.GetResources(q=globalVars.queryclient).entry[0]
    globalVars.folderContents = globalVars.docsclient.GetResources(uri=folder.content.src)
    globalVars.docsclient.DeleteResource(globalVars.folderContents.entry[0])
    
    # Get file path before uploading
    CryptoFile = open("CryptoText.txt", "r")
    globalVars.filePath = str( os.path.abspath(CryptoFile.name))
    CryptoFile.close()
    
    # Keep all past info and all new info added as a running tab in variable allContent
    # When uploading new information, allContent is used to determine all previous info
    # Then the new info is appended to it, written to file, then uploaded. File is wiped after
    if len(globalVars.allContent) == 1:
        
        globalVars.allContent = ""
    
    # Expand key for new encrypted text
    for text in info:  
        
        gibTotal = 0
        gib_For_This_Info = []
        encryptedInfo = ""
        encryptedText = "" 
        
        for char in text:
 
            charIndex = allPasswordChars.index(char)
            
            # Generate a new hash representation of this character and add it to string rep list and file
            rep = generateRep()
            stringReps[charIndex].append(rep)
            processedLines[charIndex*2 + 1] += ',' + rep
            
            # Update encrypted info
            encryptedInfo += rep
            
            print 'Generated hash for character', char, "-", rep
        
            # Generate a random amount of gibberish to be inserted alongside this information
            randNum = random.randint(0,20)
            gibTotal += randNum
            
            for i in range (randNum):
                
                gib = generateRep()
                allGib.append(gib)
                gib_For_This_Info.append(gib)
        
        # Determine where the info will be inserted in the line of gibberish
        insertIndex = random.randint(0, randNum)
        
        # Construct complete line to be inserted into file
        for i in range(gibTotal):
            
            if (i == insertIndex):
                encryptedText += encryptedInfo
                continue
            
            encryptedText += gib_For_This_Info[i]
        
        # Concatenate encrypted text with string of all content
        globalVars.allContent += encryptedText +'\n'
    
    fileContent = globalVars.allContent.split('\n')
    CryptoFile = open(globalVars.fileName, "w")
    
    for line in fileContent:
        
        if line == '' or line == '\n':
            print 'EMPTY LINE, skipped writing'
            continue
        
        line = line.rstrip('\n').replace('\r', '')
        CryptoFile.write(line +'\n')
    
    CryptoFile.close()
    
    print
    print 'Uploading changes...',
    
    # Create new resource and point media object to it
    newResource = gdata.docs.data.Resource(globalVars.filePath, "CryptoText")
    media = gdata.data.MediaSource()
    media.SetFileHandle(globalVars.filePath, 'mime/type')
    
    # Upload file into folder
    newDoc = globalVars.docsclient.CreateResource(newResource, media=media, collection=globalVars.resources[0])
    print 'Done'
    
    # Clear file content
    open(globalVars.fileName, "w").close()
    
    # Update encryption key history
    encryptKey = open("key.txt", "w")
    gibFile = open("gib.txt", "w")
    
    for line in processedLines:
        
        encryptKey.write(line + "\n")
    
    for gib in allGib:
        
        gibFile.write(gib + "\n")
    
    encryptKey.write('end')
    
    encryptKey.close()
    gibFile.close()
    
    print 'Updated encryption key history'
    print
    print 'Encrypted info:',encryptedInfo
    print 'Constructed encrypted text',encryptedText
    print
    
    decryptText(globalVars.allContent)
    finished_encrypting()
    
# Decrypts file content       
def decryptText(text):
    
    allLines = text.split("\n")
    decryptedText = ""
    
    for line in allLines:
        
        line=line.rstrip('\n')
        
        # Remove gibberish from encrypted text
        for gib in allGib:
            
            line = line.replace(gib, "")
      
        for i in range (len(stringReps)):
            
            for j in range (len(stringReps[i])):
                
                if len(stringReps[i]) == 0:
                    continue
                
                if stringReps[i][j] in line:
                    line = line.replace(stringReps[i][j], allPasswordChars[i]+'(@!&$#^%*)-+')
        
        line = line.replace("(@!&$#^%*)-+","")
        decryptedText += line + '\n'
   
    
    decryptedText = decryptedText.rstrip('\n')
    
    globalVars.decryptedContent = decryptedText.split('\n')
    

    if len(globalVars.decryptedContent) == 1 and globalVars.decryptedContent[0] == '':
        del globalVars.decryptedContent[0]
    
    # Only need to do this once through the initial startup
    # After initial startup, new info is added through the function that encrypts data
    if not globalVars.first_decryption:    
        for content in globalVars.decryptedContent:
            
            if '_access_tag' in content:
                
                if content[ : content.index('_access_tag')] in globalVars.access_fields:
                    continue
                
                elif content.endswith('_access_tag\r'):
                    globalVars.access_fields.append(content.replace('_access_tag\r', ''))
                
                elif content.endswith('_access_tag'):
                    globalVars.access_fields.append(content.replace('_access_tag', ''))
            
            else:
                globalVars.access_info.append(content.replace('\r', ''))
            
            globalVars.first_decryption = True
    
    '''
    print 'decrypted text'
    
    for line in globalVars.decryptedContent:
        print line.replace('_access_tag', '')
    '''
            
    return decryptedText
    
# Generates random hashes of random lengths to represent characters or gibberish
def generateRep():
    length = random.randint(6,13)
    stringRep = ""
    
    while stringRep in allHashes or stringRep =="":
        
        stringRep = "" 
        for i in range(length):
            
            randIndex = random.randint(0, lengthChars-1)
            stringRep += randomChars[randIndex]
    
    allHashes.append(stringRep)
    return stringRep
