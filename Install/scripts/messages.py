# -*- coding: utf-8 -*-

class nls:
    def __init__(self):
        self.title = u"© 2019 INEI - DTDIS"
        self.titleError = u'{} | Error'.format(self.title)  # ERROR
        self.error = u"Debe seleccionar un código de hoja \nantes de realizar la operación."  # ERROR
        self.succesfull = u"El proceso se realizó con éxito"
        self.onDevelop = u'Herramienta en proceso...'

    def changeCode(self, code):
        msg = u"Desea terminar el proyecto \n en la hoja {}".format(code)
        return msg

    class inicio:
        def __init__(self):
            self.title = "Seleccionar la capa de manzanas"
            self.button = "Seleccionar"
            self.error = "La ruta de entrada no contiene archivos mxd\nSeleccione una ruta válida"
            self.typeerror = "Debe seleccionar un feature class"
            self.fielderror = "El feature class no contiene los campos\nUBIGEO Y DISTRITO"

    class eje:
        def __init__(self):
            self.title = "Seleccionar la capa de EJES"
            self.button = "Seleccionar"
            self.error = "La ruta de entrada no contiene archivos mxd\nSeleccione una ruta válida"
            self.typeerror = "Debe seleccionar un feature class"
            self.fielderror = "El feature class no contiene el campo\nUBIGEO"

    class fin:
        def __init__(self):
            self.title = "Definir ruta de salida"
            self.button = "Seleccionar"
            self.error = "La ruta de salida aún no se ha definido"
            self.typeerror = "Debe seleccionar una ruta"




