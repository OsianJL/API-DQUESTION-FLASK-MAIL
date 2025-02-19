from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.user import User
from app.models.profile import Profile
from app.extensions import db

class SelfUserResource(Resource):
    @jwt_required()
    def delete(self):
        """
        Permite al usuario eliminar su propia cuenta y su perfil asociado.
        """
        # Obtener el ID del usuario autenticado (del token)
        current_user_id = int(get_jwt_identity())

        # Buscar el usuario en la base de datos
        user = db.session.get(User, current_user_id)
        if not user:
            return {"message": "Usuario no encontrado."}, 404

        # Buscar el perfil asociado (si existe) y eliminarlo
        profile = db.session.get(Profile, current_user_id)
        if profile:
            db.session.delete(profile)

        # Eliminar el usuario
        db.session.delete(user)
        db.session.commit()
        return {"message": "Cuenta de usuario y perfil eliminados exitosamente."}, 200
