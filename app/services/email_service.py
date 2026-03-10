from flask_mail import Mail, Message
from logger_config import logger_email
from config import Config
import os

mail = Mail()

class EmailService:
    """
    Servicio para envío de correos con reportes
    """
    
    @staticmethod
    def init_mail(app):
        """Inicializa extensión de correo con la aplicación"""
        mail.init_app(app)
        return mail
    
    @staticmethod
    def send_email(subject, body, recipients=None, attachment_filename=None, attachment_data=None):
        """
        Envía un correo electrónico
        
        Args:
            subject: Asunto del correo
            body: Cuerpo del correo (HTML)
            recipients: Lista de destinatarios (usa MAIL_RECIPIENTS si no se proporciona)
            attachment_filename: Nombre del archivo adjunto
            attachment_data: BytesIO del archivo adjunto
        
        Returns:
            bool: True si se envía correctamente
        """
        try:
            if not recipients:
                recipients = Config.MAIL_RECIPIENTS
            
            # Convertir string a lista si es necesario
            if isinstance(recipients, str):
                recipients = [recipients]
            
            # Asegurar que subject y body son UTF-8
            if isinstance(subject, bytes):
                subject = subject.decode('utf-8')
            if isinstance(body, bytes):
                body = body.decode('utf-8')
            
            msg = Message(
                subject=subject,
                recipients=recipients,
                html=body,
                charset='utf-8',
                sender=Config.MAIL_DEFAULT_SENDER
            )
            
            # Adjuntar archivo si se proporciona
            if attachment_filename and attachment_data:
                attachment_data.seek(0)
                msg.attach(
                    attachment_filename,
                    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                    attachment_data.read()
                )
            
            mail.send(msg)
            logger_email.info(f"Correo enviado a {', '.join(recipients)} - {subject}")
            return True
            
        except Exception as e:
            # Log del error pero no detiene el flujo
            logger_email.warning(f"No se pudo enviar correo a {recipients}: {str(e)}")
            logger_email.warning(f"Asunto: {subject}")
            # Retorna False para indicar que falló
            return False
    
    @staticmethod
    def send_daily_report(reportes_por_usuario, archivo_global_data=None):
        """
        Envía resumen diario de reportes
        
        Args:
            reportes_por_usuario: Dict con datos resumidos por usuario
            archivo_global_data: BytesIO del archivo Excel global
        
        Returns:
            bool: True si se envía correctamente
        """
        try:
            # Construir cuerpo HTML
            html_body = """
            <html>
                <head>
                    <style>
                        body { font-family: Arial, sans-serif; }
                        .header { background-color: #2c3e50; color: white; padding: 20px; }
                        .resumen-tabla { width: 100%; border-collapse: collapse; margin: 20px 0; }
                        .resumen-tabla th, .resumen-tabla td { 
                            border: 1px solid #bdc3c7; 
                            padding: 10px; 
                            text-align: left;
                        }
                        .resumen-tabla th { background-color: #34495e; color: white; }
                        .resumen-tabla tr:nth-child(even) { background-color: #ecf0f1; }
                        .footer { color: #7f8c8d; font-size: 12px; margin-top: 20px; }
                    </style>
                </head>
                <body>
                    <div class="header">
                        <h2>Resumen de Reportes Diario</h2>
                    </div>
                    
                    <table class="resumen-tabla">
                        <thead>
                            <tr>
                                <th>Usuario</th>
                                <th>Total WO</th>
                                <th>Horas Aprobadas</th>
                                <th>Horas Reales</th>
                                <th>Diferencia</th>
                            </tr>
                        </thead>
                        <tbody>
            """
            
            total_general_aprobadas = 0
            total_general_reales = 0
            total_general_wo = 0
            
            for usuario, datos in reportes_por_usuario.items():
                total_aprobadas = datos.get('total_aprobadas', 0)
                total_reales = datos.get('total_reales', 0)
                total_wo = datos.get('total_wo', 0)
                diferencia = total_reales - total_aprobadas
                
                total_general_aprobadas += total_aprobadas
                total_general_reales += total_reales
                total_general_wo += total_wo
                
                html_body += f"""
                            <tr>
                                <td>{usuario}</td>
                                <td>{total_wo}</td>
                                <td>{total_aprobadas:.2f}</td>
                                <td>{total_reales:.2f}</td>
                                <td>{diferencia:.2f}</td>
                            </tr>
                """
            
            html_body += f"""
                            <tr style="background-color: #f39c12; font-weight: bold;">
                                <td>TOTAL GENERAL</td>
                                <td>{total_general_wo}</td>
                                <td>{total_general_aprobadas:.2f}</td>
                                <td>{total_general_reales:.2f}</td>
                                <td>{total_general_reales - total_general_aprobadas:.2f}</td>
                            </tr>
                        </tbody>
                    </table>
                    
                    <div class="footer">
                        <p>Este es un correo automático generado por el sistema de reportes.</p>
                        <p>Por favor, no responda a este correo.</p>
                    </div>
                </body>
            </html>
            """
            
            return EmailService.send_email(
                subject="Resumen de Reportes Diario",
                body=html_body,
                attachment_filename="reporte_global.xlsx" if archivo_global_data else None,
                attachment_data=archivo_global_data
            )
            
        except Exception as e:
            logger_email.error(f"Error enviando reporte diario: {str(e)}")
            return False
