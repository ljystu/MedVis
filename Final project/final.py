from __future__ import division
from mevis import *
from LocalFilePathSupport import populateComboBoxWithDefaultPathVariables

gRecentDirectoryPath = ""

# Load_____________

def init():
    ctx.field("name").value = ctx.field("LocalImage1.name").value


def fileDialog():
    exp = ctx.expandFilename(ctx.field("name").stringValue())
    filename = MLABFileDialog.getOpenFileName(exp, "", "Open file")
    if filename:
        ctx.field("name").value = ctx.unexpandFilename(filename)


# ISO_____

# ----------------------------------------------------------------
def inputImageChanged():
    if ctx.field("IsoSUrface1.autoUpdate").value:
        applyIsoSurface()


# ---------------------------------------------------------------
def applyTimepoint():
    ctx.field("IsoSurface1.apply").touch()


# ---------------------------------------------------------------
def updateConnections():
    if ctx.field("IsoSurface1.autoApply").value:
        applyIsoSurface()


# ---------------------------------------------------------------
def updateFields(field=None):
    if not field:
        return

    if field.getName() == "timepoint":
        updateTimepoint()

# ---------------------------------------------------------------
def updateTimepoint():
    res = ctx.field("timepoint").intValue()
    ctx.field("RespirationCircle.currentTimePoint").setIntValue(res)


# ----------------------------------------------------------------

def deleteAllMarkers():
    ctx.field("SoView2DMarkerEditor.deleteAll").touch()


def LoadImage():
    ctx.field("DirectDicomImport.fullUserSrcPaths").value = ctx.field("name").value
    clearLogAndImport()
# ----------------------------------------------------------------
def clearLogAndImport():
  ctx.field("DirectDicomImport.clearConsole").touch()
  ctx.field("DirectDicomImport.dplImport").touch()
def addUserDir():
  global gRecentDirectoryPath
  
  actualPath = ""
  if len(gRecentDirectoryPath) > 0:
    actualPath = gRecentDirectoryPath
  else:
    actualPath = ctx.localPath()
  
  gRecentDirectoryPath = MLABFileDialog.getExistingDirectory(actualPath, "Select directory to add", MLABFileDialog.ShowDirsOnly)
  if len(gRecentDirectoryPath) > 0:
   
    newContent = (gRecentDirectoryPath + "\n")
    ctx.field("name").value = newContent

