import os
from osgeo import ogr, gdal

def ClipRasterPolygon(rasterPath, polyPath, outPath):
    #print "starting clip"
    os.system("gdalwarp -dstnodata -9999 -q -cutline " + polyPath + " -crop_to_cutline " + " -of GTiff " + rasterPath + " " + outPath)

def CreateClippingPolygons(inPath, field):
    driverSHP = ogr.GetDriverByName("ESRI Shapefile")
    ds = driverSHP.Open(inPath)
    if ds is None:
        print 'layer not open'
    lyr = ds.GetLayer()
    spatialRef = lyr.GetSpatialRef()

    for feature in lyr:
        fieldVal = feature.GetField(field)
        os.mkdir("05_MODFLOW/"+str(fieldVal))
        outds = driverSHP.CreateDataSource("05_MODFLOW/"+str(fieldVal)+"/clip.shp")
        outlyr = outds.CreateLayer(str(fieldVal)+"/clip.shp", srs=spatialRef, geom_type=ogr.wkbPolygon)
        outDfn = outlyr.GetLayerDefn()
        ingeom = feature.GetGeometryRef()
        outFeat = ogr.Feature(outDfn)
        outFeat.SetGeometry(ingeom)
        outlyr.CreateFeature(outFeat)
        print "created folder and clipping file for "+str(fieldVal)

def ClipRasters(inPath, field):
    modFolder = "05_MODFLOW/"
    driverSHP = ogr.GetDriverByName("ESRI Shapefile")
    ds = driverSHP.Open(inPath)
    demds = gdal.Open("02_rasIn/dem_vb.tif", gdal.GA_ReadOnly)
    geot = demds.GetGeoTransform()

    if ds is None:
        print 'layer not open'
    lyr = ds.GetLayer()

    print "starting clip loop"
    for feature in lyr:
        fieldVal = feature.GetField(field)
        print fieldVal
        ClipRasterPolygon("02_rasIn/dem_vb.tif", modFolder+str(fieldVal)+"/clip.shp", modFolder+str(fieldVal)+"/dem.tif")
        print "dem done"
        ClipRasterPolygon("03_out/WSESurf_lo.tif", modFolder+str(fieldVal)+"/clip.shp", modFolder+str(fieldVal)+"/WSESurf_lo.tif")
        ClipRasterPolygon("03_out/WSESurf_mid.tif", modFolder+str(fieldVal)+"/clip.shp", modFolder+str(fieldVal)+"/WSESurf_mid.tif")
        ClipRasterPolygon("03_out/WSESurf_hi.tif", modFolder+str(fieldVal)+"/clip.shp", modFolder+str(fieldVal)+"/WSESurf_hi.tif")
        print "wse done"
        ClipRasterPolygon("03_out/depLo.tif", modFolder+str(fieldVal)+"/clip.shp", modFolder+str(fieldVal)+"/depLo.tif")
        ClipRasterPolygon("03_out/depMid.tif", modFolder+str(fieldVal)+"/clip.shp", modFolder+str(fieldVal)+"/depMid.tif")
        ClipRasterPolygon("03_out/depHi.tif", modFolder+str(fieldVal)+"/clip.shp", modFolder+str(fieldVal)+"/depHi.tif")
        print "dep done"
        ClipRasterPolygon("03_out/head_start.tif", modFolder+str(fieldVal)+"/clip.shp", modFolder+str(fieldVal)+"/head_start.tif")
        ClipRasterPolygon("03_out/head_lo.tif", modFolder+str(fieldVal)+"/clip.shp", modFolder+str(fieldVal)+"/head_lo.tif")
        ClipRasterPolygon("03_out/head_mid.tif", modFolder+str(fieldVal)+"/clip.shp", modFolder+str(fieldVal)+"/head_mid.tif")
        ClipRasterPolygon("03_out/head_hi.tif", modFolder+str(fieldVal)+"/clip.shp", modFolder+str(fieldVal)+"/head_hi.tif")
        print "clipping done for "+str(fieldVal)

path = r"F:\01_etal\Projects\Modeling\BeaverWaterStorage\wrk_Data\ValidationRuns\Logan25"
huc12path = r"F:\01_etal\GIS_Data\USA\NHD\USA\Utah\Watersheds\LoganRiver_HUC8.shp"
fieldName = "HUC_12"
print "paths set"
os.chdir(path)
print "dir changed starting file creation"
CreateClippingPolygons(huc12path, fieldName)
print "files created starting clipping"
ClipRasters(huc12path,fieldName)
print "done"