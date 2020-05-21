import os
from threading import Thread
from offstack.logger import logger
from offstack.constants import VERSION,CURRDIR

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import GObject as gobject

class DashboardView():
    def __init__(self, interface, queue, Gtk, dashboard_presenter):
        interface.add_from_file(os.path.join(CURRDIR, "resources/dashboard_window.glade"))
        interface.connect_signals({
            "search_entry_key_release_event": self.search_entry_key_release_event,
            "QuestionsTreeView_cursor_changed": self.QuestionsTreeView_cursor_changed,
        })
        self.set_objects(interface, queue, Gtk, dashboard_presenter)
    
    def display(self):
        self.dashboard_window.connect("destroy", self.gtk.main_quit)

        thread = Thread(target=self.dashboard_presenter.populate_on_load, args=[self.questions_list_store])
        thread.daemon = True
        thread.start()

        gobject.idle_add(self.dashboard_window.show)

    def set_objects(self, interface, queue, Gtk, dashboard_presenter):
        self.interface = interface
        self.queue = queue
        self.gtk = Gtk
        self.dashboard_presenter = dashboard_presenter

        self.dashboard_window = self.interface.get_object("DashboardWindow")
        self.question_textview = self.interface.get_object("question_textview")
        self.answers_textview = self.interface.get_object("answers_textview")
        self.questions_list_store = self.interface.get_object("QuestionsListStore")
        self.dashboard_version_label = self.interface.get_object("dashboard_version_label")
        self.dashboard_version_label.set_text("v.{}".format(VERSION))

    def search_entry_key_release_event(self, entry, event):
        """Event handler, to filter servers after each key release"""
        user_filter_by = entry.get_text()
        server_tree_store = self.interface.get_object("QuestionsListStore")
        tree_view_object = self.interface.get_object("QuestionsTreeView")

        # Creates a new filter from a ListStore/TreeStore
        n_filter = server_tree_store.filter_new()

        # set_visible_func:
        # first_param: filter function
        # seconde_param: input to filter by
        n_filter.set_visible_func(self.column_filter, data=[self.interface, user_filter_by])
        
        # Apply the filter model to a TreeView
        tree_view_object.set_model(n_filter)

        # Updates the ListStore model
        n_filter.refilter()

    def column_filter(self, model, iterator, data=None):
        """Filter by columns and returns the corresponding rows"""
        interface = data[0]
        data = data[1].lower()
        treeview = interface.get_object("QuestionsTreeView")

        cols = treeview.get_n_columns()
        tags = model.get_value(iterator, 4).split(";")
        tags = [tag.strip().lower() for tag in tags]

        question_title = model.get_value(iterator, 1).lower()
        
    
        if len(data) > 0 and data[0] == ":":
            keys = data[1:].split()
            keys = [key.lower() for key in keys]

            if any(tag.startswith(tuple(keys)) for tag in tags):
                return True
        elif len(data) and any(tag.startswith(data) for tag in tags) or data in question_title:
            return True

    def QuestionsTreeView_cursor_changed(self, listview):
        # Get the selected server
        (model, pathlist) = listview.get_selection().get_selected_rows()

        for path in pathlist :
            tree_iter = model.get_iter(path)
            # the second param of get_value() specifies the column number, starting at 0
            question_id = model.get_value(tree_iter, 0)
            self.dashboard_presenter.load_content(question_id, self.question_textview, self.answers_textview)
            
