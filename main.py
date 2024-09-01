__version__ = 'prototype'
import kivy
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.widget import Widget
from tgtg import TgtgClient

from tgtg_item import TgtgItem


class TgtgApp(App):
    '''Entry point of the application'''
    CONFIGURATION_FILE = 'config.txt'

    def build(self):
        self._load_app_configuration()
        self.mainpage = MainPage()
        return self.mainpage
    
    def _load_app_configuration(self):
        '''Load the configuration of the application from its config file '''
        with open(self.CONFIGURATION_FILE, 'r') as file:
            self.config = {
                'email': None,
                'access_token': None,
                'refresh_token': None,
                'user_id': None,
                'cookie': None,
                'notification_on':False,
                'favorite_only': False,
            }
            for line in file:
                key, value = line.split('\n')[0].split(':')
                self.config[key] = value
    
    def _update_config_file(self):
        '''Update the configuration file'''
        with open(self.CONFIGURATION_FILE, 'w') as file:
            for key, value in self.config.items():
                file.write('{}:{}\n'.format(key, value))

    # Methods
    def is_connected(self):
        '''Check if the user is connected'''
        return self.config['email'] != "None"
    
    def is_notification_on(self):
        '''Check if the notification is on'''
        return self.config['notification_on']
    
    def is_favorite_only(self):
        '''Check if the favorite only is on'''
        return self.config['favorite_only']
    
    def save_credentials(self, credentials):
        '''Get and write the credentials'''
        
        self.config['access_token'] = credentials['access_token']
        self.config['refresh_token'] = credentials['refresh_token']
        self.config['user_id'] = credentials['user_id']
        self.config['cookie'] = credentials['cookie']
        self.update()

    # Actions
    def login(self, email):
        '''Login the user'''
        try:
            self.display_mail_verification_message(email)
            self.client = TgtgClient(email=email)
            credentials = self.client.get_credentials()
            self.config['email'] = email
            for key, value in credentials.items():
                self.config[key] = value
            self.update()
            return True
        except:
            print('The login failed')
            return False

        
    def display_mail_verification_message(self, email):
        print('A link has been sent to {}. Please confirm the connection.'.format(email))
        self.popup = Popup(title='eMail verification',
                      content=Label(text='A link has been sent to {}. Please confirm the connection.'.format(email)),
                      size_hint=(None, None), size=(400, 400))
        self.popup.open()

    def logout(self):
        '''Logout the user'''
        self.config['email'] = None
        self.config['access_token'] = None
        self.config['refresh_token'] = None
        self.config['user_id'] = None
        self.config['cookie'] = None
        self.update()

    def flip_notification_on(self):
        '''Flip the notification status'''
        self.config['notification_on'] = not self.config['notification_on']
        self.update()

    def flip_favorite_only(self):
        '''Flip the favorite only status'''
        self.config['favorite_only'] = not self.config['favorite_only']
        self.update()

    def update(self):
        '''Update the application'''
        self._update_config_file()
        self.mainpage.ids['login_button'].update()
        self.mainpage.ids['item_list'].update()
        
class MainPage(BoxLayout):
    '''Main page of the application'''
    pass

class Header(AnchorLayout):
    '''Header of the application'''
    pass

class InfoPopUp(Popup):
    '''Pop-up to display information'''
    def get_info(self):
        '''Get the information'''
        with open('info.txt', 'r') as file:
            return file.read()
        

class LoginButton(Button):
    '''Button to login'''
    def __init__(self, **kwargs):
        super(LoginButton, self).__init__(**kwargs)
        self.app = App.get_running_app()
        if self.app.is_connected():
            self.text = 'se déconnecter'
        else:
            self.text = 'se connecter'
    
    def on_press(self):
        print(self.app.mainpage.children)
        if self.app.is_connected():
            self.app.logout()
        else:
            self.showLoginPopUp()

    def update(self):
        if self.app.is_connected():
            self.text = 'se déconnecter'
        else:
            self.text = 'se connecter'

    def showLoginPopUp(self):
        login_popup = LoginPopUp()
        login_popup.open()

class LoginPopUp(Popup):
    '''Pop-up to login'''
    pass

class LoginForm(GridLayout):
    pass
        

class ButtonGrid(GridLayout):
    '''Button grid of the application'''
    def info(self):
        '''Display information'''
        info_popup = InfoPopUp()
        info_popup.open()

class Item(BoxLayout):
    '''Item of the list'''
    def __init__(self, item:TgtgItem, **kwargs):
        super(Item, self).__init__(**kwargs)
        self.item = item
        self.ids['name'].text = item.name
        self.ids['hour'].text = str(item.start_time)
        self.ids['price'].text = str(item.price/100) + "€"
    

class ItemList(BoxLayout):
    '''List of items'''
    def __init__(self, **kwargs):
        super(ItemList, self).__init__(**kwargs)
        self.app = App.get_running_app()
        self.items = []
        self.update()

    def update(self):
        if self.app.is_connected():
            self.client = TgtgClient(access_token=self.app.config['access_token'],
                                    refresh_token=self.app.config['refresh_token'],
                                    user_id=self.app.config['user_id'],
                                    cookie=self.app.config['cookie'])
            self.items = []
            self.clear_widgets()
            self.get_items()
            for item in self.items:
                self.add_widget(Item(item))

    
    def get_items(self):
        '''Get the items'''
        if self.app.is_favorite_only():
            api_response = self.client.get_items(favorites_only=False, with_stock_only=True, longitude= 1.0933836, latitude=49.4427202, radius=10)
        else:
            api_response = self.client.get_items(with_stock_only=False,longitude= 1.0933836, latitude= 49.4427202)
        print(api_response)
        for item in api_response:
            self.items.append(TgtgItem(item))
        return self.items
    
if __name__ == '__main__':
    TgtgApp().run()