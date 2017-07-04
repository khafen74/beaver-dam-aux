import os
import numpy as np
from osgeo import gdal, ogr
import csv
import math

inDir = r'F:\01_etal\Projects\Modeling\BeaverWaterStorage\wrk_Data\HUC12_data\GIS_data'
outFile = r'F:\01_etal\Projects\Modeling\BeaverWaterStorage\wrk_Data\HUC12_data\HUC12_results\results_20170302.csv'
ofile = open(outFile,'wb')
writer = csv.writer(ofile)
row = ["huc12","bratCap","totPrecipV","elMin","elMax","elMean","elSd"]
writer.writerow(row)

for subdir, dirs, files in os.walk(inDir):
    bratCap = None
    elevMin = None
    elevMax = None
    elevMean = None
    elevSd = None
    pVol = None

    if os.path.exists(subdir + "/BearRiverDEM_10m.tif"):
        demDs = gdal.Open(subdir + "/BearRiverDEM_10m.tif")
        demGeot = demDs.GetGeoTransform()
        demStats = demDs.GetRasterBand(1).GetStatistics(False, True)
        #print demStats
        if demStats is None:
            print 'ERROR: no stats'
        else:
            elevMin = demStats[0]
            elevMax = demStats[1]
            elevMean = demStats[2]
            elevSd = demStats[3]


    if os.path.exists(subdir + "/precip_huc8.tif"):
        precipDs = gdal.Open(subdir + "/precip_huc8.tif")
        precipGeot = precipDs.GetGeoTransform()
        precipData = precipDs.GetRasterBand(1).ReadAsArray()
        precipData[precipData <= 0.0] = np.nan
        pVol = (np.nansum(precipData)/1000.0) * abs(precipGeot[1] * precipGeot[5])

    if os.path.exists(subdir + "/brat_cap_20170224.shp"):
        driver = ogr.GetDriverByName("ESRI Shapefile")
        bratDs = driver.Open(subdir + "/brat_cap_20170224.shp")
        layer = bratDs.GetLayer()
        dams = 0

        for feature in layer:
            len = feature.GetFieldAsDouble("iGeo_Len")
            dens = feature.GetFieldAsDouble("oCC_EX")
            dams += math.ceil(dens * (len/1000.0))

        bratCap = dams

    row = [os.path.relpath(subdir, inDir), bratCap, pVol, elevMin, elevMax, elevMean, elevSd]
    #print row
    writer.writerow(row)

ofile.close()
print "DONE!"

    #open precip, dem, brat
    #get precip volume
    #get dem mean and sd
    #get brat max capacity
    #get HUC12 number
    #calc shape parameter of distribtuion based on mean and sd
    #calc SWE loss for different climate scenarios

