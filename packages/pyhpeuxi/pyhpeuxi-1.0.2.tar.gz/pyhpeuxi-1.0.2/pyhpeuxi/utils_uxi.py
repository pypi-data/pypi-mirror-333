# (C) Copyright 2019-2025 Hewlett Packard Enterprise Development LP.
# Apache License 2.0

import json
import csv
import os

class Utils_UXI():
    def get_token_from_file(fileName):
        """
        Use this function to retrieve the access_token from a file which is located in the working directory of the script. 
        The file must use the following structure:
        {"access_token":"your_secret_token"}
        """
        try:
            f = open(fileName, "r")
            content = f.read()
            jsonContent = json.loads(content)
            if jsonContent['access_token']:
                return jsonContent['access_token']
            else:
                raise ValueError({"status":"Error", "message":"Missing Access Token."})
     
        except KeyError as e:
            raise Exception({"status":"Error", "Message":"Missing 'access_token' key name. Ensure key name exists as per the function usage details."})
        except json.JSONDecodeError as e:
            raise Exception({"status":"Error", "Message":"Ensure a valid json file as described in the function usage details."})
        except FileNotFoundError as e:  
            raise Exception({"status":"Error", "Message":"Ensure the token file '"+ fileName+"' exists. "+e.strerror})

        except Exception as e:
            raise Exception({"status":"Error", "Message":e})
    
    def get_personal_api_client_creds_from_file(fileName):
        """
        Use this function to retrieve the client_id and client_secret from a file which is located in the working directory of the script. 
        The file must use the following structure:
        {"client_id":"your_client_id","client_secret":"your_client_secret"}
        """
        try:
            f = open(fileName, "r")
            content = f.read()
            jsonContent = json.loads(content)
            if jsonContent['client_id'] and jsonContent['client_secret']:
                return jsonContent
            else:
                raise ValueError({"status":"Error", "message":"Ensure both client_id and client_secret key names and values exist within the ."})   
        
        except KeyError as e:
            raise Exception({"status":"Error", "Message":"Missing 'client_id' key name or and client_secret. Ensure key name exists as per the function usage details."})
        except json.JSONDecodeError as e:
            raise Exception({"status":"Error", "Message":"Ensure a valid json file as described in the function usage details."})
        except FileNotFoundError as e:  
            raise Exception({"status":"Error", "Message":"Ensure the token file '"+ fileName+"' exists. "+e.strerror})

        except Exception as e:
            raise Exception({"status":"Error", "Message":e})     

    def export_to_csv(data, file_name, sub_folder="csv"):
        """
        Exports the data to a CSV file. Parameters are described below
        
        :param The data to be exported (expected to be a dictionary with an 'items' key).
        :param file_name: The name of the CSV file to create without the extension.
        :param sub_folder: The subfolder where the CSV file will be saved. #Optional, by default will create a folder called 'csv'
        """

        if 'items' in data and data['items']:
            items = data['items']
        else:
            print(f"The 'items' list is empty for {file_name}. No CSV file will be created.")
            return

        headers = items[0].keys()

        if not os.path.exists(sub_folder):
            try:
                os.makedirs(sub_folder)
            except OSError as e:
                print(f"Error creating directory {sub_folder}: {e}")
                return

        file_name = f"{file_name}.csv"
        file_path = os.path.join(sub_folder, file_name)

        try:
            with open(file_path, 'w', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=headers)
                writer.writeheader()
                for item in items:
                    writer.writerow(item)
                print(f"Data has been exported to {file_path}")
        except IOError as e:
            print(f"Error writing to file {file_path}: {e}")
