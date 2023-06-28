from faker import Faker
import random

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Audition, Role, session

if __name__ == '__main__':
    session.query(Audition).delete()
    session.query(Role).delete()

    fake = Faker()


    roles = []
    for i in range(5):
        role = Role(
            character_name = fake.job()
        )
        session.add(role)
        session.commit()
        roles.append(role)

    auditions = []
    for i in range(25):
        random_role = random.choice(roles)
        audition = Audition(
            actor = fake.unique.name(),
            location = fake.address(),
            phone = fake.phone_number(),
            hired = False,
            role = random_role
        )
        session.add(audition)
        session.commit()
        auditions.append(audition)
        
    session.close()