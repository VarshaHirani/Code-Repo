def dir_reduc(arr):
    finalPath = []
    
    #Map for storing opposite directions
    oppDirMap = {"NORTH":"SOUTH","EAST":"WEST","SOUTH":"NORTH","WEST":"EAST"}
    print("Input Path : ",arr)
    i = 0
    
    #if input is not empty
    if arr:
        while i <len(arr):
            print("current directions: ",arr[i])
            #check if there are any directions already mentioned in the path
            if finalPath:
                #check if the last direction in path is opposite of current direction
                if oppDirMap[arr[i]] == finalPath[-1]:
                    #remove the last direction
                    finalPath.pop(-1)
                else:
                    #add the current direction in final path if last direction is not 
                    #its opposite
                    finalPath.append(arr[i])
            else:
                    finalPath.append(arr[i])
            i=i+1
            print("Path",finalPath)
