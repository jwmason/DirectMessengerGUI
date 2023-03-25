# Mason Wong
# masonjw1@uci.edu
# 48567424

"""This module is in charge of the GUI"""

import tkinter as tk
import json
from tkinter import ttk
from tkinter import simpledialog as sd
import pathlib
from ds_messenger import DirectMessenger
from Profile import Profile


class Body(tk.Frame):
    """This is the body of the GUI"""
    def __init__(self, root, recipient_selected_callback=None):
        """This sets attributes"""
        tk.Frame.__init__(self, root)
        self.root = root
        self._contacts = [str]
        self._select_callback = recipient_selected_callback
        # After all initialization is complete,
        # call the _draw method to pack the widgets
        # into the Body instance
        self.configure(background="#F0F0F0")
        self._draw()

    def node_select(self, event):
        """This selects node"""
        index = int(self.posts_tree.selection()[0])
        entry = self._contacts[index]
        if self._select_callback is not None:
            self._select_callback(entry)

    def insert_contact(self, contact: str):
        """This inserts contact"""
        self._contacts.append(contact)
        id = len(self._contacts) - 1
        self._insert_contact_tree(id, contact)

    def _insert_contact_tree(self, identifer, contact: str):
        """This inserts contact tree"""
        if len(contact) > 25:
            entry = contact[:24] + "..."
        identifer = self.posts_tree.insert('', identifer, identifer, text=contact)

    def insert_user_message(self, message: str):
        """This inserts user message"""
        self.entry_editor.insert(1.0, message + '\n', 'entry-right')

    def insert_contact_message(self, message: str):
        """This inserts contact message"""
        self.entry_editor.insert(1.0, message + '\n', 'entry-left')

    def get_text_entry(self) -> str:
        """This gets text entry"""
        return self.message_editor.get('1.0', 'end').rstrip()

    def set_text_entry(self, text: str):
        """This sets text entry"""
        self.message_editor.delete(1.0, tk.END)
        self.message_editor.insert(1.0, text)

    def _draw(self):
        """This draws it to GUI"""
        posts_frame = tk.Frame(master=self, width=250, background='blue')
        posts_frame.pack(fill=tk.BOTH, side=tk.LEFT)

        self.posts_tree = ttk.Treeview(posts_frame)
        self.posts_tree.bind("<<TreeviewSelect>>", self.node_select)
        self.posts_tree.pack(fill=tk.BOTH, side=tk.TOP,
                             expand=True, padx=5, pady=5)

        entry_frame = tk.Frame(master=self, bg="")
        entry_frame.pack(fill=tk.BOTH, side=tk.TOP, expand=True)

        editor_frame = tk.Frame(master=entry_frame, bg="red")
        editor_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)

        scroll_frame = tk.Frame(master=entry_frame, bg="", width=10)
        scroll_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=False)

        message_frame = tk.Frame(master=self, bg="yellow")
        message_frame.pack(fill=tk.BOTH, side=tk.TOP, expand=False)

        self.message_editor = tk.Text(message_frame, width=0, height=5)
        self.message_editor.pack(fill=tk.BOTH, side=tk.LEFT,
                                 expand=True, padx=0, pady=0)

        self.entry_editor = tk.Text(editor_frame, width=0, height=5)
        self.entry_editor.tag_configure('entry-right', justify='right')
        self.entry_editor.tag_configure('entry-left', justify='left')
        self.entry_editor.pack(fill=tk.BOTH, side=tk.LEFT,
                               expand=True, padx=0, pady=0)

        entry_editor_scrollbar = tk.Scrollbar(master=scroll_frame,
                                              command=self.entry_editor.yview)
        self.entry_editor['yscrollcommand'] = entry_editor_scrollbar.set
        entry_editor_scrollbar.pack(fill=tk.Y, side=tk.LEFT,
                                    expand=False, padx=0, pady=0)


class Footer(tk.Frame):
    """This is class footer for buttons"""
    def __init__(self, root, send_callback=None):
        """This initiates attributes"""
        tk.Frame.__init__(self, root)
        self.root = root
        self._send_callback = send_callback
        self._draw()

    def send_click(self):
        """What happens if clicked"""
        if self._send_callback is not None:
            self._send_callback()

    def _draw(self):
        """Draws to GUI"""
        save_button = tk.Button(master=self,
                                text="Send", width=20,
                                command=self.send_click)
        # You must implement this.
        # Here you must configure the button to bind its click to
        # the send_click() function.
        save_button.pack(fill=tk.BOTH, side=tk.RIGHT, padx=5, pady=5)
        self.footer_label = tk.Label(master=self, text="Ready.")
        self.footer_label.pack(fill=tk.BOTH, side=tk.LEFT, padx=5)


class NewContactDialog(tk.simpledialog.Dialog):
    """Class for new contact"""
    def __init__(self, root, title=None, user=None, pwd=None, server=None):
        """Sets attributes"""
        self.root = root
        self.server = server
        self.user = user
        self.pwd = pwd
        super().__init__(root, title)

    def body(self, frame):
        """Sets body"""
        self.server_label = tk.Label(frame, width=30, text="DS Server Address")
        self.server_label.pack()
        self.server_entry = tk.Entry(frame, width=30)
        self.server_entry.insert(tk.END, self.server)
        self.server_entry.pack()

        self.username_label = tk.Label(frame, width=30, text="Username")
        self.username_label.pack()
        self.username_entry = tk.Entry(frame, width=30)
        self.username_entry.insert(tk.END, self.user)
        self.username_entry.pack()

        # You need to implement also the region for the user to enter
        # the Password. The code is similar to the Username you see above
        # but you will want to add self.password_entry['show'] = '*'
        # such that when the user types, the only thing that appears are
        # * symbols.
        # self.password...

        self.password_label = tk.Label(frame, width=30, text="Password")
        self.password_label.pack()
        self.password_entry = tk.Entry(frame, width=30, show='*')
        self.password_entry.insert(tk.END, self.pwd)
        self.password_entry.pack()

    def apply(self):
        """Gets entries"""
        self.user = self.username_entry.get()
        self.pwd = self.password_entry.get()
        self.server = self.server_entry.get()


class MainApp(tk.Frame):
    """This is the main app interface"""
    def __init__(self, root):
        """This sets attributes"""
        tk.Frame.__init__(self, root)
        self.root = root
        self.username = sd.askstring('Login', 'Enter username (can create one):')
        self.password = sd.askstring('Login', 'Enter password (can create one):', show='*')
        self.server = sd.askstring('Login',
                                   'Enter Server IP:')
        if not self.server:
            self.server = None
        self.recipient = None
        # You must implement this! You must configure and
        # instantiate your DirectMessenger instance after this line.
        # self.direct_messenger = ... continue!
        self.direct_messenger = DirectMessenger(self.server,
                                                self.username, self.password)
        file_path = pathlib.Path.cwd()
        file_name = f'{self.username}.dsu'
        self.current_file_path = file_path / file_name
        self.current_file_path = pathlib.Path(self.current_file_path)
        if self.current_file_path.exists():
            self.profile = Profile()
            self.profile.load_profile(self.current_file_path)
        else:
            self.profile = Profile(self.username, self.password)
            with open(self.current_file_path, 'x') as f:
                pass
        with open(self.current_file_path, 'w') as f:
            self.direct_messenger_local = DirectMessenger('168.235.86.101', self.username, self.password)
            content = self.direct_messenger_local.retrieve_all()
            content_dict = json.loads(content)
            for message in content_dict['response']['messages']:
                self.profile._messages.append(message)
            for message in self.profile.sent_messages:
                if self.recipient == message['recipient']:
                    self.profile.sent_messages.append(message['message'])
        self.profile.save_profile(pathlib.Path(self.current_file_path))
        # After all initialization is complete,
        # call the _draw method to pack the widgets
        # into the root frame
        self._draw()
        self.check_all()

    def send_message(self):
        """sends a message to user"""
        # You must implement this!
        message = self.body.get_text_entry()
        if message and self.recipient:
            success = self.direct_messenger.send(message, self.recipient)
            self.profile.sent_messages.append(
                {'recipient': self.recipient, 'message': message})
            self.profile.save_profile(pathlib.Path(self.current_file_path))
            if success:
                self.body.insert_user_message(message)
                self.body.set_text_entry("")

    def add_contact(self):
        """Adds a contact"""
        name = sd.askstring('Add Contact',
                            'Enter the name of the new contact:')
        if name and name not in self.profile.friends:
            self.profile.friends.append(name)
            self.body.insert_contact(name)

    def recipient_selected(self, recipient):
        """Selects a recipient"""
        self.recipient = recipient
        if self.recipient is not None:
            self.check_all()

    def configure_server(self):
        """Configures server for new account"""
        new_user = NewContactDialog(self.root, "Configure Account",
                              self.username, self.password, self.server)
        self.username = new_user.user
        self.password = new_user.pwd
        self.server = new_user.server
        self.direct_messenger = DirectMessenger(self.server, self.username, self.password)
        self.profile = Profile(self.username, self.password)
        file_path = pathlib.Path.cwd()
        file_name = f'{self.username}.dsu'
        self.current_file_path = file_path / file_name
        if self.current_file_path.exists():
            self.profile = Profile(self.username, self.password)
            self.profile.load_profile(self.current_file_path)
        else:
            self.profile = Profile(self.username, self.password)
            with open(self.current_file_path, 'x') as f:
                pass
        with open(self.current_file_path, 'w') as f:
            self.direct_messenger_local = DirectMessenger('168.235.86.101', self.username, self.password)
            content = self.direct_messenger_local.retrieve_all()
            content_dict = json.loads(content)
            for message in content_dict['response']['messages']:
                self.profile._messages.append(message)
        my_list = self.body.posts_tree.get_children()
        self.check_all()
        self.body.entry_editor.delete('1.0', tk.END)
        self.profile.save_profile(self.current_file_path)
        for item in my_list:
            self.body.posts_tree.delete(*f'{item}')

    def check_new(self):
        """Checks new messages"""
        new_messages = self.direct_messenger.retrieve_new()
        new_messages = json.loads(new_messages)
        new_messages = new_messages['response']['messages']
        for message in new_messages:
            contact = str(message['from'])
            if contact not in self.profile.friends:
                self.profile.friends.append(contact)
                self.profile.save_profile(self.current_file_path)
                self.body.insert_contact(str(message['from']))
        self.root.after(1000, self.check_new)

    def check_all(self):
        """Checks old messages"""
        self.body.entry_editor.delete('1.0', tk.END)
        old_messages = self.get_local_list()
        if self.recipient is None:
            for i in range(len(old_messages)):
                self.contact = old_messages[i]['from']
                if self.contact not in self.profile.friends:
                    self.body.insert_contact(self.contact)
                    self.profile.friends.append(self.contact)
        for i in range(len(old_messages)):
            self.contact = old_messages[i]['from']
            if self.contact == self.recipient:
                if self.contact not in self.profile.friends:
                    self.body.insert_contact(self.contact)
                    self.profile.friends.append(self.contact)
                self.body.insert_contact_message(old_messages[i]['message'])
        self.profile.load_profile(pathlib.Path(self.current_file_path))
        for message in self.profile.sent_messages:
            if self.recipient == message['recipient']:
                self.body.insert_user_message(message['message'])
        self.profile.save_profile(self.current_file_path)

    def get_local_list(self):
        """Gets local list for old messages"""
        self.profile.load_profile(pathlib.Path(self.current_file_path))
        my_list = self.profile._messages
        my_dicts = []
        for item in my_list:
            message = item['message']
            sender = item['from']
            my_dicts.append({'message': message, 'from': sender})

        return my_dicts

    def _draw(self):
        """Builds a menu and adds it to the root frame."""
        menu_bar = tk.Menu(self.root)
        self.root['menu'] = menu_bar
        menu_file = tk.Menu(menu_bar)

        menu_bar.add_cascade(menu=menu_file, label='File')
        menu_file.add_command(label='New')
        menu_file.add_command(label='Open...')
        menu_file.add_command(label='Close')

        settings_file = tk.Menu(menu_bar)
        menu_bar.add_cascade(menu=settings_file, label='Settings')
        settings_file.add_command(label='Add Contact',
                                  command=self.add_contact)
        settings_file.add_command(label='Configure DS Server',
                                  command=self.configure_server)

        # The Body and Footer classes must be initialized and
        # packed into the root window.
        self.body = Body(self.root,
                         recipient_selected_callback=self.recipient_selected)
        self.body.pack(fill=tk.BOTH, side=tk.TOP, expand=True)
        self.footer = Footer(self.root, send_callback=self.send_message)
        self.footer.pack(fill=tk.BOTH, side=tk.BOTTOM)


def run():
    """Runs the program"""
    main = tk.Tk()
    main.title("ICS 32 Distributed Social Messenger")
    main.geometry("720x480")
    main.option_add('*tearOff', False)
    app = MainApp(main)
    main.update()
    main.minsize(main.winfo_width(), main.winfo_height())
    identifer = main.after(2000, app.check_new)
    print(identifer)
    main.mainloop()
