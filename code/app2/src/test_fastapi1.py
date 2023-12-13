import os
import requests

# définition de l'adresse de l'API
api_address = '172.50.0.2'
# port de l'API
api_port = 8000

# requête
r = requests.get(
    url='http://{address}:{port}/'.format(address=api_address, port=api_port)
    # ,
    # params= {
    #     'username': 'alice',
    #     'password': 'wonderland'
    # }
)

output = '''
============================
    Authentication test - 1
============================

request done at "/permissions"
| username="alice"
| password="wonderland"

expected result = 200
actual restult = {status_code}

==>  {test_status}

'''


# statut de la requête
status_code = r.status_code

# affichage des résultats
if status_code == 200:
    test_status = 'SUCCESS'
else:
    test_status = 'FAILURE'
print(output.format(status_code=status_code, test_status=test_status))

# impression dans un fichier
LOG = int(os.environ.get('LOG'))
if LOG == 1:
    with open('/home/my_log/api_test.log', 'a') as file:
        file.write(output.format(status_code=status_code, test_status=test_status))



# Second test
# requête
r = requests.get(
    url='http://{address}:{port}/run_model'.format(address=api_address, port=api_port)
    # ,
    # params= {
    #     'username': 'bob',
    #     'password': 'builder'
    # }
)

output = '''
============================
    Authentication test - 2
============================

request done at "/permissions"
| username="bob"
| password="builder"

expected result = 200
actual restult = {status_code}

==>  {test_status}

'''


# statut de la requête
status_code = r.status_code

# affichage des résultats
if status_code == 200:
    test_status = 'SUCCESS'
else:
    test_status = 'FAILURE'
print(output.format(status_code=status_code, test_status=test_status))

# impression dans un fichier
LOG = int(os.environ.get('LOG'))
if LOG == 1:
    with open('/home/my_log/api_test.log', 'a') as file:
        file.write(output.format(status_code=status_code, test_status=test_status))

