# program globals #
initLoadDir = ""  # should be something like initLoadDir = <get dir from program state save file>
initSaveDir = ""  # should be something like initSaveDir = <get dir from program state save file>


def updateUserData(loadDir="./", saveDir="./"):
    global initLoadDir, initSaveDir
    with open("data.txt", "r+") as f:
        CurrentSaveData = f.read().split("\n")
        # if the save file contains the save and load directories, load them into the program
        if len(CurrentSaveData) == 2:
            initSaveDir = CurrentSaveData[0] if saveDir == "./" else saveDir
            initLoadDir = CurrentSaveData[1] if loadDir == "./" else loadDir
        # go back to the beginning of the file to overwrite
        f.seek(0)
        f.write(initSaveDir + "\n" + initLoadDir)
        # required to write when in read mode
        f.truncate()
        f.close()
    # return the initial save directory to be placed in the textbox
    return(initSaveDir)
