from sqlalchemy import ForeignKey, Column, Integer, String, Boolean, MetaData, create_engine
from sqlalchemy.orm import relationship, backref, sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base




convention = {
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
}
metadata = MetaData(naming_convention=convention)

Base = declarative_base(metadata=metadata)

engine = create_engine('sqlite:///theater_work.db')
Session = sessionmaker(bind=engine)
session = Session()

class Role(Base):
    __tablename__ = 'roles'

    id = Column(Integer(), primary_key=True)
    character_name = Column(String())

    auditions = relationship('Audition', backref='role')
    
    @property
    def locations(self):
        return [audition.location for audition in self.auditions]

    def __repr__(self):
        return f'This is a role for {self.character_name} in the Flatiron Theater Play!'
    
    def lead(self):
        for aud in self.auditions:
            if aud.hired == 1:
                return f'{aud.actor} is the lead actor for {self.character_name}'
        return 'No actor has been hired for this role.'

    def understudy(self):
        hired_auds = [aud for aud in self.auditions if aud.hired == 1]
        if len(hired_auds) >= 2:
            return hired_auds[1]
        else:
            return 'No actor has been hired for the understudy for this role'

class Audition(Base):
    __tablename__ = 'auditions'

    id = Column(Integer(), primary_key=True)
    actor = Column(String())
    location = Column(String())
    phone = Column(Integer())
    hired = Column(Boolean(False))
    role_id = Column(Integer(), ForeignKey('roles.id'))

    def __repr__(self):
        return f'This is an actor named {self.actor}'
    
    def call_back(self):
        self.hired = True
        session.add(self)
        session.commit()

    



   