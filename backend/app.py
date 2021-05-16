from application import create_app

app = create_app()


# @app.before_first_request
# def create_user():
#     from application import db
#     from application.models.authbase.user import User
#     from application.models.authbase.role import Role
#     from flask_security import SQLAlchemyUserDatastore
#     from flask_security import hash_password
#
#     db.drop_all()
#     db.create_all()
#     user_datastore = SQLAlchemyUserDatastore(db, User, Role)
#     if not user_datastore.find_user(email="test@me.com"):
#         user_datastore.create_user(email="test@me.com",
#                                    password=hash_password("password"))
#     db.session.commit()
