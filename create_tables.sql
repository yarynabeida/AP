CREATE TABLE User (
	id INT NOT NULL,
	name VARCHAR(45) NOT NULL,
	email VARCHAR(45) NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE Tag (
	id INT NOT NULL,
	name VARCHAR(45) NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE Note (
	id INT NOT NULL,
	name VARCHAR(45) NOT NULL,
    text VARCHAR(404) NOT NULL,
    idTag INT NOT NULL,
    idOwner INT NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (idTag) REFERENCES Tag(id),
    FOREIGN KEY (idOwner) REFERENCES User(id)
);

CREATE TABLE NoteStatistics (
	id INT NOT NULL,
    time DATE NOT NULL,
    userId INT NOT NULL,
    noteId INT NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (noteId) REFERENCES Note(id),
    FOREIGN KEY (userId) REFERENCES User(id)
);

