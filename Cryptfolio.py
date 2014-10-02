# -*- coding: utf-8 -*-

'''
Created on Jan 4, 2014

@author: Arya
'''


# checkbox interaction for options
# search relevance, store all search results in array and sort through them, sort by order of relevance, then display the labels in order by modifying their positions

# Import default modules
import sys
import random
import threading

# Import google drive modules
import sys, os.path
import globalVars
import gdata.docs.data

# Import custom modules
import globalVars
import Initialize
from EncryptionKey import decryptText, get_key_history, expandKey

# First adjust the kivy app window size
from kivy.config import Config
window_width = 575
window_height = 475
Config.set('graphics', 'width', window_width)
Config.set('graphics', 'height', window_height)
Config.set('graphics','resizable',0)

# App fonts
font_name_alt = 'Gravity_2.ttf'
font_name = 'Bahasa.ttf'

# Import rest of needed kivy modules
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.uix.progressbar import ProgressBar
from kivy.uix.image import Image
from kivy.core.window import WindowBase

# Global kivy widgets
global f                # Float layout, widgets are added and removed to this layout as needed
global title_label      # Title of App label
global user_field       # Username login input
global pass_field       # Password login input
global login_button     # Button to login (Can just press enter)
global login_label      # Login status
global pb               # Login screen progress
global pb_thread        # Thread function that increments progress bar
global sesh_id_field    # Field to input session ID
global sesh_id_label    # Status of session ID creation
global access_field     # Our universal text input box on the main screen that allows commands and searches
global access_label     # Lets us know what is going on while app is running
global access_input     # New info: access field
global primary_input    # New info: primary info
global secondary_input  # New info: secondary info
global submit_button    # New info: submit info
global cancel_submission_button     # New info: back button to return to main screen
global sesh_confirm_field       # Field to input session name to get ifo
global sesh_confirm_label       # Status of session name confirmation
global new_info_label   # Status of submitting new info
global reveal_button
global reveal_return_button
global access_title_label

# Global variables
global sesh_id
global submitting_info
global all_widgets
global screens_active
global pb_width
global password
global first_pass_type
global first_letter_typed
global double_call
global label_matches    # List containing label widgets for all instant search matches
global labels_active    # List of 1 (active label) and 0 (inactive label) for all matched labels
global name_matches     # Names of all matched searches
global access_reveal
global primary_reveal
global secondary_reveal
global all_reveals
global reveal_index
global showing_hidden
global MAX_MATCHES

first_pass_type = True
submitting_info = False
double_call = True
showing_hidden = True
first_letter_typed = ''
password = 'Gmail Password'
labels_active = []
label_matches = []
name_matches = []
all_reveals = []
MAX_MATCHES = 3

all_widgets = []
screens_active = [True, False, False, False, False, False]   # [ Login Screen, Sesh ID screen, Main Screen, New Info Screen, Sesh Confirm Screen, Reveal Info Screen ]

# Colors
black = (0, 0, 0, 1)
white = (1, 1, 1, 1)
red = (1, 0, 0, 1)
green = (0, 1, 0, 1)
purple = (1, 0, 1, 1)
blue = (0, 0, 1, 1)
blue_2 = (.3, .3, 1, 1)
yellow = (1, 1, 0, 1)
light_blue = (.2, .35, .75, 1)
light_green = (0, .85, 0, 1)
light_green_2 = (.2, 1, .2, 1)
red_2 = (1, .225, .225, 1)
purple_2 = (.65, 0, .85, 1)
highlight_color = (0, 1, 1, .3)

Window.clearcolor = light_blue   # Set the starting background color of window
        
class Cryptfolio(App):
    
    # Function called on app start
    def on_start(self):
        globalVars.init()
        print("Welcome")
        
    def stop_self(self):
        Window.close()

    # Function builds the widgets and displays graphics 
    def build(self):
        
        Window.bind(on_key_down = on_keypress)
        
        global title_label
        global access_field
        global access_label
        global user_field
        global pass_field
        global login_label
        global login_button
        global sesh_id_field
        global sesh_id_label
        global new_info_button
        global pb
        global pb_width
        global f
        global access_input
        global primary_input
        global secondary_input
        global submit_button
        global cancel_submission_button
        global new_info_label
        global sesh_confirm_field
        global sesh_confirm_label
        global reveal_button
        global reveal_return_button
        global all_widgets
        global access_title_label
        
        # Create the main layout that will contain all widgets. Make it fill the window space
        f = FloatLayout (
                            size = (window_width, window_height)
                        )
        
        # Access field
        field_width = window_width * .65
        field_height = window_height * .11
        x_pos = window_width * .5 - (field_width / 2)
        y_pos = window_height * .715
        font_size = field_height / 1.4
        padding_top = (field_height - font_size) / 2.75
        padding_left = field_width * .0375
        padding = [padding_left , padding_top, 6, 6]
        ########################################################################################
        access_field = create_field('', font_size, ( x_pos, y_pos), (None, None), (field_width, field_height), False, highlight_color, blue_2, font_name, padding)
        all_widgets.append(access_field)
        
        # Username field
        field_width = window_width * .65
        field_height = window_height * .125
        x_pos = window_width * .5 - (field_width / 2)
        y_pos = window_height * .55
        font_size = field_height / 1.6
        padding_top = (field_height - font_size) / 2.5
        padding_left = field_width * .045
        padding = [padding_left , padding_top, 6, 6]
        ########################################################################################
        user_field = create_field('gmail username', font_size, ( x_pos, y_pos), (None, None), (field_width, field_height), False, highlight_color, blue_2, font_name, padding)
        all_widgets.append(user_field)
        
        # Password field
        field_width = window_width * .65
        field_height = window_height * .125
        x_pos = window_width * .5 - (field_width / 2)
        y_pos = window_height * .385
        font_size = field_height / 1.6
        padding_top = (field_height - font_size) / 2.5
        padding_left = field_width * .045
        ########################################################################################
        pass_field = create_field('gmail password', font_size, ( x_pos, y_pos), (None, None), (field_width, field_height), False, highlight_color, blue_2, font_name, padding)
        all_widgets.append(pass_field)
        
        # App name label
        label_width = window_width * .35
        label_height = window_height * .15
        x_pos = (window_width * .5) - (label_width / 2)
        y_pos = window_height * .825
        font_size = label_height
        ########################################################################################
        title_label = create_label('cryptfolio', font_size, ( x_pos, y_pos ), (None, None), (label_width, label_height), font_name)
        all_widgets.append(title_label)
        
        # Login Label
        label_width = window_width * .25
        label_height = window_height * .08
        x_pos = (window_width * .5) - (label_width / 2)
        y_pos = window_height * .115
        font_size = label_height
        ########################################################################################
        login_label = create_label('', font_size, ( x_pos, y_pos), (None, None), (label_width, label_height), font_name)
        all_widgets.append(login_label)
        
        # Access Label
        label_width = window_width * .25
        label_height = window_height * .075
        x_pos = (window_width * .5) - (label_width / 2)
        y_pos = window_height * .635
        font_size = label_height
        ########################################################################################
        access_label = create_label('type to begin', font_size, ( x_pos, y_pos), (None, None), (label_width, label_height), font_name)
        all_widgets.append(access_label)
        
        # Session id label
        label_width = window_width * .25
        label_height = window_height * .08
        x_pos = (window_width * .5) - (label_width / 2)
        y_pos = window_height * .365
        font_size = label_height
        ########################################################################################
        sesh_id_label = create_label('choose a session name', font_size, ( x_pos, y_pos ), (None, None), (label_width, label_height), font_name)
        all_widgets.append(sesh_id_label)
        
        # New info label, lets us know status of submitting new info
        label_width = window_width * .25
        label_height = window_height * .08
        x_pos = (window_width * .5) - (label_width / 2)
        y_pos = window_height * .735
        font_size = label_height
        ########################################################################################
        new_info_label = create_label('submit info', font_size, ( x_pos, y_pos), (None, None), (label_width, label_height), font_name)
        all_widgets.append(new_info_label)
        
        # Login Button
        button_width = window_width * .25
        button_height = window_height * .09
        x_pos = (window_width / 2) - (button_width / 2)
        y_pos = window_height * .235
        font_size = button_height / 1.2
        ########################################################################################
        login_button = create_button('Login', purple_2, font_size, (None, None), (button_width, button_height), ( x_pos, y_pos), font_name)
        all_widgets.append(login_button)
        
        # Return from reveal button
        button_width = window_width * .25
        button_height = window_height * .09
        x_pos = window_width/2 - button_width / 2
        y_pos = window_height * .075
        font_size = button_height / 1.2
        ########################################################################################
        reveal_return_button = create_button('back', purple_2, font_size, (None, None), (button_width, button_height), ( x_pos, y_pos), font_name)
        all_widgets.append(reveal_return_button)
        
        # Reveal info button
        button_width = window_width * .25
        button_height = window_height * .09
        x_pos = (window_width)/2 - button_width / 2
        y_pos = window_height * .2
        font_size = button_height / 1.2
        ########################################################################################
        reveal_button = create_button('show', purple_2, font_size, (None, None), (button_width, button_height), ( x_pos, y_pos), font_name)
        all_widgets.append(reveal_button)
        
        # New info button
        button_width = window_width * .125
        button_height = window_height * .125
        x_pos = window_width * .845
        y_pos = window_height * .705
        font_size = button_height / 1.2
        ########################################################################################
        new_info_button = create_button('+', blue_2, font_size, (None, None), (button_width, button_height), ( x_pos, y_pos), font_name)
        all_widgets.append(new_info_button)
        
        # Cancel submission button
        button_width = window_width * .25
        button_height = window_height * .09
        x_pos = (window_width / 2) - button_width * 1.1
        y_pos = window_height * .115
        font_size = button_height / 1.2
        ########################################################################################
        cancel_submission_button = create_button('back', purple_2, font_size, (None, None), (button_width, button_height), ( x_pos, y_pos), font_name)
        all_widgets.append(cancel_submission_button)
        
        # Submit info button
        button_width = window_width * .25
        button_height = window_height * .09
        x_pos = (window_width) - x_pos - button_width
        y_pos = window_height * .12
        font_size = button_height / 1.2
        ########################################################################################
        submit_button = create_button('submit', purple_2, font_size, (None, None), (button_width, button_height), ( x_pos, y_pos), font_name)
        all_widgets.append(submit_button)
        
        # Field to input session ID
        field_width = window_width * .65
        field_height = window_height * .125
        x_pos = window_width * .5 - (field_width / 2)
        y_pos = window_height * .45
        font_size = field_height / 1.6
        padding_top = (field_height - font_size) / 2.5
        padding_left = field_width * .045
        padding = [padding_left , padding_top, 6, 6]
        ########################################################################################
        sesh_id_field = create_field('', font_size, ( x_pos, y_pos ), (None, None), (field_width, field_height), False, highlight_color, blue_2, font_name, padding)
        all_widgets.append(sesh_id_field)
        
        # Access input field for putting in new info
        field_width = window_width * .65
        field_height = window_height * .115
        x_pos = window_width * .5 - (field_width / 2)
        y_pos = window_height * .57
        font_size = field_height / 1.5
        padding_top = (field_height - font_size) / 2.65
        padding_left = field_width * .045
        padding = [padding_left , padding_top, 6, 6]
        ########################################################################################
        access_input = create_field('', font_size, ( x_pos, y_pos), (None, None), (field_width, field_height), False, highlight_color, blue_2, font_name, padding)
        all_widgets.append(access_input)
        
        # Primary input field
        field_width = window_width * .65
        field_height = window_height * .115
        x_pos = window_width * .5 - (field_width / 2)
        y_pos = window_height * .42
        font_size = field_height / 1.5
        padding_top = (field_height - font_size) / 2.65
        padding_left = field_width * .045
        ########################################################################################
        primary_input = create_field('', font_size, ( x_pos, y_pos), (None, None), (field_width, field_height), False, highlight_color, blue_2, font_name, padding)
        all_widgets.append(primary_input)
        
        # Secondary input field
        field_width = window_width * .65
        field_height = window_height * .115
        x_pos = window_width * .5 - (field_width / 2)
        y_pos = window_height * .27
        font_size = field_height / 1.5
        padding_top = (field_height - font_size) / 2.65
        padding_left = field_width * .045
        padding = [padding_left , padding_top, 6, 6]
        ########################################################################################
        secondary_input = create_field('', font_size, ( x_pos, y_pos), (None, None), (field_width, field_height), False, highlight_color, blue_2, font_name, padding)
        all_widgets.append(secondary_input)
        
        # Enter Session Field to Reveal Info
        field_width = window_width * .65
        field_height = window_height * .125
        x_pos = window_width * .5 - (field_width / 2)
        y_pos = window_height * .45
        font_size = field_height / 1.6
        padding_top = (field_height - font_size) / 2.5
        padding_left = field_width * .045
        padding = [padding_left , padding_top, 6, 6]
        ########################################################################################
        sesh_confirm_field = create_field('', font_size, ( x_pos, y_pos), (None, None), (field_width, field_height), False, highlight_color, blue_2, font_name, padding)
        all_widgets.append(sesh_confirm_field)
        
        # Session name confirm label
        label_width = window_width * .25
        label_height = window_height * .08
        x_pos = (window_width * .5) - (label_width / 2)
        y_pos = window_height * .35
        font_size = label_height
        ########################################################################################
        sesh_confirm_label = create_label('enter your session name', font_size, ( x_pos, y_pos), (None, None), (label_width, label_height), font_name)
        all_widgets.append(sesh_confirm_label)
        
        # Create a progress bar
        pb_width = window_width * .135
        pb_height = window_height * .1
        x_pos = window_width / 2 - pb_width / 2
        y_pos = window_height * .045
        pb = ProgressBar (
                            size_hint = (None, None),
                            size = (pb_width, pb_height),
                            pos = ( x_pos, y_pos ),
                            max = 50
                         )
        # Start progress bar thread function
        progress_bar()
        
        # Bind widgets to functions
        login_button.bind(on_release = login_enter)
        access_field.bind(text = text_update)
        access_field.bind(on_text_validate = process_command)
        user_field.bind(on_text_validate = login_enter)
        user_field.bind(text = text_update)
        pass_field.bind(on_text_validate = login_enter)
        pass_field.bind(text = text_update)
        user_field.bind(focus = on_focus)
        pass_field.bind(focus = on_focus)
        sesh_id_field.bind(on_text_validate = set_sesh_id)
        sesh_confirm_field.bind(on_text_validate = verify_session)
        access_input.bind(on_text_validate = submit_new_info)
        primary_input.bind(on_text_validate = submit_new_info)
        secondary_input.bind(on_text_validate = submit_new_info)
        submit_button.bind(on_release = submit_new_info)
        cancel_submission_button.bind(on_release = show_main)
        reveal_return_button.bind(on_release = show_main)
        reveal_button.bind(on_release = toggle_info)
        new_info_button.bind(on_release = new_info_process)
        
        '''
        size_x = window_width * .265
        size = (size_x, size_x)
        image = Image (
                            source = 'Chameleon.png',
                            size_hint = (None, None),
                            size = size,
                            pos = (window_width * .5 - size_x / 2, window_height * .565),
                            color = (1, 1, 1, .5)
                      )
        
        f.add_widget(image)
        '''
        
        # Add login screen widgets to the layout
        f.add_widget(user_field)
        f.add_widget(pass_field)
        f.add_widget(login_button)
        f.add_widget(login_label)
        f.add_widget(title_label)
        
        return f

def create_match_label(content):
    
    # New info label, lets us know status of submitting new info
    label_width = window_width * .25
    label_height = window_height * .075
    x_pos = (window_width * .5) - window_width * 1.25
    y_pos = window_height * .55 - window_height * labels_active.count(1) * .07
    font_size = label_height
    label = Label (
                            text = '[ref=' + content.lower() + ']' + content + '[/ref]',
                            font_size = font_size,
                            pos = ( x_pos, y_pos ),
                            size_hint = (None, None),
                            size = ( label_width, label_height ),
                            bold = True,
                            font_name = font_name,
                            markup = True
                        )
    label.bind(on_ref_press = on_label_press)
    label_matches.append(label)
    all_widgets.append(label)
    
def process_command(value):
    
    global access_field
    global submitting_info
    global screens_active
    
    if access_field.text == 'new info':
        
        screens_active[2] = False
        screens_active[3] = True
        
        access_input.text = ''
        primary_input.text = ''
        secondary_input.text = ''
        
        f.remove_widget(access_field)
        f.remove_widget(access_label)
        
        for label in label_matches:
            f.remove_widget(label)
        
        f.add_widget(access_input)
        f.add_widget(primary_input)
        f.add_widget(secondary_input)
        f.add_widget(submit_button)
        f.add_widget(cancel_submission_button)
        f.add_widget(new_info_label)
        
        Clock.schedule_once(focus_access_input, 0)
        access_input.focus = True
        
        submitting_info = True
        print 'new info submission requested'
        return
        
    Clock.schedule_once(focus_access_field, 0)

def new_info_process(value):
    global access_field
    global submitting_info
    global screens_active
        
    screens_active[2] = False
    screens_active[3] = True
    
    access_input.text = ''
    primary_input.text = ''
    secondary_input.text = ''
    
    f.remove_widget(access_field)
    f.remove_widget(access_label)
    f.remove_widget(new_info_button)
    
    for label in label_matches:
        f.remove_widget(label)
    
    f.add_widget(access_input)
    f.add_widget(primary_input)
    f.add_widget(secondary_input)
    f.add_widget(submit_button)
    f.add_widget(cancel_submission_button)
    f.add_widget(new_info_label)
    
    Clock.schedule_once(focus_access_input, 0)
    access_input.focus = True
    
    submitting_info = True
    print 'new info submission requested'
    return
    
    
def on_focus(instance, value):
    
    if screens_active[0]:
        if user_field.focus and user_field.text == 'gmail username':
            user_field.text = ''
            
            if pass_field.text == '':
                pass_field.password = False
                pass_field.text = 'gmail password'
                
        elif pass_field.focus and pass_field.text == 'gmail password':
            pass_field.text = ''
            
            if user_field.text == '':
                user_field.text = 'gmail username'
        
# Function to show main app screen
def show_main(value):
    
    global showing_hidden
    showing_hidden = True
    reveal_button.text = 'show'
   
    for i in range (len(all_reveals)):
        all_reveals[i][1].text = '- ' * len(primary_reveal)
       
        if all_reveals[i][2] != '':
            all_reveals[i][2].text = '- ' * len(secondary_reveal)
           
    new_info_label.color = (1, 1, 1, 1)
    new_info_label.text = "submit info"
    
    global screens_active
    
    for i in range (len(screens_active)):
        screens_active[i] = False
    
    screens_active[2] = True
    
    access_field.text = ''
    
    for widget in all_widgets:
        f.remove_widget(widget)
    
    f.add_widget(access_field)
    f.add_widget(access_label)
    f.add_widget(title_label)
    f.add_widget(new_info_button)
    
    access_field.focus = True

def finished_encrypting():
    new_info_label.text = 'done!'
    new_info_label.color = light_green_2
    f.remove_widget(pb)
    pb.pos = (window_width / 2 - pb_width / 2, window_height * .23)
    Clock.schedule_once(show_main, 1.25)
    
# Function that processes new info when submitted
def submit_new_info(value):
    
    if access_input.text == '' or primary_input.text == '':

        new_info_label.text = 'Not enough info'
        print ('Incomplete info')
        return
    
    elif access_input.text in globalVars.access_fields:
        new_info_label.text = 'Info already exists!'
        return
    
    info_to_encrypt = []
    
    globalVars.access_fields.append(access_input.text)
    globalVars.access_info.append(primary_input.text)
    
    info_to_encrypt.append(access_input.text + '_access_tag')
    info_to_encrypt.append(primary_input.text)
    
    if secondary_input.text != '':
        info_to_encrypt.append(secondary_input.text)
        globalVars.access_info.append(secondary_input.text)

    else:
        info_to_encrypt.append('__________')
        globalVars.access_info.append('__________')
        
    # expandKey(info_to_encrypt)
    # Encrypt the new info and expand the master key
    threading.Thread(target = expandKey, args = [info_to_encrypt, finished_encrypting]).start()
    
    new_info_label.text = 'Encrypting Data'
    pb.pos = (window_width / 2 - pb_width / 2, window_height * .665)
    f.add_widget(pb)
    
def focus_sesh_field(self):
    sesh_id_field.focus = True
def focus_access_field(self):
    access_field.focus = True
def focus_access_input(self):
    access_input.focus = True
def focus_confirm_field(self):
    sesh_confirm_field.focus = True

def change_text_color(text, color):
    text.color = color

def new_user_setup():
    login_label.text = 'Running New User Setup'
    
def set_sesh_id(value):
    
    if sesh_id_field.text == '':
        print 'You entered nothing'
        Clock.schedule_once(focus_sesh_field, 0)
        return

    global sesh_id
    global sesh_id_label
    
    sesh_id = sesh_id_field.text
    sesh_id_label.text = 'session name saved'
    sesh_id_label.color = light_green_2
    
    Clock.schedule_once(remove_sesh_id, 1)

def remove_sesh_id(self):
    
    global screens_active
    screens_active[1] = False
    screens_active[2] = True
    
    f.remove_widget(sesh_id_label)
    f.remove_widget(sesh_id_field)
    f.add_widget(access_field)
    f.add_widget(access_label)
    f.add_widget(new_info_button)
    
    access_field.focus = True
    
    # Window.size = window_width * 2, window_height * 2
    
    extract_content()
    
def on_keypress(self, keyboard, keycode, text, modifiers):
    
    global user_field
    global pass_field
    global password
    
    if keycode == 15:   # Keycode for tab
        
        user_field.text = user_field.text.rstrip('\t')
        pass_field.text = pass_field.text.rstrip('\t')
        access_input.text = access_input.text.rstrip('\t')
        primary_input.text = primary_input.text.rstrip('\t')
        secondary_input.text = secondary_input.text.rstrip('\t')
        
        # Login screen active
        if screens_active[0]:
            
            # Nothing is focused, at start of app
            if not user_field.focus and not pass_field.focus:
                
                user_field.focus = True
                
                if user_field.text == 'Gmail Username':
                    user_field.text = ''
            
            # User field is focused  
            elif user_field.focus:
                
                if user_field.text == '':
                    user_field.text = 'Gmail Username'
                
                if pass_field.text == 'Gmail Password':
                    pass_field.text = ''
                    
                pass_field.focus = True
                user_field.focus = False
            
            # Pass field is focused
            elif pass_field.focus:
                
                if user_field.text == 'Gmail Username':
                    user_field.text = ''
                
                if pass_field.text == '':
                    pass_field.password = False
                    pass_field.text = 'Gmail Password'
                    
                user_field.focus = True
                pass_field.focus = False
        
        elif screens_active[2]:
            if not access_field.focus:
                access_field.focus = True
        
        elif screens_active[4]:
            if not sesh_confirm_field.focus:
                sesh_confirm_field.focus = True
            
        elif screens_active[3]:
            
            if access_input.focus:
                primary_input.focus = True
            
            elif primary_input.focus:
                secondary_input.focus = True
            
            elif secondary_input.focus:
                access_input.focus = True
            
            else:
                access_input.focus = True
      
# Function is called every time text field is updated, used to implement instant search
# Create labels as needed, store them in a list, then turn them off and on as needed              
def text_update(instance, value):

    if screens_active[0]:
        
        global password
        global first_pass_type
        global first_letter_typed
        global double_call
        
        if pass_field.focus:
            pass_field.password = True
            
            if first_pass_type:
                first_pass_type = False
                first_letter_typed = value
                pass_field.text = '*'
                password = first_letter_typed
                return
            
            elif double_call:
                password = first_letter_typed
                pass_field.text = first_letter_typed
                double_call = False
            
            else:
                password = value
    
        return
    
    value = value.lower().replace(' ', '')
    
    # Turn all labels off
    if value == '':
          
        for i in range (len(labels_active)):
            labels_active[i] = 0
        
        for label in label_matches:
            f.remove_widget(label)
        
        return
    
    num_matches = 0
    
    for content in globalVars.access_fields:

        # Search term matches an access field
        if value in content.lower().replace(' ', ''):

            # If the label is not already made, make it
            if content not in name_matches:
                if (num_matches < MAX_MATCHES):
                    labels_active.append(1)
                    name_matches.append(content)
                    create_match_label(content)
                    index_this_label = len(name_matches) - 1
                    f.add_widget(label_matches[index_this_label])
                    num_matches += 1;
            
            # If label is found but has already been made previously, just add it back to the layout
            # But only if it has been inactive
            else:
                index_this_label = name_matches.index(content)
                
                if labels_active[index_this_label] == 0:
                    labels_active[index_this_label] = 1
                    f.add_widget(label_matches[index_this_label])
                    num_matches += 1
        
        # Search term not found in access fields      
        else:
            # Only remove the widget and set it to inactive (0) if it has already been added
            if content in name_matches:
                index_this_label = name_matches.index(content)
                f.remove_widget( label_matches[index_this_label] )
                labels_active[index_this_label] = 0
                num_matches -= 1
        
        # Reposition label matches
        position_in_actives = 0
        for i in range (len(name_matches)):
            if name_matches[i] in globalVars.access_fields and labels_active[i] == 1:
                x_pos = (window_width * .5) - (window_width * .25 * 1.75)
                y_pos = window_height * .55 - window_height * (position_in_actives) * .07
                label_matches[i].pos = ( x_pos, y_pos )
                position_in_actives += 1
            
def color_update(instance, value):
    global access_field
    access_field.foreground_color = (random.random(), random.random(), random.random(), 1)

# Function to reveal info when label is pressed
def on_label_press(instance, value):
    
    global access_reveal
    global primary_reveal
    global secondary_reveal
    global reveal_index
    
    screens_active[2] = False
    screens_active[4] = True
    
    for widget in all_widgets:
        f.remove_widget(widget)
    
    f.add_widget(sesh_confirm_field)
    f.add_widget(sesh_confirm_label)
    sesh_confirm_field.focus = True
    
    # Find index of value
    for i in range (len(globalVars.access_fields)):
        if globalVars.access_fields[i].lower() == value:
            reveal_index = i
    
    access_reveal = globalVars.access_fields[reveal_index]
    primary_reveal = globalVars.access_info[2 * reveal_index]
    
    if globalVars.access_info[2 * reveal_index + 1] != '__________':
        secondary_reveal = globalVars.access_info[2 * reveal_index + 1]
        return
    
    secondary_reveal = ''

def verify_session(value):
    if sesh_confirm_field.text == sesh_id:
        print 'Access granted'
        sesh_confirm_field.text = ''
        reveal_info()
    else:
        print 'Invalid session name'
        Clock.schedule_once(focus_confirm_field, 0)

# Create labels for access, primary, and secondary reveals and add them to a list to only create them one time
def reveal_info():
    
    for widget in all_widgets:
        f.remove_widget(widget)
    
    f.add_widget(reveal_button)
    f.add_widget(reveal_return_button)
    
    # If already in list, just display them
    for i in range (len(all_reveals)):
        
        if all_reveals[i][0].text == access_reveal:
            f.add_widget(all_reveals[i][0])
            f.add_widget(all_reveals[i][1])
            
            if all_reveals[i][2] != '':
                f.add_widget(all_reveals[i][2])
            
            return
            
    # Otherwise, create the label, add it to list, then display them
    
    label_set = []
    label_width = window_width * .25
    label_height = window_height * .1
    x_pos = (window_width * .5) - (label_width / 2)
    y_pos = window_height * .575
    font_size = label_height
    ########################################################################################
    access_label = create_label(access_reveal, font_size, ( x_pos, y_pos ), (None, None), (label_width, label_height), font_name)
    all_widgets.append(access_label)
    label_set.append(access_label)
    f.add_widget(access_label)
    
    y_pos = window_height * .45
    primary_label = create_label(' ' + '- ' * len(primary_reveal), font_size, ( x_pos, y_pos ), (None, None), (label_width, label_height), font_name)
    all_widgets.append(primary_label)
    label_set.append(primary_label)
    f.add_widget(primary_label)
    
    y_pos = window_height * .35
    
    if secondary_reveal != '':
        secondary_label = create_label(' ' + '- ' * len(secondary_reveal), font_size, ( x_pos, y_pos ), (None, None), (label_width, label_height), font_name)
        all_widgets.append(secondary_label)
        label_set.append(secondary_label)
        f.add_widget(secondary_label)
        
    else:
        label_set.append('')
    
    all_reveals.append(label_set)

def toggle_info(value):
    
    global showing_hidden
    
    # Showing hidden text, reveal true info
    if showing_hidden:
        reveal_button.text = 'hide'
        
        for i in range (len(all_reveals)):
            
            all_reveals[i][1].text = primary_reveal
            
            if all_reveals[i][2] != '':
                all_reveals[i][2].text = secondary_reveal
    
    else:
        reveal_button.text = 'show'
        
        for i in range (len(all_reveals)):
            all_reveals[i][1].text = ' ' + '- ' * len(all_reveals[i][1].text)
        
            if all_reveals[i][2] != '':
                all_reveals[i][2].text = ' ' + '- ' * len(all_reveals[i][2].text)
    
    showing_hidden = not showing_hidden
    
def login_enter(value):
    
    # If one or both fields are empty, error
    if user_field.text == '' or pass_field.text == '':
        
        print 'incomplete info!'
        login_label.text = 'incomplete Info!'
    
    # Otherwise, continue to login verification
    else:
        
        pb.value = 0
        f.add_widget(pb)
        threading.Thread(target = userLogin, args = [user_field.text, password]).start()
        login_label.color = (1, 1, 1, 1)
        login_label.text = 'Verifying User'

# Add condition to return if successfully logged in already
def progress_bar():

    threading.Timer(.01, progress_bar).start()
    
    pb.value += 1
    
    if pb.value >= 50:
        pb.value = 0

def get_resources():
    
    global screens_active
    
    login_label.text = 'Retrieving Data'
    
    # Find and access folder we are uploading to
    globalVars.resources = Initialize.findFolder(new_user_setup)
    
    # Find file in the App folder and get its contents
    Initialize.findFile()
    
    # Remove all login screen widgets to prepare to display the main screen widgets
    f.remove_widget(pb)
    f.remove_widget(user_field)
    f.remove_widget(pass_field)
    f.remove_widget(login_button)
    f.remove_widget(login_label)
    
    # Prompt user for session id
    screens_active[0] = False
    screens_active[1] = True
    f.add_widget(sesh_id_label)
    f.add_widget(sesh_id_field)
    sesh_id_field.focus = True

# Attempts to validate user credentials in order to authenticate clients
def userLogin(username, password):
    
    print 'Verifying User...',
    
    try:
        
        globalVars.docsclient.ClientLogin(username, password, globalVars.docsclient.source);
        globalVars.serviceclient.ClientLogin(username, password, globalVars.serviceclient.source)
    
    except (gdata.client.BadAuthentication, gdata.client.Error), e:
        
        f.remove_widget(pb)
        login_label.text = 'Unable to verify user'
        change_text_color(login_label, red_2)
        print str(e)
        return
    
    except:
        
        f.remove_widget(pb)  
        login_label.text = 'Unable to verify user'
        change_text_color(login_label, red_2)
        print 'Login Error'
        return
    
    print 'Done'
    get_resources()
      
def extract_content():    
    
    # Process all past key information history
    get_key_history()       
    
    # Store a decrypted version of the file's text inside the runtime variable
    if globalVars.firstTime or globalVars.fileContent == 'f':
        globalVars.fileContent = ''
    
    print
    print 'file content'
    print globalVars.fileContent
    
    globalVars.fileContent = decryptText(globalVars.fileContent)

# Create a label with specified features
def create_label(text, font_size, pos, size_hint, size, font_name):
    return Label (
                    text = text,
                    font_size = font_size,
                    pos = pos,
                    size_hint = size_hint,
                    size = size,
                    font_name = font_name
                 )

# Create input field with specified features
def create_field(text, font_size, pos, size_hint, size, multiline, selection_color, foreground_color, font_name, padding):
    return TextInput (
                        text = text,            # Default text of the field
                        font_size = font_size,  # Font size of the field
                        pos = pos,              # Position of the field
                        size_hint = size_hint,  # Size set to a fraction of the layout size
                        size = size,            # Size ( x, y ) of the field
                        multiline = multiline,  # Multiple line support
                        selection_color = selection_color,      # Color and opacity of the text selection
                        foreground_color = foreground_color,    # Color of the text
                        font_name = font_name,                  # Font
                        padding = padding                       # Text padding to reposition text within box
                     )

# Create a button with specified features
def create_button(text, background_color, font_size, size_hint, size, pos, font_name):
    return Button (
                        text = text,
                        background_color = background_color,
                        font_size = font_size,
                        size_hint = size_hint,
                        size = size,
                        pos = pos,
                        font_name = font_name
                  )
    
if __name__ == "__main__":
    Cryptfolio().run()