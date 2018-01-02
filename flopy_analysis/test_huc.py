# import flopy
# import numpy as np
# import os
#
# modelname = 'test'
# mf = flopy.modflow.Modflow(modelname, exe_name='C:/WRDAPP/MODFLOW-NWT_1.1.2/bin/MODFLOW-NWT_64',
#                              version='mfnwt')
#
# #nwt = flopy.modflow.ModflowNwt(mf)
#
# Lx = 1000.
# Ly = 1000.
# ztop = 0.
# zbot = -50.
# nlay = 1
# nrow = 10
# ncol = 10
# delr = Lx/ncol
# delc = Ly/nrow
# delv = (ztop - zbot) / nlay
# botm = np.linspace(ztop, zbot, nlay + 1)
#
# # Create the discretization object
# dis = flopy.modflow.ModflowDis(mf, nlay, nrow, ncol, delr=delr, delc=delc,
#                                top=ztop, botm=botm[1:])
#
# # Variables for the BAS package
# ibound = np.ones((nlay, nrow, ncol), dtype=np.int32)
# ibound[:, :, 0] = -1
# ibound[:, :, -1] = -1
# strt = np.ones((nlay, nrow, ncol), dtype=np.float32)
# strt[:, :, 0] = 10.
# strt[:, :, -1] = 0.
# bas = flopy.modflow.ModflowBas(mf, ibound=ibound, strt=strt)
#
# # Add LPF package to the MODFLOW model
# lpf = flopy.modflow.ModflowLpf(mf, hk=10., vka=10.)
#
# # Add OC package to the MODFLOW model
# oc = flopy.modflow.ModflowOc(mf)
#
# # Add PCG package to the MODFLOW model
# pcg = flopy.modflow.ModflowPcg(mf)
#
# # Write the MODFLOW model input files
# mf.write_input()
#
# # Run the MODFLOW model
# success, buff = mf.run_model()
#
# import matplotlib.pyplot as plt
# import flopy.utils.binaryfile as bf
# plt.subplot(1,1,1,aspect='equal')
# hds = bf.HeadFile(modelname+'.hds')
# head = hds.get_data(totim=1.0)
# levels = np.arange(1,10,1)
# extent = (delr/2., Lx - delr/2., Ly - delc/2., delc/2.)
# plt.contour(head[0, :, :], levels=levels, extent=extent)
# plt.show()

import flopy
import os
import numpy as np
from osgeo import gdal
import flopy.utils.binaryfile as bf
import csv

bratCap = '10'
modelDir = "03_out_" + bratCap
modDir = "MODFLOW_" + bratCap
huc8 = str(16010101)
huc12 = str(160101010101)
path = r'E:\konrad\Projects\Modeling\BeaverWaterStorage\wrk_Data\AnalysisRuns\BearRiverHUC8/'+ huc8 + '/HUC12/' + huc12
inDir = "02_rasIn"
os.chdir(path)

if not os.path.exists(modDir):
    os.mkdir(modDir)

modelname1 = 'start'
modelname2 = 'lo'

# mf1 = flopy.modflow.Modflow(modelname1, exe_name='C:/WRDAPP/MF2005.1_11/bin/mf2005')
# mf2 = flopy.modflow.Modflow(modelname2, exe_name='C:/WRDAPP/MF2005.1_11/bin/mf2005')

mf1 = flopy.modflow.Modflow(modelname1, exe_name='C:/WRDAPP/MODFLOW-NWT_1.1.3/bin/MODFLOW-NWT_64',
                            version='mfnwt')
mf2 = flopy.modflow.Modflow(modelname2, exe_name='C:/WRDAPP/MODFLOW-NWT_1.1.3/bin/MODFLOW-NWT_64',
                            version='mfnwt')
headtol = 0.0001 #default 0.0001
maxiterout = 200 #default 100
Continue = True #default False
maxbackiter = 100 #default 50
maxitinner = 50 #default 50
#, headtol=headtol, maxiterout=maxiterout, Continue=Continue, maxbackiter=maxbackiter, maxitinner=maxitinner
nwt1 = flopy.modflow.ModflowNwt(mf1, headtol=headtol, maxiterout=maxiterout, Continue=Continue, maxbackiter=maxbackiter, maxitinner=maxitinner)
nwt2 = flopy.modflow.ModflowNwt(mf2, headtol=headtol, maxiterout=maxiterout, Continue=Continue, maxbackiter=maxbackiter, maxitinner=maxitinner)

demPath1 = inDir + '/dem_vbfac.tif'
demPath2 = modelDir + '/WSESurf_lo.tif'

pondPath1 = modelDir + '/depLo.tif'
pondDs1 = gdal.Open(pondPath1)
pondData1 = pondDs1.GetRasterBand(1).ReadAsArray()

headPath1 = modelDir + '/head_start.tif'
headPath2 = modelDir + '/head_lo.tif'

headDs1 = gdal.Open(headPath1)
headDs2 = gdal.Open(headPath2)
demDs1 = gdal.Open(demPath1)
demDs2 = gdal.Open(demPath2)

geot = demDs1.GetGeoTransform()
headData1 = headDs1.GetRasterBand(1).ReadAsArray()
headData2 = headDs2.GetRasterBand(1).ReadAsArray()
demData1 = demDs1.GetRasterBand(1).ReadAsArray()
demData2 = demDs2.GetRasterBand(1).ReadAsArray()

demNd = demDs1.GetRasterBand(1).GetNoDataValue()
headNd = headDs1.GetRasterBand(1).GetNoDataValue()

if os.path.exists(modDir + '/ibound1.tif'):
    gdal.GetDriverByName('GTiff').Delete(modDir + '/ibound1.tif')
out_ds1 = gdal.GetDriverByName('GTiff').Create(modDir + '/ibound1.tif', demDs1.RasterXSize, demDs1.RasterYSize, 1, gdal.GDT_Int32)
out_ds1.SetProjection(demDs1.GetProjection())
out_ds1.SetGeoTransform(geot)
if os.path.exists(modDir + '/ibound2.tif'):
    gdal.GetDriverByName('GTiff').Delete(modDir + '/ibound2.tif')
out_ds2 = gdal.GetDriverByName('GTiff').Create(modDir + '/ibound2.tif', demDs1.RasterXSize, demDs1.RasterYSize, 1, gdal.GDT_Int32)
out_ds2.SetProjection(demDs1.GetProjection())
out_ds2.SetGeoTransform(geot)

if os.path.exists(modDir + '/shead1.tif'):
    gdal.GetDriverByName('GTiff').Delete(modDir + '/shead1.tif')
outs_ds1 = gdal.GetDriverByName('GTiff').Create(modDir + '/shead1.tif', demDs1.RasterXSize, demDs1.RasterYSize, 1, gdal.GDT_Float32)
outs_ds1.SetProjection(demDs1.GetProjection())
outs_ds1.SetGeoTransform(geot)
if os.path.exists(modDir + '/shead2.tif'):
    gdal.GetDriverByName('GTiff').Delete(modDir + '/shead2.tif')
outs_ds2 = gdal.GetDriverByName('GTiff').Create(modDir + '/shead2.tif', demDs1.RasterXSize, demDs1.RasterYSize, 1, gdal.GDT_Float32)
outs_ds2.SetProjection(demDs1.GetProjection())
outs_ds2.SetGeoTransform(geot)

if os.path.exists(modDir + '/ehead1.tif'):
    gdal.GetDriverByName('GTiff').Delete(modDir + '/ehead1.tif')
outh_ds1 = gdal.GetDriverByName('GTiff').Create(modDir + '/ehead1.tif', demDs1.RasterXSize, demDs1.RasterYSize, 1, gdal.GDT_Float32)
outh_ds1.SetProjection(demDs1.GetProjection())
outh_ds1.SetGeoTransform(geot)
if os.path.exists(modDir + '/ehead2.tif'):
    gdal.GetDriverByName('GTiff').Delete(modDir + '/ehead2.tif')
outh_ds2 = gdal.GetDriverByName('GTiff').Create(modDir + '/ehead2.tif', demDs1.RasterXSize, demDs1.RasterYSize, 1, gdal.GDT_Float32)
outh_ds2.SetProjection(demDs1.GetProjection())
outh_ds2.SetGeoTransform(geot)

#get stats from original DEM
stats = demDs1.GetRasterBand(1).GetStatistics(0,1)
print 'min ' + str(stats[0])

#model domain and grid definition
ztop1 = demData1
ztop2 = demData2
zbot = demData1 - 10.0
nlay = 1
nrow = demDs1.RasterYSize
ncol = demDs1.RasterXSize
delr = geot[1]
delc = abs(geot[5])

if os.path.exists(modDir + '/botm.tif'):
    gdal.GetDriverByName('GTiff').Delete(modDir + '/botm.tif')
botmDs = gdal.GetDriverByName('GTiff').Create(modDir + '/botm.tif', demDs1.RasterXSize, demDs1.RasterYSize, 1, gdal.GDT_Float32)
botmDs.SetProjection(demDs1.GetProjection())
botmDs.SetGeoTransform(geot)
botmDs.GetRasterBand(1).WriteArray(zbot)
botmDs.GetRasterBand(1).FlushCache()
botmDs = None
print "domain and grid definition done"

#create discretization object
dis1 = flopy.modflow.ModflowDis(mf1, nlay, nrow, ncol, delr=delr, delc=delc,top=ztop1,botm=zbot,itmuni=1, lenuni=2)
dis2 = flopy.modflow.ModflowDis(mf2, nlay, nrow, ncol, delr=delr, delc=delc,top=ztop2,botm=zbot,itmuni=1, lenuni=2)

#variables for the BAS package
# diff = ndimage.maximum_filter(demData1, size=(3,3)) - demData1
ibound1 = np.zeros(demData1.shape, dtype=np.int32)
ibound1[demData1 > zbot] = 1
ibound1[headData1 > 0.0] = -1
ibound1[demData1 < 0.0] = 0
# ibound1[diff >= 10.0] = 0.0
out_ds1.GetRasterBand(1).WriteArray(ibound1)

# diff = ndimage.maximum_filter(demData2, size=(3, 3)) - demData2
ibound2 = np.zeros(demData2.shape, dtype=np.int32)
ibound2[demData2 > zbot] = 1
ibound2[headData2 > 0.0] = -1
ibound2[demData2 < 0.0] = 0
# ibound2[diff >= 10.0] = 0.0
out_ds2.GetRasterBand(1).WriteArray(ibound2)

headData1[headData1 < np.nanmin(demData1)] = stats[0]
strt1 = np.where(headData1 < stats[0], demData1, headData1)
outs_ds1.GetRasterBand(1).WriteArray(strt1)
outs_ds1.GetRasterBand(1).FlushCache()
outs_ds1 = None

headData2[headData2 < np.nanmin(demData2)] = stats[0]
strt2 = np.where(headData2 < stats[0], demData2, headData2)
outs_ds2.GetRasterBand(1).WriteArray(strt2)
outs_ds2.GetRasterBand(1).FlushCache()
outs_ds2 = None

bas1 = flopy.modflow.ModflowBas(mf1, ibound=ibound1)
bas2 = flopy.modflow.ModflowBas(mf2, ibound=ibound2)

ksatDs = gdal.Open(inDir + "/ksat_vbfac.tif")
kvDs = gdal.Open(inDir + "/kv_vbfac.tif")
fcDs = gdal.Open(inDir + "/fc_vbfac.tif")
porDs = gdal.Open(inDir + "/por_vbfac.tif")
ksatData = ksatDs.GetRasterBand(1).ReadAsArray()
kvData = kvDs.GetRasterBand(1).ReadAsArray()
fcData = fcDs.GetRasterBand(1).ReadAsArray()
porData = porDs.GetRasterBand(1).ReadAsArray()
kvData[kvData < 0.0] = np.nan
ksatData[ksatData < 0.0] = np.nan

#add lpf package to the modflow model
# convert from micrometers per second to meters per second
lpf1 = flopy.modflow.ModflowLpf(mf1, hk=np.nanmean(ksatData*0.000001), vka=np.nanmean(kvData*0.000001))
lpf2 = flopy.modflow.ModflowLpf(mf2, hk=np.nanmean(ksatData*0.000001), vka=np.nanmean(kvData*0.000001))

#convert from micrometers per second to meters per second
# flopy.modflow.ModflowUpw(mf1, hk=np.nanmean(ksatData)*0.000001, vka=np.nanmean(kvData)*0.000001)
# flopy.modflow.ModflowUpw(mf2, hk=np.nanmean(ksatData)*0.000001, vka=np.nanmean(kvData)*0.000001)

#add oc pacage to the modflow model
oc1 = flopy.modflow.ModflowOc(mf1)
oc2 = flopy.modflow.ModflowOc(mf2)

#add pcg package to the modflow model
pcg1 = flopy.modflow.ModflowPcg(mf1)
pcg2 = flopy.modflow.ModflowPcg(mf2)

# Write the MODFLOW model input files
mf1.write_input()
print "model 1 inputs written"
mf2.write_input()
print "model 2 inputs written"

# Run the MODFLOW model
success1, buff1 = mf1.run_model()
print "model 1 done " + str(success1)
success2, buff2 = mf2.run_model()
print "model 2 done " + str(success2)

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
    pondData1[pondData1 == np.min(pondData1)] = 0.0
    pondData1[pondData1 < 0.0] = 0.0

    if success1 and success2:
        hdDif1 = head2[0, :, :] - head1[0, :, :]
        new1 = hdDif1 - pondData1
        hdch_ds1 = gdal.GetDriverByName('GTiff').Create(modDir + '/hdch_lo.tif', demDs1.RasterXSize, demDs1.RasterYSize,
                                                        1, gdal.GDT_Float32)
        hdch_ds1.SetProjection(demDs1.GetProjection())
        hdch_ds1.SetGeoTransform(geot)
        write = np.where(np.isnan(new1), -9999.0, new1)
        hdch_ds1.GetRasterBand(1).WriteArray(write)
        hdch_ds1.GetRasterBand(1).FlushCache()
        hdch_ds1.GetRasterBand(1).SetNoDataValue(-9999.0)
        hdch_ds1 = None