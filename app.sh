#!/bin/bash
#########################################################

## run in cloud build
 #pip3 install numpy
 #pip3 install pandas --no-build-isolation
 #pip3 install xlrd
 #pip3 install openpyxl
 #pip3 install xlsxwriter
 # not install pip3 install datatable
 # not used here yet datatable requires python3.7+


mv REPORTE_UNIFICADO_MOVIL*xlsx REPORTE_UNIFICADO_MOVIL.xlsx

# run anywhere
PYTHONIOENCODING=utf-8 python3.8 reporte_unificado_movil.py
