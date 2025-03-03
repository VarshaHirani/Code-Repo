
def create_report(names):
    duckDict = {}
    resLst = []
    # loop through each duck name
    for name in names:
        # if duck name has "Labrador Duck" return
        if "Labrador Duck" in name:
            return ["Disqualified data"] 

        else:
            # create a list of words in duck name
            tempList = name.replace('-'," ").split()
            
            #get the code of duck name
            code = GetCode(tempList[:-1])
            
            #check if code already exists in out map and accordingly add value
            if code in duckDict:
                print("Duplicate Duck Name: code: %s, val: %s" %(code,tempList[-1]))
                duckDict[code] = duckDict[code] + int(tempList[-1])

            else:
                print("Duck Code added to Output List: code: %s, val: %s" %(code,tempList[-1]))
                duckDict[code] = int(tempList[-1])
  
    #get alphabetically sorted lst of code names
    duckCodes = sorted(duckDict.keys())
    
    #get the final sorted list with values
    for key in duckCodes:
        resLst.append(key)
        resLst.append(duckDict[key])
   
    print(resLst)
    return resLst

def GetCode(duckname):
    #Function to get code name from name given in input
    code = ""
    
    #check the number of words in duck name
    nameLen = len(duckname)
    
    #based on lenght of duck name, generate the code
    
    #if there is only one word then if its lenght is less then 5, output
    #the word in upper case else first 6 letters of work in upper case
    if nameLen == 1:
        if len(duckname[0]) > 6:
            code = duckname[0][:6].upper()
        else:
            code = duckname[0].upper()
            
    #if a name has two words, take the first three letters of each word.
    elif nameLen == 2:
        code = (duckname[0][:3]+duckname[1][:3]).upper()
        
    #If a name has three words, take the first two letters of each word.
    elif nameLen == 3:
        code = (duckname[0][:2]+duckname[1][:2]+duckname[2][:2]).upper()
        
    #If a name has four words, take the first letters from the first two words, 
    #and the first two letters from the last two words.
    elif nameLen == 4:
        code = (duckname[0][:1]+duckname[1][:1]+duckname[2][:2]+duckname[3][:2]).upper()

    return code
