# Guía de Uso - Sistema de Reportes Empresariales

## 🎯 Introducción

Este documento proporciona una guía paso a paso para usar el Sistema de Gestión de Reportes Empresariales.

## 📊 1. Interfaz Principal

Al acceder a la aplicación en **http://localhost:5000**, verás:

### Dashboard Principal
- **Tarjetas de Estadísticas**: Total de registros, usuarios, grupos y horas aprobadas
- **Accesos Rápidos**: Botones para ir a Cargar, Reportes y Dashboard
- **Información del Sistema**: Características y requisitos

---

## 📤 2. Cargar Archivo Excel

### Paso a Paso

1. **Navega a**: Menú superior → "Cargar Excel" o click en tarjeta "Cargar Excel"

2. **Prepara tu archivo**:
   - Formato: Excel (.xlsx)
   - Tamaño máximo: 50MB
   - Columnas obligatorias:
     - **WO**: Número de orden (ej: WO-1001)
     - **Usuario Asignado**: Nombre del usuario (ej: Juan Pérez)
     - **Fecha**: En formato YYYY-MM-DD (ej: 2026-02-20)
     - **Horas Aprobadas**: Número decimal (ej: 8.5)
     - **Horas Reales**: Número decimal (ej: 7.5)
     - **Grupo**: Grupo de trabajo (ej: Desarrollo)

3. **Carga el archivo**:
   - Click en el área de carga o arrastra tu archivo
   - Espera a que se procese

4. **Resultado**:
   - ✅ **Éxito**: Verás estadísticas (registros insertados, usuarios, horas)
   - ❌ **Error**: Se mostrará un mensaje con la causa

### Ejemplo de Archivo Correcto

| WO | Usuario Asignado | Fecha | Horas Aprobadas | Horas Reales | Grupo |
|----|------------------|-------|-----------------|--------------|-------|
| WO-1001 | Juan Pérez | 2026-02-20 | 8.0 | 7.5 | Desarrollo |
| WO-1002 | María García | 2026-02-20 | 8.0 | 8.5 | QA |
| WO-1003 | Carlos López | 2026-02-21 | 8.0 | 9.0 | DevOps |

### Validación Automática

El sistema valida automáticamente:
- ✓ Que todas las columnas existan
- ✓ Que los datos sean del tipo correcto (números, fechas)
- ✓ Que no haya espacios extras
- ✓ Que el archivo no esté vacío

---

## 🔍 3. Ver Reportes

### Navegar a Reportes

1. Click en "Reportes" en el menú o en la tarjeta

### Interfaz de Reportes

#### Filtros (Parte Superior)

**Campo de Búsqueda por Usuario**:
- Escribe el nombre del usuario
- Búsqueda parcial (ej: escribe "Juan" para encontrar "Juan Pérez")
- Case-insensitive (mayúsculas/minúsculas no importan)

**Rango de Fechas**:
- **Fecha Inicio**: Primer día del período
- **Fecha Fin**: Último día del período

**Filtro por Grupo**:
- Dropdown con todos los grupos disponibles

**Botones**:
- **Buscar**: Aplica los filtros
- **Limpiar**: Elimina todos los filtros

#### Tabla de Resultados

La tabla muestra:
| Campo | Descripción |
|-------|-------------|
| WO | Número de orden |
| Usuario | Usuario asignado |
| Fecha | Fecha del reporte |
| Horas Aprobadas | Horas aprobadas (número) |
| Horas Reales | Horas trabajadas |
| Diferencia | Reales - Aprobadas |
| Grupo | Grupo de trabajo |

#### Resumen de Totales

Debajo de los filtros:
- **Total Horas Aprobadas**: Suma de todas las horas aprobadas
- **Total Horas Reales**: Suma de horas reales
- **Diferencia**: Diferencia total
- **Total WO**: Cantidad de órdenes

#### Paginación

- Navega entre páginas al final de la tabla
- 20 registros por página

### Ejemplo de Uso

**Quiero ver todos los reportes de Juan Pérez en febrero de 2026**:

1. En "Búsqueda por Usuario" escribe: `Juan Pérez`
2. En "Fecha Inicio" selecciona: `2026-02-01`
3. En "Fecha Fin" selecciona: `2026-02-28`
4. Click en **Buscar**

---

## 📥 4. Descargar Reportes

### Descarga Individual (Por Usuario)

**Requisito**: Primero debes buscar/seleccionar un usuario

1. En la página de Reportes, busca un usuario
2. Se habilitará el botón **"Descargar Usuario"**
3. Click en el botón
4. Se descargará un archivo `reporte_Juan Perez_20260226.xlsx`

El archivo contiene:
- Todos los reportes del usuario (con filtros aplicados)
- Fila de totales con sumas
- Formatos de tabla limpios

### Descarga Global

1. En cualquier momento en la página de Reportes
2. Click en **"Descargar Global"**
3. Se descargará `reporte_global_20260226.xlsx`

El archivo contiene:
- **Hoja 1 "Detalle"**: Todos los registros (ordenados por usuario y fecha)
- **Hoja 2 "Resumen Usuario"**: Totales por cada usuario
- Fila de totales generales

### Aplicar Filtros a Descargas

Antes de descargar, puedes aplicar filtros:
- Fechas específicas
- Grupo específico
- Usuario específico

El archivo descargado respetará los filtros aplicados.

---

## 📊 5. Dashboard

### Acceder al Dashboard

1. Click en "Dashboard" en el menú
2. O click en la tarjeta "Dashboard" de la página principal

### Modo Global

**Por defecto, ves el Dashboard Global** que contiene:

1. **Gráfico: Horas por Mes** (líneas)
   - Horas aprobadas (verde)
   - Horas reales (rojo)
   - Útil para ver tendencias mensuales

2. **Gráfico: Horas por Grupo** (barras)
   - Comparación de grupo de trabajo
   - Aprobadas vs Reales

3. **Gráfico: Top 10 Usuarios** (barras)
   - Los usuarios con más horas aprobadas

4. **Comparación General** (donut)
   - Total de horas aprobadas vs reales
   - Proporciones visuales

### Cambiar a Modo Usuario

1. Selecciona el radio button **"Vista Usuario"**
2. Aparecerán filtros:
   - Dropdown para seleccionar usuario
   - Fecha inicio (opcional)
   - Fecha fin (opcional)
3. Click en **"Cargar"**

El dashboard mostrará:
- Horas aprobadas por mes del usuario
- Horas por grupo (del usuario)
- Comparación horas aprobadas vs reales del usuario

### Interpretar Gráficos

**Gráfico de Líneas**:
- Eje X: Meses
- Eje Y: Horas
- Verde: Horas aprobadas
- Rojo: Horas reales

**Gráfico de Barras**:
- Eje Y: Grupo o Usuario
- Eje X: Horas
- Verde claro: Aprobadas
- Rojo: Reales

**Gráfico Donut**:
- Proporciona idea rápida de la distribución
- Hovering muestra los valores exactos

---

## 📧 6. Reportes Automáticos

El sistema envía reportes automáticamente:

| Hora | Tipo | Contenido |
|------|------|----------|
| 08:00 AM | Resumen Matutino | Datos acumulados del día |
| 02:00 PM | Resumen Vespertino | Actualización con nuevos datos |
| 05:30 PM | Consolidado Final | Resumen completo del día |

### Contenido del Reporte por Correo

Cada correo incluye:
1. **Tabla HTML** con totales por usuario
2. **Archivo Excel** global adjunto
3. **Totales Generales** del período

### Configuración (por administrador)

Editar `.env`:
```env
MAIL_RECIPIENTS=email1@empresa.com,email2@empresa.com
MAIL_USERNAME=tu_email@gmail.com
MAIL_PASSWORD=tu_contraseña_app
```

---

## 🔧 7. Historial de Cargas

### Ver Historial

1. En la página de "Cargar Excel"
2. En el panel derecho "Historial de Cargas"
3. Se muestran las últimas cargas con:
   - Nombre del archivo
   - Cantidad de registros
   - Fecha/hora
   - Estado (✓ exitoso o ⚠ parcial)

---

## ⚠️ 8. Mensajes de Error

### Errores Comunes

| Error | Causa | Solución |
|-------|-------|----------|
| "Columnas faltantes: Usuario Asignado, Horas Aprobadas" | El archivo no tiene esas columnas | Verifica que tu Excel tenga todas las 6 columnas obligatorias |
| "Formato de fecha inválido" | Las fechas no están en YYYY-MM-DD | Cambia el formato: 2026-02-26 (no 26/02/2026) |
| "Valores no numéricos en Horas Aprobadas" | Campo contiene texto | Asegúrate que sean números: 8.5 (no "ocho horas") |
| "Archivo demasiado grande" | Más de 50MB | Comprime el archivo o divide en partes |

### Error 404 - No Encontrado

Accediste a una página que no existe.
**Solución**: Usa el menú de navegación

### Error 500 - Error del Servidor

Algo salió mal en la aplicación.
**Solución**: 
- Contacta al administrador
- Verifica los logs en `logs/app.log`

---

## 💡 9. Tips y Trucos

### Para un Mejor Rendimiento

1. **Limita las descargas**: Si descargas muchos registros, filtra primero por usuario o fecha
2. **Usa paginación**: No intentes cargar 10,000 registros a la vez
3. **Datos limpios**: Asegúrate que los usuarios/grupos tengan nombres consistentes

### Comparación Horas

- **Diferencia Positiva**: Trabajó más de lo aprobado (valor en rojo)
- **Diferencia Negativa**: Trabajó menos de lo aprobado (valor en verde)
- **Iguales**: Hora exacta (diferencia = 0)

### Exportar y Compartir

1. Descarga el Excel
2. Comparte el archivo
3. Los colegas pueden abrir en Excel, Sheets, etc.
4. Puedes usar como backup

---

## 📞 10. Soporte

### ¿Tienes dudas?

- **Problema técnico**: Contacta al equipo de TI
- **Problema con datos**: Revisa el archivo Excel antes de cargar
- **Sugerencia**: Reporta a tu administrador

### Información del Sistema

- **URL**: http://localhost:5000
- **Navegadores soportados**: Chrome, Firefox, Edge
- **Requisitos**: JavaScript habilitado

---

## 📈 Ejemplo Completo de Flujo

### Escenario: Analizar rendimiento de Juan en Febrero

1. **Cargar datos** (si no existen):
   - Ve a "Cargar Excel"
   - Carga archivo con datos de febrero
   - Verifica que se insertaron correctamente

2. **Ver reportes**:
   - Ve a "Reportes"
   - Busca: "Juan"
   - Fecha: 2026-02-01 a 2026-02-28
   - Click "Buscar"

3. **Analizar**:
   - Lee los totales
   - Nota si trabajó más/menos de lo aprobado
   - Descarga para el archivo

4. **Dashboard**:
   - Ve a "Dashboard"
   - Modo Usuario
   - Selecciona "Juan"
   - Observa gráficos de tendencias

5. **Generar reporte**:
   - Descarga individual
   - Comparte con manager
   - Archiva para registro

---

**Última actualización**: Febrero 2026  
**Versión**: 1.0.0
