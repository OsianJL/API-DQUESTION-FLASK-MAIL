from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

class ProtectedResource(Resource):
    @jwt_required()
    def get(self):
        # get_jwt_identity() recupera el 'identity' establecido en create_access_token (en nuestro caso, el id del usuario)
        current_user = get_jwt_identity()
        return {
            "message": f"Hola, usuario {current_user}. Esta es una ruta protegida."
        }, 200
