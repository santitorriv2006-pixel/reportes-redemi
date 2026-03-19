# 📊 Carga Flexible de Excel - Análisis Automático

## ✨ Nuevas Características

Tu sistema ahora puede **analizar automáticamente cualquier archivo Excel**, sin importar:

### 🔍 Lo que el sistema busca automáticamente:

1. **WO (Orden de Trabajo)**
   - Variaciones aceptadas: WO, ORDEN TRABAJO, OT, TICKET

2. **Usuario Asignado**
   - Variaciones: Usuario, Usuario Asignado, Responsable, Técnico, Assignee

3. **Fecha**
   - Varios formatos: DD/MM/YYYY, YYYY-MM-DD, etc.

4. **Horas Aprobadas**
   - Variaciones: Horas Aprob, H. Aprobadas, Approved Hours

5. **Horas Reales**
   - Variaciones: Horas Real, H. Reales, Actual Hours, Horas Trabajo

6. **Grupo**
   - Variaciones: Equipo, Team, Departamento, Área

---

## 📝 Ejemplos de Archivos Compatibles

### ✅ Formato 1: Estándar HITSS
```
WO | Usuario Asignado | Fecha | Horas Aprobadas | Horas Reales | Grupo
WO001 | Juan Perez | 2026-03-18 | 8.0 | 8.5 | G-CONTRATISTAS
```

### ✅ Formato 2: Simplificado
```
Orden Trabajo | Responsable | Fecha Inicio | H. Aprob | H. Real | Equipo
OT-2026-001 | Maria Lopez | 18/03/2026 | 6 | 6.2 | Soporte
```

### ✅ Formato 3: Técnico
```
Ticket | Técnico | Fecha | Aprobadas | Reales | Departamento
T-123 | Carlos | 2026-03-18 | 4 | 3.9 | Desarrollo
```

### ✅ Formato 4: CUALQUIER OTRO
El sistema buscará las columnas requeridas sin importar:
- El orden de las columnas
- Los nombres exactos
- Las variaciones de nombres
- Mayúsculas/minúsculas
- Espacios adicionales

---

## 🚀 Cómo Funciona el Análisis

### Búsqueda en 3 Niveles:

1. **Coincidencia Exacta** (100% confianza)
   - Busca nombres exactos ignorando mayúsculas

2. **Coincidencia Parcial** (90% confianza)
   - Si el nombre contiene palabras clave

3. **Similitud Difusa** (70% confianza)
   - Usa algoritmo de similitud para nombres parcialmente diferentes

---

## 📋 Requisitos Mínimos

Los datos deben contener:
- ✅ Identificador de trabajo (WO, OT, Ticket, etc.)
- ✅ Persona responsable (Usuario, Técnico, etc.)
- ✅ Fecha (cualquier formato reconocible)
- ✅ Horas aprobadas (número)
- ✅ Horas reales (número)
- ✅ Grupo/Equipo

---

## ⚠️ Formato de Fecha

El sistema acepta automáticamente:
- **DD/MM/YYYY** - 18/03/2026
- **YYYY-MM-DD** - 2026-03-18
- **MM/DD/YYYY** - 03/18/2026
- **Texto normalizado** - "Marzo 18, 2026"

---

## 📊 Procesamiento de Hojas

Si tu archivo tiene múltiples hojas:
- ✅ Se procesan **todas las hojas** automáticamente
- ✅ Se combinan en un solo reporte
- ✅ Se detecta el tipo según el nombre:
  - "Solicitudes" → Tipo: Solicitud
  - "Incidentes" → Tipo: Incidente
  - "Tareas" → Tipo: Tarea
  - Otras → Tipo: Solicitud (por defecto)

---

## 🎯 Ejemplo de Carga

### Tu archivo Excel:
```
┌─────────────────────────────────────┐
│ REPORTE_EPM_MARZO_2026.xlsx        │
├─────────────────────────────────────┤
│ Hoja 1: "Solicitudes"              │
│ - Columnas en cualquier orden       │
│ - Nombres variados                  │
│                                     │
│ Hoja 2: "Incidentes"               │
│ - Diferentes formatos               │
│                                     │
│ Hoja 3: "Tareas"                   │
│ - Cualquier variación               │
└─────────────────────────────────────┘
```

### Sistema detecta automáticamente:
```
✅ Encontrando hojas...
✅ Analizando columnas...
✅ Mapeando campos requeridos...
✅ Validando datos...
✅ Combinando registros...
✅ 847 registros cargados exitosamente
```

---

## 📱 Interfaz de Upload

En la opción **"Cargar Reportes"**:
1. Haz clic en el selector de archivo
2. Selecciona tu archivo Excel (cualquier formato)
3. El sistema analiza automáticamente
4. Muestra un resumen de lo encontrado
5. Carga los datos en la base de datos

---

## ✨ Ventajas

✅ **Flexible** - Acepta cualquier formato de Excel  
✅ **Inteligente** - Busca columnas automáticamente  
✅ **Tolerante** - Perdona variaciones en nombres  
✅ **Transparente** - Muestra qué encontró y mapeo  
✅ **Robusto** - Maneja múltiples hojas  
✅ **Rápido** - Procesa miles de registros  

---

## 🐛 Si Algo No Funciona

### El sistema rechaza tu archivo si:
- ❌ Falta la columna de identificador (WO, OT, etc.)
- ❌ Falta la columna de usuario
- ❌ Falta la columna de grupo
- ❌ Faltan horas aprobadas o reales
- ❌ Falta la fecha

### Soluciones:
1. **Verifica que tu archivo tenga estas 6 columnas** (con cualquier nombre similar)
2. **Revisa los formatos de fecha y números**
3. **Elimina espacios en blanco al principio de celdas**
4. **Usa Excel 2007+ (.xlsx)**, no versiones antiguas

---

## 📞 Soporte

Si tienes dudas sobre qué nombre darle a tus columnas:
- Consulta la sección "Variaciones aceptadas" arriba
- O usa directamente los nombres estándar: WO, Usuario Asignado, Fecha, Horas Aprobadas, Horas Reales, Grupo
