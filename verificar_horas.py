#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Analizar horas en el archivo Excel
"""
import pandas as pd

df = pd.read_excel('archivos/Reportes_Convertidos.xlsx')
print('ANÁLISIS DE HORAS')
print('=' * 60)
print(f'\nColumnas: {list(df.columns)}')
print(f'\nPrimeros 20 registros:')
print(df[['WO', 'Usuario Asignado', 'Horas Aprobadas', 'Horas Reales']].head(20).to_string())

print(f'\n\nTipos de datos:')
print(df.dtypes)

print(f'\n\nValores nulos:')
print(f'  Horas Aprobadas: {df["Horas Aprobadas"].isna().sum()} nulos')
print(f'  Horas Reales: {df["Horas Reales"].isna().sum()} nulos')

print(f'\n\nRango de valores:')
print(f'  Horas Aprobadas min: {df["Horas Aprobadas"].min()}, max: {df["Horas Aprobadas"].max()}')
print(f'  Horas Reales min: {df["Horas Reales"].min()}, max: {df["Horas Reales"].max()}')

print(f'\n\nSuma total (Excel):')
print(f'  Total Horas Aprobadas: {df["Horas Aprobadas"].sum()}')
print(f'  Total Horas Reales: {df["Horas Reales"].sum()}')
