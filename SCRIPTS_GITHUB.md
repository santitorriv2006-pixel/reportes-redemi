# 📤 Scripts de Subida a GitHub

## 🚀 Opciones Disponibles

Tienes 3 scripts para subir tu proyecto a GitHub de forma automática:

---

## ✨ Opción 1: PowerShell (Recomendado - Mejor formato)

### Uso Básico:
```powershell
.\push.ps1
```

### Con Mensaje Personalizado:
```powershell
.\push.ps1 "feat: agregar nueva funcionalidad"
.\push.ps1 "fix: corregir bug en reportes"
.\push.ps1 "docs: actualizar documentación"
```

### Ejemplo Completo:
```powershell
# Subir con mensaje descriptivo
.\push.ps1 "feat: carga flexible de Excel con análisis automático"

# Salida esperada:
# ✅ Cambios agregados
# ✅ Commit creado
# ✅ Push completado
# 🎉 Todos los cambios están en GitHub
```

---

## ✨ Opción 2: Batch (Windows .bat)

### Uso Básico:
```cmd
push.bat
```

### Con Mensaje Personalizado:
```cmd
push.bat "feat: agregar nueva funcionalidad"
push.bat "fix: corregir bug en reportes"
```

### Ejemplo:
```cmd
push.bat "feat: mejoras en UI de botones"
```

---

## ✨ Opción 3: Python

### Uso Básico:
```powershell
python push_to_github.py
```

### Con Mensaje Personalizado:
```powershell
python push_to_github.py "feat: nueva característica"
python push_to_github.py "fix: corregir error"
```

### Ejemplo:
```powershell
python push_to_github.py "docs: actualizar README"
```

---

## 📋 Qué Hacen los Scripts

Los scripts automatizan estos pasos:

1. **Verifican cambios** (`git status`)
2. **Agregan archivos** (`git add -A`)
3. **Crean commit** (`git commit -m "mensaje"`)
4. **Suben a GitHub** (`git push origin main`)

---

## 🎯 Mensajes de Commit Recomendados

### Tipos de Cambios:

- **feat:** Nueva funcionalidad
  ```
  feat: agregar descarga de reportes filtrados
  ```

- **fix:** Corrección de bug
  ```
  fix: corregir error en carga de Excel
  ```

- **docs:** Documentación
  ```
  docs: actualizar guía de compilación
  ```

- **style:** Cambios de formato/CSS
  ```
  style: mejorar colores de botones
  ```

- **refactor:** Reorganización de código
  ```
  refactor: optimizar búsqueda de columnas
  ```

- **perf:** Mejoras de rendimiento
  ```
  perf: acelerar procesamiento de Excel
  ```

- **chore:** Cambios general sin código
  ```
  chore: actualizar dependencias
  ```

---

## ✅ Ejemplo de Uso Completo

### Escenario: Has hecho cambios y quieres subirlos

```powershell
# 1. Opción: Usar PowerShell
.\push.ps1 "feat: agregar validación de datos"

# 2. O usar Batch
push.bat "feat: agregar validación de datos"

# 3. O usar Python
python push_to_github.py "feat: agregar validación de datos"
```

**Output esperado:**
```
============================================================
 📤 SUBIDOR DE PROYECTOS A GITHUB
============================================================

📝 Mensaje del commit: 'feat: agregar validación de datos'

📊 Verificando cambios...
✓ Cambios detectados:
 M app/templates/reportes.html
 M app/services/excel_service.py

¿Deseas continuar? (S/N): s

============================================================
📌 Paso 1: Agregando cambios
============================================================
✅ Cambios agregados

============================================================
📌 Paso 2: Creando commit
============================================================
✅ Commit creado

============================================================
📌 Paso 3: Subiendo a GitHub
============================================================
✅ Push completado

============================================================
✅ ¡PROYECTO SUBIDO A GITHUB EXITOSAMENTE!
============================================================

📌 Último commit:
8d525cd feat: carga flexible de Excel con análisis automático

🎉 Todos los cambios están en GitHub
```

---

## 🐛 Si Algo Sale Mal

### Error: "No tienes permiso"
```
❌ fatal: Authentication failed
```
**Solución:**
1. Verifica tu token de GitHub
2. Usa: `git config --global user.name "tu usuario"`
3. Usa: `git config --global user.email "tu@email.com"`

### Error: "Rama no existe"
```
❌ fatal: The current branch main does not have upstream tracking
```
**Solución:**
```powershell
git push -u origin main
.\push.ps1  # Después usa el script
```

### Error: "Hay conflictos"
**Solución:**
```powershell
git pull origin main
# Resuelve conflictos manualmente
.\push.ps1
```

---

## 💡 Consejos

✅ **Usa mensajes descriptivos** - facilita el seguimiento  
✅ **Sube cambios regularmente** - no dejes acumular demasiados  
✅ **Verifica los cambios** - revisa qué se sube  
✅ **Usa ramas** - para cambios grandes o experimentales  

---

## 🔗 Configuración GitHub

### Primera vez que usas GitHub en esta máquina:

```powershell
# Configura tu usuario
git config --global user.name "Tu Nombre"
git config --global user.email "tu@email.com"

# Genera token (en GitHub.com)
# Settings → Developer settings → Personal access tokens → Generate new token
# Copia el token y guárdalo

# Cuando Git pida contraseña, usa el token
```

---

## 📞 Resumen Rápido

| Acción | Comando |
|--------|---------|
| Subir con mensaje | `.\push.ps1 "tu mensaje"` |
| Ver cambios | `git status` |
| Ver últimos commits | `git log --oneline` |
| Ver rama actual | `git branch` |

---

¡Elige el script que más te guste y úsalo! 🚀
