#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para subir el proyecto a GitHub de forma automatizada
Uso: python push_to_github.py "mensaje del commit"
"""

import subprocess
import sys
import os
from datetime import datetime

def ejecutar_comando(comando, descripcion):
    """Ejecuta un comando shell y retorna si fue exitoso"""
    print(f"\n{'='*60}")
    print(f"📌 {descripcion}")
    print(f"{'='*60}")
    print(f"Ejecutando: {comando}\n")
    
    try:
        resultado = subprocess.run(
            comando,
            shell=True,
            cwd=os.getcwd(),
            capture_output=False,
            text=True
        )
        
        if resultado.returncode == 0:
            print(f"✅ {descripcion} - Completado")
            return True
        else:
            print(f"❌ {descripcion} - Error")
            return False
    except Exception as e:
        print(f"❌ Error ejecutando comando: {str(e)}")
        return False

def obtener_status_git():
    """Obtiene el estado del repositorio git"""
    try:
        resultado = subprocess.run(
            "git status --porcelain",
            shell=True,
            capture_output=True,
            text=True
        )
        return resultado.stdout
    except:
        return None

def main():
    """Función principal"""
    
    print("\n" + "="*60)
    print(" 📤 SUBIDOR DE PROYECTOS A GITHUB")
    print("="*60 + "\n")
    
    # Obtener mensaje del commit
    if len(sys.argv) > 1:
        mensaje_commit = " ".join(sys.argv[1:])
    else:
        # Mensaje por defecto con fecha
        fecha = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        mensaje_commit = f"actualizaciones - {fecha}"
    
    print(f"📝 Mensaje del commit: '{mensaje_commit}'")
    
    # Verificar estado
    print("\n📊 Verificando estado del repositorio...")
    status = obtener_status_git()
    
    if status:
        print(f"✓ Cambios detectados:")
        print(status)
    else:
        print("⚠️ No hay cambios o no es un repositorio git")
        sys.exit(1)
    
    # Confirmación
    respuesta = input("\n¿Deseas continuar? (s/n): ").strip().lower()
    if respuesta != 's' and respuesta != 'si':
        print("❌ Operación cancelada")
        sys.exit(0)
    
    # Paso 1: Agregar cambios
    if not ejecutar_comando("git add -A", "Añadiendo cambios"):
        print("❌ No se pudieron agregar los cambios")
        sys.exit(1)
    
    # Paso 2: Crear commit
    comando_commit = f'git commit -m "{mensaje_commit}"'
    if not ejecutar_comando(comando_commit, "Creando commit"):
        print("⚠️ Posiblemente no hay cambios nuevos")
    
    # Paso 3: Push
    if not ejecutar_comando("git push origin main", "Subiendo a GitHub"):
        print("\n❌ Error al subir a GitHub")
        print("💡 Intenta:")
        print("   1. Verifica tu conexión a internet")
        print("   2. Verifica tu acceso a GitHub (token/contraseña)")
        print("   3. Ejecuta: git push origin main")
        sys.exit(1)
    
    # Verificar resultado
    print("\n" + "="*60)
    print("✅ ¡PROYECTO SUBIDO A GITHUB EXITOSAMENTE!")
    print("="*60)
    
    # Mostrar información
    try:
        resultado = subprocess.run(
            "git log --oneline -1",
            shell=True,
            capture_output=True,
            text=True
        )
        print(f"\n📌 Último commit: {resultado.stdout.strip()}")
    except:
        pass
    
    print("\n🎉 Todos los cambios están en GitHub\n")

if __name__ == '__main__':
    main()
