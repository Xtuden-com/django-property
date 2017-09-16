import logging

from smtplib import SMTPException

from django.core.mail import EmailMessage
from django.template.loader import get_template
from django.template import TemplateDoesNotExist, TemplateSyntaxError


class Emailer(object):

    logger = logging.getLogger('email')

    def __init__(self, subject, recipient, from_email, reply_to, data, filename):
        self.subject = subject
        self.filename = filename
        self.recipient = recipient
        self.from_email = from_email
        self.reply_to = reply_to
        self.data = data

    def __render_template(self):
        """
        Function renders a template by loading from disk and using self.data as context
        :return: The template processed or boolean false if not processed
        """
        template = get_template(self.filename)
        try:
            return template.render(self.data)
        except TemplateDoesNotExist as ex:
            self.logger.error('Template {} does not exist'.format(self.filename))
            self.logger.error(ex)
        except TemplateSyntaxError as ex:
            self.logger.error('Template {} has syntax error'.format(self.filename))
            self.logger.error(ex)
        return False

    def __deliver(self, email):
        """
        Function will attempt to deliver email
        :param email: an email address
        :return: Boolean on whether successful
        """
        try:
            return bool(email.send(fail_silently=False))
        except SMTPException as ex:
            self.logger.error("Unable to send email")
            self.logger.error(ex)
        return False

    def send(self):
        """
        Function gets template content and attempts to send email
        :return: Boolean on whether successful
        """
        content = self.__render_template()
        if content:
            email = EmailMessage(
                self.subject,
                content,
                self.from_email,
                self.recipient,
            )
            if self.reply_to:
                email.reply_to = self.reply_to
            return self.__deliver(email)
        return False
