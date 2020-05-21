import os
from threading import Thread

from offstack.constants import CURRDIR
from offstack.logger import logger

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import  GObject as gobject

class DialogView:
    def __init__(self, interface, queue, Gtk):
        interface.add_from_file(os.path.join(CURRDIR, "resources/dialog_window.glade"))
        
        interface.connect_signals({
            "close_dialog_button_clicked": self.close_dialog_button_clicked,
            "MessageDialog_delete_event": self.MessageDialog_delete_event,
        })

        self.messagedialog_window = interface.get_object("MessageDialog")
        self.dialog_header = interface.get_object("dialog_header")
        self.primary_text_title = interface.get_object("primary_text_title")
        self.message_dialog_spinner = interface.get_object("message_dialog_spinner")

        self.close_dialog_button = interface.get_object("close_dialog_button")
        
        self.interface = interface
        self.queue = queue
        self.interface = interface
        self.gtk = Gtk

        thread = Thread(target=self.listener)
        thread.daemon = True
        thread.start()

    def listener(self):
        while True:
            kwargs = self.queue.get()

            try:
                if "display" in kwargs.get("action"):
                    # self.display_dialog(**kwargs)
                    gobject.idle_add(self.display, kwargs)
                    self.queue.task_done()
                if "update" in kwargs.get("action"):
                    # self.update_dialog(**kwargs)
                    gobject.idle_add(self.update, kwargs)
                    self.queue.task_done()

                if "hide" in kwargs.get("action"):
                    # self.hide_dialog()
                    gobject.idle_add(self.hide)
                    self.queue.task_done()
                    
                if "hide_spinner" in kwargs.get("action"):
                    # self.hide_spinner()
                    gobject.idle_add(self.hide_spinner)
                    self.queue.task_done()
            except TypeError:
                logger.debug(">>> Error occurs due to testing.") 

    def display(self, kwargs):
        self.close_dialog_button.show()
        self.message_dialog_spinner.hide()
        self.dialog_header.hide()

        if "header" in kwargs:
            self.dialog_header.set_markup(kwargs.get("header")) 
            self.dialog_header.show()

        if "label" in kwargs:
            self.primary_text_title.set_markup(kwargs.get("label")) 

        if "spinner" in kwargs and kwargs.get("spinner"):
            self.message_dialog_spinner.show()

        if "hide_close_button" in kwargs and kwargs.get("hide_close_button"):
            self.close_dialog_button.hide()
            self.messagedialog_window.connect("destroy", self.gtk.main_quit)
        
        self.messagedialog_window.show()

    def update(self, kwargs):
        self.close_dialog_button.show()
        self.message_dialog_spinner.hide()
        self.dialog_header.hide()

        if "header" in kwargs:
            self.dialog_header.set_markup(kwargs.get("header")) 
            self.dialog_header.show()

        if "label" in kwargs:
            self.primary_text_title.set_markup(kwargs.get("label")) 

        if "spinner" in kwargs and kwargs.get("spinner"):
            self.message_dialog_spinner.show()

        if "hide_close_button" in kwargs and kwargs.get("hide_close_button"):
            self.close_dialog_button.hide()
            self.messagedialog_window.connect("destroy", self.gtk.main_quit)            

    def hide_spinner(self):
        self.message_dialog_spinner.hide()

    def hide(self):
        self.messagedialog_window.hide()

    def close_dialog_button_clicked(self, button):
        """Button/Event handler to close message dialog.
        """
        self.interface.get_object("MessageDialog").hide()
        
    # To avoid getting the MessageDialog destroyed and not being re-rendered again
    def MessageDialog_delete_event(self, window, event):
        """On Delete handler is used to hide the dialog and so that it successfully renders next time it is called
        
        -Returns:Boolean
        - It needs to return True, otherwise the content will not re-render after closing the window
        """
        if window.get_property("visible") is True:
            window.hide()
            return True

                