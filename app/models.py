import hashlib
from .main import db
from .config import SECRET_KEY


permissions = db.Table('app_permissions',
                       db.Column('permission_id', db.Integer, db.ForeignKey('app_permission.id'), primary_key=True),
                       db.Column('role_id', db.Integer, db.ForeignKey('app_role.id'), primary_key=True)
                       )


class Role(db.Model):
    __tablename__ = 'app_role'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    permissions = db.relationship('Permission', secondary=permissions, lazy='subquery',
                                  backref=db.backref('roles', lazy=True))


class Permission(db.Model):
    __tablename__ = 'app_permission'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False, unique=True)


class User(db.Model):
    __tablename__ = 'app_user'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(255), nullable=False, unique=True)
    role_id = db.Column(db.Integer, db.ForeignKey('app_role.id'), nullable=False)
    role = db.relationship('Role', backref='user')
    password = db.Column(db.String(255))

    @classmethod
    def get_hash_password(cls, password):
        password_src = password + SECRET_KEY
        password_hash = hashlib.md5(password_src.encode())
        password_hash_hexdigest = password_hash.hexdigest()
        return password_hash_hexdigest

    def set_password(self, password):
        password_hash_hexdigest = User.get_hash_password(password)
        self.password = password_hash_hexdigest

    @classmethod
    def login(cls, username, password):
        password_hash_hexdigest = cls.get_hash_password(password)
        user = cls.query.filter_by(username=username, password=password_hash_hexdigest).first()
        return user
