from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from app.models.user import User
from app.models.profile import Profile
from app.extensions import db
from app.models.public_message import PublicMessage
from app.models.chat import Chat
from app.models.chat_message import ChatMessage
from datetime import datetime, timezone


# Creamos una vista personalizada para el modelo User
class UserModelView(ModelView):
    # Forzamos que se muestren las columnas id y email
    column_list = ('id', 'email')
    # Evitamos mostrar el campo 'password_hash'
    column_exclude_list = ['password_hash']
    form_excluded_columns = ['password_hash']
    # Opcional: Podrías deshabilitar la edición o creación desde el admin
    # si prefieres que las contraseñas se manejen solo vía el registro y login
    can_create = True
    can_edit = True
    can_delete = True

class ProfileModelView(ModelView):
    # Configura las columnas que quieres mostrar para el perfil
    column_list = ('user_id', 'username', 'image_url', 'moto')
    # Puedes agregar otras configuraciones según necesites
    can_create = True
    can_edit = True
    can_delete = True

class MessagesModelView(ModelView):
    # Configura las columnas que quieres mostrar para el modelo PublicMessage
    column_list = ('id', 'user_id', 'username', 'tematica', 'idioma', 'contestado', 'content', 'reply', 'responder_id', 'created_at', 'updated_at')
    # Puedes agregar otras configuraciones según necesites
    can_create = True
    can_edit = True
    can_delete = True    

class ChatMessagesModelView(ModelView):
    # Configura las columnas que quieres mostrar para el modelo ChatMessage
    column_list = ('id', 'chat_id', 'sender_id', 'content', 'created_at')
    # Puedes agregar otras configuraciones según necesites
    can_create = True
    can_edit = True
    can_delete = True

class ChatModelView(ModelView):
    # Configura las columnas que quieres mostrar para el modelo Chat
    column_list = ('id', 'user1_id', 'user2_id', 'created_at')
    # Puedes agregar otras configuraciones según necesites
    can_create = True
    can_edit = True
    can_delete = True
     
def init_admin(app):
    admin = Admin(app, name="Panel de Administración", template_mode="bootstrap3")
    # Registramos la vista del modelo User en el panel
    admin.add_view(UserModelView(User, db.session))
    admin.add_view(ProfileModelView(Profile, db.session))
    admin.add_view(MessagesModelView(PublicMessage, db.session)) # Añade la vista para PublicMessage
    admin.add_view(ChatModelView(Chat, db.session)) # Añade la vista para Chat
    admin.add_view(ChatMessagesModelView(ChatMessage, db.session)) # Añade la vista para ChatMessage