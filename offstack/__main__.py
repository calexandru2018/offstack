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

from offstack.logger import logger
from offstack.constants import CONFIG_DIR, USERDATA, CURRDIR
from offstack.utils import check_user_credentials

from offstack.views.login_view import LoginView
from offstack.views.dialog_view import DialogView

from offstack.presenters.login_presenter import LoginPresenter

from offstack.services.login_service import LoginService

def init():
    queue = Queue()
    interface = Gtk.Builder()

    # Apply CSS
    style_provider = Gtk.CssProvider()
    style_provider.load_from_path(os.path.join(CURRDIR, "resources/main.css"))

    Gtk.StyleContext.add_provider_for_screen(
        Gdk.Screen.get_default(),
        style_provider,
        Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
    )
    
    dialog_view = DialogView(interface, queue, Gtk)

    login_presenter = LoginPresenter(queue, LoginService())
    login_view = LoginView(interface, queue, Gtk, login_presenter)
    login_view.display()

    # if not check_user_credentials(): 
    #     display_login(interface, OAuth2Session, Firefox, opts, queue, Gtk)
    # else:
    #     display_dashboard(interface, OAuth2Session, Firefox, opts, queue, Gtk)

    Gtk.main()