#For calculating volumes from existing layers

import flopy
import os
import numpy as np
from osgeo import gdal
import flopy.utils.binaryfile as bf
import csv
import glob

#Start by running for 05, 25, 50, 100
bratCap = '25'
modelDir = "03_out_" + bratCap
modDir = "MODFLOW_" + bratCap
huc8 = str(16010201)
path = r'F:\01_etal\Projects\Modeling\BeaverWaterStorage\wrk_Data\AnalysisRuns\BearRiverHUC8/'+ huc8 + '/HUC12'
outfile = r'F:\01_etal\Projects\Modeling\BeaverWaterStorage\wrk_Data\AnalysisRuns\BearRiverHUC8/'+ huc8 + '/OverallResults' + '/' + modDir + '.csv'
inDir = "02_rasIn"
os.chdir(path)
ofile = open(outfile, 'wb')
writer = csv.writer(ofile)
row = ["huc12", "brat_cap","surface_lo", "surface_mid", "surface_hi", "gw_lo", "gw_mid", "gw_hi", "fix_lo", "fix_mid", "fix_hi"]
writer.writerow(row)

#assign name and create modlfow model object
for subdir, dirs, files in os.walk(path):
    if os.path.exists(subdir + "/" + inDir + "/dem_vb.tif"):  # and float(os.path.relpath(subdir,path)) < 160102040505:
        print subdir + " running " + os.path.relpath(subdir, path)
        os.chdir(subdir)
        if not os.path.exists(modDir):
            os.mkdir(modDir)