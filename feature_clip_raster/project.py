from osgeo import gdal

huc8s = ['16010101', '16010102', '16010201', '16010202', '16010203', '16010204']
files = ['fc_vbfac.tif', 'por_vbfac.tif', 'ksat_vbfac.tif', 'kv_vbfac.tif']
demds = gdal.Open(r'E:\konrad\Projects\Modeling\BeaverWaterStorage\wrk_Data\AnalysisRuns\BearRiverHUC8\16010204\02_rasIn\dem_vbfac.tif', gdal.GA_ReadOnly)

for huc8 in huc8s:
    for file in files:
        rasPath = 'E:/konrad/Projects/Modeling/BeaverWaterStorage/wrk_Data/AnalysisRuns/BearRiverHUC8/' + huc8 + '/02_rasIn/' + file
        ds = gdal.Open(rasPath, gdal.GA_Update)
        ds.SetProjection(demds.GetProjection())
        ds = None