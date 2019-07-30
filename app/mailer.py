class Mailer:
    def __init__(self, app):
        self.server = app.config.get('SMTP_SERVER')
        self.port = app.config.get('SMTP_PORT')
        self.user = app.config.get('SMTP_USER')
        self.password = app.config.get('SMTP_PASSWORD')
        self.target_mail = app.config.get('SMTP_TARGET_EMAIL')

    def send_mail(self, subject, msg):
        import smtplib
        server = smtplib.SMTP(self.server, self.port)

        server.ehlo()
        server.starttls()
        server.ehlo()

        # Next, log in to the server
        server.login(self.user, self.password)

        # Send the mail
        message = 'Subject: {}\n\n{}'.format(subject, msg)
        return server.sendmail(self.user, self.target_mail, message)

    def send_error_mail(self, msg):
        return self.send_mail('Error en web de causas comunes', msg)

