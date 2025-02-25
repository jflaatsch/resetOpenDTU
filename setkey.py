import keyring

service_name = 'OpenDTU'
username = 'admin'
password = 'changed' #TODO:: change this to the actual password when needed

keyring.set_password(service_name, 'username', username)
keyring.set_password(service_name, 'password', password)
print(f'Password for {service_name} set for {username}')