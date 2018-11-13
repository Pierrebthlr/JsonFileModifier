"""Modify file script
"""
#See also:
#
#
import json
import sys

def parse_modification_file(filepath):
    """
    Parse the modification file return a list of tuple corresponding
    to the changes to apply. Each tuple is composed by a list of key
    to access the value to change and by the new value.

    Parameters
    ----------
    filepath : str
        Filepath for file_object to be parsed

    Returns
    -------
    changes_to_apply : list
        Parsed changes to apply

    """

    changes_to_apply = []  # create an empty list to collect the
    #modications to apply
    with open(filepath, 'r') as file_object:
        line = file_object.readline()
        while line: # process the file line by line
            args = line.split(":", 1)
            if len(args) != 2: # check if the change match with the expect number of parameters
                raise ValueError("The change "+line+" should have two parameters")
            else:
                args[0] = args[0].replace("\"", "") \
                .replace("\n", "").replace(" ", "") # eliminate useless characters
                change_location = args[0].split(".") # separate the key into a key list
                print(args[1])
                obj = json.loads(args[1])
                changes_to_apply.append((change_location, obj))
            line = file_object.readline()

    return changes_to_apply

def apply_modification(change, json_object):

    """
    This function is a recursive function.
    Each time the function is called, the value of the json_object
    corresponding to the first key of the key list provided by change[0]
    will be accessed.
    This key is then removed from the list and the function is called
    with the value of the json_object accessedself.

    When the list is empty, it means that you have access
    to the value you are trying to modify.
    The new value is then returned.
    The call stack is destacked to reconstitute the JSON object

    Parameters
    ----------
    change : tuple composed by the keys to access the value to changes
    and the new value

    json_object: JSON object that you want to modify


    Returns
    -------
        json_object: reconstituted JSON object with the return of the
        recursive calls
        change[1]: the new value

    """

    if change[0]: #if change[0] is not empty we have to continue to access
    #to the JSON object value
        key = change[0][0]
        change[0].pop(0)
        json_object[key] = apply_modification(change, json_object[key])
        return json_object

    return change[1]



def modify_file(json_file_to_modify, modification_file):
    """
    This function is the main function for applying changes to the JSON file.
    The function will take care of parsing the JSON file,
    and call the functions to parse the file containing the changes
    and apply them.
    The function will then write the result to a file.
    The function is responsible for reporting any errors during modifications.

    Parameters
    ----------
    json_file_to_modify: path to the json file you want to modify

    modification_file: path to the file containing the changes to be made


    Returns
    -------

    """

    #Read and load of the JSON file
    with open(json_file_to_modify, 'r') as file_to_modify:
        try:
            obj = json.load(file_to_modify)
        except ValueError:
            print("error loading the JSON file: "+json_file_to_modify)
        finally:
            file_to_modify.close()

    #Read and application of the change file

    try:
        changes = []
        changes = parse_modification_file(modification_file)
    except ValueError:
        print("error when parsing the modification file : \n")
        print(ValueError.args[0])

    for change in changes:
        try:
            apply_modification(change, obj)
        except KeyError:
            location = ""
            for key in change[0]:
                location += key +"."
            print("error this key: "+location+"\n")
            print("doesn't exist, this change can't be applied\n")

    #write of the changes in a new json file
    json_file_modified = json_file_to_modify.split(".json")[0]
    json_file_modified += "_edit.json" #create a new file name
    with open(json_file_modified, 'w+') as json_file_modified:
        try:
            json_file_modified.write(json.dumps(obj))
        except ValueError:
            print("error loading the JSON file: "+json_file_to_modify)
        finally:
            json_file_modified.close()


#Call of the main function with the terminal args
modify_file(sys.argv[1], sys.argv[2])
