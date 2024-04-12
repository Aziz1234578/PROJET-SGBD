-- Création de la base de données
CREATE DATABASE IF NOT EXISTS Projet_sbgd;

-- Utilisation de la base de données
USE Projet_sbgd;

-- Création de la table CoordinateurPedagogique
CREATE TABLE IF NOT EXISTS CoordinateurPedagogique (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(255),
    prenom VARCHAR(255),
    mail VARCHAR(255),
    mdp VARCHAR(255)
);

-- Création de la table Enseignement
CREATE TABLE IF NOT EXISTS Enseignement (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_enseignant INT,
    libelle VARCHAR(255),
    FOREIGN KEY (id_enseignant) REFERENCES Enseignant(id)
);

-- Création de la table Enseignant
CREATE TABLE IF NOT EXISTS Enseignant (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_enseignement INT,
    nom VARCHAR(255),
    prenom VARCHAR(255),
    mail VARCHAR(255),
    mdp VARCHAR(255),
    FOREIGN KEY (id_enseignement) REFERENCES Enseignement(id)
);

-- Création de la table CahierDeTexte
CREATE TABLE IF NOT EXISTS CahierDeTexte (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_classe INT,
    date DATE,
    contenu TEXT,
    FOREIGN KEY (id_classe) REFERENCES Classe(id)
);

-- Création de la table Classe
CREATE TABLE IF NOT EXISTS Classe (
    id INT AUTO_INCREMENT PRIMARY KEY,
    libelle VARCHAR(255),
    id_responsable INT,
    FOREIGN KEY (id_responsable) REFERENCES ResponsableClasse(id)
);

-- Insertion des classes dans la table Classe
INSERT INTO Classe (libelle) VALUES 
('DSTI1A'),
('DSTI1B'),
('DSTI1C'),
('DSTI2A'),
('DSTI2B'),
('DSTI2C'),
('GLSIA'),
('GLSIB'),
('GLSIC'),
('DIT');


-- Création de la table Etudiant
CREATE TABLE IF NOT EXISTS Etudiant (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_responsable INT,
    id_classe INT,
    nom VARCHAR(255),
    prenom VARCHAR(255),
    mail VARCHAR(255),
    mdp VARCHAR(255),
    FOREIGN KEY (id_responsable) REFERENCES ResponsableClasse(id),
    FOREIGN KEY (id_classe) REFERENCES Classe(id)
);

-- Création de la table ResponsableClasse
CREATE TABLE IF NOT EXISTS ResponsableClasse (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(255),
    prenom VARCHAR(255),
    id_classe INT,
    mail VARCHAR(255),
    mdp VARCHAR(255),
    FOREIGN KEY (id_classe) REFERENCES Classe(id)
);

-- Création de la table Avis
CREATE TABLE IF NOT EXISTS Avis (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_etudiant INT,
    contenu TEXT,
    FOREIGN KEY (id_etudiant) REFERENCES Etudiant(id)
);

-- Création de la table RapportCoordinateur
CREATE TABLE IF NOT EXISTS RapportCoordinateur (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_classe INT,
    contenu TEXT,
    FOREIGN KEY (id_classe) REFERENCES Classe(id)
);

-- Création de la table Commissionpeda
CREATE TABLE IF NOT EXISTS Commissionpeda (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(255),
    prenom VARCHAR(255),
    mail VARCHAR(255),
    mdp VARCHAR(255)
);

-- Création de la table Recommendations
CREATE TABLE IF NOT EXISTS Recommendations (
    contenu TEXT
);

-- Création de la table MembreDediee
CREATE TABLE IF NOT EXISTS MembreDediee (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(255),
    prenom VARCHAR(255),
    mail VARCHAR(255),
    mdp VARCHAR(255)
);

-- Création de la table PV
CREATE TABLE PV (
    id INT AUTO_INCREMENT PRIMARY KEY,
    pdf_adresse VARCHAR(255)
);


-- Création de la table ChefDepartement
CREATE TABLE IF NOT EXISTS ChefDepartement (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(255),
    prenom VARCHAR(255),
    mail VARCHAR(255),
    mdp VARCHAR(255)
);

-- Création de la table SituationDept
CREATE TABLE IF NOT EXISTS SituationDept (
    id INT AUTO_INCREMENT PRIMARY KEY,
    contenu TEXT
);

-- Création de la table ResponsablePedagogique
CREATE TABLE IF NOT EXISTS ResponsablePedagogique (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(255),
    prenom VARCHAR(255),
    mail VARCHAR(255),
    mdp VARCHAR(255)
);

-- Création de la table RapportRP
CREATE TABLE IF NOT EXISTS RapportRP (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_classe INT,
    contenu TEXT,
    FOREIGN KEY (id_classe) REFERENCES Classe(id)
);
-- Création de la table PointExecution
CREATE TABLE IF NOT EXISTS PointExecution (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_rp INT,
    contenu TEXT,
    FOREIGN KEY (id_rp) REFERENCES ResponsablePedagogique(id)
);


-- Création de la table DirecteurEtudes
CREATE TABLE IF NOT EXISTS DirecteurEtudes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(255),
    prenom VARCHAR(255),
    mail VARCHAR(255),
    mdp VARCHAR(255)
);

-- Insertion du Chef de département
INSERT INTO ChefDepartement (nom, prenom, mail, mdp) VALUES 
('Ndiaye', 'Mamadou', 'mamadoundiaye@esp.sn', 'mdpchef');

-- Insertion du Membre dédié
INSERT INTO MembreDediee (nom, prenom, mail, mdp) VALUES 
('Diop', 'Aïssatou', 'aissatoudiop@esp.sn', 'mdpmembre');

-- Insertion du Coordinateur pédagogique
INSERT INTO CoordinateurPedagogique (nom, prenom, mail, mdp) VALUES 
('Sow', 'Fatou', 'fatousow@esp.sn', 'mdpcoordo');

-- Insertion du Responsable pédagogique
INSERT INTO ResponsablePedagogique (nom, prenom, mail, mdp) VALUES 
('Faye', 'Ousmane', 'ousmanefaye@esp.sn', 'mdpresponsable');

-- Insertion du Directeur des études
INSERT INTO DirecteurEtudes (nom, prenom) VALUES 
('Diallo', 'Mariama','mariamadiallo@esp.sn','mdpdirecteuretudes');


-- Création d'un nouvel utilisateur
CREATE USER 'admin'@'localhost' IDENTIFIED BY 'passer';

-- Attribution des autorisations à l'utilisateur sur la base de données
GRANT ALL PRIVILEGES ON Projet_sbgd.* TO 'admin'@'localhost';

-- Rafraîchir les privilèges
FLUSH PRIVILEGES;
