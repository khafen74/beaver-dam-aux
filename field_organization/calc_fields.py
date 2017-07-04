import os
from osgeo import gdal, ogr

inshp = r"F:\01_etal\Projects\Modeling\BeaverWaterStorage\wrk_Data\AnalysisRuns\BearRiverHUC8\EntireBasin\shp\brat100_huc12.shp"

driver = ogr.GetDriverByName("ESRI Shapefile")
ds = driver.Open(inshp, 1) # the second argument (1) makes the data source writeable
lyr = ds.GetLayer()

field = ogr.FieldDefn("per1", ogr.OFTReal)
lyr.CreateField(field)
field = ogr.FieldDefn("per2", ogr.OFTReal)
lyr.CreateField(field)
field = ogr.FieldDefn("per3", ogr.OFTReal)
lyr.CreateField(field)
field = ogr.FieldDefn("per4", ogr.OFTReal)
lyr.CreateField(field)
field = ogr.FieldDefn("per5", ogr.OFTReal)
lyr.CreateField(field)

for feature in lyr:

    tLo = feature.GetFieldAsDouble("totalLo")
    tMid = feature.GetFieldAsDouble("totalMid")
    tHi = feature.GetFieldAsDouble("totalHi")
    swe1 = feature.GetFieldAsDouble("swe1")
    swe2 = feature.GetFieldAsDouble("swe2")
    swe3 = feature.GetFieldAsDouble("swe3")
    swe4 = feature.GetFieldAsDouble("swe4")
    swe5 = feature.GetFieldAsDouble("swe5")

    feature.SetField("per1", (tMid / swe1) * 100.0)
    feature.SetField("per2", (tMid / swe2) * 100.0)
    feature.SetField("per3", (tMid / swe3) * 100.0)
    feature.SetField("per4", (tMid / swe4) * 100.0)
    feature.SetField("per5", (tMid / swe5) * 100.0)

    lyr.SetFeature(feature)

    print (tMid/swe1) * 100.0

feature.Destroy()
ds.Destroy()


