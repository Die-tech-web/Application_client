import zeep
import json

class SoapClient:
    def __init__(self, wsdl_url):
        self.client = zeep.Client(wsdl=wsdl_url)

    def authenticate(self, email, password):
        return self.client.service.authenticate(email, password)

    def list_users(self, token):
        response = self.client.service.listUsers(token)
        users_json = json.loads(response)
        # Ajout de vérifications pour s'assurer que les champs sont corrects
        for user in users_json:
            user['prenom'] = user.get('prenom', 'N/A')
            user['nom'] = user.get('nom', 'N/A')
            user['email'] = user.get('email', 'N/A')
        return users_json

    def add_user(self, token, user):
        return self.client.service.addUser(token, user['prenom'], user['nom'], user['email'], user['mot_de_passe'], user['type'])

    def delete_user(self, token, user_id):
        return self.client.service.deleteUser(token, user_id)

    def update_user(self, token, user):
        return self.client.service.modifyUser(token, user['id'], user['prenom'], user['nom'], user['email'], user['mot_de_passe'], user['type'])
