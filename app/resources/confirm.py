from flask import request, jsonify, current_app
from flask_restful import Resource
from app.extensions import db
from app.models.user import User
from app.utils.token import confirm_token

class ConfirmEmailResource(Resource):
    def get(self, token):
        # Verificar el token de confirmación
        email = confirm_token(token)
        if not email:
            return {"message": "El token de confirmación es inválido o ha expirado."}, 400

        # Buscar el usuario por email
        user = User.query.filter_by(email=email).first()
        if not user:
            return {"message": "Usuario no encontrado."}, 404

        # Verificar si ya ha confirmado
        if user.confirmed:
            return {"message": "El email ya ha sido confirmado."}, 200

        # Marcar el usuario como confirmado
        user.confirmed = True
        db.session.commit()

        return {"message": "Email confirmado exitosamente."}, 200
