import flopy
import os
import numpy as np
from osgeo import gdal
import flopy.utils.binaryfile as bf

dirPath = "E:/konrad/Projects/Modeling/BeaverWaterStorage/wrk_Data/CurtisCreekGW/MODFLOW"
dirIn = "inputs"
dirOut = "outputs"
os.chdir(dirPath)

modelname1 = 'base'
modelname2 = 'beaver'

# mf1 = flopy.modflow.Modflow(modelname1, exe_name='C:/WRDAPP/MF2005.1_11/bin/mf2005')
# mf2 = flopy.modflow.Modflow(modelname2, exe_name='C:/WRDAPP/MF2005.1_11/bin/mf2005')

mf1 = flopy.modflow.Modflow(modelname1, exe_name='C:/WRDAPP/MODFLOW-NWT_1.1.3/bin/MODFLOW-NWT_64',
                            version='mfnwt')
mf2 = flopy.modflow.Modflow(modelname2, exe_name='C:/WRDAPP/MODFLOW-NWT_1.1.3/bin/MODFLOW-NWT_64',
                            version='mfnwt')

nwt1 = flopy.modflow.ModflowNwt(mf1)
nwt2 = flopy.modflow.ModflowNwt(mf2)

demPath1 = dirIn + '/dem_vb.tif'
demPath2 = dirIn + '/wse_surf.tif'
demDs1 = gdal.Open(demPath1)
demData1 = demDs1.GetRasterBand(1).ReadAsArray()
demDs2 = gdal.Open(demPath2)
demData2 = demDs2.GetRasterBand(1).ReadAsArray()

geot = demDs1.GetGeoTransform()

pondPath = dirIn + '/dep_mid.tif'
pondDs = gdal.Open(pondPath)
pondData = pondDs.GetRasterBand(1).ReadAsArray()

headPath1 = dirIn + '/head_start.tif'
headPath2 = dirIn + '/head_mid.tif'
headDs1 = gdal.Open(headPath1)
headData1 = headDs1.GetRasterBand(1).ReadAsArray()
headDs2 = gdal.Open(headPath2)
headData2 = headDs2.GetRasterBand(1).ReadAsArray()

if os.path.exists(dirIn + '/ibound_base.tif'):
    gdal.GetDriverByName('GTiff').Delete(dirIn + '/ibound_base.tif')
out_ds1 = gdal.GetDriverByName('GTiff').Create(dirIn + '/ibound_base.tif', demDs1.RasterXSize, demDs1.RasterYSize, 1,
                                               gdal.GDT_Int32)
out_ds1.SetProjection(demDs1.GetProjection())
out_ds1.SetGeoTransform(geot)
if os.path.exists(dirIn + '/ibound_beaver.tif'):
    gdal.GetDriverByName('GTiff').Delete(dirIn + '/ibound_beaver.tif')
out_ds2 = gdal.GetDriverByName('GTiff').Create(dirIn + '/ibound_beaver.tif', demDs1.RasterXSize, demDs1.RasterYSize, 1,
                                               gdal.GDT_Int32)
out_ds2.SetProjection(demDs1.GetProjection())
out_ds2.SetGeoTransform(geot)

if os.path.exists(dirIn + '/shead_base.tif'):
    gdal.GetDriverByName('GTiff').Delete(dirIn + '/shead_base.tif')
outs_ds1 = gdal.GetDriverByName('GTiff').Create(dirIn + '/shead_base.tif', demDs1.RasterXSize, demDs1.RasterYSize, 1,
                                                gdal.GDT_Float32)
outs_ds1.SetProjection(demDs1.GetProjection())
outs_ds1.SetGeoTransform(geot)
if os.path.exists(dirIn + '/shead_beaver.tif'):
    gdal.GetDriverByName('GTiff').Delete(dirIn + '/shead_beaver.tif')
outs_ds2 = gdal.GetDriverByName('GTiff').Create(dirIn + '/shead_beaver.tif', demDs1.RasterXSize, demDs1.RasterYSize, 1,
                                                gdal.GDT_Float32)
outs_ds2.SetProjection(demDs1.GetProjection())
outs_ds2.SetGeoTransform(geot)

if os.path.exists(dirOut + '/ehead_base.tif'):
    gdal.GetDriverByName('GTiff').Delete(dirOut + '/ehead_base.tif')
outh_ds1 = gdal.GetDriverByName('GTiff').Create(dirOut + '/ehead_base.tif', demDs1.RasterXSize, demDs1.RasterYSize, 1,
                                                gdal.GDT_Float32)
outh_ds1.SetProjection(demDs1.GetProjection())
outh_ds1.SetGeoTransform(geot)
if os.path.exists(dirOut + '/ehead_beaver.tif'):
    gdal.GetDriverByName('GTiff').Delete(dirOut + '/ehead_beaver.tif')
outh_ds2 = gdal.GetDriverByName('GTiff').Create(dirOut + '/ehead_beaver.tif', demDs1.RasterXSize, demDs1.RasterYSize, 1,
                                                gdal.GDT_Float32)
outh_ds2.SetProjection(demDs1.GetProjection())
outh_ds2.SetGeoTransform(geot)

stats = demDs1.GetRasterBand(1).GetStatistics(0,1)
print 'min ' + str(stats[0])

ztop1 = demData1
ztop2 = demData2
zbot = demData1 - 10.0
nlay = 1
nrow = demDs1.RasterYSize
ncol = demDs1.RasterXSize
delr = geot[1]
delc = abs(geot[5])

if os.path.exists(dirIn + '/botm.tif'):
    gdal.GetDriverByName('GTiff').Delete(dirIn + '/botm.tif')
botmDs = gdal.GetDriverByName('GTiff').Create(dirIn + '/botm.tif', demDs1.RasterXSize, demDs1.RasterYSize, 1, gdal.GDT_Float32)
botmDs.SetProjection(demDs1.GetProjection())
botmDs.SetGeoTransform(geot)
botmDs.GetRasterBand(1).WriteArray(zbot)
botmDs.GetRasterBand(1).FlushCache()
botmDs = None
print "domain and grid definition done"

dis1 = flopy.modflow.ModflowDis(mf1, nlay, nrow, ncol, delr=delr, delc=delc,top=ztop1,botm=zbot,itmuni=4, lenuni=2)
dis2 = flopy.modflow.ModflowDis(mf2, nlay, nrow, ncol, delr=delr, delc=delc,top=ztop2,botm=zbot,itmuni=4, lenuni=2)

#variables for the BAS package
ibound1 = np.zeros(demData1.shape, dtype=np.int32)
ibound1[demData1 > zbot] = 1
ibound1[headData1 > 0.0] = -1
ibound1[demData1 < 0.0] = 0
out_ds1.GetRasterBand(1).WriteArray(ibound1)

ibound2 = np.zeros(demData2.shape, dtype=np.int32)
ibound2[demData2 > zbot] = 1
ibound2[headData2 > 0.0] = -1
ibound2[demData2 < 0.0] = 0
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

bas1 = flopy.modflow.ModflowBas(mf1, ibound=ibound1, strt=strt1)
bas2 = flopy.modflow.ModflowBas(mf2, ibound=ibound2, strt=strt2)

#ksat in meters per day

#for field measured ksat values
ksatDs = gdal.Open(dirIn + '/ksat_mms.tif')
ksatData = ksatDs.GetRasterBand(1).ReadAsArray()
# ksatData[demData1<0.0] = 0.0

#for SSURGO ksat values
# ksatData[ksatData<0.0]=2.4
# ksatData = ksatData*0.000001*60*60*24
# ksatData[demData1<0.0] = np.nan
#
# print np.nanmean(ksatData)
# ksatData[ksatData==np.nan]=0.0

#for SSURGO mean ksat
# ksatData[ksatData<0.0]=2.4
# ksatData = ksatData*0.000001*60*60*24
# ksatData[ksatData<0.0] = np.nan
# ksatData = np.nanmean(ksatData)

#Test ksat data
ksatData = 1.0

# lpf1 = flopy.modflow.ModflowLpf(mf1, hk=ksatData, vka=ksatData)
# lpf2 = flopy.modflow.ModflowLpf(mf2, hk=ksatData, vka=ksatData)

upw1 = flopy.modflow.ModflowUpw(mf1, hk=ksatData, vka=ksatData)
upw2 = flopy.modflow.ModflowUpw(mf2, hk=ksatData, vka=ksatData)

oc1 = flopy.modflow.ModflowOc(mf1)
oc2 = flopy.modflow.ModflowOc(mf2)

pcg1 = flopy.modflow.ModflowPcg(mf1)
pcg2 = flopy.modflow.ModflowPcg(mf2)

print "writing inputs"
mf1.write_input()
print "model 1 inputs written"
mf2.write_input()
print "model 2 inputs written"

success1, buff1 = mf1.run_model()
print "model 1 done " + str(success1)
success2, buff2 = mf2.run_model()
print "model 2 done " + str(success2)

print 'opening binary file'
if os.path.getsize(modelname1+'.hds') > 500:
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
if os.path.getsize(modelname2+'.hds') > 500:
    hds2 = bf.HeadFile(modelname2+'.hds')
    head2 = hds2.get_data(totim=1.0)
    head2[head2 < 0.0] = -9999.0
    outh_ds2.GetRasterBand(1).WriteArray(head2[0,:,:])
    outh_ds2.GetRasterBand(1).SetNoDataValue(-9999.0)
    head2[head2==np.min(head2)] = np.nan
    success2 = True
    print 'head 2 done'

pondData[pondData==np.min(pondData)] = 0.0
pondData[pondData < 0.0] = 0.0

if success1 and success2:
    hdDif1 = head2[0, :, :] - head1[0, :, :]
    new1 = hdDif1 - pondData
    hdch_ds1 = gdal.GetDriverByName('GTiff').Create(dirOut + '/hdch_test2.tif', demDs1.RasterXSize, demDs1.RasterYSize, 1,
                                                    gdal.GDT_Float32)
    hdch_ds1.SetProjection(demDs1.GetProjection())
    hdch_ds1.SetGeoTransform(geot)
    write = np.where(np.isnan(new1), -9999.0, new1)
    hdch_ds1.GetRasterBand(1).WriteArray(write)
    hdch_ds1.GetRasterBand(1).FlushCache()
    hdch_ds1.GetRasterBand(1).SetNoDataValue(-9999.0)
    write[write < -5.0] = np.nan
    # write[write > 1.0] = np.nan
    del write
    hdch_ds1 = None
