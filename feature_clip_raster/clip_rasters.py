import os
import ntpath
from osgeo import ogr, gdal

class Clipper():
    def __init__(self, clipShp, clipField, outDir, rastersToClip = None, vectorsToClip = None, rasterSubdir = None, vectorSubdir = None):
        self.setClippingShapefile(clipShp)
        self.setClipField(clipField)
        self.setOutputDirectory(outDir)
        self.setRastersToClip(rastersToClip)
        self.setVectorsToClip(vectorsToClip)
        self.rasSubdir = rasterSubdir
        self.setRasSubdir(rasterSubdir)
        self.setVecSubdir(vectorSubdir)
        self.driverSHP = ogr.GetDriverByName("ESRI Shapefile")
        self.driverTFF = gdal.GetDriverByName("GTiff")

    def clearRasters(self):
        self.rasters = []

    def clearVectors(self):
        self.vectors = []

    def clipRastersByFeatures(self):
        ds = self.driverSHP.Open(self.clipShp)
        if ds is None:
            print 'clipping layer did not open successfully'

        lyr = ds.GetLayer()

        for feature in lyr:
            nameVal = feature.GetField(self.clipField)
            if self.bRasSubdir:
                basePath = str(nameVal)+"/"+str(self.rasSubdir)
            else:
                basePath = str(nameVal)
            for raster in self.rasters:
                fn = ntpath.basename(raster)
                outPath = str(basePath) + "/" + str(fn)
                if os.path.exists(outPath):
                    self.driverTFF.Delete(outPath)
                clipPath = str(nameVal) + "/clip.shp"
                self.clipRasterPolygon(raster, clipPath, outPath)

    def clipRastersByFile(self):
        print 'clip raster by file is not yet implemented'

    def clipRasterPolygon(self, rasterPath, polyPath, outPath):
        os.system("gdalwarp -dstnodata -9999 -q -cutline " + polyPath + " -crop_to_cutline " + " -of GTiff " + rasterPath + " " + outPath)

    def clipVectorByFeatures(self):
        ds = self.driverSHP.Open(self.clipShp)
        if ds is None:
            print 'clipping layer did not open successfully'

        lyr = ds.GetLayer()

        for feature in lyr:
            nameVal = feature.GetField(self.clipField)
            if self.bVecSubdir:
                basePath = str(nameVal)+"/"+str(self.vecSubdir)
            else:
                basePath = str(nameVal)
            for vector in self.vectors:
                fn = ntpath.basename(vector)
                outPath = str(basePath) + "/" + str(fn)
                if os.path.exists(outPath):
                    self.driverSHP.DeleteDataSource(outPath)
                clipPath = str(nameVal) + "/clip.shp"
                self.clipVectorPolygon(vector, clipPath, outPath)

    def clipVectorByFile(self):
        print 'clip vector by file is not yet implemented'

    def clipVectorPolygon(self, inPath, clipPath, outPath):
        #Clipping vector and input vector must have the same coordinate system
        os.system("ogr2ogr -clipsrc " + clipPath + " " + outPath + " " + inPath)

    def createClippingFeatures(self):
        ds = self.driverSHP.Open(self.clipShp)
        if ds is None:
            print 'Clipping layer not open'
        lyr = ds.GetLayer()
        spatialRef = lyr.GetSpatialRef()

        for feature in lyr:
            nameVal = feature.GetField(self.clipField)
            if not os.path.exists(nameVal):
                os.mkdir(str(nameVal))
            if self.bRasSubdir:
                if not os.path.exists(str(nameVal)+"/"+str(self.rasSubdir)):
                    os.mkdir(str(nameVal)+"/"+str(self.rasSubdir))
            if self.bVecSubdir:
                if not os.path.exists(str(nameVal)+"/"+str(self.vecSubdir)):
                    os.mkdir(str(nameVal)+"/"+str(self.vecSubdir))
            if os.path.exists(str(nameVal) + "/clip.shp"):
                self.driverSHP.DeleteDataSource(str(nameVal) + "/clip.shp")
            outds = self.driverSHP.CreateDataSource(str(nameVal) + "/clip.shp")
            outlyr = outds.CreateLayer(str(nameVal)+"/clip.shp", srs=spatialRef, geom_type=ogr.wkbPolygon)
            outDfn = outlyr.GetLayerDefn()
            ingeom = feature.GetGeometryRef()
            outFeat = ogr.Feature(outDfn)
            outFeat.SetGeometry(ingeom)
            outlyr.CreateFeature(outFeat)

    def runClipByFeatures(self):
        self.createClippingFeatures()
        self.clipRastersByFeatures()
        self.clipVectorByFeatures()

    def runClipByFile(self):
        print 'clip by file is not yet implemented'

    def setClipField(self, field):
        self.clipField = field

    def setClippingShapefile(self, clipShp):
        self.clipShp = clipShp

    def setOutputDirectory(self, dir):
        if os.path.exists(dir):
            os.chdir(dir)
        else:
            os.mkdir(dir)
            os.chdir(dir)
            print 'output directory does not exist'

    def setRastersToClip(self, rasters):
        self.rasters = rasters

    def setRasSubdir(self, subDir):
        self.rasSubdir = subDir
        if self.rasSubdir != None:
            self.bRasSubdir = True
            print 'ras subdir = ' + self.rasSubdir
        else:
            self.bRasSubdir = False

    def setVectorsToClip(self, vectors):
        self.vectors = vectors

    def setVecSubdir(self, subDir):
        self.vecSubdir = subDir
        if self.vecSubdir != None:
            self.bVecSubdir = True
            print 'vec subdir = ' + self.vecSubdir
        else:
            self.bVecSubdir = False

#Run Here
raster1 = r'F:\01_etal\Projects\Modeling\BeaverWaterStorage\wrk_Data\AnalysisRuns\BearRiverHUC8\16010204\02_rasIn\dem_vb.tif'
raster2 = r'F:\01_etal\Projects\Modeling\BeaverWaterStorage\wrk_Data\AnalysisRuns\BearRiverHUC8\16010204\02_rasIn\fil_vb.tif'
raster3 = r'F:\01_etal\Projects\Modeling\BeaverWaterStorage\wrk_Data\AnalysisRuns\BearRiverHUC8\16010204\02_rasIn\fdir_vb.tif'
raster4 = r'F:\01_etal\Projects\Modeling\BeaverWaterStorage\wrk_Data\AnalysisRuns\BearRiverHUC8\16010204\02_rasIn\fac_1km_vb.tif'
raster5 = r'G:\01_etal\GIS_Data\USA\Soil\SSURGO\Utah\BearRiver\16010204_LowerBearMalad\ksat_vb_ms.tif'
raster6 = r'G:\01_etal\GIS_Data\USA\Soil\SSURGO\Utah\BearRiver\16010204_LowerBearMalad\kv_vb_ms.tif'
raster7 = r'G:\01_etal\GIS_Data\USA\Soil\SSURGO\Utah\BearRiver\16010204_LowerBearMalad\fc_vb.tif'
raster8 = r'F:\01_etal\Projects\Modeling\BeaverWaterStorage\wrk_Data\AnalysisRuns\BearRiverHUC8\16010204\02_rasIn\fdird_vb.tif'
raster9 = r'F:\01_etal\Projects\Modeling\BeaverWaterStorage\wrk_Data\AnalysisRuns\BearRiverHUC8\16010204\02_rasIn\fac_01km_vb.tif'
#dempath = r'G:\01_etal\GIS_Data\USA\DEM\NED_10m\Utah\BearRiver\BearRiverDEM_10m.tif'
#precippath = r'G:\01_etal\GIS_Data\USA\Climate\Prism\Precip\BearRiverAve\precip_huc8.tif'
#bratpath = r'G:\01_etal\GIS_Data\USA\BRAT\Utah\BearRiver\EntireDrainage\outputs\brat_cap_20170224.shp'
rasList = [raster1, raster2, raster3, raster4, raster5, raster6, raster7, raster8, raster9]
#rasList = [raster9]
#rasList = [dempath, precippath]
vector1 = r'F:\01_etal\Projects\Modeling\BeaverWaterStorage\wrk_Data\AnalysisRuns\BearRiverHUC8\16010204\01_shpIn\brat_cap_20170224.shp'
#vector2 = r'F:\01_etal\Projects\Modeling\BeaverWaterStorage\wrk_Data\AnalysisRuns\BridgeCreek\10m\2012\01_shpIn\points_snap.shp'
vecList = [vector1]
#vecList = []
#vecList = [bratpath]
clipShp = r'G:\01_etal\GIS_Data\USA\NHD\Utah\Watersheds\BearRiverNHD\16010204\HUC12_utm12.shp'
#clipShp = r'G:\01_etal\GIS_Data\USA\NHD\Utah\Watersheds\BearRiverNHD\HUC12_utm12.shp'
outDir = r'F:\01_etal\Projects\Modeling\BeaverWaterStorage\wrk_Data\AnalysisRuns\BearRiverHUC8\16010204\HUC12'
#outDir = r'F:\01_etal\Projects\Modeling\BeaverWaterStorage\wrk_Data\HUC12_data\GIS_data'
rasSubdir = "02_rasIn"
vecSubdir = "01_shpIn"
clipField = "HUC12"

myClipper = Clipper(clipShp, clipField, outDir, rasList, vecList, rasSubdir, vecSubdir)
myClipper.runClipByFeatures()
