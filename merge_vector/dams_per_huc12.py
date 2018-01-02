import os
import ogr
import csv

huc8s = [16010101, 16010102, 16010201, 16010202, 16010203, 16010204]
caps = ["05","25","50","100"]
baseDir = r"E:\konrad\Projects\Modeling\BeaverWaterStorage\wrk_Data\AnalysisRuns\BearRiverHUC8"
outfile = r"E:\konrad\Projects\Modeling\BeaverWaterStorage\wrk_Data\AnalysisRuns\BearRiverHUC8\EntireBasin\HUC12damcounts.csv"
filename = 'ModeledDamPoints.shp'
ofile = open(outfile, 'wb')
writer = csv.writer(ofile)
row = ["huc12", "dams005","dams025", "dams050", "dams100"]
writer.writerow(row)
for huc8 in huc8s:
    searchDir = baseDir + '/' + str(huc8) + '/HUC12'
    for subdir, dirs, files in os.walk(searchDir):
        if os.path.exists(subdir + '/03_out_05/'+filename):
            row[0] = os.path.relpath(subdir, searchDir)
            for i in range(0,4):
                modelDir = subdir + '/03_out_'+caps[i]
                ds = ogr.Open(modelDir + "/" + filename)
                lyr = ds.GetLayer()
                row[i+1] = lyr.GetFeatureCount()
            writer.writerow(row)

ofile.close()

