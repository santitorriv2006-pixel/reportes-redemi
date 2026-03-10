import pandas as pd
from io import BytesIO
from datetime import datetime
from flask import send_file
from logger_config import logger_excel
from app.models import Reporte

class ExportService:
    """
    Servicio para exportar datos a Excel
    """
    
    COLUMNAS_REPORTE = [
        'WO',
        'Usuario Asignado',
        'Fecha',
        'Horas Aprobadas',
        'Horas Reales',
        'Diferencia Horas',
        'Grupo'
    ]
    
    @staticmethod
    def export_usuario_excel(usuario, fecha_inicio=None, fecha_fin=None, grupo=None):
        """
        Exporta reportes de un usuario específico a Excel
        
        Args:
            usuario: Nombre del usuario
            fecha_inicio: Fecha inicio (opcional)
            fecha_fin: Fecha fin (opcional)
            grupo: Filtrar por grupo (opcional)
        
        Returns:
            BytesIO: Archivo Excel en memoria
        """
        try:
            # Consultar reportes del usuario
            query = Reporte.query.filter_by(usuario_asignado=usuario)
            
            if fecha_inicio:
                query = query.filter(Reporte.fecha >= fecha_inicio)
            if fecha_fin:
                query = query.filter(Reporte.fecha <= fecha_fin)
            if grupo:
                query = query.filter_by(grupo=grupo)
            
            reportes = query.all()
            
            if not reportes:
                logger_excel.warning(f"No hay reportes para usuario {usuario}")
                return None
            
            # Crear dataframe
            datos = []
            total_aprobadas = 0
            total_reales = 0
            
            for reporte in reportes:
                datos.append({
                    'WO': reporte.wo,
                    'Usuario Asignado': reporte.usuario_asignado,
                    'Fecha': reporte.fecha.strftime('%Y-%m-%d'),
                    'Horas Aprobadas': reporte.horas_aprobadas,
                    'Horas Reales': reporte.horas_reales,
                    'Diferencia Horas': reporte.calcular_diferencia(),
                    'Grupo': reporte.grupo
                })
                total_aprobadas += reporte.horas_aprobadas
                total_reales += reporte.horas_reales
            
            df = pd.DataFrame(datos)
            
            # Agregar fila de totales
            fila_totales = {
                'WO': 'TOTAL',
                'Usuario Asignado': usuario,
                'Fecha': '',
                'Horas Aprobadas': total_aprobadas,
                'Horas Reales': total_reales,
                'Diferencia Horas': round(total_reales - total_aprobadas, 2),
                'Grupo': ''
            }
            
            df = pd.concat([df, pd.DataFrame([fila_totales])], ignore_index=True)
            
            # Crear archivo Excel
            output = BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name='Reporte', index=False)
                
                # Formatear columnas
                worksheet = writer.sheets['Reporte']
                for column in worksheet.columns:
                    max_length = 0
                    column_letter = column[0].column_letter
                    for cell in column:
                        try:
                            if len(str(cell.value)) > max_length:
                                max_length = len(cell.value)
                        except:
                            pass
                    adjusted_width = min(max_length + 2, 50)
                    worksheet.column_dimensions[column_letter].width = adjusted_width
            
            output.seek(0)
            logger_excel.info(f"Reporte de usuario {usuario} exportado exitosamente")
            
            return output
            
        except Exception as e:
            logger_excel.error(f"Error exportando reporte de usuario {usuario}: {str(e)}")
            return None
    
    @staticmethod
    def generar_excel_reporte(reportes, usuario):
        """
        Genera un archivo Excel a partir de una lista de reportes
        
        Args:
            reportes: Lista de objetos Reporte
            usuario: Nombre del usuario para el título
        
        Returns:
            BytesIO: Archivo Excel en memoria
        """
        try:
            if not reportes:
                logger_excel.warning("No hay reportes para generar Excel")
                return None
            
            # Crear dataframe
            datos = []
            total_aprobadas = 0
            total_reales = 0
            
            for reporte in reportes:
                datos.append({
                    'WO': reporte.wo,
                    'Usuario Asignado': reporte.usuario_asignado,
                    'Fecha': reporte.fecha.strftime('%Y-%m-%d'),
                    'Horas Aprobadas': reporte.horas_aprobadas,
                    'Horas Reales': reporte.horas_reales,
                    'Diferencia Horas': reporte.calcular_diferencia(),
                    'Grupo': reporte.grupo,
                    'Status': reporte.status,
                    'Tipo': reporte.tipo
                })
                total_aprobadas += reporte.horas_aprobadas
                total_reales += reporte.horas_reales
            
            df = pd.DataFrame(datos)
            
            # Agregar fila de totales
            fila_totales = {
                'WO': 'TOTAL',
                'Usuario Asignado': usuario,
                'Fecha': '',
                'Horas Aprobadas': total_aprobadas,
                'Horas Reales': total_reales,
                'Diferencia Horas': round(total_reales - total_aprobadas, 2),
                'Grupo': '',
                'Status': '',
                'Tipo': ''
            }
            
            df = pd.concat([df, pd.DataFrame([fila_totales])], ignore_index=True)
            
            # Crear archivo Excel
            output = BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name='Reporte', index=False)
                
                # Formatear columnas
                worksheet = writer.sheets['Reporte']
                for column in worksheet.columns:
                    max_length = 0
                    column_letter = column[0].column_letter
                    for cell in column:
                        try:
                            if len(str(cell.value)) > max_length:
                                max_length = len(cell.value)
                        except:
                            pass
                    adjusted_width = min(max_length + 2, 50)
                    worksheet.column_dimensions[column_letter].width = adjusted_width
            
            output.seek(0)
            logger_excel.info(f"Reporte para {usuario} generado exitosamente")
            
            return output
            
        except Exception as e:
            logger_excel.error(f"Error generando Excel reporte: {str(e)}")
            return None
    
    @staticmethod
    def export_global_excel(fecha_inicio=None, fecha_fin=None, grupo=None):
        """
        Exporta todos los reportes filtrados a Excel
        
        Args:
            fecha_inicio: Fecha inicio (opcional)
            fecha_fin: Fecha fin (opcional)
            grupo: Filtrar por grupo (opcional)
        
        Returns:
            BytesIO: Archivo Excel en memoria
        """
        try:
            # Consultar todos los reportes
            query = Reporte.query
            
            if fecha_inicio:
                query = query.filter(Reporte.fecha >= fecha_inicio)
            if fecha_fin:
                query = query.filter(Reporte.fecha <= fecha_fin)
            if grupo:
                query = query.filter_by(grupo=grupo)
            
            reportes = query.order_by(
                Reporte.usuario_asignado,
                Reporte.fecha
            ).all()
            
            if not reportes:
                logger_excel.warning("No hay reportes para exportar")
                return None
            
            # Crear dataframe
            datos = []
            total_aprobadas = 0
            total_reales = 0
            
            for reporte in reportes:
                datos.append({
                    'WO': reporte.wo,
                    'Usuario Asignado': reporte.usuario_asignado,
                    'Fecha': reporte.fecha.strftime('%Y-%m-%d'),
                    'Horas Aprobadas': reporte.horas_aprobadas,
                    'Horas Reales': reporte.horas_reales,
                    'Diferencia Horas': reporte.calcular_diferencia(),
                    'Grupo': reporte.grupo
                })
                total_aprobadas += reporte.horas_aprobadas
                total_reales += reporte.horas_reales
            
            df = pd.DataFrame(datos)
            
            # Agregar resumen por usuario
            resumen_usuario = df.groupby('Usuario Asignado').agg({
                'Horas Aprobadas': 'sum',
                'Horas Reales': 'sum'
            }).reset_index()
            
            # Agregar fila de totales generales
            fila_totales = {
                'WO': 'TOTAL GENERAL',
                'Usuario Asignado': '',
                'Fecha': '',
                'Horas Aprobadas': total_aprobadas,
                'Horas Reales': total_reales,
                'Diferencia Horas': round(total_reales - total_aprobadas, 2),
                'Grupo': ''
            }
            
            df = pd.concat([df, pd.DataFrame([fila_totales])], ignore_index=True)
            
            # Crear archivo Excel con múltiples hojas
            output = BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name='Detalle', index=False)
                resumen_usuario.to_excel(writer, sheet_name='Resumen Usuario', index=False)
                
                # Formatear columnas
                for sheet_name in ['Detalle', 'Resumen Usuario']:
                    worksheet = writer.sheets[sheet_name]
                    for column in worksheet.columns:
                        max_length = 0
                        column_letter = column[0].column_letter
                        for cell in column:
                            try:
                                if len(str(cell.value)) > max_length:
                                    max_length = len(cell.value)
                            except:
                                pass
                        adjusted_width = min(max_length + 2, 50)
                        worksheet.column_dimensions[column_letter].width = adjusted_width
            
            output.seek(0)
            logger_excel.info("Reporte global exportado exitosamente")
            
            return output
            
        except Exception as e:
            logger_excel.error(f"Error exportando reporte global: {str(e)}")
            return None
    
    @staticmethod
    def get_filename_export(usuario=None, incluir_fecha=True):
        """
        Genera nombre de archivo para descarga
        
        Args:
            usuario: Nombre del usuario (None para global)
            incluir_fecha: Incluir fecha en el nombre
        
        Returns:
            str: Nombre del archivo
        """
        fecha = datetime.now().strftime('%Y%m%d') if incluir_fecha else ''
        
        if usuario:
            nombre_seguro = usuario.replace(' ', '_').replace('/', '_')
            return f"reporte_{nombre_seguro}_{fecha}.xlsx"
        else:
            return f"reporte_global_{fecha}.xlsx"
