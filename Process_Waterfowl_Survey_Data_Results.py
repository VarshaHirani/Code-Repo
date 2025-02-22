"""
A wildlife study involving ducks is taking place in North America. Researchers are visiting some wetlands in a certain area taking a survey of what they see. The researchers will submit reports that need to be processed by your function.

Input
The input for your function will be an array with a list of common duck names along with the counts made by the researchers. The names and counts are separated by spaces in one array element. The number of spaces between the name and the count could vary; but, there will always be at least one. A name may be repeated because a report may be a combination of surveys from different locations.

An example of an input array would be:

["Redhead 3", "Gadwall 1", "Smew 4", "Greater Scaup 10", "Redhead 3", "Gadwall 9", "Greater Scaup 15", "Common Eider 6"]
Processing
Your function should change the names of the ducks to a six-letter code according to given rules (see below). The six-letter code should be in upper case. The counts should be summed for a species if it is repeated.

Output
The final data to be returned from your function should be an array sorted by the species codes and the total counts as integers. The codes and the counts should be individual elements.

An example of an array to be returned (based on the example input array above) would be:

["COMEID", 6, "GADWAL", 10, "GRESCA", 25, "REDHEA", 6, "SMEW", 4]
The codes are strings in upper case and the totaled counts are integers.

Special Note
If someone has "Labrador Duck" in their list, the whole list should be thrown out as this species has been determined to be extinct. The person who submitted the list is obviously unreliable. Their lists will not be included in the final data. In such cases, return an array with a single string element in it: "Disqualified data"

Rules for converting a common name to a six-letter code:

Hyphens should be considered as spaces.
If a name has only one word, use the first six letters of the name. If that name has less than six letters, use what is there.
If a name has two words, take the first three letters of each word.
If a name has three words, take the first two letters of each word.
If a name has four words, take the first letters from the first two words, and the first two letters from the last two words.
"""

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
