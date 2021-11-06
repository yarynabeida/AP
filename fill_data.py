from models import Session, User, Tag, Note, NoteStatistics

session = Session()

# filling User table without any links
user_1 = User(id=1, name='Jake', email='jakemail@gmail.com', password='12345')
user_2 = User(id=2, name='Stanley', email='stanleymail@gmail.com', password='1abc')

# filling Tag table without any links
tag_1 = Tag(id=1, name='#business')
tag_2 = Tag(id=2, name='#book')

# using one to many links (between Tag and Note; between User and Note) to fill Note table
note_1 = Note(id=1, name='What to read', text='Lorem ipsum dolor sit amet', owner=user_1, tag=tag_2)
note_2 = Note(id=2, name='How to run a company', text='Ut enim ad minim veniam', owner=user_2, tag=tag_1)
note_3 = Note(id=3, name='tmp', text='Uferferminim veniam', owner=user_1, tag=tag_1)

# using many to many link (between User and Note) to fill NoteStatistics table
statistics_1 = NoteStatistics(id=1, time='2020-01-01', user=user_1, note=note_1)
statistics_2 = NoteStatistics(id=2, time='2020-05-17', user=user_2, note=note_2)

session.add(user_1)
session.add(user_2)
session.add(tag_1)
session.add(tag_2)
session.add(note_1)
session.add(note_2)
session.add(note_3)
session.add(statistics_1)
session.add(statistics_2)

session.commit()

print(session.query(User).all()[0])
print(session.query(User).all()[1])
print(session.query(Tag).all()[0])
print(session.query(Tag).all()[1])
print(session.query(Note).all()[0])
print(session.query(Note).all()[1])
print(session.query(NoteStatistics).all()[0])
print(session.query(NoteStatistics).all()[1])

session.close()
