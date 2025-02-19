from flask import request, jsonify
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.profile import Profile
from app.extensions import db

class ProfileResource(Resource):
    @jwt_required()
    def get(self, user_id):
        """Obtener el perfil del usuario autenticado."""
        current_user_id = int(get_jwt_identity())
        if current_user_id != user_id:
            return {"message": "No autorizado para ver este perfil."}, 403
        profile = db.session.get(Profile, user_id)
        if not profile:
            return {"message": "Perfil no encontrado."}, 404
        return {
            "user_id": profile.user_id,
            "username": profile.username,
            "image_url": profile.image_url,
            "moto": profile.moto
        }, 200

    @jwt_required()
    def post(self):
        """
        Crear un perfil para el usuario autenticado.
        Se espera que el usuario aún no tenga un perfil.
        """
        current_user_id = int(get_jwt_identity())
        if db.session.get(Profile, current_user_id):
            return {"message": "El perfil ya existe."}, 400
        data = request.get_json()
        username = data.get("username")
        image_url = data.get("image_url")
        moto = data.get("moto")
        if not username:
            return {"message": "Username es requerido."}, 400
        profile = Profile(user_id=current_user_id, username=username, image_url=image_url, moto=moto)
        db.session.add(profile)
        db.session.commit()
        return {"message": "Perfil creado exitosamente."}, 201

    @jwt_required()
    def patch(self, user_id):
        """
        Actualización parcial del perfil.
        Permite modificar solo los campos enviados en la petición.
        """
        current_user_id = int(get_jwt_identity())
        if current_user_id != user_id:
            return {"message": "No autorizado para modificar este perfil."}, 403
        profile = db.session.get(Profile, user_id)
        if not profile:
            return {"message": "Perfil no encontrado."}, 404
        data = request.get_json()
        if "username" in data:
            profile.username = data["username"]
        if "image_url" in data:
            profile.image_url = data["image_url"]
        if "moto" in data:
            profile.moto = data["moto"]
        db.session.commit()
        return {"message": "Perfil actualizado exitosamente."}, 200

    @jwt_required()
    def delete(self, user_id):
        """Eliminar el perfil del usuario autenticado."""
        current_user_id = int(get_jwt_identity())
        if current_user_id != user_id:
            return {"message": "No autorizado para eliminar este perfil."}, 403
        profile = db.session.get(Profile, user_id)
        if not profile:
            return {"message": "Perfil no encontrado."}, 404
        db.session.delete(profile)
        db.session.commit()
        return {"message": "Perfil eliminado exitosamente."}, 200
