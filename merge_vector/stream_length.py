import os
import ogr

huc8s = [16010101, 16010102, 16010201, 16010202, 16010203, 16010204]
baseDirName = "HUC12"
cap = "100"
filename = "brat_cap_20170224.shp"
baseDir = r"F:\01_etal\Projects\Modeling\BeaverWaterStorage\wrk_Data\AnalysisRuns\BearRiverHUC8"


#loop through all shapefiles and add features to new shapefile

for huc8 in huc8s:
    length = 0
    dams = 0
    searchDir = baseDir + "/" + str(huc8) + "/" + baseDirName
    print searchDir
    for subdir, dirs, files in os.walk(searchDir):
        if os.path.relpath(subdir, searchDir).split("\\")[-1] == ("01_shpIn"):
            if os.path.exists(subdir + "/" + filename):
                dsCopy = ogr.Open(subdir + "/" + filename)
                lyrCopy = dsCopy.GetLayer()
                for featCopy in lyrCopy:
                    dens = featCopy.GetFieldAsDouble("oCC_EX")
                    geom = featCopy.GetGeometryRef()
                    length = length + geom.Length()
                    dams = dams + (dens / 1000) * geom.Length()
                    outFeat = None
                    #outLyr.SyncToDisk()
    print str(huc8) + " " + str(length) + " " + str(dams)