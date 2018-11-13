# JsonFileModifier
This program allows you to modify value in a JSON file from a file that groups the changes to be made

To use this application you have to run the script "modifyfilescript.py" with two arguments :
    1. the path to the JSON file you want to modify 
    2. the path to the file that groups all the change to be made
    
Call exemple : 

   python modifyfilescript.py "./exFileToModify.json" "./exModificationFile" 
   
   
exFileToModify.json : Exemple of a JSON file

exModificationFile : Exemple of a change file

the result of the program will be write on the file : exFileToModify_edit.json
   
On the Modification file one change should be write on one line. 

