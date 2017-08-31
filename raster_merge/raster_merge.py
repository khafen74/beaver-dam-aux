import os
from osgeo import gdal

import subprocess

filea = r'F:\01_etal\Projects\Modeling\BeaverWaterStorage\wrk_Data\AnalysisRuns\BearRiverHUC8\16010101\02_rasIn\dem_vb.tif'
fileb = r'F:\01_etal\Projects\Modeling\BeaverWaterStorage\wrk_Data\AnalysisRuns\BearRiverHUC8\16010102\02_rasIn\dem_vb.tif'
filec = r'F:\01_etal\Projects\Modeling\BeaverWaterStorage\wrk_Data\AnalysisRuns\BearRiverHUC8\16010201\02_rasIn\dem_vb.tif'
output = r'F:\01_etal\Projects\Modeling\BeaverWaterStorage\wrk_Data\AnalysisRuns\BearRiverHUC8\16010101\z_crap\testmerge.tif'


class Merger():
    #dataDir = subdir and desired data file, for this purpose the folder containg model outputs, usually a variation of '03_out/depMid.tif'
    #copyDir = path containing rasters to be merged, this is a custom setup for model outputs
    #mergeDir = path to which files from copyDir will be copied and prepped for the mosaic
    #outPath = path of output mosaic raster
    def __init__(self, dataFile, copyDir = None, outPath = None):
        self.setCopyDir(copyDir)
        self.setOutPath(outPath)
        self.setDataFile(dataFile)

    def setCopyDir(self, copyDir):
        if copyDir is not None:
            if os.path.exists(copyDir):
                self.copyDir = copyDir

    def setDataFile(self, dataFile):
        self.dataFile = dataFile

    def setOutPath(self, outPath):
        if os.path.exists(outPath):
            gdal.GetDriverByName('GTiff').Delete(outPath)
            self.outPath = outPath
        else:
            if not os.path.exists(os.path.dirname(outPath)):
                os.mkdir(os.path.dirname(outPath))

            self.outPath = outPath

    def getMergePaths(self):
        self.mergeFiles = []
        for subdir, dirs, files in os.walk(self.copyDir):
            rasPath = subdir + "/" + self.dataFile
            if os.path.exists(rasPath):
                self.mergeFiles.append(rasPath)

    def run(self):
        self.getMergePaths()
        files = " ".join(self.mergeFiles)
        os.system("gdal_merge.bat -n -9999 -a_nodata -9999 -of GTiff -o " + self.outPath + " " + files)


#code to run for merging data from all HUC12s

# basePath = '03_out_100'
# #basePath = 'MODFLOW_100'
# hucName = '16010204'
# outDir = "03_out_100_merge"
# mainDir = "F:/01_etal/Projects/Modeling/BeaverWaterStorage/wrk_Data/AnalysisRuns/BearRiverHUC8"
#
# dataFile1 = basePath + '/depMid.tif'
# dataFile2 = basePath + '/depLo.tif'
# dataFile3 = basePath + '/depHi.tif'
#
# dataFile4 = basePath + '/hdch_mid_fc.tif'
# dataFile5 = basePath + '/hdch_lo_fc.tif'
# dataFile6 = basePath + '/hdch_hi_fc.tif'
#
# dataFile1 = basePath + '/pondID.tif'
#
# copyDir = mainDir + '/' + hucName + '/HUC12'
#
# outPath1 = mainDir + '/' + hucName + '/' + outDir + '/depMid_m.tif'
# outPath2 = mainDir + '/' + hucName + '/' + outDir + '/depLo_m.tif'
# outPath3 = mainDir + '/' + hucName + '/' + outDir + '/depHi_m.tif'
#
# outPath4 = mainDir + '/' + hucName + '/' + outDir + '/hdch_mid_m3.tif'
# outPath5 = mainDir + '/' + hucName + '/' + outDir + '/hdch_lo_m3.tif'
# outPath6 = mainDir + '/' + hucName + '/' + outDir + '/hdch_hi_m3.tif'
#
# outPath1 = mainDir + '/' + hucName + '/' + outDir + '/pondID.tif'
#
# # dataFile = [dataFile1, dataFile2, dataFile3]
# # outPath = [outPath1, outPath2, outPath3]
#
# #dataFile = [dataFile4, dataFile5, dataFile6]
# #outPath = [outPath4, outPath5, outPath6]
#
# #for multiple files
# dataFile = [dataFile1]
# outPath = [outPath1]
#
# for i in range(0, len(dataFile), 1):
#     tester = Merger(dataFile[i], copyDir, outPath[i])
#     tester.run()
#
# #for single file
# # tester = Merger(dataFile1, copyDir, outPath1)
# # tester.run()

##########################################################################################
############# Code to run to merge HUC12s for each HUC8 ##################################
##########################################################################################

cap = '05'
basePath = '03_out_' + cap
print basePath
# basePath = 'MODFLOW_100'
hucNames = ['16010101', '16010102', '16010201', '16010202', '16010203', '16010204']
outDir = basePath +"_merge"
mainDir = "F:/01_etal/Projects/Modeling/BeaverWaterStorage/wrk_Data/AnalysisRuns/BearRiverHUC8"

dataFile1 = basePath + '/depMid.tif'
dataFile2 = basePath + '/depLo.tif'
dataFile3 = basePath + '/depHi.tif'

dataFile4 = basePath + '/hdch_mid_fc.tif'
dataFile5 = basePath + '/hdch_lo_fc.tif'
dataFile6 = basePath + '/hdch_hi_fc.tif'

dataFile1 = basePath + '/pondID.tif'

for hucName in hucNames:
    copyDir = mainDir + '/' + hucName + '/HUC12'

    outPath1 = mainDir + '/' + hucName + '/' + outDir + '/depMid_m.tif'
    outPath2 = mainDir + '/' + hucName + '/' + outDir + '/depLo_m.tif'
    outPath3 = mainDir + '/' + hucName + '/' + outDir + '/depHi_m.tif'

    outPath4 = mainDir + '/' + hucName + '/' + outDir + '/hdch_mid_m3.tif'
    outPath5 = mainDir + '/' + hucName + '/' + outDir + '/hdch_lo_m3.tif'
    outPath6 = mainDir + '/' + hucName + '/' + outDir + '/hdch_hi_m3.tif'

    outPath1 = mainDir + '/' + hucName + '/' + outDir + '/pondID.tif'

    # dataFile = [dataFile1, dataFile2, dataFile3]
    # outPath = [outPath1, outPath2, outPath3]

    # dataFile = [dataFile4, dataFile5, dataFile6]
    # outPath = [outPath4, outPath5, outPath6]

    dataFile = [dataFile1]
    outPath = [outPath1]

    for i in range(0, len(dataFile), 1):
        tester = Merger(dataFile[i], copyDir, outPath[i])
        tester.run()

##########################################################################################
############# Code to run to merge HUC8s for entire basin ################################
##########################################################################################

#old method
#basePath = '03_out_50_merge'

print 'merging huc8s for entire region'

#new method, base path already set by huc12
basePath = outDir
subDir = 'EntireBasin'
outDir = "out_" + cap
mainDir = "F:/01_etal/Projects/Modeling/BeaverWaterStorage/wrk_Data/AnalysisRuns/BearRiverHUC8"

dataFile1 = basePath + '/depMid_m.tif'
dataFile2 = basePath + '/depLo_m.tif'
dataFile3 = basePath + '/depHi_m.tif'
dataFile4 = basePath + '/hdch_mid_m3.tif'
dataFile5 = basePath + '/hdch_lo_m3.tif'
dataFile6 = basePath + '/hdch_hi_m3.tif'

dataFile1 = basePath + '/pondID.tif'

copyDir = mainDir

outPath1 = mainDir + '/' + subDir + '/' + outDir + '/depMid_m.tif'
outPath2 = mainDir + '/' + subDir + '/' + outDir + '/depLo_m.tif'
outPath3 = mainDir + '/' + subDir + '/' + outDir + '/depHi_m.tif'
outPath4 = mainDir + '/' + subDir + '/' + outDir + '/hdch_mid_m3.tif'
outPath5 = mainDir + '/' + subDir + '/' + outDir + '/hdch_lo_m3.tif'
outPath6 = mainDir + '/' + subDir + '/' + outDir + '/hdch_hi_m3.tif'

outPath1 = mainDir + '/' + subDir + '/' + outDir + '/pondID.tif'

# dataFile = [dataFile1, dataFile2, dataFile3, dataFile4, dataFile5, dataFile6]
# outPath = [outPath1, outPath2, outPath3, outPath4, outPath5, outPath6]
dataFile = [dataFile1]
outPath = [outPath1]

for i in range(0, len(dataFile), 1):
    tester = Merger(dataFile[i], copyDir, outPath[i])
    tester.run()