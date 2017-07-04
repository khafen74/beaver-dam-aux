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

    def getMergePaths(self):
        self.mergeFiles = []
        for subdir, dirs, files in os.walk(self.copyDir):
            rasPath = subdir + "/" + self.dataFile
            if os.path.exists(rasPath):
                self.mergeFiles.append(rasPath)

    def run(self):
        self.getMergePaths()
        files = " ".join(self.mergeFiles)
        os.system("gdal_merge.bat -n -9999 -a_nodata -9999 -of GTiff -o " + outPath + " " + files)


#code to run
dataFile = 'MODFLOW_100/hdch_mid.tif'
copyDir = r'F:\01_etal\Projects\Modeling\BeaverWaterStorage\wrk_Data\AnalysisRuns\BearRiverHUC8\16010102\HUC12'
outPath = r'F:\01_etal\Projects\Modeling\BeaverWaterStorage\wrk_Data\AnalysisRuns\BearRiverHUC8\16010102\03_out_100_merge\headChange_m.tif'
tester = Merger(dataFile, copyDir, outPath)
tester.run()