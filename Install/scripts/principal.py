# -*- coding: utf-8 -*-
import arcpy,pythonaddins,sys
from settings import*
from messages import *
from multiprocessing import Pool
arcpy.env.overwriteOutput=True

ds_temp = Dataset()
decorador = os.path.join(IMG_DIR, 'loader.exe')


def decorator_loader(func):
    def decorator(*args):
        import subprocess
        import signal
        import os
        p = subprocess.Popen(decorador)
        func(*args)
        os.kill(p.pid, signal.SIGTERM)
    return decorator

class GenerarPoligono(object):
    def __init__(self,mz):
        self.mz = mz
        self.gdb= '{}.gdb'.format(self.mz.split('.gdb')[0])
        self.fc = self.mz#arcpy.MakeFeatureLayer_management(self.mz)


    def createStats(self):
        fv = FIELD_V
        self.listQuery =[]
        arcpy.AddField_management(self.mz,fv[0],fv[1],fv[2],fv[3],fv[4])
        print "calculando"
        with arcpy.da.UpdateCursor(self.fc, ["UBIGEO","CATEGNNUU","NOMNNUU",fv[0]]) as cursor:
            for i in cursor:
                con = u"{}-{}-{}".format(i[0],i[1],i[2])
                if i[0]not in valid["ubi"]:
                    valid["ubi"].append(i[0])
                i[3]=con
                if con not in self.listQuery:
                    self.listQuery.append(con)
                cursor.updateRow(i)
        self.createDataset(ds_temp.Ds_bufferin)
        self.createDataset(ds_temp.Ds_bufferout)

    def createDataset(self,name):
        self.dn =name
        self.dataset = os.path.join(self.gdb, name)
        if os.path.exists(self.dataset):
            pass
        else:
            arcpy.CreateFeatureDataset_management(
                out_dataset_path=self.gdb,
                out_name=name,
                spatial_reference=spatial_reference)


    def createPolygons(self):
            lyr =self.fc
            dsin= ds_temp.join(self.gdb,buffer="in")
            valid["df"]=dsin
            dsout= ds_temp.join(self.gdb)
            bfout= os.path.join(dsout,'temp_bufferout')
            bfin= os.path.join(dsin,'temp_bufferin')
            arcpy.env.outputCoordinateSystem = arcpy.SpatialReference("WGS 1984 UTM Zone 18S")
            arcpy.Buffer_analysis(in_features=lyr,
                                  out_feature_class=bfout,
                                  buffer_distance_or_field=ds_temp.len_bufout, line_side="FULL", line_end_type="ROUND",
                                  dissolve_option="LIST", dissolve_field=FIELD_V[0], method="PLANAR")
            arcpy.Buffer_analysis(in_features=bfout,
                                  out_feature_class=bfin,
                                  buffer_distance_or_field=ds_temp.len_bufin, line_side="FULL", line_end_type="ROUND",
                                  dissolve_option="LIST", dissolve_field=FIELD_V[0], method="PLANAR")
            del lyr
            polyg= os.path.join(dsin,ds_temp.multi)
            arcpy.MultipartToSinglepart_management(bfin,polyg)
            valid["pl"]=polyg
            arcpy.Densify_edit(polyg, "DISTANCE", "5 Meters")


    def runProcess(self):
        self.createStats()
        self.createPolygons()

    @decorator_loader
    def main(self):
        self.runProcess()


valid = {"pl": 0, "ubi":[], "df":0}





if __name__ == "__main__":
    poo = GenerarPoligono("mz")
    poo.mz = sys.argv[1]

    poo.main()

