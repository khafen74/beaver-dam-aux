import flopy
import os
import numpy as np
from osgeo import gdal
import flopy.utils.binaryfile as bf
import csv
import glob
from scipy import ndimage

#Start by running for 05, 25, 50, 100
#bratCap = '100'
bratCaps = ['05', '25', '50', '100']
bratCaps = ['50']
for bratCap in bratCaps:
    modelDir = "03_out_" + bratCap
    modDir = "MODFLOW_" + bratCap
    huc8 = str(16010204)
    path = r'E:\konrad\Projects\Modeling\BeaverWaterStorage\wrk_Data\AnalysisRuns\BearRiverHUC8/'+ huc8 + '/HUC12'
    outfile = r'E:\konrad\Projects\Modeling\BeaverWaterStorage\wrk_Data\AnalysisRuns\BearRiverHUC8/'+ huc8 + '/OverallResults' + '/' + modDir + '.csv'
    inDir = "02_rasIn"
    os.chdir(path)
    ofile = open(outfile, 'wb')
    writer = csv.writer(ofile)
    row = ["huc12", "brat_cap","surface_lo", "surface_mid", "surface_hi", "gw_lo", "gw_mid", "gw_hi", "fix_lo", "fix_mid", "fix_hi"]
    # row = ["huc12", "brat_cap","surface_lo", "surface_mid", "surface_hi", "gw_lo", "gw_mid", "gw_hi",  "pgw_lo", "pgw_mid", "pgw_hi",
    #        "fix_lo", "fix_mid", "fix_hi"]
    writer.writerow(row)

    #assign name and create modlfow model object
    for subdir, dirs, files in os.walk(path):
        if os.path.exists(subdir + "/" + modelDir + "/depMid.tif") and (os.path.relpath(subdir,path)) != '160102040505':
            print subdir + " running " + os.path.relpath(subdir, path)
            os.chdir(subdir)
            if not os.path.exists(modDir):
                os.mkdir(modDir)
            os.getcwd()
            modelname1 = 'start'
            modelname2 = 'lo'
            modelname3 = 'mid'
            modelname4 = 'hi'

            # mf1 = flopy.modflow.Modflow(modelname1, exe_name='C:/WRDAPP/MF2005.1_11/bin/mf2005')
            # mf2 = flopy.modflow.Modflow(modelname2, exe_name='C:/WRDAPP/MF2005.1_11/bin/mf2005')
            # mf3 = flopy.modflow.Modflow(modelname3, exe_name='C:/WRDAPP/MF2005.1_11/bin/mf2005')
            # mf4 = flopy.modflow.Modflow(modelname4, exe_name='C:/WRDAPP/MF2005.1_11/bin/mf2005')

            # mf1 = flopy.modflow.Modflow(modelname1, exe_name='C:/WRDAPP/64/mf2k5_h5_parallel_64')
            # mf2 = flopy.modflow.Modflow(modelname2, exe_name='C:/WRDAPP/64/mf2k5_h5_parallel_64')
            # mf3 = flopy.modflow.Modflow(modelname3, exe_name='C:/WRDAPP/64/mf2k5_h5_parallel_64')
            # mf4 = flopy.modflow.Modflow(modelname4, exe_name='C:/WRDAPP/64/mf2k5_h5_parallel_64')

            mf1 = flopy.modflow.Modflow(modelname1, exe_name='C:/WRDAPP/MODFLOW-NWT_1.1.3/bin/MODFLOW-NWT_64',
                                        version='mfnwt')
            mf2 = flopy.modflow.Modflow(modelname2, exe_name='C:/WRDAPP/MODFLOW-NWT_1.1.3/bin/MODFLOW-NWT_64',
                                        version='mfnwt')
            mf3 = flopy.modflow.Modflow(modelname3, exe_name='C:/WRDAPP/MODFLOW-NWT_1.1.3/bin/MODFLOW-NWT_64',
                                        version='mfnwt')
            mf4 = flopy.modflow.Modflow(modelname4, exe_name='C:/WRDAPP/MODFLOW-NWT_1.1.3/bin/MODFLOW-NWT_64',
                                        version='mfnwt')

            # add nwt package
            # headtol = 0.0001 #default 0.0001
            # maxiterout = 200 #default 100
            # Continue = True #default False
            # maxbackiter = 100 #default 50
            # maxitinner = 50 #default 50
            #, headtol=headtol, maxiterout=maxiterout, Continue=Continue, maxbackiter=maxbackiter, maxitinner=maxitinner
            nwt1 = flopy.modflow.ModflowNwt(mf1)
            nwt2 = flopy.modflow.ModflowNwt(mf2)
            nwt3 = flopy.modflow.ModflowNwt(mf3)
            nwt4 = flopy.modflow.ModflowNwt(mf4)
            print "nwt package set up"

            demPath1 = inDir + '/dem_vbfac.tif'
            demPath2 = modelDir + '/WSESurf_lo.tif'
            demPath3 = modelDir + '/WSESurf_mid.tif'
            demPath4 = modelDir + '/WSESurf_hi.tif'

            pondPath1 = modelDir + '/depLo.tif'
            pondPath2 = modelDir + '/depMid.tif'
            pondPath3 = modelDir + '/depHi.tif'
            pondDs1 = gdal.Open(pondPath1)
            pondData1 = pondDs1.GetRasterBand(1).ReadAsArray()
            pondDs2 = gdal.Open(pondPath2)
            pondData2 = pondDs2.GetRasterBand(1).ReadAsArray()
            pondDs3 = gdal.Open(pondPath3)
            pondData3 = pondDs3.GetRasterBand(1).ReadAsArray()

            headPath1 = modelDir + '/head_start.tif'
            headPath2 = modelDir + '/head_lo.tif'
            headPath3 = modelDir + '/head_mid.tif'
            headPath4 = modelDir + '/head_hi.tif'

            headDs1 = gdal.Open(headPath1)
            headDs2 = gdal.Open(headPath2)
            headDs3 = gdal.Open(headPath3)
            headDs4 = gdal.Open(headPath4)
            demDs1 = gdal.Open(demPath1)
            demDs2 = gdal.Open(demPath2)
            demDs3 = gdal.Open(demPath3)
            demDs4 = gdal.Open(demPath4)
            geot = demDs1.GetGeoTransform()
            headData1 = headDs1.GetRasterBand(1).ReadAsArray()
            headData2 = headDs2.GetRasterBand(1).ReadAsArray()
            headData3 = headDs3.GetRasterBand(1).ReadAsArray()
            headData4 = headDs4.GetRasterBand(1).ReadAsArray()
            demData1 = demDs1.GetRasterBand(1).ReadAsArray()
            demData2 = demDs2.GetRasterBand(1).ReadAsArray()
            demData3 = demDs3.GetRasterBand(1).ReadAsArray()
            demData4 = demDs4.GetRasterBand(1).ReadAsArray()
            demNd = demDs1.GetRasterBand(1).GetNoDataValue()
            headNd = headDs1.GetRasterBand(1).GetNoDataValue()
            #demData1[demData == -9999.0]=np.nan

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
            if os.path.exists(modDir + '/ibound3.tif'):
                gdal.GetDriverByName('GTiff').Delete(modDir + '/ibound3.tif')
            out_ds3 = gdal.GetDriverByName('GTiff').Create(modDir + '/ibound3.tif', demDs1.RasterXSize, demDs1.RasterYSize, 1, gdal.GDT_Int32)
            out_ds3.SetProjection(demDs1.GetProjection())
            out_ds3.SetGeoTransform(geot)
            if os.path.exists(modDir + '/ibound4.tif'):
                gdal.GetDriverByName('GTiff').Delete(modDir + '/ibound4.tif')
            out_ds4 = gdal.GetDriverByName('GTiff').Create(modDir + '/ibound4.tif', demDs1.RasterXSize, demDs1.RasterYSize, 1, gdal.GDT_Int32)
            out_ds4.SetProjection(demDs1.GetProjection())
            out_ds4.SetGeoTransform(geot)

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
            if os.path.exists(modDir + '/shead3.tif'):
                gdal.GetDriverByName('GTiff').Delete(modDir + '/shead3.tif')
            outs_ds3 = gdal.GetDriverByName('GTiff').Create(modDir + '/shead3.tif', demDs1.RasterXSize, demDs1.RasterYSize, 1, gdal.GDT_Float32)
            outs_ds3.SetProjection(demDs1.GetProjection())
            outs_ds3.SetGeoTransform(geot)
            if os.path.exists(modDir + '/shead4.tif'):
                gdal.GetDriverByName('GTiff').Delete(modDir + '/shead4.tif')
            outs_ds4 = gdal.GetDriverByName('GTiff').Create(modDir + '/shead4.tif', demDs1.RasterXSize, demDs1.RasterYSize, 1, gdal.GDT_Float32)
            outs_ds4.SetProjection(demDs1.GetProjection())
            outs_ds4.SetGeoTransform(geot)

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
            if os.path.exists(modDir + '/ehead3.tif'):
                gdal.GetDriverByName('GTiff').Delete(modDir + '/ehead3.tif')
            outh_ds3 = gdal.GetDriverByName('GTiff').Create(modDir + '/ehead3.tif', demDs1.RasterXSize, demDs1.RasterYSize, 1, gdal.GDT_Float32)
            outh_ds3.SetProjection(demDs1.GetProjection())
            outh_ds3.SetGeoTransform(geot)
            if os.path.exists(modDir + '/ehead4.tif'):
                gdal.GetDriverByName('GTiff').Delete(modDir + '/ehead4.tif')
            outh_ds4 = gdal.GetDriverByName('GTiff').Create(modDir + '/ehead4.tif', demDs1.RasterXSize, demDs1.RasterYSize, 1, gdal.GDT_Float32)
            outh_ds4.SetProjection(demDs1.GetProjection())
            outh_ds4.SetGeoTransform(geot)

            print "datasets created"

            #get stats from original DEM
            stats = demDs1.GetRasterBand(1).GetStatistics(0,1)
            print 'min ' + str(stats[0])

            #model domain and grid definition
            ztop1 = demData1
            ztop2 = demData2
            ztop3 = demData3
            ztop4 = demData4
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
            dis3 = flopy.modflow.ModflowDis(mf3, nlay, nrow, ncol, delr=delr, delc=delc,top=ztop3,botm=zbot,itmuni=1, lenuni=2)
            dis4 = flopy.modflow.ModflowDis(mf4, nlay, nrow, ncol, delr=delr, delc=delc,top=ztop4,botm=zbot,itmuni=1, lenuni=2)
            print "discretization object created"

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

            # diff = ndimage.maximum_filter(demData3, size=(3, 3)) - demData3
            ibound3 = np.zeros(demData3.shape, dtype=np.int32)
            ibound3[demData3 > zbot] = 1
            ibound3[headData3 > 0.0] = -1
            ibound3[demData3 < 0.0] = 0
            # ibound3[diff >= 10.0] = 0.0
            out_ds3.GetRasterBand(1).WriteArray(ibound3)

            # diff = ndimage.maximum_filter(demData4, size=(3, 3)) - demData4
            ibound4 = np.zeros(demData4.shape, dtype=np.int32)
            ibound4[demData4 > zbot] = 1
            ibound4[headData4 > 0.0] = -1
            ibound4[demData4 < 0.0] = 0
            # ibound4[diff >= 10.0] = 0.0
            out_ds4.GetRasterBand(1).WriteArray(ibound4)
            print "ibound created"

            #strt = np.ones((nrow, ncol), dtype=np.float32)
            #strt.fill(zbot + 10.0)
            #print np.where(headData > 0.0, headData, strt)
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

            headData3[headData3 < np.nanmin(demData3)] = stats[0]
            strt3 = np.where(headData3 < stats[0], demData3, headData3)
            outs_ds3.GetRasterBand(1).WriteArray(strt3)
            outs_ds3.GetRasterBand(1).FlushCache()
            outs_ds3 = None

            headData4[headData4 < np.nanmin(demData4)] = stats[0]
            strt4 = np.where(headData4 < stats[0], demData4, headData4)
            outs_ds4.GetRasterBand(1).WriteArray(strt4)
            outs_ds4.GetRasterBand(1).FlushCache()
            outs_ds4 = None
            print "head data created"

            bas1 = flopy.modflow.ModflowBas(mf1, ibound=ibound1, strt=strt1)
            bas2 = flopy.modflow.ModflowBas(mf2, ibound=ibound2, strt=strt2)
            bas3 = flopy.modflow.ModflowBas(mf3, ibound=ibound3, strt=strt3)
            bas4 = flopy.modflow.ModflowBas(mf4, ibound=ibound4, strt=strt4)
            print "bas package set up"

            #Open hydraulic conductivity and field capacity rasters and get data
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
            # lpf1 = flopy.modflow.ModflowLpf(mf1, hk=np.nanmean(ksatData*0.000001), vka=np.nanmean(kvData*0.000001))
            # lpf2 = flopy.modflow.ModflowLpf(mf2, hk=np.nanmean(ksatData*0.000001), vka=np.nanmean(kvData*0.000001))
            # lpf3 = flopy.modflow.ModflowLpf(mf3, hk=np.nanmean(ksatData*0.000001), vka=np.nanmean(kvData*0.000001))
            # lpf4 = flopy.modflow.ModflowLpf(mf4, hk=np.nanmean(ksatData*0.000001), vka=np.nanmean(kvData*0.000001))

            #convert from micrometers per second to meters per second
            upw1 = flopy.modflow.ModflowUpw(mf1, hk=np.nanmean(ksatData)*0.000001, vka=np.nanmean(kvData)*0.000001)
            upw2 = flopy.modflow.ModflowUpw(mf2, hk=np.nanmean(ksatData)*0.000001, vka=np.nanmean(kvData)*0.000001)
            upw3 = flopy.modflow.ModflowUpw(mf3, hk=np.nanmean(ksatData)*0.000001, vka=np.nanmean(kvData)*0.000001)
            upw4 = flopy.modflow.ModflowUpw(mf4, hk=np.nanmean(ksatData)*0.000001, vka=np.nanmean(kvData)*0.000001)
            print "lpf package set up"

            #add oc pacage to the modflow model
            oc1 = flopy.modflow.ModflowOc(mf1)
            oc2 = flopy.modflow.ModflowOc(mf2)
            oc3 = flopy.modflow.ModflowOc(mf3)
            oc4 = flopy.modflow.ModflowOc(mf4)
            print "oc package set up"

            #add pcg package to the modflow model
            pcg1 = flopy.modflow.ModflowPcg(mf1)
            pcg2 = flopy.modflow.ModflowPcg(mf2)
            pcg3 = flopy.modflow.ModflowPcg(mf3)
            pcg4 = flopy.modflow.ModflowPcg(mf4)
            print "pcg package set up"


            # Write the MODFLOW model input files
            mf1.write_input()
            print "model 1 inputs written"
            mf2.write_input()
            print "model 2 inputs written"
            mf3.write_input()
            print "model 3 inputs written"
            mf4.write_input()
            print "model 4 inputs written"

            print "model inputs created"

            # Run the MODFLOW model
            success1, buff1 = mf1.run_model()
            print "model 1 done " + str(success1)
            success2, buff2 = mf2.run_model()
            print "model 2 done " + str(success2)
            success3, buff3 = mf3.run_model()
            print "model 3 done " + str(success3)
            success4, buff4 = mf4.run_model()
            print "model 4 done " + str(success4)

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
            if os.path.getsize(modelname3+'.hds') > 5000:
                hds3 = bf.HeadFile(modelname3+'.hds')
                head3 = hds3.get_data(totim=1.0)
                head3[head3 < 0.0] = -9999.0
                outh_ds3.GetRasterBand(1).WriteArray(head3[0,:,:])
                outh_ds3.GetRasterBand(1).SetNoDataValue(-9999.0)
                head3[head3==np.min(head3)] = np.nan
                success3 = True
                print 'head 3 done'
            if os.path.getsize(modelname4+'.hds') > 5000:
                hds4 = bf.HeadFile(modelname4+'.hds')
                head4 = hds4.get_data(totim=1.0)
                head4[head4 < 0.0] = -9999.0
                outh_ds4.GetRasterBand(1).WriteArray(head4[0,:,:])
                outh_ds4.GetRasterBand(1).SetNoDataValue(-9999.0)
                head4[head4==np.min(head4)] = np.nan
                success4 = True
                print 'head 4 done'

            print "calculating head differences"
            pondData1[pondData1==np.min(pondData1)] = 0.0
            pondData2[pondData2==np.min(pondData2)] = 0.0
            pondData3[pondData3==np.min(pondData3)] = 0.0
            fixlo=0
            fixmid=0
            fixhi=0
            gwlo = 0.0
            gwmid = 0.0
            gwhi = 0.0
            pondData1[pondData1 < 0.0] = 0.0
            pondData2[pondData2 < 0.0] = 0.0
            pondData3[pondData3 < 0.0] = 0.0

            slo = np.nansum(pondData1) * abs(geot[1]) * abs(geot[5])
            smid = np.nansum(pondData2) * abs(geot[1]) * abs(geot[5])
            shi = np.nansum(pondData3) * abs(geot[1]) * abs(geot[5])

            fcData[fcData<0.0] = np.nan
            porData[porData < 0.0] = np.nan
            fcDataFrac = fcData / 100.0
            porDataFrac = porData / 100.0
            if success1 and success2:
                hdDif1 = head2[0,:,:] - head1[0,:,:]
                new1 = hdDif1 - pondData1
                hdch_ds1 = gdal.GetDriverByName('GTiff').Create(modDir + '/hdch_lo.tif', demDs1.RasterXSize, demDs1.RasterYSize, 1, gdal.GDT_Float32)
                hdch_ds1.SetProjection(demDs1.GetProjection())
                hdch_ds1.SetGeoTransform(geot)
                write = np.where(np.isnan(new1), -9999.0, new1)
                hdch_ds1.GetRasterBand(1).WriteArray(write)
                hdch_ds1.GetRasterBand(1).FlushCache()
                hdch_ds1.GetRasterBand(1).SetNoDataValue(-9999.0)
                write[write < -5.0] = np.nan
                #write[write > 1.0] = np.nan
                newFc1 = np.multiply(fcDataFrac, write)
                newPor1 = np.multiply(porDataFrac, write)
                gwlo = np.nansum(newFc1) * abs(geot[1]) * abs(geot[5])
                pgwlo = np.nansum(newPor1) * abs(geot[1]) * abs(geot[5])
                if (gwlo > (1.5 * slo) or gwlo < 0.0) and (np.nanmax(write) > 1.5 or np.nanmin(write) < -1.0):
                    write[write < -0.25] = np.nan
                    write[write > 1.0] = np.nan
                    newFc1 = np.multiply(fcDataFrac, write)
                    newPor1 = np.multiply(porDataFrac, write)
                    gwlo = np.nansum(newFc1) * abs(geot[1]) * abs(geot[5])
                    pgwlo = np.nansum(newPor1) * abs(geot[1]) * abs(geot[5])
                    fixlo=1
                del write
                hdch_ds1 = None
                write2 = np.where(np.isnan(newFc1), -9999.0, newFc1)
                hdch_ds11 = gdal.GetDriverByName('GTiff').Create(modDir + '/hdch_lo_fc.tif', demDs1.RasterXSize,
                                                                demDs1.RasterYSize, 1, gdal.GDT_Float32)
                hdch_ds11.SetProjection(demDs1.GetProjection())
                hdch_ds11.SetGeoTransform(geot)
                hdch_ds11.GetRasterBand(1).WriteArray(write2)
                hdch_ds11.GetRasterBand(1).FlushCache()
                hdch_ds11.GetRasterBand(1).SetNoDataValue(-9999.0)
                del write2
                hdch_ds11 = None

            if success1 and success3:
                hdDif2 = head3[0,:,:] - head1[0,:,:]
                new2 = hdDif2 - pondData2
                hdch_ds2 = gdal.GetDriverByName('GTiff').Create(modDir + '/hdch_mid.tif', demDs1.RasterXSize, demDs1.RasterYSize, 1, gdal.GDT_Float32)
                hdch_ds2.SetProjection(demDs1.GetProjection())
                hdch_ds2.SetGeoTransform(geot)
                write = np.where(np.isnan(new2), -9999.0, new2)
                hdch_ds2.GetRasterBand(1).WriteArray(write)
                hdch_ds2.GetRasterBand(1).FlushCache()
                hdch_ds2.GetRasterBand(1).SetNoDataValue(-9999.0)
                write[write < -5.0] = np.nan
                #write[write > 1.5] = np.nan
                newFc2 = np.multiply(fcDataFrac, write)
                newPor2 = np.multiply(porDataFrac, write)
                gwmid = np.nansum(newFc2) * abs(geot[1]) * abs(geot[5])
                pgwmid = np.nansum(newPor2) * abs(geot[1]) * abs(geot[5])
                if (gwmid > (2.0 * smid) or gwmid < 0.0) and (np.nanmax(write) > 2.0 or np.nanmin(write) < -1.0):
                    write[write < -0.25] = np.nan
                    write[write > 1.5] = np.nan
                    newFc2 = np.multiply(fcDataFrac, write)
                    newPor2 = np.multiply(porDataFrac, write)
                    gwmid = np.nansum(newFc2) * abs(geot[1]) * abs(geot[5])
                    pgwmid = np.nansum(newPor2) * abs(geot[1]) * abs(geot[5])
                    fixmid=1
                del write
                hdch_ds2 = None
                write2 = np.where(np.isnan(newFc2), -9999.0, newFc2)
                hdch_ds21 = gdal.GetDriverByName('GTiff').Create(modDir + '/hdch_mid_fc.tif', demDs1.RasterXSize,
                                                                 demDs1.RasterYSize, 1, gdal.GDT_Float32)
                hdch_ds21.SetProjection(demDs1.GetProjection())
                hdch_ds21.SetGeoTransform(geot)
                hdch_ds21.GetRasterBand(1).WriteArray(write2)
                hdch_ds21.GetRasterBand(1).FlushCache()
                hdch_ds21.GetRasterBand(1).SetNoDataValue(-9999.0)
                del write2
                hdch_ds21 = None

            if success1 and success4:
                hdDif3 = head4[0,:,:] - head1[0,:,:]
                new3 = hdDif3 - pondData3
                hdch_ds3 = gdal.GetDriverByName('GTiff').Create(modDir + '/hdch_hi.tif', demDs1.RasterXSize, demDs1.RasterYSize, 1, gdal.GDT_Float32)
                hdch_ds3.SetProjection(demDs1.GetProjection())
                hdch_ds3.SetGeoTransform(geot)
                write = np.where(np.isnan(new3), -9999.0, new3)
                hdch_ds3.GetRasterBand(1).WriteArray(write)
                hdch_ds3.GetRasterBand(1).FlushCache()
                hdch_ds3.GetRasterBand(1).SetNoDataValue(-9999.0)
                write[write < -5.0] = np.nan
                #write[write > 2.5] = np.nan
                newFc3 = np.multiply(fcDataFrac, write)
                newPor3 = np.multiply(porDataFrac, write)
                gwhi = np.nansum(newFc3) * abs(geot[1]) * abs(geot[5])
                pgwhi = np.nansum(newPor3) * abs(geot[1]) * abs(geot[5])
                if (gwhi > (2.0 * shi) or gwhi < 0.0) and (np.nanmax(write) > 3.0 or np.nanmin(write) < -1.0):
                    write[write < -0.5] = np.nan
                    write[write > 2.2] = np.nan
                    newFc3 = np.multiply(fcDataFrac, write)
                    newPor3 = np.multiply(porDataFrac, write)
                    gwhi = np.nansum(newFc3) * abs(geot[1]) * abs(geot[5])
                    pgwhi = np.nansum(newPor3) * abs(geot[1]) * abs(geot[5])
                    fixhi=1
                del write
                hdch_ds3 = None
                write2 = np.where(np.isnan(newFc3), -9999.0, newFc3)
                hdch_ds31 = gdal.GetDriverByName('GTiff').Create(modDir + '/hdch_hi_fc.tif', demDs1.RasterXSize,
                                                                 demDs1.RasterYSize, 1, gdal.GDT_Float32)
                hdch_ds31.SetProjection(demDs1.GetProjection())
                hdch_ds31.SetGeoTransform(geot)
                hdch_ds31.GetRasterBand(1).WriteArray(write2)
                hdch_ds31.GetRasterBand(1).FlushCache()
                hdch_ds31.GetRasterBand(1).SetNoDataValue(-9999.0)
                del write2
                hdch_ds31 = None

            print "done"

            #row = [os.path.relpath(subdir, path), bratCap, slo, smid, shi, gwlo, gwmid, gwhi, pgwlo, pgwmid, pgwhi, fixlo, fixmid, fixhi]
            row = [os.path.relpath(subdir, path), bratCap, slo, smid, shi, gwlo, gwmid, gwhi, fixlo, fixmid, fixhi]
            print row
            writer.writerow(row)

            print "huc 12 done"

    ofile.close()
    print "MODFLOW done for all HUC12"
