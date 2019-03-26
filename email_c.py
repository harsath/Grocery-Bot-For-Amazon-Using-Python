import smtplib
import creds as config
class EmailSender:
    def send_email(self,subject, msg):
        try:
            #Using SMTP Client For Sending Messaged Via Gmail.
            server = smtplib.SMTP('smtp.gmail.com:587')
            server.ehlo()
            server.starttls()
            server.login(config.FROM_EMAIL, config.FROM_PASSWORD)
            message = 'Subject: {}\n\n{}'.format(subject, msg)
            server.sendmail(config.FROM_EMAIL,config.TO_EMAIL,message)
            server.quit()
            print("Email Send Successfully.")
        except:
            print("Email failed to send.")
