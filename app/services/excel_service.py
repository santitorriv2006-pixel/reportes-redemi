import pandas as pd
from datetime import datetime
import os
from difflib import get_close_matches
from logger_config import logger_excel
from config import Config

class ExcelProcessingService:
    """
    Servicio para procesar y validar archivos Excel
    """
    
    # Columnas requeridas con variaciones aceptadas
    COLUMNAS_REQUERIDAS = {
        'WO': ['WO', 'wo', 'ORDEN TRABAJO', 'orden trabajo', 'orden_trabajo', 'ot', 'ticket'],
        'Usuario Asignado': ['Usuario Asignado', 'usuario', 'usuario asignado', 'usuario_asignado', 'assignee', 'responsable', 'técnico'],
        'Fecha': ['Fecha', 'fecha', 'date', 'fecha_inicio', 'fecha inicio'],
        'Horas Aprobadas': ['Horas Aprobadas', 'horas aprobadas', 'horas_aprobadas', 'horas aprob', 'h. aprobadas', 'approved hours'],
        'Horas Reales': ['Horas Reales', 'horas reales', 'horas_reales', 'horas real', 'h. reales', 'actual hours', 'horas trabajo'],
        'Grupo': ['Grupo', 'grupo', 'team', 'equipo', 'grupo_trabajo', 'departamento', 'area']
    }
    
    @staticmethod
    def allowed_file(filename):
        """Verifica que el archivo tenga extensión permitida"""
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS
    
    @staticmethod
    def find_column(df_columns, target_column):
        """
        Busca una columna en el dataframe usando fuzzy matching
        
        Args:
            df_columns: Lista de columnas del dataframe
            target_column: Columna que estamos buscando
            
        Returns:
            tuple: (nombre_columna_encontrada, confianza) o (None, 0)
        """
        # Variaciones aceptadas para este campo
        variaciones = ExcelProcessingService.COLUMNAS_REQUERIDAS.get(target_column, [])
        
        # Buscar coincidencia exacta (case-insensitive)
        for col in df_columns:
            col_lower = col.lower().strip()
            for variacion in variaciones:
                if col_lower == variacion.lower():
                    logger_excel.info(f"Columna '{target_column}' encontrada como '{col}'")
                    return col, 1.0
        
        # Buscar coincidencia parcial
        for col in df_columns:
            for variacion in variaciones:
                if variacion.lower() in col.lower() or col.lower() in variacion.lower():
                    logger_excel.info(f"Columna '{target_column}' encontrada parcialmente como '{col}'")
                    return col, 0.9
        
        # Buscar con similitud
        matches = get_close_matches(target_column.lower(), 
                                   [c.lower() for c in df_columns], 
                                   n=1, cutoff=0.6)
        if matches:
            # Encontrar la columna original
            for col in df_columns:
                if col.lower() == matches[0]:
                    logger_excel.warning(f"Columna '{target_column}' encontrada como '{col}' (similitud)")
                    return col, 0.7
        
        logger_excel.warning(f"Columna '{target_column}' NO encontrada en el archivo")
        return None, 0
    
    @staticmethod
    def validate_file(filepath):
        """
        Valida el archivo Excel antes de procesarlo
        Busca automáticamente las columnas requeridas en cualquier hoja
        
        Returns:
            tuple: (es_valido, mensaje_error, datos)
        """
        excel_file = None
        try:
            # Leer el archivo
            excel_file = pd.ExcelFile(filepath)
            logger_excel.info(f"🔍 Analizando archivo con hojas: {excel_file.sheet_names}")
            
            dfs_combined = []
            
            # Procesar cada hoja
            for idx, sheet_name in enumerate(excel_file.sheet_names, 1):
                logger_excel.info(f"\n📄 Procesando hoja {idx}: '{sheet_name}'")
                
                try:
                    df = pd.read_excel(filepath, sheet_name=sheet_name, dtype=str)
                    if df.empty:
                        logger_excel.warning(f"   ⚠️ Hoja vacía")
                        continue
                    
                    logger_excel.info(f"   ✓ {len(df)} filas, columnas: {list(df.columns)}")
                    
                    # Buscar columnas requeridas
                    col_map = {}
                    columnas_faltantes = []
                    
                    for col_requerida in ExcelProcessingService.COLUMNAS_REQUERIDAS.keys():
                        col_encontrada, confianza = ExcelProcessingService.find_column(
                            df.columns, 
                            col_requerida
                        )
                        
                        if col_encontrada:
                            col_map[col_requerida] = col_encontrada
                            logger_excel.info(f"   ✓ {col_requerida} → '{col_encontrada}' (confianza: {confianza:.0%})")
                        else:
                            columnas_faltantes.append(col_requerida)
                            logger_excel.warning(f"   ✗ {col_requerida} - NO ENCONTRADA")
                    
                    # Si falta alguna columna obligatoria, saltar esta hoja
                    if columnas_faltantes:
                        logger_excel.warning(f"   ❌ Hoja rechazada. Faltan: {', '.join(columnas_faltantes)}")
                        continue
                    
                    # Renombrar columnas al formato estándar
                    df = df.rename(columns=col_map)
                    
                    # Determinar el tipo de dato
                    tipo = 'Solicitud'
                    if 'incidente' in sheet_name.lower():
                        tipo = 'Incidente'
                    elif 'tarea' in sheet_name.lower():
                        tipo = 'Tarea'
                    
                    df['Tipo'] = tipo
                    dfs_combined.append(df)
                    logger_excel.info(f"   ✅ Hoja procesada como tipo '{tipo}'")
                    
                except Exception as e:
                    logger_excel.error(f"   ❌ Error procesando hoja '{sheet_name}': {str(e)}")
                    continue
            
            if not dfs_combined:
                return False, "❌ No se encontraron hojas con las columnas requeridas", None
            
            # Combinar todos los dataframes
            df = pd.concat(dfs_combined, ignore_index=True)
            logger_excel.info(f"\n✅ Total de registros válidos: {len(df)}")
            
            # Validar tipos de datos
            errores = []
            
            # Validar Fecha
            try:
                df['Fecha'] = pd.to_datetime(df['Fecha'], errors='raise')
            except Exception as e:
                logger_excel.error(f"Error en formato de fecha: {str(e)}")
                # Intentar diferentes formatos
                try:
                    df['Fecha'] = pd.to_datetime(df['Fecha'], format='%d/%m/%Y', errors='coerce')
                    if df['Fecha'].isna().any():
                        raise ValueError("Fecha inválida después de convertir")
                except:
                    errores.append(f"Formato de fecha inválido")
            
            # Validar Horas Aprobadas
            try:
                df['Horas Aprobadas'] = pd.to_numeric(df['Horas Aprobadas'], errors='coerce')
                if df['Horas Aprobadas'].isna().any():
                    raise ValueError("Valores no numéricos")
            except Exception as e:
                errores.append(f"Error en Horas Aprobadas: {str(e)}")
            
            # Validar Horas Reales
            try:
                df['Horas Reales'] = pd.to_numeric(df['Horas Reales'], errors='coerce')
                if df['Horas Reales'].isna().any():
                    raise ValueError("Valores no numéricos")
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
            
            logger_excel.info(f"✅ Validación exitosa. {len(df)} registros para procesar")
            return True, None, df
            
        except Exception as e:
            mensaje = f"❌ Error al procesar archivo: {str(e)}"
            logger_excel.error(mensaje)
            return False, mensaje, None
        finally:
            # Cerrar el archivo Excel
            if excel_file is not None:
                try:
                    excel_file.close()
                except:
                    pass
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
