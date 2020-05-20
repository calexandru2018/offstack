import os
import time
from concurrent import futures

# from offstack.dashboard_window import display_dashboard
from offstack.managers import oAuthManager, DriverManager
from offstack.utils import request_access_token, check_user_credentials
from offstack.logger import logger
from offstack.constants import (
    CLIENT_ID,
    CLIENT_SECRET,
    REDIRECT_URI,
    SCOPE,
    VERSION,
    USERDATA,
    CURRDIR,
    SUB_MAIN_LABEL_TEXT
)

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import  GObject as obj

class LoginView:
    def __init__(self, interface, queue, Gtk, login_presenter):
        interface.add_from_file(os.path.join(CURRDIR, "resources/login_window.glade"))
        interface.connect_signals({
            "login_button_clicked": self.login_button_clicked,
            "need_help_login_label_clicked": self.need_help_login_label_clicked,
        })
        self.set_objects(interface, queue, Gtk, login_presenter)

    def display(self):
        self.login_view.show()

    def set_objects(self, interface, queue, Gtk,login_presenter):
        self.interface = interface
        self.queue = queue
        self.gtk = Gtk
        self.login_presenter = login_presenter

        self.login_view = interface.get_object("LoginWindow")
        self.login_view.connect("destroy", Gtk.main_quit)
        self.login_sub_label = interface.get_object("login_sub_label")
        self.login_sub_label.set_text(SUB_MAIN_LABEL_TEXT)
        self.login_version_label = interface.get_object("login_version_label")
        self.login_version_label.set_text("v.{}".format(VERSION))
        self.popover = self.interface.get_object("need_help_popover_menu")

        self.email_field = self.interface.get_object('login_username_entry')
        self.password_field = self.interface.get_object('password_username_entry')
   
    def login_button_clicked(self, button):
        self.queue.put(dict(action="display", header="Initializing Profile", label="Starting profile initialization...", spinner=True, hide_close_button=True))
        
        with futures.ThreadPoolExecutor(max_workers=1) as executor:
            var_dict = dict(
                        username_field=self.email_field.get_text().strip(), 
                        password_field=self.password_field.get_text().strip(),
            )
            future = executor.submit(self.login_presenter.on_initialize_profile, **var_dict)
            return_value = future.result()
            print("futures result: ", return_value)
        
        # if return_value:
        #     self.login_view.hide()
        #     self.dashboard_view.display_window()

        # thread = Thread(target=save_access_token, args=[ email, password])
        #     thread.daemon = True
        #     thread.start()
        # if not len(email) == 0 and not len(password) == 0:          
        #     thread = Thread(target=save_access_token, args=[self.interface, self.Firefox, self.browser_opts, self.OAuth2Session, email, password, self.queue, self.gtk])
        #     thread.daemon = True
        #     thread.start()
        # else:
        #     print("some of the fields were left empty")

    def need_help_login_label_clicked(self, label, link):
        self.popover.show()


