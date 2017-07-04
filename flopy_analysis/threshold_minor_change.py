import os
import numpy as np
from osgeo import gdal
import csv

bratCapList = ["05", "25", "50","100"]
huc8List = ["16010101", "16010102", "16010201", "16010202", "16010203", "16010204"]
rasList = ["depLo.tif", "depMid.tif", "depHi.tif", "hdch_lo.tif", "hdch_mid.tif", "hdch_hi.tif"]
inDir = "02_rasIn"

for huc8 in huc8List:
    path = r'F:/01_etal/Projects/Modeling/BeaverWaterStorage/wrk_Data/AnalysisRuns/BearRiverHUC8/' + huc8 + '/HUC12'
    outfile = r'F:/01_etal/Projects/Modeling/BeaverWaterStorage/wrk_Data/AnalysisRuns/BearRiverHUC8/' + huc8 + '/' + huc8 + '_results_thresh.csv'
    ofile = open(outfile, 'wb')
    writer = csv.writer(ofile)
    row = ["huc12", "brat_cap", "surface_lo", "surface_mid", "surface_hi", "gw_lo", "gw_mid", "gw_hi"]
    writer.writerow(row)

    for subdir, dirs, files in os.walk(path):
        if os.path.exists(subdir + "/" + inDir + "/dem_vb.tif"):
            os.chdir(subdir)
            fcDs = gdal.Open(inDir + "/fc_vb.tif")
            fcData = fcDs.GetRasterBand(1).ReadAsArray()

            for bratCap in bratCapList:
                modelDir = "03_out_" + bratCap
                modDir = "MODFLOW_" + bratCap

                sloDs = gdal.Open(modelDir + "/" + rasList[0])
                sloData = sloDs.GetRasterBand(1).ReadAsArray()
                smidDs = gdal.Open(modelDir + "/" + rasList[1])
                smidData = smidDs.GetRasterBand(1).ReadAsArray()
                shiDs = gdal.Open(modelDir + "/" + rasList[2])
                shiData = shiDs.GetRasterBand(1).ReadAsArray()

                gloDs = gdal.Open(modDir + "/" + rasList[3])
                gloData = gloDs.GetRasterBand(1).ReadAsArray()
                gmidDs = gdal.Open(modDir + "/" + rasList[4])
                gmidData = gmidDs.GetRasterBand(1).ReadAsArray()
                ghiDs = gdal.Open(modDir + "/" + rasList[5])
                ghiData = ghiDs.GetRasterBand(1).ReadAsArray()

    ofile.close()