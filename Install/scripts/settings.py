import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
STATICS_DIR = os.path.join(BASE_DIR, "statics")
GDB_DIR = os.path.join(STATICS_DIR, "GDB")
IMG_DIR = os.path.join(STATICS_DIR, "Images")
TBX_DIR = os.path.join(STATICS_DIR, "nnuu.tbx")
PDF_DIR = os.path.join(IMG_DIR, 'UserGuide.pdf')
FIELD_V = ["Concat_1", "TEXT", "#", "#", 120]
spatial_reference = "PROJCS['WGS_1984_UTM_Zone_18S',GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Transverse_Mercator'],PARAMETER['False_Easting',500000.0],PARAMETER['False_Northing',10000000.0],PARAMETER['Central_Meridian',-75.0],PARAMETER['Scale_Factor',0.9996],PARAMETER['Latitude_Of_Origin',0.0],UNIT['Meter',1.0]];-5120900 1900 10000;-100000 10000;-100000 10000;0.001;0.001;0.001;IsHighPrecision"

class Dataset:
    def __init__(self):
        self.Ds_bufferout="TEMP_B_Out"
        self.Ds_bufferin ="TEMP_B_In"
        self.len_bufout  = "30 Meters"
        self.len_bufin   = "-27 Meters"
        self.multi       = "Polygon_nnuu"
    def join(self,gdb,buffer="out"):
        if buffer.lower()=="in":
            x=os.path.join(gdb,self.Ds_bufferin)
        else:
            x=os.path.join(gdb,self.Ds_bufferout)
        return x
