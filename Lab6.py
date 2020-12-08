import os
import smtplib
from email.encoders import encode_base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.audio import MIMEAudio
from tkinter import *
from tkinter import filedialog as fd

pathDec = ''
path_media=''

root = Tk()

path_file_label = Label(root, text='Введите путь к файлу с електронными адресами')
path_file_entry = Entry(root, width=50)

text_message_label = Label(root, text='Введите текст сообщения для рассылки')
text_message_entry = Entry(root, width=50)

server_label = Label(root, text='Введите SMTP сервер')
server_entry = Entry(root, width=50)

port_label = Label(root, text='Введите порт')
port_entry = Entry(root, width=50)

login_label = Label(root, text='Введите логин')
login_entry = Entry(root, width=50)

password_label = Label(root, text='Введите пароль')
password_entry = Entry(root, width=50)

media_button = Button(root, bg='black', fg='white', width=100, text='Выберите аудиофайл')
output_file_button = Button(root, bg='black', fg='white', width=100, text='Выберите файл для записи результатов')
start_button = Button(root, width=100, text='Стартуем!')

result_label = Label(root, width=100, text='')

def openfile(event):
    global pathDec
    path = fd.askopenfilename()

output_file_button.bind('<Button-1>', openfile)

def open_media_file(event):
    global path_media
    path_media = fd.askopenfilename()

media_button.bind('<Button-1>', open_media_file)

def send(event):

   #with open(path, 'r+') as password_list:
        sms_list = open(path_file_entry.get(), 'r+')
        email_list = sms_list.read().split('\n')
        try:
            msg = MIMEMultipart()
            msg['From'] = login_entry.get()
            msg['To'] = ", ".join(email_list)
            msg['Subject'] = "Test Message"
            msg.attach(MIMEText(text_message_entry.get(), 'plain'))
            fp = open(path_media, "rb")
            name = os.path.basename(path_media)
            to_attach = MIMEAudio("application", "octet-stream")
            to_attach.set_payload(fp.read())
            encode_base64(to_attach)
            to_attach.add_header("Content-Disposition", "attachment",filename=name)
            fp.close()
            msg.attach(to_attach)
            server = smtplib.SMTP(server_entry.get(),int(port_entry.get()))
            server.starttls()
            server.login(msg['From'], password_entry.get())
            server.sendmail(msg['From'], email_list, msg.as_string())
            server.quit()
        except :
            result_label['text'] = "Что-то пошло не так"
        else:
            result_label['text'] = "Все ок"
            output = open(pathDec, 'w')
            output.write(server_entry.get() + '\n' +
                         port_entry.get() + '\n' +
                         login_entry.get() + '\n' +
                         password_entry.get() + '\n' +
                         path_file_entry.get() + '\n' +
                         msg['To'] + '\n' +
                         result_label['text'])
            output.close()
start_button.bind('<Button-1>', send)

path_file_label.pack()
path_file_entry.pack()
text_message_label.pack()
text_message_entry.pack()
server_label.pack()
server_entry.pack()
port_label.pack()
port_entry.pack()
login_label.pack()
login_entry.pack()
password_label.pack()
password_entry.pack()
media_button.pack()
output_file_button.pack()
start_button.pack()
result_label.pack()

root.mainloop()