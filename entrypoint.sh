#!/bin/bash

echo "📦 Applying DB schema and inserting default user if needed..."

python -c "
from db import Base, engine, User
from sqlalchemy.orm import sessionmaker
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
db = Session()
if not db.query(User).first():
    user = User(username='admin', password_hash=User.hash_password('admin'))
    db.add(user)
    db.commit()
    print('✅ Default user created: admin / admin')
else:
    print('ℹ️  User already exists')
"

echo "🚀 Launching Streamlit..."
exec streamlit run main.py --server.port=8501 --server.address=0.0.0.0
