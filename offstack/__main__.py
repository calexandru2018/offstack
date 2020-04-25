import os
from queue import Queue

from requests_oauthlib import OAuth2Session
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
opts = Options()
opts.headless = True
opts.add_argument('--no-sandbox')
assert opts.headless  # Operating in headless mode

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import  Gtk, Gdk, GObject

from .logger import logger
from .constants import CONFIG_DIR, USERDATA, CURRDIR
from .utils import check_user_credentials

from .login_window import LoginHandlers
from .dialog_window import DialogHandlers
from .dashboard_window import DashboardHandlers

def init():
    queue = Queue()
    interface = Gtk.Builder()

    # Apply CSS
    style_provider = Gtk.CssProvider()
    style_provider.load_from_path(CURRDIR+"/resources/main.css")

    Gtk.StyleContext.add_provider_for_screen(
        Gdk.Screen.get_default(),
        style_provider,
        Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
    )

    interface.add_from_file(CURRDIR+"/resources/dialog_window.glade")
    interface.connect_signals(DialogHandlers(interface, queue))
    
    if not check_user_credentials(): 
        interface.add_from_file(CURRDIR+"/resources/login_window.glade")
        login_window = interface.get_object("LoginWindow")
        interface.connect_signals(LoginHandlers(interface, OAuth2Session, Firefox, opts, queue))

        login_window.show()
    else:
        interface.add_from_file(CURRDIR+"/resources/dashboard_window.glade")
        dashboard_window = interface.get_object("DashboardWindow")
        interface.connect_signals(DashboardHandlers(interface, OAuth2Session, Firefox, opts, queue))
        
        dashboard_window.show()

    Gtk.main()