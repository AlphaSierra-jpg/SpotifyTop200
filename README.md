# Groupe de coste_c 977977



## **STEP ONE** : Songs' recovery
- We put up a MongoDB database on docker.
- We did scrapping on the Spotify web site in order to deduce the downloading url. 
- We put in place multi threading in the recovery of the files and the setup in MongoDB. 


## **STEP TWO** : Lyrics' recovery
- We used Genius' python module to recover the songs' lyrics. 
- The requests are in multi threading. 
- Their result is the stocked in a new collection on MongoDB. 


## **STEP THREE** : Key-words' recovery
- We used an IA model trained in deep learning to recover each text's key-words in 8 different languages. 
- These will then all be stocked in databases. 


## **STEP FOUR** : Correlation with the trends

