# Ejemplo de Archivo Excel - Sistema de Reportes Empresariales

Este documento muestra exactamente cómo debe ser tu archivo Excel para que funcione correctamente.

## Estructura de Columnas

Tu archivo DEBE tener exactamente estas 6 columnas (en cualquier orden):

| WO | Usuario Asignado | Fecha | Horas Aprobadas | Horas Reales | Grupo |
|----|------------------|-------|-----------------|--------------|-------|
| WO-1001 | Juan Pérez | 2026-02-20 | 8.0 | 7.5 | Desarrollo |
| WO-1002 | María García | 2026-02-20 | 8.0 | 8.5 | QA |
| WO-1003 | Carlos López | 2026-02-21 | 8.0 | 9.0 | DevOps |
| WO-1004 | Juan Pérez | 2026-02-21 | 7.0 | 6.5 | Desarrollo |
| WO-1005 | Ana Martínez | 2026-02-22 | 8.0 | 8.2 | Análisis |

## Especificaciones

### Campo: WO (Orden de Trabajo)
- **Tipo**: Texto
- **Formato**: WO-XXXX (ej: WO-1001, WO-2500)
- **Obligatorio**: Sí
- **Ejemplos válidos**: WO-1001, WO-2000, WO-ABC123

### Campo: Usuario Asignado
- **Tipo**: Texto
- **Formato**: Nombre completo (ej: Juan Pérez)
- **Obligatorio**: Sí
- **Importante**: Mantén consistencia (no mezcles "Juan Pérez", "J. Pérez", etc.)
- **Ejemplos válidos**: Juan Pérez, María García, José Rodríguez

### Campo: Fecha
- **Tipo**: Fecha
- **Formato**: YYYY-MM-DD (ej: 2026-02-20)
- **Obligatorio**: Sí
- **❌ INCORRECTO**: 20/02/2026, 02-20-2026, 20-Feb-2026
- **✅ CORRECTO**: 2026-02-20

### Campo: Horas Aprobadas
- **Tipo**: Número decimal
- **Formato**: Cualquier número decimal (ej: 8.0, 7.5, 8.25)
- **Obligatorio**: Sí
- **Rango recomendado**: 0 a 24
- **Ejemplos válidos**: 8, 8.0, 8.5, 7.25

### Campo: Horas Reales
- **Tipo**: Número decimal
- **Formato**: Cualquier número decimal (ej: 7.5, 8.25, 9.0)
- **Obligatorio**: Sí
- **Rango recomendado**: 0 a 24
- **Ejemplos válidos**: 8, 8.0, 8.5, 9.25

### Campo: Grupo
- **Tipo**: Texto
- **Formato**: Nombre del grupo (ej: Desarrollo, QA, DevOps)
- **Obligatorio**: Sí
- **Importante**: Mantén consistencia en los nombres
- **Ejemplos válidos**: Desarrollo, QA, DevOps, Análisis, Diseño

## Ejemplo Completo

```
WO | Usuario Asignado | Fecha | Horas Aprobadas | Horas Reales | Grupo
---|---|---|---|---|---
WO-1001 | Juan Pérez | 2026-02-20 | 8.0 | 7.5 | Desarrollo
WO-1002 | María García | 2026-02-20 | 8.0 | 8.5 | QA
WO-1003 | Carlos López | 2026-02-21 | 8.0 | 9.0 | DevOps
WO-1004 | Juan Pérez | 2026-02-21 | 7.0 | 6.5 | Desarrollo
WO-1005 | Ana Martínez | 2026-02-22 | 8.0 | 8.2 | Análisis
WO-1006 | María García | 2026-02-22 | 8.0 | 8.3 | QA
WO-1007 | José Rodríguez | 2026-02-23 | 8.0 | 8.1 | Desarrollo
WO-1008 | Laura Fernández | 2026-02-23 | 8.0 | 7.9 | Diseño
```

## En Excel

Cuando abras este archivo en Excel, vería:

```
Fila 1 (Encabezados):
| WO | Usuario Asignado | Fecha | Horas Aprobadas | Horas Reales | Grupo |

Fila 2:
| WO-1001 | Juan Pérez | 2026-02-20 | 8 | 7.5 | Desarrollo |

Fila 3:
| WO-1002 | María García | 2026-02-20 | 8 | 8.5 | QA |

... más filas ...
```

## ✅ Checklist Antes de Cargar

- [ ] Archivo tiene extensión .xlsx
- [ ] Tiene exactamente 6 columnas
- [ ] Los nombres de columnas son exactos: WO, Usuario Asignado, Fecha, Horas Aprobadas, Horas Reales, Grupo
- [ ] Las fechas están en formato YYYY-MM-DD
- [ ] Horas Aprobadas y Horas Reales son números
- [ ] No hay espacios extra en los nombres de usuarios o grupos
- [ ] Todos los campos requeridos tienen valores (no hay celdas vacías)
- [ ] El archivo no está vacío (al menos 1 fila de datos)
- [ ] El archivo pesa menos de 50MB

## 🚫 Errores Comunes

### Error: "Columnas faltantes: Usuario Asignado"

**Causa**: La columna se llama "Usuario" en lugar de "Usuario Asignado"

**Solución**: Renombra la columna a exactamente "Usuario Asignado"

### Error: "Formato de fecha inválido"

**Causa**: Las fechas están en formato 20/02/2026 en lugar de 2026-02-20

**Solución**: Cambia el formato a YYYY-MM-DD

### Error: "Valores no numéricos en Horas Aprobadas"

**Causa**: El campo contiene "8 horas" en lugar de solo "8"

**Solución**: Asegúrate que contenga solo números

### Error: "Valores no numéricos en Horas Reales"

**Causa**: Mezcla de números y texto

**Solución**: Convierte a formato numérico

## 📋 Cómo Crear tu Archivo

### Opción 1: Desde Excel
1. Abre Excel
2. Crea 6 columnas con los nombres exactos
3. Rellena los datos
4. Guarda como .xlsx

### Opción 2: Desde Google Sheets
1. Crea una hoja en Google Sheets
2. Agrega los datos
3. Descarga como .xlsx

### Opción 3: Desde CSV
1. Crea archivo CSV con los datos
2. Abre en Excel
3. Guarda como .xlsx

## 💡 Consejos

- **Consistencia de nombres**: "Juan Pérez" siempre igual, no "juan perez" o "JUAN PÉREZ"
- **Fechas**: Siempre YYYY-MM-DD. Excel puede ayudarte con esto.
- **Números**: Sin símbolos de moneda ni espacios. Usa punto (.) como decimal.
- **Grupos**: Crea una lista estándar de grupos (Desarrollo, QA, etc.)

## 📞 ¿Necesitas ayuda?

Si tu archivo no carga:
1. Verifica la estructura con esta guía
2. Revisa los mensajes de error
3. Consulta la sección "GUIA_DE_USO.md"

---

**Última actualización**: Febrero 2026
