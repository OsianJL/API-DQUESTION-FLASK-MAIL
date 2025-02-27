from flask import request, url_for, current_app
from flask_restful import Resource
from app.models.user import User
from app.extensions import db, mail
from app.services.token import generate_reset_token, confirm_reset_token
from app.services.validators import validate_password
from flask_mail import Message

class PasswordResetRequestResource(Resource):
    def post(self):
        """
        Permite al usuario solicitar el restablecimiento de su contraseña.
        Se espera que se envíe un JSON con el campo "email".
        Si el email está registrado, se genera un token y se envía un email con el enlace de reset.
        """
        data = request.get_json()
        email = data.get("email")
        if not email:
            return {"message": "El email es requerido."}, 400

        user = User.query.filter_by(email=email).first()
        if not user:
            return {"message": "El email no está registrado."}, 404

        # Generar token de restablecimiento
        token = generate_reset_token(email)
        #!! sustituir esta linea
        reset_url = url_for("password_reset_confirm", token=token, _external=True)  
        #!! sustituir esta linea cuando queramos dirigir al usuario a nuestra app, y no al backend
        #!! usaremos algo como reset_url = "myapp://reset_password?token=" + token


        # Preparar el mensaje de email
        subject = "Restablece tu contraseña"
        html_body = f"""
        <p>Hola,</p>
        <p>Hemos recibido una solicitud para restablecer tu contraseña.</p>
        <p>Para hacerlo, haz clic en el siguiente enlace:</p>
        <p><a href="{reset_url}">{reset_url}</a></p>
        <p>Si no solicitaste este cambio, ignora este correo.</p>
        """
        msg = Message(subject=subject, recipients=[email], html=html_body)
        try:
            mail.send(msg)
            current_app.logger.info(f"Email de reset de contraseña enviado a {email}")
        except Exception as e:
            current_app.logger.error(f"Error al enviar email: {e}")
            return {"message": "Registro realizado, pero fallo al enviar el email de restablecimiento."}, 500

        return {"message": "Se ha enviado un email con las instrucciones para restablecer la contraseña."}, 200


class PasswordResetConfirmResource(Resource):
    def post(self, token):
        data = request.get_json()
        new_password = data.get("new_password")
        if not new_password:
            return {"message": "La nueva contraseña es requerida."}, 400

        # Validar la contraseña si es necesario
        if not validate_password(new_password):
            return {"message": "La contraseña no cumple con los requisitos."}, 400

        email = confirm_reset_token(token)
        if not email:
            return {"message": "El token es inválido o ha expirado."}, 400

        user = User.query.filter_by(email=email).first()
        if not user:
            return {"message": "Usuario no encontrado."}, 404

        # Actualizar la contraseña del usuario
        user.set_password(new_password)
        db.session.commit()

        return {"message": "Contraseña actualizada exitosamente."}, 200