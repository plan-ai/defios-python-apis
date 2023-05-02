import os

os.system("black ../DefiOSPython")
print("")
os.system("black dummy_db_scripts/")
print("")
os.system("black ../tests")
