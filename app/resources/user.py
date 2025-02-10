from flask_restful import Resource, reqparse
from flask import current_app
from app.models.user import User
from app.extensions import db

class AdminUserResource(Resource):
    def delete(self, user_id):
        # Definir el parser para obtener el parámetro admin_key de la petición
        parser = reqparse.RequestParser()
        parser.add_argument('admin_key', type=str, required=True, help="La clave de administrador es requerida.")
        args = parser.parse_args()
        admin_key = args.get('admin_key')

        # Verificar que la clave proporcionada coincida con la configurada
        if admin_key != current_app.config.get("ADMIN_SECRET"):
            return {"message": "No autorizado. Clave de administrador inválida."}, 403

        user = User.query.get(user_id)
        if not user:
            return {"message": "Usuario no encontrado."}, 404

        db.session.delete(user)
        db.session.commit()
        return {"message": "Usuario eliminado exitosamente."}, 200
