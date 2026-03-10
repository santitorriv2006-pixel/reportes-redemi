from datetime import datetime, timedelta
from sqlalchemy import Index
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import secrets

# Crear instancia de SQLAlchemy aquí para evitar imports circulares
db = SQLAlchemy()


class Usuario(UserMixin, db.Model):
    """
    Modelo para usuarios del sistema
    """
    __tablename__ = 'usuarios'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    rol = db.Column(db.String(50), default='usuario')  # usuario, admin
    activo = db.Column(db.Boolean, default=True)
    fecha_registro = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    ultimo_login = db.Column(db.DateTime, nullable=True)
    
    def __repr__(self):
        return f'<Usuario {self.email}>'
    
    def set_password(self, password):
        """Establece la contraseña hasheada"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Verifica si la contraseña coincide"""
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'email': self.email,
            'rol': self.rol,
            'activo': self.activo,
            'fecha_registro': self.fecha_registro.isoformat()
        }


class CodigoVerificacion(db.Model):
    """
    Modelo para almacenar códigos de verificación temporal para 2FA
    """
    __tablename__ = 'codigos_verificacion'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(120), nullable=False, index=True)
    codigo = db.Column(db.String(6), nullable=False)
    intentos = db.Column(db.Integer, default=0)
    fecha_creacion = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, index=True)
    fecha_expiracion = db.Column(db.DateTime, nullable=False)
    usado = db.Column(db.Boolean, default=False)
    
    def __repr__(self):
        return f'<CodigoVerificacion {self.email}>'
    
    @staticmethod
    def generar_codigo():
        """Genera un código de 6 dígitos"""
        return str(secrets.randbelow(1000000)).zfill(6)
    
    def est_expirado(self):
        """Verifica si el código ha expirado"""
        return datetime.utcnow() > self.fecha_expiracion
    
    def es_valido(self):
        """Verifica si el código es válido"""
        return not self.usado and not self.est_expirado()


class Reporte(db.Model):
    """
    Modelo para almacenar reportes empresariales cargados desde Excel
    """
    __tablename__ = 'reportes'
    
    # Campos principales
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    wo = db.Column(db.String(50), nullable=False, index=True)
    usuario_asignado = db.Column(db.String(120), nullable=False, index=True)
    fecha = db.Column(db.Date, nullable=False, index=True)
    horas_aprobadas = db.Column(db.Float, nullable=False)
    horas_reales = db.Column(db.Float, nullable=False)
    grupo = db.Column(db.String(100), nullable=False, index=True)
    status = db.Column(db.String(100), nullable=True, index=True, default='Pending')
    tipo = db.Column(db.String(50), nullable=True, index=True, default='Solicitud')
    fecha_carga = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    # Índices compuestos para optimización de búsquedas
    __table_args__ = (
        Index('idx_usuario_fecha', 'usuario_asignado', 'fecha'),
        Index('idx_usuario_grupo', 'usuario_asignado', 'grupo'),
        Index('idx_grupo_fecha', 'grupo', 'fecha'),
        Index('idx_fecha_usuario', 'fecha', 'usuario_asignado'),
        Index('idx_tipo', 'tipo'),
    )
    
    def __repr__(self):
        return f'<Reporte {self.wo} - {self.usuario_asignado}>'
    
    def to_dict(self):
        """Convierte el objeto a diccionario"""
        return {
            'id': self.id,
            'wo': self.wo,
            'usuario_asignado': self.usuario_asignado,
            'fecha': self.fecha.isoformat() if self.fecha else None,
            'horas_aprobadas': self.horas_aprobadas,
            'horas_reales': self.horas_reales,
            'grupo': self.grupo,
            'status': self.status,
            'tipo': self.tipo,
            'fecha_carga': self.fecha_carga.isoformat() if self.fecha_carga else None,
            'diferencia': round(self.horas_reales - self.horas_aprobadas, 2)
        }
    
    def calcular_diferencia(self):
        """Calcula la diferencia entre horas reales y aprobadas"""
        return round(self.horas_reales - self.horas_aprobadas, 2)


class HistorialCarga(db.Model):
    """
    Modelo para registrar el histórico de cargas de archivos
    """
    __tablename__ = 'historial_carga'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre_archivo = db.Column(db.String(255), nullable=False)
    cantidad_registros = db.Column(db.Integer, nullable=False)
    registros_procesados = db.Column(db.Integer, nullable=False)
    registros_error = db.Column(db.Integer, default=0)
    fecha_carga = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, index=True)
    estado = db.Column(db.String(50), default='exitoso')  # exitoso, parcial, error
    mensaje_error = db.Column(db.Text, nullable=True)
    usuario_carga = db.Column(db.String(120), nullable=True)
    
    def __repr__(self):
        return f'<HistorialCarga {self.nombre_archivo} - {self.estado}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'nombre_archivo': self.nombre_archivo,
            'cantidad_registros': self.cantidad_registros,
            'registros_procesados': self.registros_procesados,
            'registros_error': self.registros_error,
            'fecha_carga': self.fecha_carga.isoformat(),
            'estado': self.estado,
            'porcentaje_exito': round(
                (self.registros_procesados / self.cantidad_registros * 100) 
                if self.cantidad_registros > 0 else 0, 2
            )
        }
