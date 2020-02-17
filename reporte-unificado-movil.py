import os.path
import pandas as pd 
import numpy as np
from datetime import datetime
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

class ReporteUM:
    def __init__(self):
        self.today = datetime.today().strftime('%Y-%m-%d')
        self.excel_file = "REPORTE_UNIFICADO_MOVIL.xlsx"
        self.sheet = "UNIFICADO_MOVIL"
        self.output = 'REPORTE_UNIFICADO_MOVIL_{}.xlsx'.format(self.today)

    def upload(self):
        if os.path.isfile(self.excel_file):
            self.rp = pd.read_excel(self.excel_file, index_col=0, sheet_name=self.sheet)
            self.rp = self.rp.reset_index()
            print("xlsx imported as rp")
            print(type(self.rp))
        else:
            print("no data file in root.")

    def transform(self):
        self.rp["id_pedido"] = self.rp["id_pedido"].astype(str)
        self.search = "10"
        self.bool_rp = self.rp["id_pedido"].str.startswith(self.search, na=False)
        self.rp10 = self.rp[self.bool_rp]

    def merge(self):
        self.rpm = pd.merge(self.rp, self.rp10[['contactid', 'id_pedido']], on='contactid', how = 'left')
        self.rpm = self.rpm.drop('id_pedido_x', axis = 1)
        self.rpm = self.rpm.rename({'id_pedido_y':'id_pedido'}, axis = 1)
        self.rpm['id_pedido'] = self.rpm['id_pedido'].fillna(self.rp['id_pedido'])
        self.rpm = self.rpm.replace(np.nan, '', regex=True)
        rgx = r'\D'
        filter = self.rpm['id_pedido'].str.contains(rgx)
        self.rpm = self.rpm[~filter]
    
    def export(self):
        self.rpm.to_excel(self.output, index=False)


reporte = ReporteUM()
reporte.upload()
reporte.transform()
reporte.merge()
reporte.export()


#print("--- first 5 rows ---")
#print(rp.head(5))
#print("--- row x col ---")
#print(rp.shape)
#print("---- casting id_pedido to str ----")

#print("--- rp col types ---")
#print(rp.dtypes.head(3))

#print("---- printing booled series ----")
#print(bool_rp.head(5))
#print("---- adding contactid as column not only index or row name ----")

"""

#merge data frames
print("--- merging dataframes ---")
rpm = pd.merge(rp, rp10[['contactid', 'id_pedido']], on='contactid', how = 'left')
rpm = rpm.drop('id_pedido_x', axis = 1)
rpm = rpm.rename({'id_pedido_y':'id_pedido'}, axis = 1)
rpm['id_pedido'] = rpm['id_pedido'].fillna(rp['id_pedido'])
rpm = rpm.replace(np.nan, '', regex=True)
#print(rpm)

#remove rows with non numeric values at id_pedido
rgx = r'\D'
filter = rpm['id_pedido'].str.contains(rgx)
rpm = rpm[~filter]
#print(rpm)

rpm.to_excel(output, index=False)



# paso 1: filtra "fec_registro" = today
# later

# tarea: id_pedido tiene registros con 53 y 54, deben ser reemplazados por los valores que inician con 10
#search = 10


# la llave a usarse es "contact_id" para encontrar y reemplazar.
# los valores no se eliminan
# se mantienen los pedidos duplicados con el mismo id_pedido 
# valores de id_pedido con 0 o vacios permanecen en la tabla
# los duplicados se encuentran en la columna id_pedido
# eliminar id_pedido con valores no numericos

"""