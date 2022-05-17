# SpotifyTop200

Partie 1 : Récupération des chansons
We put up a MongoDB database on docker.
We did scrapping on the Spotify web site in order to deduce the downloading url. 
On a mis en place du multi threading dans la récupération des fichiers et la mise en place dans mongoDB. 

Partie 2 : Récupération des paroles
On a utilisé le module python de genius pour récupérer les paroles des chansons. 
Les requêtes sont en multi threading. Leur résultat est ensuite stocké dans une nouvelle collection sur mongoDB. 

Partie 3 : Récupération des mots clés
On a utilisé un modèle d'IA entraîné en deep learning pour récupérer les mots clés d'un texte en 8 différentes langues. 
Elles sont stockées en bases de données après

Partie 4 : Corrélation avec les tendances