# program globals #
initLoadDir = ""  # should be something like initLoadDir = <get dir from program state save file>
initSaveDir = ""  # should be something like initSaveDir = <get dir from program state save file>
initVidFmt = ""
initAudFmt = ""


def updateUserData(loadDir="./", saveDir="./", vidFmt=None, audFmt=None):
    global initLoadDir, initSaveDir, initVidFmt, initAudFmt
    with open("data.txt", "r+") as f:
        CurrentSaveData = f.read().split("\n")
        # if the save file contains the save and load directories, load them into the program
        initSaveDir = CurrentSaveData[0] if saveDir == "./" else saveDir
        initLoadDir = CurrentSaveData[1] if loadDir == "./" else loadDir
        initVidFmt = CurrentSaveData[2] if vidFmt is None else vidFmt
        initAudFmt = CurrentSaveData[3] if audFmt is None else audFmt

        # go back to the beginning of the file to overwrite
        f.seek(0)
        f.write(initSaveDir + "\n" + initLoadDir + "\n" + initVidFmt + "\n" + initAudFmt)
        # required to write when in read mode
        f.truncate()
        f.close()
    # return the initial save directory to be placed in the textbox
    return initSaveDir, initVidFmt, initAudFmt
