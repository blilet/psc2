# Génération de fichier global JSON

Pour stocker les informations relatives à une conférence labélisée manuellement (on suppose qu'elle provient de YouTube), on utilise le notebook loadOneFile.ipynb qui nous aide à travers l'execution de chaque cellule à sauvegarder toutes les interruptions (supprimer une éventuellemnt) en un fichier .json. 

Ce fichier .json est stocké dans un répertoire ./outputs avec le nom de son extract (voir notebook). Après avoir stocké suffisament de conférences, on merge le tout en utilisant le notebook JSONmerge.ipynb en un fichier global appelé combined.json qui sera utilisé eventuellement pour tester le réseau développé.


