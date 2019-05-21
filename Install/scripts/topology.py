# -*- coding: utf-8 -*-
from principal import *

class CreateTopology():

    def __init__(self,eje):
        self.polig  = valid["pl"]
        self.eje    = eje

    def snapEje(self):
        sent = "OBJECTID={}"
        senteje= "UBIGEO IN ('{}')".format("','".join(valid["ubi"]))
        self.fceje= arcpy.MakeFeatureLayer_management(self.eje,'eje',senteje)
        self.fcpoli= arcpy.MakeFeatureLayer_management(self.polig,'fcpoli')
        pythonaddins.MessageBox(self.calcTime(),"Tiempo de espera aproximado")
        with arcpy.da.SearchCursor(self.polig, "OBJECTID") as cursor:
            c = 1
            for i in cursor:
                mfl = arcpy.SelectLayerByAttribute_management(self.fcpoli, "NEW_SELECTION", sent.format(str(i[0])))
                arcpy.edit.Snap(mfl, [['eje', "EDGE", "10 Meters"]])
                print c
                c += 1
    def setTopology(self):
        #creamos la topologia en el dataset de in
        topo =os.path.join(valid["df"],"topo")
        arcpy.CreateTopology_management(valid["df"], "topo")
        arcpy.AddFeatureClassToTopology_management(topo, self.polig)
        arcpy.AddRuleToTopology_management( topo, "Must Not Overlap (Area)", self.polig)
        arcpy.ValidateTopology_management(topo)
        arcpy.ExportTopologyErrors_management(topo,valid["df"], "topo")
        arcpy.env.workspace= valid["df"]
        listfc= arcpy.ListFeatureClasses()
        for fc in listfc:
            if fc.endswith("_line") or fc.endswith("_point"):
                if arcpy.Exists(fc):
                    arcpy.Delete_management(fc)
        top_poly=os.path.join(valid["df"],'topo_poly')
        arcpy.AddField_management(top_poly,"area_sqm","DOUBLE")
        arcpy.env.outputCoordinateSystem = arcpy.SpatialReference("WGS 1984 UTM Zone 18S")
        arcpy.CalculateField_management(top_poly, "area_sqm", "!shape.area@squaremeters!", "PYTHON_9.3")
        with arcpy.da.UpdateCursor(top_poly, "area_sqm", "area_sqm<400") as cursoru:
            for i in cursoru:
                cursoru.deleteRow()




    def calcTime(self):
        #calcula el tiempo aproximado que tomara realizar el snap
        numerofts= len([row for row in arcpy.da.SearchCursor(self.polig,"OBJECTID")])
        minutes= numerofts/14
        if minutes>=60 and minutes%60!=0:
            hr= minutes/60
            min= minutes%60
            time = "{} horas y {} minutos".format(hr,min)
        elif minutes>=60 and minutes%60==0:
            hr = minutes / 60
            time = "{} horas".format(hr)
        else:
            time = "{} minutos".format(minutes)
        return "El proceso puede tardar un aproximado de\n{}".format(time)


    def cleanMxd(self):
        mxd = arcpy.mapping.MapDocument("current")
        df = mxd.activeDataFrame
        lyr = arcpy.mapping.ListLayers(mxd, 'temp*', df)[0]
        arcpy.mapping.RemoveLayer(df, lyr)
        del mxd, df, lyr

    @decorator_loader
    def main(self):
        self.snapEje()
        self.setTopology()
        self.cleanMxd()



if __name__ == "__main__":
    poo = CreateTopology("eje")
    poo.eje = sys.argv[1]
    poo.main()

