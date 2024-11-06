from kivy.app import App 
from kivy.uix.screenmanager import ScreenManager, Screen  
from kivy.lang import Builder   
from kivy.uix.popup import Popup  
from kivy.uix.label import Label  
import firebase_admin
from firebase_admin import credentials, storage, db, firestore,auth
import os
import random  
import smtplib
from kivy.uix.spinner import Spinner  
from email.mime.text import MIMEText 
from kivy.properties import StringProperty 
import re
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.clock import Clock 
from kivy.uix.filechooser import FileChooserIconView
import uuid
import bcrypt

firebase_credentials = {
#your fire base credentials
}

cred = credentials.Certificate(firebase_credentials)
firebase_admin.initialize_app(cred, {
#database and store buccket
})

bucket = storage.bucket()  
db = firestore.client()

# Email Sending Function 
def send_email(to_email, subject, body):
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    sender_email = "YourEmail@gmail.com"
    sender_password = "Email_app passsword "  
    
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = to_email

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
            print("Email sent successfully")
    except Exception as e:
        print(f"Failed to send email: {str(e)}")

# Function for create otp 
def generate_otp():
    return random.randint(100000, 999999)  


#KV Code For Styling and make screens 
   
Builder.load_string('''  
<BaseScreen>:
    ScrollView:
        BoxLayout:
            orientation: 'vertical'
            padding: dp(10), dp(20)
            spacing: dp(15)
            canvas.before:
                Color:
                    rgba: 1, 1, 1, 1
                Rectangle:
                    source: r'bg.png'
                    pos: self.pos
                    size: self.size
                    
            Label:
                text: "Inviculture"
                font_size: '24sp'  # More consistent text size
                bold: True
                color: 0, 0, 0, 1
                size_hint_y: None
                height: '50dp'  # Fixed height for better alignment
                
            BoxLayout:
                id: main_content
                padding: dp(10), dp(20)
                spacing: dp(15)
                orientation: 'vertical'
                
            BoxLayout:
                size_hint_y: None
                padding: dp(10), dp(20)
                spacing: dp(15)
                orientation: 'vertical'                   

                Button:
                    text: "Go Back"
                    size_hint_y: None
                    height: '50dp'  # Consistent button height
                    background_color: 0.1, 0.5, 0.3, 1
                    font_size: '18sp'  # Standard font size
                    color: 1, 1, 1, 1
                    on_press: app.root.current = 'login'

<LoginScreen>:
    ScrollView:
        BoxLayout:
            orientation: 'vertical'
            padding: dp(10), dp(20)
            spacing: dp(15)

            canvas.before:
                Color:
                    rgba: 1, 1, 1, 1
                Rectangle:
                    source: r'bg.png'
                    pos: self.pos
                    size: self.size

            BoxLayout:
                id: main_content
                size_hint_y: None
                height: '70dp'
                padding: [10, 10]

                canvas.before:
                    Color:
                        rgba: 0.8, 0.9, 0.8, 1  
                    RoundedRectangle:
                        source: r'bg.png'
                        pos: self.pos
                        size: self.size
                        radius: [10]
                    Line:
                        width: 3
                        rounded_rectangle: (self.x, self.y, self.width, self.height, 10)

                Label:
                    text: "Welcome Sir, Please Login First"
                    font_size: '22sp'
                    bold: True
                    color: 0, 0, 0, 1
                    halign: 'center'
                    valign: 'middle'
                    size_hint_y: None
                    height: '60dp'
                    padding: [10, 10]
                    text_size: self.size

            TextInput:
                id: login_email
                hint_text: "Email"
                multiline: False
                size_hint_y: None
                height: '50dp'
                padding_x: [10, 10]  # Adds padding inside TextInput
                background_color: 1, 1, 1, 0.9
                foreground_color: 0, 0, 0, 1
                font_size: '18sp'

            RelativeLayout:
                size_hint_y: None
                height: '50dp'
                TextInput:
                    id: login_password
                    hint_text: "Password"
                    multiline: False
                    size_hint_y: None
                    height: '50dp'
                    padding_x: [10, 10]
                    background_color: 1, 1, 1, 0.9
                    foreground_color: 0, 0, 0, 1
                    font_size: '18sp'
                    password: True

                ToggleButton:
                    id: toggle_show_password_login
                    size_hint_x: None
                    width: '50dp'
                    pos_hint: {'right': 1, 'center_y': 0.5}
                    text: 'Hide'
                    background_color: 1, 1, 1, 1                   
                    on_state: 
                        login_password.password = self.state == 'normal'  
                        self.text = "Hide" if self.state == 'normal' else "Show"

            Button:
                text: "Login"
                size_hint_y: None
                height: '60dp'
                background_color: 0.1, 0.5, 0.3, 1
                font_size: '18sp'
                color: 1, 1, 1, 1
                background_normal: r'home_button.png'
                background_down: r'home_button.png'
                on_press:
                    self.text = "Logging in..."
                    root.login()
                on_release:
                    self.text = "Login"

            Button:
                text: "Signup"
                size_hint_y: None
                height: '60dp'
                background_color: 0.2, 0.6, 0.4, 1
                font_size: '18sp'
                color: 1, 1, 1, 1
                background_normal: r'home_button.png'
                background_down: r'home_button.png'
                on_press:
                    app.root.current = 'signup'

            Button:
                text: "Forgot Password"
                size_hint_y: None
                height: '60dp'
                background_color: 0.2, 0.6, 0.4, 1
                font_size: '18sp'
                color: 1, 1, 1, 1
                background_normal: r'home_button.png'
                background_down: r'home_button.png'
                on_press:
                    app.root.current = 'forgot_password'

<SignupScreen>:
    ScrollView:
        BoxLayout:
            orientation: 'vertical'
            padding: dp(10), dp(20)
            spacing: dp(15)

            canvas.before:
                Color:
                    rgba: 1, 1, 1, 1
                Rectangle:
                    source: r'bg.png'  
                    pos: self.pos
                    size: self.size

            BoxLayout:
                id: main_content
                size_hint_y: None
                height: '60dp' 
                padding: [10, 10]

                canvas.before:
                    RoundedRectangle:
                        source: r'bg.png'
                        pos: self.pos
                        size: self.size
                        radius: [10]
                    Color:
                        rgba: 0.8, 0.9, 0.8, 1  
                    Line:
                        width: 2
                        rounded_rectangle: (self.x, self.y, self.width, self.height, 10)

                Label:
                    text: "Sign Up, Please"
                    font_size: '20sp'  
                    bold: True
                    color: 0, 0, 0, 1
                    halign: 'center'
                    valign: 'middle'
                    text_size: self.size
                             
            TextInput:
                id: signup_username
                hint_text: "Username"
                size_hint_y: None
                height: '50dp'  
                background_color: 1, 1, 1, 0.9
                foreground_color: 0, 0, 0, 1
                font_size: '18sp'  
            
            TextInput:
                id: signup_email
                hint_text: "Email"
                size_hint_y: None
                height: '50dp'
                background_color: 1, 1, 1, 0.9
                foreground_color: 0, 0, 0, 1
                font_size: '18sp'
                      
            RelativeLayout:
                size_hint_y: None
                height: '50dp'  
                TextInput:
                    id: signup_password
                    hint_text: "Password"
                    multiline: False
                    size_hint_y: None
                    height: '50dp' 
                    background_color: 1, 1, 1, 0.9
                    foreground_color: 0, 0, 0, 1
                    font_size: '18sp'
                    password: True

                ToggleButton:
                    id: toggle_show_password_signup
                    size_hint_x: None
                    width: '50dp'  
                    pos_hint: {'right': 1, 'center_y': 0.5}  
                    text: 'Hide'  
                    background_color: 1, 1, 1, 1                   
                    on_state: 
                        signup_password.password = self.state == 'normal'  
                        self.text = "Hide" if self.state == 'normal' else "Show" 
            
            TextInput:
                id: confirm_password
                hint_text: "Confirm Password"
                size_hint_y: None
                height: '50dp'
                background_color: 1, 1, 1, 0.9
                foreground_color: 0, 0, 0, 1
                font_size: '18sp'
                password: True
            
            TextInput:
                id: signup_phone
                hint_text: "Phone Number"
                size_hint_y: None
                height: '50dp'
                background_color: 1, 1, 1, 0.9
                foreground_color: 0, 0, 0, 1
                font_size: '18sp'
            
            Button:
                text: "Sign Up"
                size_hint_y: None
                height: '60dp'  
                background_color: 0.1, 0.5, 0.3, 1
                font_size: '18sp'
                color: 1, 1, 1, 1
                background_normal: r'home_button.png'  
                background_down: r'home_button.png'            
                on_press: 
                    self.text = "Signing up...."
                    self.background_color = 0.2, 0.7, 0.4, 1  
                    root.signup()  
                on_release: 
                    self.text = "Sign Up" 
                    self.background_color = 0.1, 0.5, 0.3, 1  

            Button:
                text: "Back to Login"
                size_hint_y: None
                height: '60dp'  
                background_color: 0.2, 0.6, 0.4, 1
                font_size: '18sp'
                color: 1, 1, 1, 1
                background_normal: r'home_button.png'  
                background_down: r'home_button.png'            
                on_press: 
                    self.background_color = 0.3, 0.7, 0.5, 1  
                    app.root.current = 'login'  
                on_release: 
                    self.background_color = 0.2, 0.6, 0.4, 1  
                    
<ForgotPasswordScreen>:
    ScrollView:
        BoxLayout:
            orientation: 'vertical'
            padding: dp(10), dp(20)
            spacing: dp(15)

            canvas.before:
                Color:
                    rgba: 1, 1, 1, 1
                Rectangle:
                    source: r'bg.png'
                    pos: self.pos
                    size: self.size

            BoxLayout:
                id: main_content
                size_hint_y: None
                height: '60dp'
                padding: [10, 10]

                canvas.before:
                    RoundedRectangle:
                        source: r'bg.png'
                        pos: self.pos
                        size: self.size
                        radius: [10]
                    Color:
                        rgba: 0.8, 0.9, 0.8, 1
                    Line:
                        width: 2
                        rounded_rectangle: (self.x, self.y, self.width, self.height, 10)

                Label:
                    text: "Forgot Password"
                    font_size: '24sp'
                    bold: True
                    color: 0, 0, 0, 1
                    halign: 'center'
                    valign: 'middle'
                    text_size: self.size

            TextInput:
                id: forgot_email
                hint_text: "Enter your email"
                size_hint_y: None
                height: '50dp'
                background_color: 1, 1, 1, 1
                foreground_color: 0, 0, 0, 1
                font_size: '18sp'
                padding: [10, 10]
                canvas.before:
                    Color:
                        rgba: 0.8, 0.8, 0.8, 1  # Border color
                    Line:
                        width: 2
                        rectangle: (self.x, self.y, self.width, self.height)

            Button:
                text: "Send OTP"
                size_hint_y: None
                height: '60dp'
                background_color: 0.2, 0.6, 0.4, 1
                background_normal: r'home_button.png'
                background_down: r'home_button.png'
                font_size: '18sp'
                color: 1, 1, 1, 1
                on_press: root.send_otp()
                canvas.before:
                    RoundedRectangle:
                        pos: self.pos
                        size: self.size
                        radius: [10]
                    Color:
                        rgba: dp(15), 0.5, 0.3, 0.3
                    RoundedRectangle:
                        pos: (self.x, self.y - 5)  # Shadow effect
                        size: self.size
                        radius: [10]

            Button:
                text: "Back to Login"
                size_hint_y: None
                height: '60dp'
                background_color: 0.2, 0.6, 0.4, 1
                background_normal: r'home_button.png'
                background_down: r'home_button.png'
                font_size: '18sp'
                color: 1, 1, 1, 1
                on_press: app.root.current = 'login'
                canvas.before:
                    RoundedRectangle:
                        pos: self.pos
                        size: self.size
                        radius: [10]
                    Color:
                        rgba: dp(15), 0.5, 0.3, 0.3
                    RoundedRectangle:
                        pos: (self.x, self.y - 5)  # Shadow effect
                        size: self.size
                        radius: [10]


<VerifyOTPScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: dp(10), dp(20)
        spacing: dp(15)
        canvas.before:
            Rectangle:
                source: r'bg.png'  
                pos: self.pos
                size: self.size

        BoxLayout:
            id: main_content
            size_hint_y: None
            height: '60dp'  
            padding: [10, 10]
            canvas.before: 
                RoundedRectangle:
                    source: r'bg.png'
                    pos: self.pos
                    size: self.size
                    radius: [10]
                Color:
                    rgba: 0.8, 0.9, 0.8, 1  
                Line:
                    width: 2
                    rounded_rectangle: (self.x, self.y, self.width, self.height, 10)
            Label:
                text: "Enter Your Otp"
                font_size: '20sp' 
                bold: True
                color: 0, 0, 0, 1
                halign: 'center'
                valign: 'middle'
                text_size: self.size
                            
        TextInput:
            id: otp_input
            hint_text: "Enter OTP"
            size_hint_y: None
            height: '50dp'
            background_color: 1, 1, 1, 0.9
            foreground_color: 0, 0, 0, 1
            font_size: '18sp'  
            
        Button:
            text: "Verify OTP"
            size_hint_y: None
            height: '60dp'
            background_color: 0.2, 0.6, 0.4, 1
            font_size: '18sp'
            color: 1, 1, 1, 1
            background_normal: r'home_button.png'  
            background_down: r'home_button.png'                       
            on_press: root.verify_otp()
            
        Button:
            text: "Back to Forgot Password"
            size_hint_y: None
            height: '60dp'
            background_color: 0.2, 0.6, 0.4, 1
            font_size: '18sp'
            color: 1, 1, 1, 1
            background_normal: r'home_button.png'  
            background_down: r'home_button.png'                       
            on_press: app.root.current = 'forgot_password'           

<ResetPasswordScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: dp(10), dp(20)
        spacing: dp(15)
        canvas.before:
            Rectangle:
                source: r'bg.png'  
                pos: self.pos
                size: self.size

        BoxLayout:
            id: main_content
            size_hint_y: None
            height: '60dp'  
            padding: [10, 10]
            canvas.before:
                RoundedRectangle:
                    source: r'bg.png'
                    pos: self.pos
                    size: self.size
                    radius: [10]
                Color:
                    rgba: 0.8, 0.9, 0.8, 1 
                Line:
                    width: 2
                    rounded_rectangle: (self.x, self.y, self.width, self.height, 10)
            Label:
                text: "Reset your Password"
                font_size: '20sp'  
                bold: True
                color: 0, 0, 0, 1
                halign: 'center'
                valign: 'middle'
                text_size: self.size
                              
        TextInput:
            id: new_password
            hint_text: "New Password"
            size_hint_y: None
            height: '50dp'
            background_color: 1, 1, 1, 0.9
            foreground_color: 0, 0, 0, 1
            font_size: '18sp'            
            password: True
            
        TextInput:
            id: confirm_password
            hint_text: "Confirm Password"
            size_hint_y: None
            height: '50dp'
            background_color: 1, 1, 1, 0.9
            foreground_color: 0, 0, 0, 1
            font_size: '18sp'            
            password: True
            
        Button:
            text: "Reset Password"
            size_hint_y: None
            height: '60dp'
            background_color: 0.2, 0.6, 0.4, 1
            font_size: '18sp'
            color: 1, 1, 1, 1  
            background_normal: r'home_button.png'  
            background_down: r'home_button.png'                     
            on_press: root.reset_password()
            
        Button:
            text: "Back to Login"
            size_hint_y: None
            height: '60dp'
            background_color: 0.2, 0.6, 0.4, 1
            font_size: '18sp'
            color: 1, 1, 1, 1
            background_normal: r'home_button.png'  
            background_down: r'home_button.png'                       
            on_press: app.root.current = 'login'
           
<HomeScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: dp(10), dp(20)
        spacing: dp(15)
        canvas.before:
            Color:
                rgba:0.2, 0.6, 0.4, 1
            Rectangle:
                source: r'bg.png'
                pos: self.pos
                size: self.size  
        BoxLayout:
            id: main_content
            size_hint_y: None
            height: '60dp' 
            padding: [10, 10]
            canvas.before:
                Color:
                    rgba: 1, 1, 1, 1 
                RoundedRectangle:
                    source: r'bg.png'
                    pos: self.pos
                    size: self.size
                    radius: [10]
                Color:
                    rgba: 0.8, 0.9, 0.8, 1 
                Line:
                    width: 2
                    rounded_rectangle: (self.x, self.y, self.width, self.height, 10)
            Label:
                text: "Welcome To Inviculture"
                font_size: '20sp' 
                bold: True
                color: 0, 0, 0, 1
                halign: 'center'
                valign: 'middle'
                text_size: self.size
                
        Button:
            text: "Upload Problem"
            size_hint_y: None
            height: '50dp'  
            background_color: 0.2, 0.6, 0.4, 1
            font_size: 18
            color: 1, 1, 1, 1
            background_normal: 'home_button.png'  
            background_normal: 'home_button.png'                        
            on_press: app.root.current = 'ProblemScreen'
        Button:
            text: "Image Gallery"
            size_hint_y: None
            height: '50dp'  
            background_color: 0.2, 0.6, 0.4, 1
            font_size: 18
            color: 1, 1, 1, 1 
            background_normal: 'home_button.png' 
            background_normal: 'home_button.png'           
            on_press: app.root.current = 'gallery'
        Button:
            text: "About Us"
            size_hint_y: None
            height: '50dp' 
            background_color: 0.2, 0.6, 0.4, 1
            font_size: 18
            color: 1, 1, 1, 1 
            background_normal: 'home_button.png' 
            background_normal: 'home_button.png'                                          
            on_press: app.root.current = 'about_us'
        Button:
            text: "Your Profile" 
            size_hint_y: None
            height: '50dp'  
            background_color: 0.2, 0.6, 0.4, 1
            font_size: 18
            color: 1, 1, 1, 1
            background_normal: 'home_button.png'
            background_normal: 'home_button.png'
            on_press: app.root.current = 'profile' 
                              
<ProfileScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: dp(10), dp(20)
        spacing: dp(15)
        canvas.before:
            Color:
                rgba: 1, 1, 1, 1
            Rectangle:
                source: r'bg.png' 
                pos: self.pos
                size: self.size 

        BoxLayout:
            id: main_content
            size_hint_y: None
            height: '60dp'
            padding: [10, 10]
            canvas.before:
                Color:
                    rgba: 1, 1, 1, 1
                RoundedRectangle:
                    source: r'bg.png'
                    pos: self.pos
                    size: self.size
                    radius: [10]
                Color:
                    rgba: 0.8, 0.9, 0.8, 1
                Line:
                    width: 2
                    rounded_rectangle: (self.x, self.y, self.width, self.height, 10)
            Label:
                text: "Welcome To inviculture - Farmer Helper App"
                font_size: '20sp'
                bold: True
                color: 1, 1, 1, 1
                halign: 'center'  # This can stay centered if you want the title centered
                valign: 'middle'
                text_size: self.size

        ScrollView:
            BoxLayout:
                id: user_details
                orientation: 'vertical'
                size_hint_y: None
                height: self.minimum_height
                padding: [10, 10]
                spacing: 10
                
                BoxLayout:
                    size_hint_y: None
                    height: '40dp'
                    Label:
                        id:user_name_label
                        font_size: '18sp'
                        color: 0, 0, 0.5, 1
                        text_size: self.size                

                BoxLayout:
                    size_hint_y: None
                    height: '40dp'
                    Label:
                        id:name_label
                        font_size: '18sp'
                        color: 0, 0, 0.5, 1
                        text_size: self.size

                # Email Box
                BoxLayout:
                    size_hint_y: None
                    height: '40dp'
                    Label:
                        id:email_label
                        font_size: '18sp'
                        color: 0, 0, 0.5, 1
                        text_size: self.size

                # Mobile Number Box
                BoxLayout:
                    size_hint_y: None
                    height: '40dp'
                    Label:
                        id:phone_label
                        font_size: '18sp'
                        color: 0, 0, 0.5, 1
                        text_size: self.size

                # Gender Box
                BoxLayout:
                    size_hint_y: None
                    height: '40dp'
                    Label:
                        id:gender_label
                        font_size: '18sp'
                        color: 0, 0, 0.5, 1
                        text_size: self.size
                        
                BoxLayout:
                    size_hint_y: None
                    height: '40dp'
                    Label:
                        id:age_label
                        font_size: '18sp'
                        color: 0, 0, 0.5, 1
                        text_size: self.size                        

                BoxLayout:
                    size_hint_y: None
                    height: '40dp'
                    Label:
                        id:category_label
                        font_size: '18sp'
                        color: 0, 0, 0.5, 1
                        text_size: self.size
                        
                BoxLayout:
                    size_hint_y: None
                    height: '40dp'
                    Label:
                        id:type_label
                        font_size: '18sp'
                        color: 0, 0, 0.5, 1
                        text_size: self.size                        

                BoxLayout:
                    size_hint_y: None
                    height: '40dp'
                    Label:
                        id:Address_line1_label
                        font_size: '18sp'
                        color: 0, 0, 0.5, 1
                        text_size: self.size

                BoxLayout:
                    size_hint_y: None
                    height: '40dp'
                    Label:
                        id:Address_line2_label
                        font_size: '18sp'
                        color: 0, 0, 0.5, 1
                        text_size: self.size
                        
                BoxLayout:
                    size_hint_y: None
                    height: '40dp'
                    Label:
                        id:district_label
                        font_size: '18sp'
                        color: 0, 0, 0.5, 1
                        text_size: self.size
                        
                BoxLayout:
                    size_hint_y: None
                    height: '40dp'
                    Label:
                        id:State_label
                        font_size: '18sp'
                        color: 0, 0, 0.5, 1
                        text_size: self.size                                                

        Button:
            text: "Register Your details with us"
            size_hint_y: None
            height: '50dp'  
            background_color: 0.2, 0.6, 0.4, 1
            font_size: 18
            color: 1, 1, 1, 1   
            background_normal: r'home_button.png'  
            background_down: r'home_button.png'                       
            on_press: app.root.current = 'Register'
            
        Button:
            text: "Back"
            size_hint_y: None
            height: '50dp'  
            background_color: 0.2, 0.6, 0.4, 1
            font_size: 18
            color: 1, 1, 1, 1
            background_normal: r'home_button.png'  
            background_down: r'home_button.png'           
            on_press: app.root.current = 'home'


<RegisterScreen>:
    ScrollView:
        BoxLayout:
            orientation: 'vertical'
            padding: dp(10), dp(20)
            spacing: dp(15)
            size_hint_y: None
            height: self.minimum_height
            canvas.before:
                Rectangle:
                    source: r'bg.png'
                    pos: self.pos
                    size: self.size
                    
            BoxLayout:
                size_hint_y: None
                height: '60dp'
                padding: [10, 10]
                canvas.before:
                    RoundedRectangle:
                        source: r'bg.png'
                        pos: self.pos
                        size: self.size
                        radius: [10]
                    Color:
                        rgba: 0.8, 0.9, 0.8, 1
                    Line:
                        width: 2
                        rounded_rectangle: (self.x, self.y, self.width, self.height, 10)
                Label:
                    text: "Register Your Details with Us"
                    font_size: '20sp'
                    bold: True
                    color: 0, 0, 0, 1
                    halign: 'center'
                    valign: 'middle'
                    text_size: self.size

            TextInput:
                id: Register_email
                hint_text: "Your Registered Email"
                size_hint_y: None
                height: '50dp'
                font_size: '18sp'
                background_color: 1, 1, 1, 0.9
                foreground_color: 0, 0, 0, 1
                
            TextInput:
                id: Register_Name
                hint_text: "Enter Your Name"
                size_hint_y: None
                height: '50dp'
                font_size: '18sp'
                background_color: 1, 1, 1, 0.9
                foreground_color: 0, 0, 0, 1                

            TextInput:
                id: Register_age
                hint_text: "Age"
                size_hint_y: None
                height: '50dp'
                font_size: '18sp'
                background_color: 1, 1, 1, 0.9
                foreground_color: 0, 0, 0, 1
                
            TextInput:
                id: Register_gender
                hint_text: "Gender Male or Female"
                size_hint_y: None
                height: '50dp'
                font_size: '18sp'
                background_color: 1, 1, 1, 0.9
                foreground_color: 0, 0, 0, 1


            TextInput:
                id: Register_category
                hint_text: "Category SC or ST or OBC or General"
                size_hint_y: None
                height: '50dp'
                font_size: '18sp'
                background_color: 1, 1, 1, 0.9
                foreground_color: 0, 0, 0, 1

            TextInput:
                id: Register_type
                hint_text: "Type of farmer Small(If you have field > 0.5 h) or Big"
                size_hint_y: None
                height: '50dp'
                font_size: '18sp'
                background_color: 1, 1, 1, 0.9
                foreground_color: 0, 0, 0, 1

            TextInput:
                id: Register_Addres_line1
                hint_text: "Address Line 1"
                size_hint_y: None
                height: '50dp'
                font_size: '18sp'
                background_color: 1, 1, 1, 0.9
                foreground_color: 0, 0, 0, 1

            TextInput:
                id: Register_Addres_line2
                hint_text: "Address Line 2"
                size_hint_y: None
                height: '50dp'
                font_size: '18sp'
                background_color: 1, 1, 1, 0.9
                foreground_color: 0, 0, 0, 1

            TextInput:
                id: Register_district
                hint_text: "District"
                size_hint_y: None
                height: '50dp'
                font_size: '18sp'
                background_color: 1, 1, 1, 0.9
                foreground_color: 0, 0, 0, 1

            TextInput:
                id: Register_state
                hint_text: "State"
                size_hint_y: None
                height: '50dp'
                font_size: '18sp'
                background_color: 1, 1, 1, 0.9
                foreground_color: 0, 0, 0, 1


            Button:
                text: "Register"
                size_hint_y: None
                height: '60dp'  
                font_size: '18sp'
                background_color: 0.2, 0.6, 0.4, 1
                color: 1, 1, 1, 1
                background_normal: r'home_button.png'  
                background_down: r'home_button.png'            
                on_press: root.update_user()

            Button:
                text: "Back"
                size_hint_y: None
                height: '60dp'
                font_size: '18sp'
                background_color: 0.2, 0.6, 0.4, 1
                color: 1, 1, 1, 1 
                background_normal: r'home_button.png'  
                background_down: r'home_button.png'                      
                on_press: app.root.current = 'profile'

<ImageGalleryScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: dp(10), dp(20)
        spacing: dp(15) 
        canvas.before:
            Color:
                rgba: 0.2, 0.6, 0.4, 1
            Rectangle:
                source: r'bg.png'  
                pos: self.pos
                size: self.size                  
        BoxLayout:
            size_hint_y: None
            height: '60dp' 
            padding: [10, 10]
            canvas.before:
                Color:
                    rgba: 1, 1, 1, 1  
                RoundedRectangle:
                    source: r'bg.png'
                    pos: self.pos
                    size: self.size
                    radius: [10]
                Color:
                    rgba: 0.8, 0.9, 0.8, 1 
                Line:
                    width: 2
                    rounded_rectangle: (self.x, self.y, self.width, self.height, 10)
            Label:
                text: "Latest Problem of Plants"
                font_size: '20sp'  
                bold: True
                color: 0, 0, 0, 1
                halign: 'center'
                valign: 'middle'
                text_size: self.size
                     
        ScrollView:
            size_hint: (1, None)
            height: '300dp'  
            BoxLayout:
                id: problems_box  
                orientation: 'vertical'
                size_hint_y: None
                height: self.minimum_height  

                BoxLayout:
                    orientation: 'horizontal'
                    size_hint_y: None
                    height: '80dp'  
                    Image:
                        source: r'1st problem.png'  
                        size_hint_x: None
                        width: '60dp'  
                        size_hint: (None, None)  # Use tuple format for size_hint
                        pos_hint: {"center_x": 0.5, "center_y": 0.5}                 
                    BoxLayout:
                        orientation: 'vertical'
                        Label:
                            text: "1. Leaves turning yellow due to overwatering."
                            size_hint_y: None
                            height: '40dp'
                        Label:
                            text: "Description: The leaves are showing signs of yellowing due to excessive water intake."
                            size_hint_y: None
                            height: '40dp'
                BoxLayout:
                    orientation: 'horizontal'
                    size_hint_y: None
                    height: '80dp'  
                    Image:
                        source: r'3rd problem.jpg'  
                        size_hint_x: None
                        width: '60dp'  
                        size_hint: (None, None)  # Use tuple format for size_hint
                        pos_hint: {"center_x": 0.5, "center_y": 0.5}                 
                    BoxLayout:
                        orientation: 'vertical'
                        Label:
                            text: "2. Fungal infection causing leaf spots."
                            size_hint_y: None
                            height: '40dp'
                        Label:
                            text: "Description: Fungal spores are affecting the leaves, requiring treatment."
                            size_hint_y: None
                            height: '40dp'
        Button:
            text: "Back"
            size_hint_y: None
            height: 50
            background_color: 0.2, 0.6, 0.4, 1
            font_size: 18
            color: 1, 1, 1, 1 
            background_normal: 'home_button.png' 
            background_normal: 'home_button.png' 
            on_press: app.root.current = 'home'

<ProblemScreen>:
    ScrollView:
        BoxLayout:
            orientation: 'vertical'
            padding: dp(10), dp(20)
            spacing: 10 
            canvas.before:
                Color:
                    rgba: 0.2, 0.6, 0.4, 1
                Rectangle:
                    source: r'bg.png'  
                    pos: self.pos
                    size: self.size 
                    
            BoxLayout:
                size_hint_y: None
                height: '60dp'
                padding: [10, 10]
                canvas.before:
                    Color:
                        rgba:1, 1, 1, 1                
                    RoundedRectangle:
                        source: r'bg.png'
                        pos: self.pos
                        size: self.size
                        radius: [10]
                    Color:
                        rgba: 0.8, 0.9, 0.8, 1
                    Line:
                        width: 3
                        rounded_rectangle: (self.x, self.y, self.width, self.height, 10)
                Label:
                    text: "Register Your Problem with Us"
                    font_size: '20sp'
                    bold: True
                    color: 0, 0, 0, 1
                    halign: 'center'
                    valign: 'middle'
                    text_size: self.size

            TextInput:
                id: Register_Problem
                hint_text: "What is problem you have.....?"
                size_hint_y: None
                height: '100dp'
                font_size: '18sp'
                background_color: 1, 1, 1, 0.9
                foreground_color: 0, 0, 0, 1
                             

            BoxLayout:
                orientation: 'vertical'
                padding: [10, 10, 10, 10]
                spacing: 10

            Label:
                text: "Do you want to upload an image?"
                font_size: '20sp'
    
            Spinner:
                id: Register_Image
                text: "Select"
                values: ["Yes", "No"]
                size_hint_y: None
                height: '50dp'
                font_size: '18sp'
                color: 0, 0, 0, 1
                background_color: 0.2, 0.6, 0.4, 1
                background_down: r'home_button.png'
                background_normal: r'home_button.png'
                bold: True 
                
            Label:
                id: selected_image_label
                text: "No image selected"
                font_size: '20sp'
                bold: True
                color: 0, 0, 0, 1
                halign: 'center'
                valign: 'middle'
                text_size: self.size               

            Button:
                text: "Select Image"
                size_hint_y: None
                height: '60dp'
                font_size: '18sp'
                background_color: 0.2, 0.6, 0.4, 1
                color: 1, 1, 1, 1
                background_normal: r'home_button.png'  
                background_down: r'home_button.png'            
                on_press: root.open_filechooser()               

            Button:
                text: "Register"
                size_hint_y: None
                height: '60dp'  
                font_size: '18sp'
                background_color: 0.2, 0.6, 0.4, 1
                color: 1, 1, 1, 1
                background_normal: r'home_button.png'  
                background_down: r'home_button.png'            
                on_press: root.upload_problem()

            Button:
                text: "Back"
                size_hint_y: None
                height: '60dp'
                font_size: '18sp'
                background_color: 0.2, 0.6, 0.4, 1
                color: 1, 1, 1, 1 
                background_normal: r'home_button.png'  
                background_down: r'home_button.png'                      
                on_press: app.root.current = 'home'
            
<AboutUsScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: dp(10), dp(20)
        spacing: dp(15)
        canvas.before:
            Color:
                rgba: 0.8, 0.9, 0.8, 1
            Rectangle:
                source: r'bg.png'  
                pos: self.pos
                size: self.size

        # Container for welcome message
        BoxLayout:
            size_hint_y: None
            height: '60dp'
            padding: [10, 10]
            canvas.before:
                Color:
                    rgba: 1, 1, 1, 1
                RoundedRectangle:
                    source: r'bg.png'
                    pos: self.pos
                    size: self.size
                    radius: [10]
                Color:
                    rgba: 0.8, 0.9, 0.8, 1
                Line:
                    width: 2
                    rounded_rectangle: (self.x, self.y, self.width, self.height, 10)
            Label:
                text: "About Us"
                font_size: '20sp'
                bold: True
                color: 0, 0, 0, 1
                halign: 'center'
                valign: 'middle'
                text_size: self.size

        ScrollView:
            size_hint: (1, None)
            height: '300dp'
            BoxLayout:
                id: Aboutus_box
                orientation: 'vertical'
                size_hint_y: None
                height: self.minimum_height
                padding: [10, 10]

                Label:
                    text: "Welcome to Inviculture, a platform dedicated to empowering farmers by connecting them with experienced agronomists."
                    size_hint_y: None
                    color: 0, 0, 0.5, 1
                    height: self.texture_size[1]
                    
                Label:
                    text: "Founded with the vision of Ayush Gangwar and a team committed to advancing agricultural practices."
                    size_hint_y: None
                    color: 0, 0, 0.5, 1
                    height: self.texture_size[1]

                Label:
                    text: "Our mission is to make it easier for farmers to make informed decisions that increase crop yields."
                    size_hint_y: None
                    color: 0, 0, 0.5, 1
                    height: self.texture_size[1]

                Label:
                    text:"At Inviculture, we believe in the strength of collaboration."
                    size_hint_y :None 
                    color : (0 , .5 , .8 , .9)
                    height :self.texture_size[1]

                Label:
                    text:"Join us on this journey to transform agriculture one farm at a time."
                    size_hint_y :None 
                    color : (0 , .5 , .8 , .9)
                    height :self.texture_size[1]

                # New Contact Details Section
                Label:
                    text:"Contact Us"
                    font_size:'18sp'
                    bold : True 
                    color : (0 , .5 , .8 , .9)
                    size_hint_y :None 
                    height :dp(30)

                Label:
                    text:"Email : inviculture119@gmail.com"
                    size_hint_y :None 
                    color : (0 , .5 , .8 , .9)
                    height :self.texture_size[1]

                Label:
                    text:"Phone : +91 9456 9355 85"
                    size_hint_y :None 
                    color : (0 , .5 , .8 , .9)
                    height :self.texture_size[1]

                Label:
                    text:"Follow us on social media:"
                    size_hint_y :None 
                    color : (0 , .5 , .8 , .9)
                    height :self.texture_size[1]

                Label:
                    text:"Facebook | Instagram"
                    size_hint_y :None 
                    color : (0 , .5 , .8 , .9)
                    height :self.texture_size[1]

        Button:
            text:"Back"
            size_hint_y :None 
            height :dp(50)
            background_color:(0.2 , .6 , .4 , .9)
            font_size :18 
            color:(1 , .9 , .9 , .9) 
            background_normal: r'home_button.png'  
            background_down: r'home_button.png'             
            on_press : app.root.current = 'home'

''')

class BaseScreen(Screen):  
    def show_popup(self, title, message):  
        popup = Popup(title=title, content=Label(text=message), size_hint=(0.8, 0.4))  
        popup.open()
        Clock.schedule_once(lambda dt: popup.dismiss(), 5) 


class LoginScreen(Screen):
    def login(self):
        email = self.ids.login_email.text
        password = self.ids.login_password.text
        
        if not self.is_valid_email(email):
            self.show_popup("Login Error", "Please enter a valid email address")
            return

        if email and password:  
            try:  
                user_ref = db.collection('users').document(email).get()
                
                if user_ref.exists:
                    user_data = user_ref.to_dict()
                    
                    if bcrypt.checkpw(password.encode('utf-8'), user_data.get('password').encode('utf-8')):
                        App.get_running_app().user_email = email  
                        self.manager.user_email = email  
                        self.manager.current = 'home'  
                    else:  
                        self.show_popup("Login Error", "Invalid email or password")  
                else:
                    self.show_popup("Login Error", "Invalid email or password")  
            except Exception as e:  
                self.show_popup("Login Error", str(e))  
        else:  
            self.show_popup("Login Error", "Please enter both email and password") 

    def is_valid_email(self, email):
        regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        return re.match(regex, email) is not None 

    def show_popup(self, title, message):  
        popup = Popup(title=title, content=Label(text=message), size_hint=(0.8, 0.4))  
        popup.open()
        Clock.schedule_once(lambda dt: popup.dismiss(), 5)        
           
class SignupScreen(BaseScreen):
    def signup(self):  
        email = self.ids.signup_email.text  
        password = self.ids.signup_password.text 
        confirm_password = self.ids.confirm_password.text
        username = self.ids.signup_username.text  
        phone = self.ids.signup_phone.text  

        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            self.show_popup("Invalid Email", "Please enter a valid email address.")
            return

        if not phone.isdigit():
            self.show_popup("Invalid Phone Number", "Please enter a valid phone number containing only digits.")
            return

        if not re.match(r'^(?=.*[A-Z])(?=.*\W)(?=.*\d)[A-Za-z\d\W]{8,}$', password):
            self.show_popup("Invalid Password", "Password must be at least 8 characters long, contain one uppercase letter, one symbol, and one digit.")
            return

        if not re.match(r'^[A-Za-z0-9_]+$', username):
            self.show_popup("Invalid Username", "Username can only contain letters, numbers, and underscores.")
            return

        if password == confirm_password:
            if email and password and username and phone:  
                try:  
                    doc_ref = db.collection('users').document(email)
                    doc = doc_ref.get()
                    if doc.exists:
                        self.show_popup("Signup Error", "This email is already registered. Please login.")
                        self.manager.current = 'login'
                    else:
                        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
                        
                        user_data = {  
                            "email": email,  
                            "phone": phone,  
                            "password": hashed_password.decode('utf-8'),  
                            "username": username  
                        }  
                        doc_ref.set(user_data)
                        self.manager.current = 'login'  
                except Exception as e:  
                    self.show_popup("Signup Error", str(e))  
            else:  
                self.show_popup("Signup Error", "Please fill in all the details")
        else:
            self.show_popup("Password Error", "Passwords do not match. Please check.")       

class ForgotPasswordScreen(BaseScreen):  
    def send_otp(self):  
        email = self.ids.forgot_email.text

        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            self.show_popup("Invalid Email", "Please enter a valid email address.")
            return
        
        if email:  
            try:  
                doc_ref = db.collection('users').document(email)
                doc = doc_ref.get()
                
                if doc.exists:
                    otp = generate_otp()  
                    body = f"Your OTP is: {otp}"  
                    send_email(email, "Your OTP", body)  
                    self.otp = otp  
                    self.show_popup("OTP Sent", f"OTP has been sent to {email}")  
                    self.manager.current = 'verify_otp'  
                else:
                    self.show_popup("User Not Found", "No account found with this email. Please sign up first.")
                    self.manager.current = 'signup' 
            except Exception as e:  
                self.show_popup("Error", str(e))  
        else:  
            self.show_popup("Error", "Please enter a valid email")  

class VerifyOTPScreen(BaseScreen):  
    def verify_otp(self):  
        entered_otp = self.ids.otp_input.text  
        if entered_otp == str(self.manager.get_screen('forgot_password').otp):  
            self.show_popup("Success", "OTP verified successfully!")  
            self.manager.current = 'reset_password'  
        else:  
            self.show_popup("Error", "Invalid OTP. Please try again.")  

class ResetPasswordScreen(BaseScreen):  
    def reset_password(self):  
        new_password = self.ids.new_password.text  
        confirm_password = self.ids.confirm_password.text  
        email = self.manager.get_screen('forgot_password').ids.forgot_email.text  

        if new_password and confirm_password == confirm_password:  
            try:
                hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())  
                user_ref = db.collection('users').document(email)  
                user_ref.update({'password': hashed_password.decode('utf-8')})  
                self.show_popup("Success", "Password reset successfully!")  
                self.manager.current = 'login'  

            except Exception as e:  
                self.show_popup("Error", str(e))  
        else:  
            self.show_popup("Error", "Passwords do not match or are empty")  

class HomeScreen(Screen):
    pass

class ProfileScreen(Screen):
    username = StringProperty('')
    Name = StringProperty('') 
    type = StringProperty('')   
    email = StringProperty('')
    category = StringProperty('')
    phone = StringProperty('')
    Address_line1 = StringProperty('')
    Address_line2 = StringProperty('')
    gender = StringProperty('')
    State = StringProperty('')
    district = StringProperty('')
    age = StringProperty('')    
    
    def on_enter(self):
        user_email = self.manager.user_email
        print(f"User email from ScreenManager: {user_email}")

        try:
            user_ref = db.collection("users").document(user_email).get() 
            
            if user_ref.exists:  
                user_data = user_ref.to_dict()
                self.ids.user_name_label.text = f"User_name: {user_data.get('username', 'Not Found')}"
                self.ids.name_label.text = f"Name: {user_data.get('Name', 'Not Found')}"
                self.ids.type_label.text = f"Type: {user_data.get('type', 'Not Found')}"
                self.ids.email_label.text = f"Email: {user_data.get('email', 'Not Found')}"
                self.ids.category_label.text = f"Category: {user_data.get('category', 'Not Found')}"
                self.ids.phone_label.text = f"Phone: {user_data.get('phone', 'Not Found')}"
                self.ids.Address_line1_label.text = f"Address line 1: {user_data.get('Address_line1', 'Not Found')}"
                self.ids.Address_line2_label.text = f"Address line 2: {user_data.get('Address_line2', 'Not Found')}"
                self.ids.gender_label.text = f"Gender: {user_data.get('gender', 'Not Found')}"
                self.ids.State_label.text = f"State: {user_data.get('State', 'Not Found')}"
                self.ids.district_label.text = f"District: {user_data.get('district', 'Not Found')}"
                self.ids.age_label.text = f"Age: {user_data.get('age', 'Not Found')}"
            else:
                self.ids.user_name_label.text = "username: Not Found Please Register with us"
                self.ids.type_label.text = "type: Not Found Please Register with us"
                self.ids.name_label.text = "Name: Not Found Please Register with us"
                self.ids.email_label.text = "Email: Not Found Please Register with us"
                self.ids.phone_label.text = "Phone: Not Found Please Register with us"
                self.ids.Address_line1_label.text = "Address line 1: Not Found Please Register with us"
                self.ids.Address_line2_label.text = "Address line 2: Not Found Please Register with us"
                self.ids.gender_label.text = "Gender: Not Found Please Register with us"
                self.ids.category_label.text = "category: Not Found Please Register with us"
                self.ids.State_label.text = "State: Not Found Please Register with us"
                self.ids.district_label.text = "district: Not Found Please Register with us"
                self.ids.age_label.text = "age: Not Found Please Register with us"
                
        except Exception as e:
            print(f"Error fetching user data: {str(e)}")

# REgister your Details With us     
class RegisterScreen(Screen):
    def show_popup(self, title, message):  
        popup = Popup(title=title, content=Label(text=message), size_hint=(0.8, 0.4))  
        popup.open()
        Clock.schedule_once(lambda dt: popup.dismiss(), 5) 
        
    def update_user(self):
        email = self.ids.Register_email.text  
        name = self.ids.Register_Name.text
        age = self.ids.Register_age.text
        gender = self.ids.Register_gender.text
        category = self.ids.Register_category.text
        type_ = self.ids.Register_type.text
        address_line1 = self.ids.Register_Addres_line1.text
        address_line2 = self.ids.Register_Addres_line2.text
        state = self.ids.Register_state.text
        district = self.ids.Register_district.text

        if email and name and age and gender and address_line1 and address_line2 and category and type_ and state and district:
            if not age.isdigit() or int(age) <= 0:
                self.show_popup("Update Error", "Please enter a valid age.")
                return

            try:
                doc_ref = db.collection('users').document(email)

                user_data = {
                    "Name": name,
                    "age": int(age),  
                    "gender": gender,
                    "category": category,
                    "type": type_,
                    "Address_line1": address_line1,
                    "Address_line2": address_line2,
                    "State": state,
                    "district": district
                }

                doc_ref.set(user_data, merge=True)
                user_email = self.manager.user_email
                body = f"Thank You For Registering Your Detais With INVICULTURE , We Always Here for Your Help"
                # self.send_email(user_email,body)                
                self.show_popup("Update Success", "User details updated successfully.")
                
                self.clear_fields()
                self.manager.current = 'login'
            except Exception as e:
                self.show_popup("Update Error", str(e))
                print(f"Error during update: {e}") 
        else:
            self.show_popup("Error", "Please fill in all the details")

    def clear_fields(self):
        self.ids.Register_email.text = ''
        self.ids.Register_Name.text = ''
        self.ids.Register_age.text = ''
        self.ids.Register_gender.text = ''
        self.ids.Register_category.text = ''
        self.ids.Register_type.text = ''
        self.ids.Register_Addres_line1.text = ''
        self.ids.Register_Addres_line2.text = ''
        self.ids.Register_state.text = ''
        self.ids.Register_district.text = ''

 
class ImageGalleryScreen(BaseScreen):  
    pass  

class ProblemScreen(Screen):
    # Store Users Selected image_location for a Short time Period 
    selected_image_path = StringProperty("")  

    def show_popup(self, title, message):  
        popup = Popup(title=title, content=Label(text=message), size_hint=(0.8, 0.4))  
        popup.open()
        Clock.schedule_once(lambda dt: popup.dismiss(), 5)   
    
    selected_image_path = StringProperty("") 
    
    def upload_image_to_firebase(self, image_path):
        blob = bucket.blob(f'user_problems/{os.path.basename(image_path)}')
        blob.upload_from_filename(image_path)
        return blob.public_url
    
    def open_filechooser(self): 
        downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
        content = FileChooserIconView(path=downloads_path)
        content.filters = ['*.png', '*.jpg', '*.jpeg', '*.gif', '*.bmp']
        content.bind(on_submit=self.file_selected)
        self.popup = Popup(title="Select Image", content=content, size_hint=(0.9, 0.9))
        self.popup.open() 

    def file_selected(self, file_chooser, selection, *args):
        if selection:
            selected_file_path = selection[0]
            print(f"Selected file: {selected_file_path}")
            self.selected_image_path = selected_file_path 
            self.ids.selected_image_label.text = os.path.basename(selected_file_path)  
            self.popup.dismiss() 

    def upload_problem(self):
        Problem = self.ids.Register_Problem.text  
        user_email = self.manager.user_email 

        if Problem and self.selected_image_path and user_email:  
            try:
                unique_problem_id = re.sub(r'\W+', '', str(uuid.uuid4()))  
                
                Problem_image = self.upload_image_to_firebase(self.selected_image_path) 

                user_ref = db.collection('User_Problems').document(user_email)
                
                problem_data = {
                    "Problem_Text": Problem,
                    "Problem_Image": Problem_image,
                    "Problem_ID": unique_problem_id 
                }
                user_ref.set({unique_problem_id: problem_data}, merge=True)
                body = f"Your problem has been registered successfully with ID: {unique_problem_id} , Please Note down it For Future Need"
                self.send_email(user_email, unique_problem_id, body)
                self.show_popup("Success", "Problem registered successfully.")
                self.clear_fields()
            except Exception as e:
                self.show_popup("Error", str(e))
                print(f"Error during update: {e}")
        else:
            self.show_popup("Error", "Please fill in all the details")

    def clear_fields(self):
        self.ids.Register_Problem.text = ""
        self.ids.selected_image_label.text = "No image selected"  # Reset the label as well
        self.selected_image_path = ""  # Reset the selected image path

#About us Screen
class AboutUsScreen(BaseScreen):  
    pass  

# Screen Maneger
class MyScreenManager(ScreenManager):
    #store Users Email for Create a Loggin Session
    user_email = StringProperty("")
            
class MyApp(App):
     
    def build(self):  
        sm = MyScreenManager()  
        sm.add_widget(LoginScreen(name='login'))  
        sm.add_widget(SignupScreen(name='signup'))  
        sm.add_widget(ForgotPasswordScreen(name='forgot_password'))
        sm.add_widget(ProfileScreen(name='profile'))
        sm.add_widget(RegisterScreen(name='Register'))  
        sm.add_widget(VerifyOTPScreen(name='verify_otp'))  
        sm.add_widget(ResetPasswordScreen(name='reset_password'))  
        sm.add_widget(HomeScreen(name='home'))  
        sm.add_widget(ImageGalleryScreen(name='gallery'))  
        sm.add_widget(ProblemScreen(name='ProblemScreen'))  
        sm.add_widget(AboutUsScreen(name='about_us'))  
        return sm  

if __name__ == '__main__':  
    MyApp().run()

