import pandas as pd
from datetime import datetime
import os
from logger_config import logger_excel
from config import Config

class ExcelProcessingService:
    """
    Servicio para procesar y validar archivos Excel
    """
    
    COLUMNAS_OBLIGATORIAS = {
        'WO',
        'Usuario Asignado',
        'Fecha',
        'Horas Aprobadas',
        'Horas Reales',
        'Grupo'
    }
    
    @staticmethod
    def allowed_file(filename):
        """Verifica que el archivo tenga extensión permitida"""
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS
    
    @staticmethod
    def validate_file(filepath):
        """
        Valida el archivo Excel antes de procesarlo
        Soporta múltiples hojas: 1-Solicitudes, 2-Incidentes, 3-Tareas
        
        Returns:
            tuple: (es_valido, mensaje_error, datos)
        """
        excel_file = None
        try:
            # Leer todas las hojas del archivo
            excel_file = pd.ExcelFile(filepath)
            logger_excel.info(f"Hojas encontradas: {excel_file.sheet_names}")
            
            dfs_combined = []
            
            # Mapear hojas a tipos
            sheet_type_map = {
                '1-Solicitudes': 'Solicitud',
                '2-Incidentes': 'Incidente',
                '3-Tareas': 'Tarea'
            }
            
            # Procesar cada hoja
            for sheet_name in excel_file.sheet_names:
                if sheet_name not in sheet_type_map:
                    continue
                    
                df = pd.read_excel(filepath, sheet_name=sheet_name)
                logger_excel.info(f"Hoja leída: {sheet_name} con {len(df)} registros")
                
                # Verificar columnas obligatorias
                columnas_faltantes = ExcelProcessingService.COLUMNAS_OBLIGATORIAS - set(df.columns)
                if columnas_faltantes:
                    mensaje = f"Columnas faltantes en {sheet_name}: {', '.join(columnas_faltantes)}"
                    logger_excel.error(mensaje)
                    continue
                
                # Agregar columna de tipo
                df['Tipo'] = sheet_type_map[sheet_name]
                dfs_combined.append(df)
            
            if not dfs_combined:
                return False, "No se encontraron hojas válidas (1-Solicitudes, 2-Incidentes, 3-Tareas)", None
            
            # Combinar todos los dataframes
            df = pd.concat(dfs_combined, ignore_index=True)
            logger_excel.info(f"Total de registros combinados: {len(df)}")
            
            # Validar tipos de datos
            errores = []
            
            # Validar Fecha
            try:
                df['Fecha'] = pd.to_datetime(df['Fecha'])
            except Exception as e:
                errores.append(f"Formato de fecha inválido: {str(e)}")
            
            # Validar Horas Aprobadas
            try:
                df['Horas Aprobadas'] = pd.to_numeric(df['Horas Aprobadas'], errors='coerce')
                if df['Horas Aprobadas'].isna().any():
                    raise ValueError("Valores no numéricos en Horas Aprobadas")
            except Exception as e:
                errores.append(f"Error en Horas Aprobadas: {str(e)}")
            
            # Validar Horas Reales
            try:
                df['Horas Reales'] = pd.to_numeric(df['Horas Reales'], errors='coerce')
                if df['Horas Reales'].isna().any():
                    raise ValueError("Valores no numéricos en Horas Reales")
            except Exception as e:
                errores.append(f"Error en Horas Reales: {str(e)}")
            
            if errores:
                mensaje = "; ".join(errores)
                logger_excel.error(mensaje)
                return False, mensaje, None
            
            # Limpiar datos
            df = df.dropna(subset=['WO', 'Usuario Asignado', 'Grupo'])
            df['WO'] = df['WO'].astype(str).str.strip()
            df['Usuario Asignado'] = df['Usuario Asignado'].astype(str).str.strip()
            df['Grupo'] = df['Grupo'].astype(str).str.strip()
            
            logger_excel.info(f"Validación exitosa. {len(df)} registros para procesar")
            return True, None, df
            
        except Exception as e:
            mensaje = f"Error al procesar archivo: {str(e)}"
            logger_excel.error(mensaje)
            return False, mensaje, None
        finally:
            # Cerrar el archivo Excel
            if excel_file is not None:
                try:
                    excel_file.close()
                except:
                    pass
    
    @staticmethod
    def prepare_for_database(df):
        """
        Prepara el dataframe para insertar en la base de datos
        
        Returns:
            list: Lista de diccionarios listos para insertar
        """
        registros = []
        
        for idx, row in df.iterrows():
            try:
                registro = {
                    'wo': str(row['WO']).strip(),
                    'usuario_asignado': str(row['Usuario Asignado']).strip(),
                    'fecha': pd.to_datetime(row['Fecha']).date(),
                    'horas_aprobadas': float(row['Horas Aprobadas']),
                    'horas_reales': float(row['Horas Reales']),
                    'grupo': str(row['Grupo']).strip(),
                    'tipo': str(row['Tipo']).strip() if 'Tipo' in row else 'Solicitud',
                    'fecha_carga': datetime.utcnow()
                }
                registros.append(registro)
            except Exception as e:
                logger_excel.warning(f"Error en fila {idx}: {str(e)}")
                continue
        
        return registros
    
    @staticmethod
    def get_file_stats(df):
        """Obtiene estadísticas del archivo cargado"""
        return {
            'total_registros': len(df),
            'usuarios_unicos': df['Usuario Asignado'].nunique(),
            'grupos_unicos': df['Grupo'].nunique(),
            'fecha_minima': df['Fecha'].min().strftime('%Y-%m-%d'),
            'fecha_maxima': df['Fecha'].max().strftime('%Y-%m-%d'),
            'total_horas_aprobadas': float(df['Horas Aprobadas'].sum()),
            'total_horas_reales': float(df['Horas Reales'].sum()),
        }
