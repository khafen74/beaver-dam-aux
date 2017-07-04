import os
import numpy as np
from osgeo import gdal

bratCap = '05'
modelDir = "03_out_" + bratCap
modDir = "MODFLOW_" + bratCap
path = r'F:\01_etal\Projects\Modeling\BeaverWaterStorage\wrk_Data\AnalysisRuns\BearRiverHUC8\16010204\HUC12'
inDir = "02_rasIn"
os.chdir(path)

#assign name and create modlfow model object
for subdir, dirs, files in os.walk(path):
    if os.path.exists(subdir + "/" + inDir + "/dem_vb.tif"):
        os.chdir(subdir)
        demDs = gdal.Open(inDir + '/dem_vb.tif')
        fcDs = gdal.Open(inDir + "/fc_vb.tif")
        demData = demDs.GetRasterBand(1).ReadAsArray()
        fcData = fcDs.GetRasterBand(1).ReadAsArray()
        demShape = np.shape(demData)
        fcShape = np.shape(fcData)
        # print subdir + " rows: DEM " + str(demDs.RasterYSize) + " FC " + str(fcDs.RasterYSize)
        # print subdir + " cols: DEM " + str(demDs.RasterXSize) + " FC " + str(demDs.RasterXSize)
        if (demDs.RasterYSize != fcDs.RasterYSize):
            print subdir + " ERROR! different number of rows: DEM " + str(demData.shape[0]) + " FC " + str(fcData.shape[0])
            print "rows: DEM " + str(demDs.RasterYSize) + " FC " + str(fcDs.RasterYSize)
            # if fcDs.RasterYSize < demDs.RasterYSize:
            #     addrow = np.empty([1,demDs.RasterXSize])
            #     addrow.fill(-9999.)
            #     print np.shape(addrow)[1]
            #     fcData = np.vstack([fcData, addrow])
            #     print np.shape(fcData)
            #     outDs = gdal.GetDriverByName('GTiff').Create(inDir + "/fc_vb_fix.tif", demDs.RasterXSize,
            #                                                     demDs.RasterYSize, 1, gdal.GDT_Float32)
            #     outDs.GetRasterBand(1).SetNoDataValue(-9999.)
            #     outDs.SetProjection(demDs.GetProjection())
            #     geot = demDs.GetGeoTransform()
            #     outDs.SetGeoTransform(demDs.GetGeoTransform())
            #     outDs.GetRasterBand(1).WriteArray(fcData)
            #     outDs.GetRasterBand(1).FlushCache()
            #     print fcDs.RasterYSize

        if (demDs.RasterXSize != fcDs.RasterXSize):
            print subdir + " ERROR! different number of cols: DEM " + str(demData.shape[1]) + " FC " + str(fcData.shape[1])
            print fcData

        del demData
        del fcData
        demDs = None
        fcDs = None
        outDs = None

        #print os.path.relpath(r'F:\01_etal\Projects\Modeling\BeaverWaterStorage\wrk_Data\AnalysisRuns\BearRiverHUC8\16010101\HUC12\160101010104', r'F:\01_etal\Projects\Modeling\BeaverWaterStorage\wrk_Data\AnalysisRuns\BearRiverHUC8\16010101\HUC12')