# Example of sharing from an app
#
# Can only share files that are in shared storage

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from os.path import join
from android.permissions import request_permissions, Permission

from sharesnd import ShareSend
from storage import SharedStorage, PrivateStorage
from picker import Picker

class ShareSendExample(App):

    def build(self):
        self.create_test_file()
        self.share = ShareSend()
        self.picker = Picker(self.picker_callback)
        request_permissions([Permission.READ_EXTERNAL_STORAGE])
        
        b1 = Button(text='Share plain TEXT via a ShareSheet',
                    on_press=self.button1_pressed)
        b2 = Button(text='Share "test.html" FILE via a ShareSheet',
                    on_press=self.button2_pressed)
        b3 = Button(text='Pick a file to share with Gmail',
                    on_press=self.button3_pressed)
        b4 = Button(text='Pick a video/mp4 to share with Receive\nThe Recieve example must be installed.',
                    on_press=self.button4_pressed)
        box = BoxLayout(orientation='vertical')
        box.add_widget(b1)
        box.add_widget(b2)
        box.add_widget(b3)
        box.add_widget(b4)
        self.box = box
        return box

    def button1_pressed(self,b):
        self.share.share_text('Greetings Earthlings')

    def button2_pressed(self,b):
        uri = SharedStorage().getUri('test.html')
        if uri:
            self.share.share_uri(uri)
    
    def button3_pressed(self,b):
        self.target = 'com.google.android.gm'
        self.picker.pick_file()

    def button4_pressed(self,b):
        self.target = 'org.test.receive'
        self.picker.pick_file('video/mp4')

    def picker_callback(self,uri):
        if uri:
            self.share.share_uri(uri, self.target) 

    def create_test_file(self):
        # create a file in Private storage
        filename = join(PrivateStorage().getCacheDir(),'test.html')
        with open(filename, "w") as f:
            f.write("<html>\n")
            f.write(" <head>\n")
            f.write(" </head>\n")
            f.write(" <body>\n")
            f.write("  <h1>Greetings Earthlings<h1>\n")
            f.write("  <h1>We come in please?<h1>\n")
            f.write(" </body>\n")
            f.write("</html>\n")
        # Insert the test case in this app's Shared Storage so it will have a Uri
        SharedStorage().insert(filename)
        
ShareSendExample().run()
