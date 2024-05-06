CREATE DATABASE aprilDock
GO

USE aprilDock
GO

CREATE TABLE users (
	Userid int IDENTITY(1,1) PRIMARY KEY,
	FirstName varchar(255),
	LastName varchar(255),
	Email varchar(255),
	Pwd varchar(255),
	IsConfirmed int DEFAULT 0
);
GO

INSERT INTO users (FirstName, LastName, Email, Pwd) 
VALUES 
('Michael', 'Jordan', 'mj@app.net', 'asdf'), 
('John', 'Smith', 'jsmith@app.net', '1two34');
GO
