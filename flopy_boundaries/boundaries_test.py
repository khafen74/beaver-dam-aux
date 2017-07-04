import flopy
import os
import numpy as np
from osgeo import gdal
import flopy.utils.binaryfile as bf

os.chdir(r'F:\01_etal\Projects\Modeling\BeaverWaterStorage\wrk_Data\ValidationRuns\TempleFork_10m')
modelname1 = 'var_zbot_base'
modelname2 = 'var_zbot_mid'
mf1 = flopy.modflow.Modflow(modelname1, exe_name='C:/WRDAPP/64/mf2k5_h5_64')
mf2 = flopy.modflow.Modflow(modelname2, exe_name='C:/WRDAPP/64/mf2k5_h5_64')

#read DEM data, get geo transform, get no data
demPath = '02_rasIn/fil10m_vb.tif'
demPath2 = '03_out/WSESurf_mid.tif'
demDs = gdal.Open(demPath)
demDs2 = gdal.Open(demPath2)
geot = demDs.GetGeoTransform()
demData = demDs.GetRasterBand(1).ReadAsArray()
demData2 = demDs2.GetRasterBand(1).ReadAsArray()
demNd = demDs.GetRasterBand(1).GetNoDataValue()

#read pond data
pondPath = '03_out/depMid.tif'
pondDs = gdal.Open(pondPath)
pondData = pondDs.GetRasterBand(1).ReadAsArray()

#read initial head data
headPath1 = '03_out/head_start.tif'
headPath2 = '03_out/head_mid.tif'
headDs1 = gdal.Open(headPath1)
headDs2 = gdal.Open(headPath2)
headData1 = headDs1.GetRasterBand(1).ReadAsArray()
headData2 = headDs2.GetRasterBand(1).ReadAsArray()
headNd = headDs1.GetRasterBand(1).GetNoDataValue()

#create the ibound rasters
out_ds1 = gdal.GetDriverByName('GTiff').Create('05_MODFLOW/ibound1.tif', demDs.RasterXSize, demDs.RasterYSize, 1, gdal.GDT_Int32)
out_ds1.SetProjection(demDs.GetProjection())
out_ds1.SetGeoTransform(geot)
out_ds2 = gdal.GetDriverByName('GTiff').Create('05_MODFLOW/ibound2.tif', demDs.RasterXSize, demDs.RasterYSize, 1, gdal.GDT_Int32)
out_ds2.SetProjection(demDs.GetProjection())
out_ds2.SetGeoTransform(geot)

#create the starting head rasters
outs_ds1 = gdal.GetDriverByName('GTiff').Create('05_MODFLOW/shead1.tif', demDs.RasterXSize, demDs.RasterYSize, 1, gdal.GDT_Float32)
outs_ds1.SetProjection(demDs.GetProjection())
outs_ds1.SetGeoTransform(geot)
outs_ds2 = gdal.GetDriverByName('GTiff').Create('05_MODFLOW/shead2.tif', demDs.RasterXSize, demDs.RasterYSize, 1, gdal.GDT_Float32)
outs_ds2.SetProjection(demDs.GetProjection())
outs_ds2.SetGeoTransform(geot)

#create the ending (modeled) head rasters
outh_ds1 = gdal.GetDriverByName('GTiff').Create('05_MODFLOW/ehead1.tif', demDs.RasterXSize, demDs.RasterYSize, 1, gdal.GDT_Float32)
outh_ds1.SetProjection(demDs.GetProjection())
outh_ds1.SetGeoTransform(geot)
outh_ds2 = gdal.GetDriverByName('GTiff').Create('05_MODFLOW/ehead2.tif', demDs.RasterXSize, demDs.RasterYSize, 1, gdal.GDT_Float32)
outh_ds2.SetProjection(demDs.GetProjection())
outh_ds2.SetGeoTransform(geot)

print "datasets created"

#get stats from original DEM
stats = demDs.GetRasterBand(1).GetStatistics(0,1)
print 'min ' + str(stats[0])

#model domain and grid definition
ztop1 = demData #set the model top equal to the DEM
ztop2 = demData2 #here the model top is equal to the DEM plus the water in the ponds
zbot = demData - 3.0
nlay = 1 #only 1 layer in this model
nrow = demDs.RasterYSize #set to same size as DEM
ncol = demDs.RasterXSize
delr = geot[1] #same cell width as DEM
delc = abs(geot[5]) #same cell height as DEM
print "domain and grid definition done"

#create discretization object
dis1 = flopy.modflow.ModflowDis(mf1, nlay, nrow, ncol, delr=delr, delc=delc,top=ztop1,botm=zbot,itmuni=1)
dis2 = flopy.modflow.ModflowDis(mf2, nlay, nrow, ncol, delr=delr, delc=delc,top=ztop2,botm=zbot,itmuni=1)

#variables for the BAS package
ibound1 = np.zeros(demData.shape, dtype=np.int32)
#set areas
ibound1[demData > zbot] = 1
ibound1[headData1 > 0.0] = -1
ibound1[demData < 0.0] = 0
out_ds1.GetRasterBand(1).WriteArray(ibound1)

ibound2 = np.zeros(demData2.shape, dtype=np.int32)
ibound2[demData2 > zbot] = 1
ibound2[headData2 > zbot] = -1
ibound2[demData2 < 0.0] = 0
out_ds2.GetRasterBand(1).WriteArray(ibound2)
print "ibound created"

headData1[headData1 < np.nanmin(demData)] = stats[0]
outs_ds1.GetRasterBand(1).WriteArray(headData1)

headData2[headData2 < np.nanmin(demData2)] = stats[0]
outs_ds2.GetRasterBand(1).WriteArray(headData2)

print "head data created"

bas1 = flopy.modflow.ModflowBas(mf1, ibound=ibound1, strt=headData1)
bas2 = flopy.modflow.ModflowBas(mf2, ibound=ibound2, strt=headData2)

lpf1 = flopy.modflow.ModflowLpf(mf1, hk=0.0152024955899, vka=0.00776183538781)
lpf2 = flopy.modflow.ModflowLpf(mf2, hk=0.0152024955899, vka=0.00776183538781)

print "lpf package set up"

oc1 = flopy.modflow.ModflowOc(mf1)
oc2 = flopy.modflow.ModflowOc(mf2)

print "oc package set up"

pcg1 = flopy.modflow.ModflowPcg(mf1)
pcg2 = flopy.modflow.ModflowPcg(mf2)

print "pcg package set up"

mf1.write_input()
print "model 1 inputs written"
mf2.write_input()
print "model 2 inputs written"

success1, buff1 = mf1.run_model()
print "model 1 done " + str(success1)
success2, buff2 = mf2.run_model()
print "model 2 done " + str(success2)

print 'opening binary file'
if os.path.getsize(modelname1+'.hds') > 5000:
    hds1 = bf.HeadFile(modelname1+'.hds')
    print 'binary file imported'
    head1 = hds1.get_data(totim=1.0)
    head1[head1 < 0.0] = -9999.0
    outh_ds1.GetRasterBand(1).WriteArray(head1[0,:,:])
    outh_ds1.GetRasterBand(1).SetNoDataValue(-9999.0)
    head1[head1==np.min(head1)] = np.nan
    success1 = True
    print np.nansum(head1)
    print 'head 1 done'
if os.path.getsize(modelname2+'.hds') > 5000:
    hds2 = bf.HeadFile(modelname2+'.hds')
    head2 = hds2.get_data(totim=1.0)
    head2[head2 < 0.0] = -9999.0
    outh_ds2.GetRasterBand(1).WriteArray(head2[0,:,:])
    outh_ds2.GetRasterBand(1).SetNoDataValue(-9999.0)
    head2[head2==np.min(head2)] = np.nan
    success2 = True
    print 'head 2 done'

print "calculating head differences"
pondData[pondData==np.min(pondData)] = 0.0
gwlo = 0.0
gwmid = 0.0
gwhi = 0.0

if success1 and success2:
    hdDif1 = head2[0,:,:] - head1[0,:,:]
    new1 = hdDif1 - pondData
    hdch_ds1 = gdal.GetDriverByName('GTiff').Create('hdch_mid.tif', demDs.RasterXSize, demDs.RasterYSize, 1, gdal.GDT_Float32)
    hdch_ds1.SetProjection(demDs.GetProjection())
    hdch_ds1.SetGeoTransform(geot)
    write = np.where(np.isnan(new1), -9999.0, new1)
    hdch_ds1.GetRasterBand(1).WriteArray(write)
    hdch_ds1.GetRasterBand(1).SetNoDataValue(-9999.0)
    gwlo = np.nansum(new1) * abs(geot[1]) * abs(geot[5]) * 0.528668