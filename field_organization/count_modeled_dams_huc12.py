import os
from osgeo import gdal, ogr

driver = ogr.GetDriverByName("ESRI Shapefile")

baseShp = r"F:\01_etal\Projects\Modeling\BeaverWaterStorage\wrk_Data\AnalysisRuns\BearRiverHUC8\EntireBasin\shp\HUC12.shp"
folders = ["03_out_05", "03_out_25", "03_out_50", "03_out_100"]
filename = "ModeledDamPoints.shp"
field = "HUC12"
rootDir = r"F:\01_etal\Projects\Modeling\BeaverWaterStorage\wrk_Data\AnalysisRuns\BearRiverHUC8"

baseDs = driver.Open(baseShp, 1) # the second argument (1) makes the data source writeable
lyr = baseDs.GetLayer()

# field = ogr.FieldDefn("dams5", ogr.OFTInteger)
# lyr.CreateField(field)
# field = ogr.FieldDefn("dams25", ogr.OFTInteger)
# lyr.CreateField(field)
# field = ogr.FieldDefn("dams50", ogr.OFTInteger)
# lyr.CreateField(field)
# field = ogr.FieldDefn("dams100", ogr.OFTInteger)
# lyr.CreateField(field)

for feature in lyr:
    huc12name = feature.GetFieldAsString(field)
    huc8name = huc12name[0:8]
    #print huc8name
    for folder in folders:
        file = rootDir + "/" + huc8name + "/" + "HUC12/" + huc12name + "/" + folder + "/" +filename
        if os.path.exists(file):
            #print file
            ds = driver.Open(file, 1)
            lyrTemp = ds.GetLayer()
            print lyrTemp.GetFeatureCount()
            if folder == folders[0]:
                feature.SetField("dams5", lyrTemp.GetFeatureCount())
            elif folder == folders[1]:
                feature.SetField("dams25", lyrTemp.GetFeatureCount())
            elif folder == folders[2]:
                feature.SetField("dams50", lyrTemp.GetFeatureCount())
            elif folder == folders[3]:
                feature.SetField("dams100", lyrTemp.GetFeatureCount())
            lyr.SetFeature(feature)

feature.Destroy()
baseDs.Destroy()




