import csv
from abc import ABC, abstractmethod
import datetime

class ReseauSocial:
    def __init__(self):
        self.__utilisateurs = []

    def ajouter_utilisateur(self, utilisateur):
        if utilisateur.email not in [a.email for a in self.__utilisateurs]:
            self.__utilisateurs.append(utilisateur)
            print(f"Utilisateur {utilisateur.nom} ajouté.")
        else:
            print(f"L'email {utilisateur.email} est déjà utilisé.")

    def sauvegarder_donnees(self, list="utilisateurs.csv"):
        with open(list, "w") as file:
            writer = csv.writer(file)
            writer.writerow(["Nom", "Email", "Mot_de_passe"])
            for utilisateur in self.__utilisateurs:
                writer.writerow([utilisateur.nom, utilisateur.email, utilisateur._Utilisateur__mp])
            print("Donnees sauvegarde")
    
    def charger_donnees(self, fichier="utilisateurs.csv"):
        with open(fichier, "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                utilisateur = Utilisateur("Nom","Email","Mot_de_passe")
                self.ajouter_utilisateur(utilisateur)
        print("Données chargées depuis le fichier CSV.")



#--------------------------------------------------------------------------------------------


class Utilisateur:
    def __init__(self, nom, email, mp):
        self.nom = nom
        self.email = email
        self.__mp = mp
        self.logged_in = False
        self.amis = []

    def login(self, email, mp):
        if self.email == email and self.__mp == mp:
            self.logged_in = True
            print("Connexion reussie.")
        else:
            print("Email ou mot de passe invalide.")

    def logout(self):
        if self.logged_in:
            self.logged_in = False
            print("Deconnexion reussie.")
        else:
            print("Deconnexion interrompue")

    def ajouter_ami(self, ami):
        if ami.email not in [a.email for a in self.amis]:
            self.amis.append(ami)
            ami.amis.append(self)
            print(f"{ami.nom} a été ajouté à votre liste d'amis.")
        else:
            print(f"{ami.nom} est déjà dans votre liste d'amis.")

    def supprimer_ami(self, ami):
        if ami.email in [a.email for a in self.amis]:
            self.amis = [a for a in self.amis if a.email != ami.email]
            ami.amis = [a for a in ami.amis if a.email != self.email]
            print(f"{ami.nom} a été supprimé de votre liste d'amis.")
        else:
            print(f"{ami.nom} n'est pas dans votre liste d'amis.")

    def consulter_liste_amis(self):
        if self.amis:
            print("Voici votre liste d'amis :")
            for ami in self.amis:
                print(f"- {ami.nom} ({ami.email})")
        else:
            print("Vous n'avez pas encore d'amis.")
    
    def sauvegarder(utilisateurs,list="amis.csv"):
        with open(list,"w") as file:
            writer = csv.writer(file)
            for utilisateur in utilisateurs:
                for ami in utilisateur.amis:
                    writer.writerow([utilisateur.email, ami.email])


#--------------------------------------------------------------------------------------------


class Publication(ABC):
    def __init__(self, auteur, contenu, time=None):
        self.auteur = auteur
        self.contenu = contenu

        if time is not None:
            self.datestr = time
            self.date = int(time.timestamp())
        else:
            date = datetime.datetime.now()
            self.date = int(date.timestamp())
            self.datestr = date

    @abstractmethod
    def afficher(self):
        pass

    def save_to_csv(self):
        with open('publications.csv', 'a') as file:
            writer = csv.writer(file)
            writer.writerow([self.auteur, self.contenu, self.datestr])

class MessageTexte(Publication):
    def afficher(self):
        return f"Texte de {self.auteur}: {self.contenu}"

class MessageImage(Publication):
    def __init__(self, auteur, contenu, time, url_image):
        super().__init__(auteur, contenu, time)
        self.url_image = url_image

    def afficher(self):
        return f"Image de {self.auteur}: {self.contenu} (URL: {self.url_image}), (Time: {self.datestr})"


#--------------------------------------------------------------------------------------------


utilisateur1 = Utilisateur("Ali", "ali@gmail.com", "password123")
utilisateur2 = Utilisateur("Wiam", "wiam@gmail.com", "password456")
utilisateur3 = Utilisateur("Hamza", "Hamza@gmail.com", "password789")

utilisateurs = [utilisateur1, utilisateur2, utilisateur3]

reseau = ReseauSocial()
reseau.ajouter_utilisateur(utilisateur1)
reseau.ajouter_utilisateur(utilisateur2)
reseau.ajouter_utilisateur(utilisateur3)
reseau.sauvegarder_donnees()
reseau.charger_donnees()

utilisateur1.ajouter_ami(utilisateur2)
utilisateur1.supprimer_ami(utilisateur3)
utilisateur1.consulter_liste_amis()
Utilisateur.sauvegarder(utilisateurs, "amis.csv")

message1 = MessageTexte("Ali", "Bonjour tout le monde!")
message1.save_to_csv()

message2 = MessageImage("Wiam", "Voici une photo", None, "http://example.com/photo.jpg")
message2.save_to_csv()

