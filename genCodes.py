# -*- coding: utf-8 -*-
import arcpy,os

arcpy.env.overwriteOutput=True

mzs_ini=mzs = arcpy.GetParameterAsText(0)
plg_ini=plg = arcpy.GetParameterAsText(1)
# mzs= arcpy.management.MakeFeatureLayer(mzs_ini, 'mz').getOutput(0)
# plg= arcpy.management.MakeFeatureLayer(plg_ini, 'plg').getOutput(0)
arcpy.AddWarning("modified")
arcpy.AddWarning(type(plg))
arcpy.AddWarning(type(mzs))
# if type(plg)!=str and type(plg)!=unicode:
#     plg = plg.dataSource
# if type(mzs)!=str and type(mzs)!=unicode:
#     mzs = mzs.dataSource


listf= [mzs,plg]
concat = "Concat_1"
field  = "CODNNUU"
idmz   = "IDMANZANA"
report = "REPORT"

#Agregamos el campo que contendrá el código de nnuu
for lyr in listf:
    if field not in [x.name for x in arcpy.ListFields(lyr)]:
        arcpy.AddField_management(lyr,field,"TEXT","","",4)
    else:
        pass
if report not in [x.name for x in arcpy.ListFields(mzs)]:
    arcpy.AddField_management(mzs,report,"TEXT","","",4)
#funcion para calcular el código de nnuu
def calc(x):
    x=arcpy.management.MakeFeatureLayer(x, 'plg').getOutput(0)
    x=x.dataSource
    ws = "{}.gdb".format(x.split(".gdb")[0])
    edit = arcpy.da.Editor(ws)
    edit.startEditing()
    with arcpy.da.UpdateCursor(x,[concat,field],sql_clause=(None,'ORDER BY Concat_1')) as cursoru:
        count =1
        for i in cursoru:
            if count ==1:
                i[1] = str(count).zfill(4)
                ubi= i[0][0:6]
            else:
                if ubi==i[0][0:6]:
                    i[1]=str(count).zfill(4)
                else :
                    ubi= i[0][0:6]
                    count =1
                    i[1]=str(count).zfill(4)
            count+=1
            cursoru.updateRow(i)
    del cursoru
    edit.stopEditing(True)

calc(plg)

#definimos parámetros para llamar al feature layer
fieldsPolygon = [x.name for x in arcpy.ListFields(plg)]
fieldsMzs = [x.name for x in arcpy.ListFields(mzs)]
def fx(x):
    if x== concat or x== field or x == idmz:
        res= "{0} {0} VISIBLE NONE"        
    else:
        res="{0} {0} HIDDEN NONE"
    return res.format(x)
field_pol = "; ".join(list(map(fx,fieldsPolygon)))
field_mzs = "; ".join(list(map(fx,fieldsMzs)))
fl_pol=arcpy.MakeFeatureLayer_management(in_features=plg,
                                  out_layer="polig_cod", where_clause="", workspace="",
                                  field_info=field_pol)
fl_mzs = arcpy.MakeFeatureLayer_management(mzs,"fl_mzs",field_info=field_mzs)


with arcpy.da.SearchCursor(fl_pol,["SHAPE@",concat,field]) as cursor:
    for i in cursor:
        fc = arcpy.SelectLayerByLocation_management(fl_mzs,"INTERSECT",i[0],"","NEW_SELECTION")
        with arcpy.da.UpdateCursor(fc,[concat,field,report]) as cursorP:
            for act in cursorP:
                if act[0]==i[1]:
                    act[1]=i[2]
                else:
                    act[2]="err"
                cursorP.updateRow(act)
        del cursorP
del cursor
arcpy.SelectLayerByAttribute_management(fl_pol,"CLEAR_SELECTION")

arcpy.AddWarning("Script made by\n Jorge Yupanqui Herrera")
arcpy.SetParameterAsText(2,mzs_ini)
arcpy.SetParameterAsText(3,plg_ini)
