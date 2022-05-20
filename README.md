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
- We created a mini web server in which we display a chart of the utilisation of key-word in terms of time.
- We can also indicate two key-words in order to have a correlation between two curves. 


## For starters : 
- To install the project, you need to execute the script named init.sh
- The following command displays all the options you can use : python3 main.py -h  
- And this one helps install the project in full : python3 main.py -c -l -k -g 
- Don't forget to check if docker and docker-compose are installed on your desktop. If not, make sur to install them before launching your project. 
- To find spotify's cookie : We need to go on their website, inspect the element, then choose a random date. We then go to the network category, which contains in the name the previously selected date. If it doesn't work, just try with another date. 
The cookie is available for 15 minutes. You'll have to change the cookie variable in the main.py file. 
We also need to generate a token to use the genius' api on their site. Then, you'll have to modify the Token variable in the main.py file. 

