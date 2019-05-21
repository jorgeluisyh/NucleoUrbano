# -*- coding: utf-8 -*-
import os,sys
import arcpy
import pythonaddins
import threading
import subprocess

BASE_addin    = os.path.dirname(__file__)
SCRIPTS_DIR = os.path.join(BASE_addin,"scripts")
sys.path.insert(0,SCRIPTS_DIR)

from topology import *
pdf = PDF_DIR

class GenCodes(object):
    """Implementation for NnuuTool_addin.gencodes (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        pythonaddins.GPToolDialog(TBX_DIR, 'genCodes')
        pass

class GenPolig(object):
    """Implementation for NnuuTool_addin.genpolig (Button)"""
    def __init__(self):
        self.enabled = False
        self.checked = False
    def onClick(self):
        # pythonaddins.MessageBox(nls().onDevelop, nls().titleError)
        poo = GenerarPoligono(loaddata.loc)
        poo.main()
        gentopo.enabled=True
        # filepy = os.path.join(SCRIPTS_DIR, 'principal.py')
        # pythonexe = os.path.join(sys.exec_prefix, 'python.exe')
        # subprocess.Popen("%s %s %s" % (pythonexe, filepy, loaddata.loc),
        #                  shell=True)

class GenTopo(object):
    """Implementation for NnuuTool_addin.gentopo (Button)"""
    def __init__(self):
        self.enabled = False
        self.checked = False
    def onClick(self):
        self.fcEje = pythonaddins.OpenDialog(nls().eje().title, False, "#", nls().eje().button, lambda x: x,
                                           "Feature Class")
        # pythonaddins.MessageBox(gentopo.fcEje, nls().titleError)
        self.runButton()
    def runButton(self):
        foo=CreateTopology(gentopo.fcEje)
        foo.main()
        # filepy = os.path.join(SCRIPTS_DIR, 'topology.py')
        # pythonexe = os.path.join(sys.exec_prefix, 'python.exe')
        # subprocess.Popen("%s %s %s" % (pythonexe, filepy, gentopo.fcEje),
        #                  shell=True)



class LoadData(object):
    """Implementation for NnuuTool_addin.loaddata (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
        self.ubi     = None
    def onClick(self):
        print
        genpolig.enabled = False
        gentopo.enabled = False
        nomdist.value = ''
        nomdist.refresh()

        self.ubi = pythonaddins.OpenDialog(nls().inicio().title,False,"#",nls().inicio().button,lambda x:x,"Feature Class")
        self.loc = unicode(self.ubi)
        evalue = os.path.basename(self.ubi).split('.')

        if len(evalue)==1:

            if '.gdb' in self.loc:
                try:
                    nomdist.value = self.getName()
                    nomdist.refresh()
                    genpolig.enabled = True
                    pythonaddins.MessageBox(nls().succesfull, nls().title)
                except:
                    pythonaddins.MessageBox(nls().inicio().fielderror, nls().titleError)
                    loaddata.onClick()
            else:
                pythonaddins.MessageBox(nls().inicio().typeerror, nls().titleError)
                loaddata.onClick()
        else:
            pythonaddins.MessageBox(nls().inicio().typeerror, nls().titleError)
            loaddata.onClick()

    def getName(self):

        (x, y) = [x for x in
                  arcpy.da.SearchCursor(self.loc,["UBIGEO", "DISTRITO"] )][0]
        self.ndist ="{}-{}".format(x,y)
        return self.ndist




class NomDist(object):
    """Implementation for NnuuTool_addin.nomdist (ComboBox)"""
    def __init__(self):
        self.items = ["item1", "item2"]
        self.editable = True
        self.enabled = False
        self.dropdownWidth = 'WWWWWW'
        self.width = 'WWW'*5
        self.value = ''
    def onSelChange(self, selection):
        pass
    def onEditChange(self, text):
        pass
    def onFocus(self, focused):
        pass
    def onEnter(self):
        pass
    def refresh(self):
        pass

class Info(object):
    """Implementation for NnuuTool_addin.info (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):

        if os.path.exists(pdf):
            openFiles(pdf).process()
        else:
            pythonaddins.MessageBox(nls().onDevelop, nls().titleError)
        # info.checked=False

class openFiles(object):
    def __init__(self, parameter):
        self.parameter = parameter

    def process(self):
        t = threading.Thread(target=os.startfile, args=(self.parameter,))
        t.start()
        t.join()