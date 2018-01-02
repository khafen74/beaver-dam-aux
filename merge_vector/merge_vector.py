import os
import ogr

huc8s = [16010101, 16010102, 16010201, 16010202, 16010203, 16010204]
baseDirName = "HUC12"
cap = "100"
filename = "ModeledDamPoints.shp"
baseDir = r"E:\konrad\Projects\Modeling\BeaverWaterStorage\wrk_Data\AnalysisRuns\BearRiverHUC8"
newfile = r"E:\konrad\Projects\Modeling\BeaverWaterStorage\wrk_Data\AnalysisRuns\BearRiverHUC8\EntireBasin" + "/out_" + cap + "/ModeledDamPoints.shp"
driver = ogr.GetDriverByName("ESRI Shapefile")
outDs = driver.CreateDataSource(newfile)
outLyr = outDs.CreateLayer(newfile, geom_type=ogr.wkbPoint)
field = ogr.FieldDefn("ht_mid", ogr.OFTReal)
outLyr.CreateField(field)
field = ogr.FieldDefn("dam_type", ogr.OFTString)
outLyr.CreateField(field)
field = ogr.FieldDefn("vol_lo", ogr.OFTReal)
outLyr.CreateField(field)
field = ogr.FieldDefn("vol_mid", ogr.OFTReal)
outLyr.CreateField(field)
field = ogr.FieldDefn("vol_hi", ogr.OFTReal)
outLyr.CreateField(field)

#loop through all shapefiles and add features to new shapefile

for huc8 in huc8s:
    prim = 0
    sec = 0
    searchDir = baseDir + "/" + str(huc8) + "/" + baseDirName
    print searchDir
    for subdir, dirs, files in os.walk(searchDir):
        if os.path.relpath(subdir, searchDir).split("\\")[-1] == ("03_out_"+cap):
            if os.path.exists(subdir + "/" + filename):
                dsCopy = ogr.Open(subdir + "/" + filename)
                lyrCopy = dsCopy.GetLayer()
                for featCopy in lyrCopy:
                    damHeight = featCopy.GetFieldAsDouble("ht_mid")
                    outFeat = ogr.Feature(outLyr.GetLayerDefn())
                    outFeat.SetField("ht_mid", damHeight)
                    outFeat.SetField("vol_lo", featCopy.GetFieldAsDouble("vol_lo"))
                    outFeat.SetField("vol_mid", featCopy.GetFieldAsDouble("vol_mid"))
                    outFeat.SetField("vol_hi", featCopy.GetFieldAsDouble("vol_hi"))
                    outFeat.SetGeometry(featCopy.GetGeometryRef().Clone())
                    outLyr.CreateFeature(outFeat)
                    outFeat = None
                    outLyr.SyncToDisk()
