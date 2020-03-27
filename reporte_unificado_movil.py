import os.path
import pandas as pd
import numpy as np
from datetime import datetime
import xlsxwriter
import glob
import re

"""
import datatable as dt
https://datatable.readthedocs.io/en/latest/quick-start.html

csv_file = "REPORTE_UNIFICADO_MOVIL.csv"
excel_file = "REPORTE_UNIFICADO_MOVIL.xlsx"
sheet = "UNIFICADO_MOVIL"


if os.path.isfile(csv_file):
    rp = dt.fread(csv_file)
    print("csv imported as rp")
elif os.path.isfile(excel_file):
    rp = pd.read_excel(excel_file, index_col=0, sheet_name=sheet)
    rp = dt.Frame(rp)
    print("xlsx imported as rp")
else:
    print("no data file has been found")

print(type(rp))
"""

shape_before_transformation = []
shape_current_month = []
shape_after_transformation = []


class ReporteUM:
    def __init__(self, file):
        self.today = datetime.today().strftime('%Y-%m-%d')
        self.input = file
        self.output = re.sub(r'input', 'output', file)
        self.sheet = "UNIFICADO_MOVIL"
        #self.output = 'REPORTE_UNIFICADO_MOVIL_{}.xlsx'.format(self.today)

    def upload(self):
        if os.path.isfile(self.input):
            self.rp = pd.read_excel(
                self.input, index_col=0, sheet_name=self.sheet)
            self.rp = self.rp.reset_index()
            print("xlsx imported as rp")
            # print(type(self.rp))
            shape_before_transformation = self.rp.shape
            print('before transformation: ', shape_before_transformation)
        else:
            print("no data file in root.")

    def clean(self):
        self.rp = self.rp.replace(
            np.nan, '', regex=True)  # NaN to empty string
        self.rp["id_pedido"] = self.rp["id_pedido"].astype(str)
        filter = self.rp["id_pedido"].str.contains("[A-Za-z]", na=False)
        self.rp = self.rp[filter == False]  # Lo opuesto al filtro
        shape_clean_data = self.rp.shape
        print('clean data:', shape_clean_data)

    def filter_by_month(self, mo):
        filter = self.rp["fec_registro"].dt.month.isin([mo])
        self.rp = self.rp[filter]
        shape_current_month = self.rp.shape
        print('current month:', shape_current_month)

    def transform(self):
        self.search = "10"
        self.bool_rp = self.rp["id_pedido"].str.startswith(
            self.search, na=False)
        self.rp10 = self.rp[self.bool_rp]
        self.merge()

    def merge(self):
        self.rpm = pd.merge(
            self.rp, self.rp10[['contactid', 'id_pedido']], on='contactid', how='left')
        #self.rpm = self.rpm.drop('id_pedido_x', axis = 1)
        #self.rpm = self.rpm.rename({'id_pedido_y':'id_pedido'}, axis = 1)
        self.rpm['id_pedido_y'] = self.rpm['id_pedido_y'].fillna(
            self.rp['id_pedido'])
        # rgx = r'\w+[\d@]\w+|^$|nan'
        # filter = self.rpm['id_pedido_y'].str.contains(rgx)
        # self.rpm = self.rpm[filter]
        shape_after_transformation = self.rpm.shape
        print('after transformation: ', shape_after_transformation)

    def export(self):
        engine = 'xlsxwriter'  # or 'openpyxl', 'xlwt'
        writer = pd.ExcelWriter(self.output, engine=engine)
        self.rpm.to_excel(writer, index=False)
        writer.close()
        print('export: ', 'done')
        #self.rpm.to_excel(self.output, index=False)

    def log(self, file_name):
        ts = datetime.now()
        ts = ts.strftime('%Y-%m-%d %H:%M:%S')
        lvar = str(len(self.rpm))
        with open(file_name, "a+") as file_object:
            file_object.write(ts)
            file_object.write(",")
            file_object.write(lvar)
            file_object.write("\n")
        print('log: ', 'done')


"""
Definitions ends here
"""

files = list(glob.glob('input/*'))
for file in files:
    reporte = ReporteUM(file)
    time_0 = datetime.now().time()
    print('time_0: ', time_0)

    reporte.upload()
    time_1 = datetime.now().time()
    print('time_1: ', time_1)

    reporte.clean()
    time_2 = datetime.now().time()
    print('time_2: ', time_2)

    # reporte.filter_by_month(2)
    reporte.filter_by_month(datetime.now().month)
    time_3 = datetime.now().time()
    print('time_3: ', time_3)

    reporte.transform()
    time_4 = datetime.now().time()
    print('time_4: ', time_4)

    reporte.export()
    time_5 = datetime.now().time()
    print('time_5: ', time_5)

    reporte.log("log.csv")
    time_6 = datetime.now().time()
    print('time_6: ', time_6)
