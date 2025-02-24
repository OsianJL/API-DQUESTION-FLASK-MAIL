# populate_db.py
from app import create_app
from app.extensions import db
from app.models.user import User
from app.models.profile import Profile
from app.models.public_message import PublicMessage
import random

def populate():
    app = create_app()
    with app.app_context():
        # Si deseas limpiar las tablas antes de poblar, descomenta las siguientes líneas:
        db.drop_all()
        db.create_all()

        users = []
        # Crear 10 usuarios y sus perfiles
        for i in range(10):
            email = f'user{i}@example.com'
            password = "Test@1234"
            # Crea un usuario; el id se genera automáticamente
            user = User(email=email, password=password, confirmed=True)
            db.session.add(user)
            db.session.commit()  # Commit para obtener el id del usuario

            # Crea un perfil para el usuario
            username = f'username{i}'
            image_url = f'http://example.com/images/{i}.jpg'
            moto = f'Mi moto {i}'
            profile = Profile(user_id=user.id, username=username, image_url=image_url, moto=moto)
            db.session.add(profile)
            db.session.commit()

            users.append(user)
        
        print("Base de datos poblada con 10 usuarios y sus perfiles.")

        # Seleccionar 3 usuarios (por ejemplo, los de índice 0, 1 y 2) para que escriban preguntas
        question_authors = users[:3]
        message_ids = []
        # Cada uno escribe 5 mensajes (preguntas)
        for author in question_authors:
            for j in range(5):
                tematica = random.choice(["Ciencia", "Tecnología", "Arte", "Deporte"])
                idioma = random.choice(["Español", "Inglés", "Francés"])
                content = f"Pregunta {j+1} de {author.email}: ¿Qué opinas sobre {tematica}?"
                new_message = PublicMessage(
                    user_id=author.id,
                    # Aquí, usamos el username del perfil asociado; asumimos que el perfil ya se creó
                    username=f'username{users.index(author)}',
                    tematica=tematica,
                    idioma=idioma,
                    content=content
                )
                db.session.add(new_message)
                db.session.commit()
                message_ids.append(new_message.id)
        
        print("Se han creado 15 mensajes (5 por cada uno de 3 usuarios).")

        # Seleccionar 2 usuarios para responder:
        # Uno que esté entre los 3 autores y otro que no esté entre ellos.
        responder_entre = random.choice(question_authors)
        responder_fuera = random.choice(users[3:])  # del resto

        # Para cada uno, responder a 2 mensajes (aleatorios) asegurándose de que no respondan a sus propios mensajes.
        def responder_mensajes(responder):
            responded = 0
            # Hacemos una copia de la lista de mensajes para evitar modificar la original
            available_message_ids = message_ids.copy()
            random.shuffle(available_message_ids)
            for msg_id in available_message_ids:
                # Obtenemos el mensaje
                msg = db.session.get(PublicMessage, msg_id)
                if msg.user_id == responder.id:
                    continue  # No puede responder a su propio mensaje
                # Asignamos una respuesta
                msg.reply = f"Respuesta de {responder.email} al mensaje {msg.id}"
                msg.contestado = True
                msg.responder_id = responder.id  # Guardamos el id del que responde
                db.session.commit()
                responded += 1
                if responded >= 2:
                    break

        responder_mensajes(responder_entre)
        responder_mensajes(responder_fuera)

        print(f"El usuario {responder_entre.email} y el usuario {responder_fuera.email} han respondido a 2 preguntas cada uno.")

if __name__ == '__main__':
    populate()
