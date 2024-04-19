CREATE TABLE users (
	Userid int IDENTITY(1,1) PRIMARY KEY,
	FirstName varchar(255),
	LastName varchar(255),
	Email varchar(255),
	Pwd varchar(255) 
);

INSERT INTO users (FirstName, LastName, Email, Pwd) VALUES ('Michael', 'Jordan', 'mj@app.net', 'asdf');
INSERT INTO users (FirstName, LastName, Email, Pwd) VALUES ('John', 'Smith', 'jsmith@app.net', '1two34');



SELECT * FROM users;