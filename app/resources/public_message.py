from flask import request, jsonify
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.public_message import PublicMessage
from app.models.user import User
from app.models.profile import Profile
from app.extensions import db

class PublicMessageResource(Resource):
    @jwt_required()
    def post(self):
        """
        Crear un mensaje público.
        El mensaje se crea con el usuario autenticado, asignando su ID y username.
        """
        current_user_id = int(get_jwt_identity())
        user = db.session.get(User, current_user_id)
        if not user:
            return {"message": "Usuario no encontrado."}, 404

        data = request.get_json()
        tematica = data.get("tematica")
        idioma = data.get("idioma")
        content = data.get("content")
        if not tematica or not idioma or not content:
            return {"message": "Se requieren tematica, idioma y content."}, 400
        
         # Obtener el username desde el perfil asociado
        profile = db.session.get(Profile, current_user_id)
        if profile:
            username = profile.username
        else:
            # En caso de que no exista un perfil, se puede optar por un manejo alternativo,
            # por ejemplo, usando el email o retornando un error. en este caso usamos un string Q-unknown-user
            username = "Q-unknown-user"

        new_message = PublicMessage(
            user_id=current_user_id,
            username=username, 
            tematica=tematica,
            idioma=idioma,
            content=content
        )
        db.session.add(new_message)
        db.session.commit()
        return {"message": "Mensaje publicado exitosamente.", "id": new_message.id}, 201

    @jwt_required()
    def get(self):
        """
        Listar mensajes públicos.
        Se pueden aplicar filtros opcionales a través de query parameters:
        - tematica
        - idioma
        - contestado (true/false)
        """
        # Obtén los filtros de la URL
        tematica = request.args.get("tematica")
        idioma = request.args.get("idioma")
        contestado = request.args.get("contestado")

        query = PublicMessage.query
        if tematica:
            query = query.filter_by(tematica=tematica)
        if idioma:
            query = query.filter_by(idioma=idioma)
        if contestado is not None:
            # Convertir a booleano
            if contestado.lower() in ['true', '1']:
                query = query.filter_by(contestado=True)
            else:
                query = query.filter_by(contestado=False)

        messages = query.all()
        # Serializamos los mensajes, sin incluir el campo reply
        result = []
        for msg in messages:
            result.append({
                "id": msg.id,
                "user_id": msg.user_id,
                "username": msg.username,
                "tematica": msg.tematica,
                "idioma": msg.idioma,
                "content": msg.content,
                "contestado": msg.contestado,
                "created_at": msg.created_at.isoformat() if msg.created_at else None
            })
        return {"messages": result}, 200

class PublicMessageDetailResource(Resource):
    @jwt_required()
    def get(self, message_id):
        """
        Obtener el detalle de un mensaje público.
        Si el usuario autenticado es el autor, se incluirá la respuesta (reply) y el responder id.
        """
        current_user_id = int(get_jwt_identity())
        message = db.session.get(PublicMessage, message_id)
        if not message:
            return {"message": "Mensaje no encontrado."}, 404

        data = {
            "id": message.id,
            "user_id": message.user_id,
            "username": message.username,
            "tematica": message.tematica,
            "idioma": message.idioma,
            "content": message.content,
            "contestado": message.contestado,
            "created_at": message.created_at.isoformat() if message.created_at else None
        }
        # Solo mostrar la respuesta si el usuario autenticado es el autor
        if current_user_id == message.user_id:
            data["reply"] = message.reply
            data["responder_id"] = message.responder_id
        return data, 200

    @jwt_required()
    def patch(self, message_id):
        """
        Responder a un mensaje.
        Se permite a un usuario (que no sea el autor) enviar una respuesta.
        La respuesta se guarda en el campo reply, se marca contestado=True,
        y se almacena el ID del usuario que responde en responder_id.
        Nota: La respuesta solo será visible para el autor cuando consulte el detalle.
        """
        current_user_id = int(get_jwt_identity())
        message = db.session.get(PublicMessage, message_id)
        if not message:
            return {"message": "Mensaje no encontrado."}, 404

        if current_user_id == message.user_id:
            return {"message": "No puedes responder a tu propio mensaje."}, 403

        data = request.get_json()
        reply = data.get("reply")
        if not reply:
            return {"message": "Se requiere el campo 'reply'."}, 400

        message.reply = reply
        message.contestado = True
        message.responder_id = current_user_id  # Guardamos el ID del que responde
        db.session.commit()
        return {"message": "Respuesta enviada exitosamente.", "responder_id": current_user_id}, 200


    @jwt_required()
    def delete(self, message_id):
        """
        Permite al autor del mensaje eliminarlo.
        """
        current_user_id = int(get_jwt_identity())
        message = db.session.get(PublicMessage, message_id)
        if not message:
            return {"message": "Mensaje no encontrado."}, 404
        if current_user_id != message.user_id:
            return {"message": "No autorizado para eliminar este mensaje."}, 403

        db.session.delete(message)
        db.session.commit()
        return {"message": "Mensaje eliminado exitosamente."}, 200
