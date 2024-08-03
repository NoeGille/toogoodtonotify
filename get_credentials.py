from tgtg import TgtgClient

client = TgtgClient(email="noe.gille76@gmail.com")
credentials = client.get_credentials()
file = open('token.txt', 'w')
file.write('access_token:{}\n'.format(credentials['access_token']))
file.write('refresh_token:{}\n'.format(credentials['refresh_token']))
file.write('user_id:{}\n'.format(credentials['user_id']))
file.write('cookie:{}\n'.format(credentials['cookie']))
file.close()

