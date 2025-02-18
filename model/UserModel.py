from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)

# Configuração do banco de dados
DATABASE_URL = "sqlite:///database/database.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Cria a tabela no banco de dados
Base.metadata.create_all(bind=engine)

class UserModel:
    def __init__(self, db_session):
        self.db = db_session

    def get_user(self, user_id: int):
        return self.db.query(User).filter(User.id == user_id).first()

    def get_users(self, skip: int = 0, limit: int = 10):
        return self.db.query(User).offset(skip).limit(limit).all()

    def create_user(self, username: str, email: str, password: str):
        new_user = User(username=username, email=email, password=password)
        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)
        return new_user

    def update_user(self, user_id: int, username: str = None, email: str = None, password: str = None):
        user = self.db.query(User).filter(User.id == user_id).first()
        if user:
            if username:
                user.username = username
            if email:
                user.email = email
            if password:
                user.password = password
            self.db.commit()
            self.db.refresh(user)
        return user

    def delete_user(self, user_id: int):
        user = self.db.query(User).filter(User.id == user_id).first()
        if user:
            self.db.delete(user)
            self.db.commit()
        return user
    
    def get_user_by_email(self, email: str):
        return self.db.query(User).filter(User.email == email).first()
    
    def get_user_by_username(self, username: str):
        return self.db.query(User).filter(User.username == username).first()

# Exemplo de uso
if __name__ == "__main__":
    db = SessionLocal()
    user_model = UserModel(db)
    
    # Criar um novo usuário
    new_user = user_model.create_user(username="example_user", email="user@example.com", password="password123")
    
    # Ler usuários
    users = user_model.get_users()
    print(users)
    
    # Atualizar um usuário
    user_model.update_user(user_id=1, username="updated_user")
    
    # Deletar um usuário
    user_model.delete_user(user_id=1)
    
    db.close()