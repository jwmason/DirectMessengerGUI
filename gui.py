import tkinter as tk
import json
from tkinter import ttk, filedialog, simpledialog
from typing import Text
from ds_messenger import DirectMessenger
from Profile import Profile
import pathlib
import os.path


class Body(tk.Frame):
    def __init__(self, root, recipient_selected_callback=None):
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
        index = int(self.posts_tree.selection()[0])
        entry = self._contacts[index]
        if self._select_callback is not None:
            self._select_callback(entry)

    def insert_contact(self, contact: str):
        self._contacts.append(contact)
        id = len(self._contacts) - 1
        self._insert_contact_tree(id, contact)

    def _insert_contact_tree(self, id, contact: str):
        if len(contact) > 25:
            entry = contact[:24] + "..."
        id = self.posts_tree.insert('', id, id, text=contact)

    def insert_user_message(self, message:str):
        self.entry_editor.insert(1.0, message + '\n', 'entry-right')

    def insert_contact_message(self, message:str):
        self.entry_editor.insert(1.0, message + '\n', 'entry-left')

    def get_text_entry(self) -> str:
        return self.message_editor.get('1.0', 'end').rstrip()

    def set_text_entry(self, text:str):
        self.message_editor.delete(1.0, tk.END)
        self.message_editor.insert(1.0, text)

    def _draw(self):
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
    def __init__(self, root, send_callback=None):
        tk.Frame.__init__(self, root)
        self.root = root
        self._send_callback = send_callback
        self._draw()

    def send_click(self):
        if self._send_callback is not None:
            self._send_callback()

    def _draw(self):
        save_button = tk.Button(master=self, text="Send", width=20, command=self.send_click)
        # You must implement this.
        # Here you must configure the button to bind its click to
        # the send_click() function.
        save_button.pack(fill=tk.BOTH, side=tk.RIGHT, padx=5, pady=5)
        self.footer_label = tk.Label(master=self, text="Ready.")
        self.footer_label.pack(fill=tk.BOTH, side=tk.LEFT, padx=5)


class NewContactDialog(tk.simpledialog.Dialog):
    def __init__(self, root, title=None, user=None, pwd=None, server=None):
        self.root = root
        self.server = server
        self.user = user
        self.pwd = pwd
        super().__init__(root, title)

    def body(self, frame):
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
        #self.password...

        self.password_label = tk.Label(frame, width=30, text="Password")
        self.password_label.pack()
        self.password_entry = tk.Entry(frame, width=30, show='*')
        self.password_entry.insert(tk.END, self.pwd)
        self.password_entry.pack()

    def apply(self):
        self.user = self.username_entry.get()
        self.pwd = self.password_entry.get()
        self.server = self.server_entry.get()


class MainApp(tk.Frame):
    def __init__(self, root):
        tk.Frame.__init__(self, root)
        self.root = root
        self.username = simpledialog.askstring('Login', 'Enter username (can create one):')
        self.password = simpledialog.askstring('Login', 'Enter password (can create one):', show='*')
        self.server = simpledialog.askstring('Login', 'Enter Server IP:')
        if not self.server:
            self.server = None
        self.recipient = None
        # You must implement this! You must configure and
        # instantiate your DirectMessenger instance after this line.
        #self.direct_messenger = ... continue!
        self.direct_messenger = DirectMessenger(self.server, self.username, self.password)
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
        # You must implement this!
        message = self.body.get_text_entry()
        if message and self.recipient:
            success = self.direct_messenger.send(message, self.recipient)
            self.profile.sent_messages.append({'recipient': self.recipient, 'message': message})
            self.profile.save_profile(pathlib.Path(self.current_file_path))
            if success:
                self.body.insert_user_message(message)
                self.body.set_text_entry("")

    def add_contact(self):
        # You must implement this!
        # Hint: check how to use tk.simpledialog.askstring to retrieve
        # the name of the new contact, and then use one of the body
        # methods to add the contact to your contact list
        name = simpledialog.askstring('Add Contact', 'Enter the name of the new contact:')
        if name and name not in self.profile.friends:
            self.profile.friends.append(name)
            self.body.insert_contact(name)

    def recipient_selected(self, recipient):
        self.recipient = recipient
        if self.recipient is not None:
            self.check_all()

    def configure_server(self):
        ud = NewContactDialog(self.root, "Configure Account",
                              self.username, self.password, self.server)
        self.username = ud.user
        self.password = ud.pwd
        self.server = ud.server
        # You must implement this!
        # You must configure and instantiate your
        # DirectMessenger instance after this line.
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
        # You must implement this!
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
        self.body.entry_editor.delete('1.0', tk.END)
        # old_messages = self.direct_messenger.retrieve_all()
        # old_messages = json.loads(old_messages)
        # old_messages = old_messages['response']['messages']
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
        self.profile.load_profile(pathlib.Path(self.current_file_path))
        my_list = self.profile._messages
        my_dicts = []
        for item in my_list:
            message = item['message']
            sender = item['from']
            my_dicts.append({'message': message, 'from': sender})
        
        return my_dicts

    def _draw(self):
        # Build a menu and add it to the root frame.
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
    # All Tkinter programs start with a root window. We will name ours 'main'.
    main = tk.Tk()

    # 'title' assigns a text value to the Title Bar area of a window.
    main.title("ICS 32 Distributed Social Messenger")

    # This is just an arbitrary starting point. You can change the value
    # around to see how the starting size of the window changes.
    main.geometry("720x480")

    # adding this option removes some legacy behavior with menus that
    # some modern OSes don't support. If you're curious, feel free to comment
    # out and see how the menu changes.
    main.option_add('*tearOff', False)

    # Initialize the MainApp class, which is the starting point for the
    # widgets used in the program. All of the classes that we use,
    # subclass Tk.Frame, since our root frame is main, we initialize
    # the class with it.
    app = MainApp(main)

    # When update is called, we finalize the states of all widgets that
    # have been configured within the root frame. Here, update ensures that
    # we get an accurate width and height reading based on the types of widgets
    # we have used. minsize prevents the root window from resizing too small.
    # Feel free to comment it out and see how the resizing
    # behavior of the window changes.
    main.update()
    main.minsize(main.winfo_width(), main.winfo_height())
    id = main.after(2000, app.check_new)
    print(id)
    # And finally, start up the event loop for the program (you can find
    # more on this in lectures of week 9 and 10).
    main.mainloop()
