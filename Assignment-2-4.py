from __future__ import division
from mevis import *
from LocalFilePathSupport import populateComboBoxWithDefaultPathVariables


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
def applyIsoSurface():
    ctx.field("IsoSurface1.apply").touch()


# ---------------------------------------------------------------
def updateConnections():
    if ctx.field("IsoSurface1.autoApply").value:
        applyIsoSurface()


# ---------------------------------------------------------------
def updateFields(field=None):
    if not field:
        return

    if field.getName() == "quality":
        updateResolution()

    if ctx.field("autoApply").value:
        applyIsoSurface()


# ---------------------------------------------------------------
def updateResolution():
    res = ctx.field("quality").intValue()
    ctx.field("IsoSurface1.quality").setIntValue(res)


# ----------------------------------------------------------------

def deleteAllMarkers():
    ctx.field("SoView2DMarkerEditor.deleteAll").touch()


def LoadImage():
    ctx.field("LocalImage1.name").value = ctx.field("name").value
    ctx.field("LocalImage1.load").touch()
# ----------------------------------------------------------------
