# Projet_SDR_IISE

📌 Présentation du Projet

Ce projet implémente un système de contrôle d'accès par reconnaissance faciale basé sur une architecture client-serveur distribuée. Il permet à des clients de capturer des images de visages et de les envoyer à un serveur central qui se charge de l’identification et de la gestion des accès.


📁 Structure du Projet

🧩 ProjetClient

    Module contenant l’interface graphique utilisateur :
    
    Capture d’images du visage via webcam.
    
    Envoi des images au serveur via gRPC.
    
    Affichage du résultat (accès autorisé/refusé).

🧠 ProjetServeur

    Module du serveur de reconnaissance faciale :
    
    Réception des images via gRPC.
    
    Traitement des visages avec la bibliothèque face_recognition.
    
    Comparaison avec les visages enregistrés.
    
    Application Django pour l’administration des employés et des historiques d’accès.

🧪 ClientCam
    
    Client en ligne de commande pour les tests :
    
    Capture d’image depuis le terminal.
    
    Envoi direct au serveur pour test ou débogage.

📡 protos
    
    Contient les fichiers .proto nécessaires à la communication gRPC :
    
    Définition des messages (images, réponses, statuts).
    
    Définition des services utilisés entre clients et serveur.
    
    Génération des classes Python via grpcio-tools.

🔧 Technologies utilisées
Python avec :
    
    face_recognition (basée sur dlib)
    
    OpenCV pour la capture et le traitement d’image
    
    gRPC pour la communication distribuée
    
    Django pour l'interface web et la gestion des données
    
    Protobuf pour la définition des services RPC
    
    MySQL pour la base de données des employés

🎯 Objectifs du projet

Capturer et reconnaître des visages de manière distribuée.

Gérer dynamiquement les utilisateurs autorisés via une interface d’administration.

Séparer clairement les rôles (client/serveur/tests).

Offrir une base évolutive pour d'autres systèmes d'accès biométrique.
