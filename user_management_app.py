class UserManagementApp:
    def __init__(self, soap_client, rest_client):
        self.soap_client = soap_client
        self.rest_client = rest_client
        self.token = None

    def run(self):
        email = input("Enter email: ")
        password = input("Enter password: ")

        self.token = self.soap_client.authenticate(email, password)

        if self.token:
            print("Authenticated successfully.")
            self.show_menu()
        else:
            print("Authentication failed.")

    def show_menu(self):
        while True:
            print("\nMenu:")
            print("1. List Users")
            print("2. Add User")
            print("3. Delete User")
            print("4. Update User")
            print("5. List Articles (REST)")
            print("6. Exit")
            choice = input("Enter choice: ")

            if choice == '1':
                self.list_users()
            elif choice == '2':
                self.add_user()
            elif choice == '3':
                self.delete_user()
            elif choice == '4':
                self.update_user()
            elif choice == '5':
                self.list_articles()
            elif choice == '6':
                break
            else:
                print("Invalid choice.")

    def list_users(self):
        users = self.soap_client.list_users(self.token)
        for user in users:
            print(user)

    def add_user(self):
        name = input("Enter name: ")
        email = input("Enter email: ")
        password = input("Enter password: ")
        user = {'name': name, 'email': email, 'password': password}
        self.soap_client.add_user(self.token, user)
        print("User added.")

    def delete_user(self):
        user_id = input("Enter user ID to delete: ")
        self.soap_client.delete_user(self.token, user_id)
        print("User deleted.")

    def update_user(self):
        user_id = input("Enter user ID to update: ")
        name = input("Enter new name: ")
        email = input("Enter new email: ")
        password = input("Enter new password: ")
        user = {'id': user_id, 'name': name, 'email': email, 'password': password}
        self.soap_client.update_user(self.token, user)
        print("User updated.")

    def list_articles(self):
        articles = self.rest_client.get_all_articles()
        for article in articles:
            print(article)
