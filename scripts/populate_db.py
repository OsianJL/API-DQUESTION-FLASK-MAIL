# populate_db.py
from app import create_app
from app.extensions import db
from app.models.user import User
from app.models.profile import Profile

def populate():
    app = create_app()
    with app.app_context():
        # Opcional: Si deseas limpiar las tablas antes de poblar, puedes descomentar las siguientes líneas:
        db.drop_all()
        db.create_all()

        # Vamos a crear 10 usuarios y sus perfiles correspondientes
        for i in range(10):
            email = f'user{i}@example.com'
            password = "Test@1234"
            confirmed = True
            # Crea un usuario; el id se generará automáticamente mediante la función generate_random_id()
            user = User(email=email, password=password, confirmed=confirmed)
            db.session.add(user)
            db.session.commit()  # Es importante commitear para obtener el id del usuario

            # Crea un perfil para el usuario recién creado
            username = f'username{i}'
            image_url = f'http://example.com/images/{i}.jpg'  # URL de imagen ficticia
            moto = f'Mi moto {i}'
            profile = Profile(user_id=user.id, username=username, image_url=image_url, moto=moto)
            db.session.add(profile)
            db.session.commit()

        print("Base de datos poblada con 10 usuarios y sus perfiles.")

if __name__ == '__main__':
    populate()
