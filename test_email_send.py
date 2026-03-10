from app import create_app
from app.services.email_service import EmailService

app = create_app()

with app.app_context():
    try:
        result = EmailService.send_email(
            subject="Prueba de Correo - Sistema REDEMI",
            body="<h2>Este es un correo de prueba</h2><p>Si recibes este mensaje, el sistema de correos está funcionando correctamente.</p>",
            recipients=["santiagotorr245@gmail.com"]
        )
        
        if result:
            print("✅ Correo enviado exitosamente")
        else:
            print("❌ Error al enviar correo (revisa los logs)")
            
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
