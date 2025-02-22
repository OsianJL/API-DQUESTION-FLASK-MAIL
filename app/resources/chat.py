from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.chat import Chat
from app.models.chat_message import ChatMessage
from app.models.user import User
from app.extensions import db
from sqlalchemy import or_

class ChatListResource(Resource):
    @jwt_required()
    def get(self):
        """
        Lista todas las conversaciones en las que participa el usuario autenticado.
        """
        current_user_id = int(get_jwt_identity())
        chats = Chat.query.filter(
            or_(Chat.user1_id == current_user_id, Chat.user2_id == current_user_id)
        ).all()
        result = []
        for chat in chats:
            result.append({
                "chat_id": chat.id,
                "user1_id": chat.user1_id,
                "user2_id": chat.user2_id,
                "created_at": chat.created_at.isoformat() if chat.created_at else None
            })
        return {"chats": result}, 200

class ChatResource(Resource):
    @jwt_required()
    def post(self):
        """
        Inicia una conversación entre el usuario autenticado y otro usuario.
        Si ya existe un chat entre ambos, se retorna el chat existente.
        Se espera en el JSON de la petición un parámetro "other_user_id".
        """
        current_user_id = int(get_jwt_identity())
        data = request.get_json()
        other_user_id = data.get("other_user_id")
        if not other_user_id:
            return {"message": "El campo 'other_user_id' es requerido."}, 400
        if current_user_id == other_user_id:
            return {"message": "No puedes iniciar un chat contigo mismo."}, 400

        # Para evitar duplicados, ordenamos los IDs: el menor en user1_id y el mayor en user2_id.
        user1 = min(current_user_id, other_user_id)
        user2 = max(current_user_id, other_user_id)

        chat = Chat.query.filter_by(user1_id=user1, user2_id=user2).first()
        if chat:
            return {"message": "Chat ya existe.", "chat_id": chat.id}, 200

        chat = Chat(user1_id=user1, user2_id=user2)
        db.session.add(chat)
        db.session.commit()
        return {"message": "Chat creado exitosamente.", "chat_id": chat.id}, 201

class ChatMessageResource(Resource):
    @jwt_required()
    def get(self, chat_id):
        """
        Lista todos los mensajes de un chat.
        Solo pueden acceder a ellos los usuarios que participan en el chat.
        """
        current_user_id = int(get_jwt_identity())
        chat = db.session.get(Chat, chat_id)
        if not chat:
            return {"message": "Chat no encontrado."}, 404
        if current_user_id not in [chat.user1_id, chat.user2_id]:
            return {"message": "No autorizado para ver este chat."}, 403

        messages = ChatMessage.query.filter_by(chat_id=chat_id).all()
        result = []
        for msg in messages:
            result.append({
                "message_id": msg.id,
                "sender_id": msg.sender_id,
                "content": msg.content,
                "created_at": msg.created_at.isoformat() if msg.created_at else None
            })
        return {"messages": result}, 200

    @jwt_required()
    def post(self, chat_id):
        """
        Envía un mensaje en el chat indicado.
        """
        current_user_id = int(get_jwt_identity())
        chat = db.session.get(Chat, chat_id)
        if not chat:
            return {"message": "Chat no encontrado."}, 404
        if current_user_id not in [chat.user1_id, chat.user2_id]:
            return {"message": "No autorizado para enviar mensajes en este chat."}, 403

        data = request.get_json()
        content = data.get("content")
        if not content:
            return {"message": "El campo 'content' es requerido."}, 400

        new_msg = ChatMessage(chat_id=chat_id, sender_id=current_user_id, content=content)
        db.session.add(new_msg)
        db.session.commit()
        return {"message": "Mensaje enviado exitosamente.", "message_id": new_msg.id}, 201
