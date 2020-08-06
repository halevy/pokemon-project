CREATE DATABASE POKEMON;


USE POKEMON;

CREATE TABLE Pokemon(
    p_id INT NOT NULL PRIMARY KEY,
    p_name VARCHAR(20),
    height TINYINT,
    weight INT
);
USE POKEMON;
CREATE TABLE Trainer(
    t_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    t_name VARCHAR(20),
    town VARCHAR(50),
    UNIQUE(t_name, town)
);
USE POKEMON;
CREATE TABLE Type_(
    ty_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    ty_name VARCHAR(20),
    UNIQUE(ty_name)
);
USE POKEMON;
CREATE TABLE Pokemon_Type(
    p_id INT NOT NULL,
    ty_id INT NOT NULL,
    PRIMARY KEY(p_id, ty_id),
    FOREIGN KEY(p_id) REFERENCES Pokemon(p_id),
    FOREIGN KEY(ty_id) REFERENCES Type_(ty_id)
)
USE POKEMON;
CREATE TABLE OwnedBy(
    p_id INT NOT NULL,
    t_id INT NOT NULL,
    ty_id INT NOT NULL,
    PRIMARY KEY(p_id, t_id, ty_id),
    FOREIGN KEY(p_id,ty_id) REFERENCES Pokemon_Type(p_id,ty_id),
    FOREIGN KEY(t_id) REFERENCES Trainer(t_id)

)
