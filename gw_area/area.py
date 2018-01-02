import os
import gdal
import csv
import numpy as np

basedir = "E:/konrad/Projects/Modeling/BeaverWaterStorage/wrk_Data/AnalysisRuns/BearRiverHUC8/EntireBasin"
outfile = basedir + "/area_affected.csv"
caps = ["05","25","50","100"]
swfiles = ["depLo_m.tif", "depMid_m.tif", "depHi_m.tif"]
gwfiles = ["hdch_lo_m3.tif", "hdch_mid_m3.tif", "hdch_hi_m3.tif"]

ofile = open(outfile, 'wb')
writer = csv.writer(ofile)
row = ["capacity", "low", "mid", "high", "slow", "smid", "shigh", "glow", "gmid", "ghigh"]
writer.writerow(row)

for cap in caps:
    row[0] = cap
    for i in range(0, len(swfiles)) :
        sw = gdal.Open(basedir + "/out_" + cap + "/" + swfiles[i])
        gw = gdal.Open(basedir + "/out_" + cap + "/" + gwfiles[i])
        geot = sw.GetGeoTransform()
        swdata = sw.GetRasterBand(1).ReadAsArray()
        gwdata = gw.GetRasterBand(1).ReadAsArray()

        row[i+1]=(((swdata > 0.01) | (gwdata > 0.01)).sum()) * geot[1] * geot[1]
        row[i+4] = ((swdata > 0.01).sum()) * geot[1] * geot[1]
        row[i+7] = ((gwdata > 0.01).sum()) * geot[1] * geot[1]

    print row
    writer.writerow(row)

ofile.close()



