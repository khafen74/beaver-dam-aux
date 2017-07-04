import os
import glob

path = r'F:\01_etal\Projects\Modeling\BeaverWaterStorage\wrk_Data\AnalysisRuns\BearRiverHUC8\16010201\HUC12'
os.chdir(path)

#assign name and create modlfow model object
for subdir, dirs, files in os.walk(path):
    os.chdir(subdir)
    for filename in glob.glob("hi*"):
        os.remove(filename)

    for filename in glob.glob("mid*"):
        os.remove(filename)

    for filename in glob.glob("lo*"):
        os.remove(filename)

    for filename in glob.glob("start*"):
        os.remove(filename)
