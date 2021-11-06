from sqlalchemy import Column, Integer, VARCHAR, Date, ForeignKey
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session, relationship

# engine = create_engine("mysql://root:A2452756b@127.0.0.1/my_db")
engine = create_engine("mysql://root:123abc!!!@127.0.0.1:3306/my_db")

SessionFactory = sessionmaker(bind=engine)

Session = scoped_session(SessionFactory)

Base = declarative_base()


class NoteStatistics(Base):
    __tablename__ = 'notestatistics'
    id = Column(Integer, primary_key=True)
    time = Column(Date)
    userId = Column(Integer, ForeignKey('user.id'))
    noteId = Column(Integer, ForeignKey('note.id'))

    # creating many to many link using this table
    user = relationship("User", back_populates="notes")
    note = relationship("Note", back_populates="users")

    def __str__(self):
        return f"--------------------------------------------\n" \
               f"| NoteStatistics Table                     |\n" \
               f"--------------------------------------------\n" \
               f"- Id\t\t: {self.id}\n" \
               f"- Time\t\t: {self.time}\n" \
               f"- UserId\t: {self.userId}\n" \
               f"- NoteId\t: {self.noteId}\n" \
               f"--------------------------------------------\n"


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(VARCHAR(length=45), nullable=False)
    email = Column(VARCHAR(length=45), nullable=False)
    password = Column(VARCHAR(length=45), nullable=False)

    # creating link to Note using NoteStatistics table
    notes = relationship("NoteStatistics", back_populates="user")

    def __str__(self):
        return f"--------------------------------------------\n" \
               f"| User Table                               |\n" \
               f"--------------------------------------------\n" \
               f"- Id\t: {self.id}\n" \
               f"- Name\t: {self.name}\n" \
               f"- Email\t: {self.email}\n" \
               f"- Password\t: {self.password}\n" \
               f"--------------------------------------------\n"


class Tag(Base):
    __tablename__ = "tag"
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(VARCHAR(length=45), nullable=False)

    def __str__(self):
        return f"--------------------------------------------\n" \
               f"| Tag Table                                |\n" \
               f"--------------------------------------------\n" \
               f"- Id\t: {self.id}\n" \
               f"- Name\t: {self.name}\n" \
               f"--------------------------------------------\n"


class Note(Base):
    __tablename__ = "note"
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(VARCHAR(length=45), nullable=False)
    text = Column(VARCHAR(length=404), nullable=False)

    idTag = Column(Integer, ForeignKey('tag.id'), nullable=False)
    tag = relationship(Tag, backref="note", lazy=False)

    idOwner = Column(Integer, ForeignKey('user.id'), nullable=False)
    owner = relationship(User, backref="note", lazy=False)

    # creating link to User using NoteStatistics table
    users = relationship("NoteStatistics", back_populates="note")

    def __str__(self):
        return f"--------------------------------------------\n" \
               f"| Note Table                               |\n" \
               f"--------------------------------------------\n" \
               f"- Id\t\t: {self.id}\n" \
               f"- Name\t\t: {self.name}\n" \
               f"- Text\t\t: {self.text}\n" \
               f"- IdTag\t\t: {self.idTag}\n" \
               f"- IdOwner\t: {self.idOwner}\n" \
               f"--------------------------------------------\n"
