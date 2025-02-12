from config.app import * 
import pandas as pd
from datetime import datetime

def GenerateReportVentas(app: App):
    conn = app.bd.getConection()
    ventas_df = pd.read_sql_query("SELECT * FROM VENTAS", conn)
    region_df = pd.read_sql_query("SELECT * FROM REGION", conn)
    
    merged_df = ventas_df.merge(region_df, left_on='region', right_on='name', how='left')
    
    report_df = merged_df.groupby(['name', 'product_id'])['quantity'].sum().reset_index()
    report_df.rename(columns={'name': 'region', 'quantity': 'total_vendido'}, inplace=True)
    
    report_df = report_df.sort_values(by='total_vendido', ascending=False)
    
    path = "/workspaces/PROYECTOFINAL/proyecto/files/datafuente.csv"
    report_df.to_csv(path, index=False)
    
    sendMail(app, path)

def sendMail(app: App, data):
    fecha = datetime.today().strftime('%Y-%m-%d')  
    asunto = f"Reporte de Ventas - {fecha}"  
    app.mail.send_email('from@example.com', asunto, 'Reporte', data)

