#
#
# main() will be run when you invoke this action
#
# @param Cloud Functions actions accept a single parameter, which must be a JSON object.
#
# @return The output of this action, which must be a JSON object.
#
#
from cloudant.client import Cloudant
from cloudant.error import CloudantException
import requests

#{
#  "_id": "e91c8b09bcff74b33f0b0a39247108d1",
#  "_rev": "1-6d3a316e140863cdb147048888d26051",
#  "id": 1,
#  "name": "Berkly Shepley",
#  "dealership": 15,
#  "review": "Total grid-enabled service-desk",
#  "purchase": true,
#  "purchase_date": "07/11/2020",
#  "car_make": "Audi",
#  "car_model": "A6",
#  "car_year": 2010
#}



def main(dict):

    if dict["name"]:
    
        databaseName = "reviews"

        try:
            client = Cloudant.iam(
                account_name=dict["COUCH_USERNAME"],
                api_key=dict["IAM_API_KEY"],
                connect=True,
            )
            #print("Databases: {0}".format(client.all_dbs()))

            my_database = client[databaseName] 
            
            # Create review document content data
            data = {
                #'_id': 'julia30', # Setting _id is optional
                'name': dict["name"],
                'dealership': dict["dealership"],
                "review": dict["review"],
                "purchase": dict["purchase"],
                "purchase_date": dict["purchase_date"],
                "car_make": dict["car_make"],
                "car_model": dict["car_model"],
                "car_year": dict["car_year"]
                }

            # Create a document using the Database API
            my_document = my_database.create_document(data)

            # Check that the document exists in the database
            if my_document.exists():
                print('SUCCESS!!')
                return({"status":200,"message": "Review added"})
    
        except CloudantException as ce:
            print("unable to connect")
            return {"error": ce}
        except (requests.exceptions.RequestException, ConnectionResetError) as err:
            print("connection error")
            return {"error": err}

        return {"dbs": client.all_dbs()}
       
       
    else:
        return {"status":500,"message":"Error: missing name"}
    

