import logging

from smtplib import SMTPException

from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template.loader import get_template
from django.template import TemplateDoesNotExist, TemplateSyntaxError


class Emailer(object):
    logger = logging.getLogger('email')

    def __init__(self, config):
        self.config = config

    def __render_template(self, filename):
        """
        Function renders a template by loading from disk and using self.data as context
        :return: The template processed or boolean false if not processed
        """
        try:
            template = get_template(filename)
            return template.render(self.config['data'])
        except TemplateDoesNotExist as ex:
            self.logger.error('Template {} does not exist'.format(filename))
            self.logger.error(ex)
        except TemplateSyntaxError as ex:
            self.logger.error('Template {} has syntax error'.format(filename))
            self.logger.error(ex)
        except Exception as ex:
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

    def __send_plain(self):
        """
        Get plain content for email and send message
        :return: boolean
        """
        plain_content = self.__render_template(self.config['templates']['plain'])
        if plain_content:
            email = EmailMessage(
                self.config['subject'],
                plain_content,
                self.config['from_email'],
                self.config['recipient'],
            )
            if self.config['reply_to']:
                email.reply_to = self.config['reply_to']
            return self.__deliver(email)
        return False

    def __send_multipart(self):
        html_content = self.__render_template(self.config['templates']['html'])
        plain_content = self.__render_template(self.config['templates']['plain'])
        if html_content and plain_content:
            email = EmailMultiAlternatives(
                self.config['subject'],
                plain_content,
                self.config['from_email'],
                self.config['recipient']
            )
            if self.config['reply_to']:
                email.reply_to = self.config['reply_to']
            email.attach_alternative(html_content, 'text/html')
            return self.__deliver(email)
        return False

    def send(self):
        """
        Function gets template content and attempts to send email
        :return: Boolean on whether successful
        """
        if 'plain' in self.config['templates'] and 'html' in self.config['templates']:
            self.__send_multipart()
        else:
            self.__send_plain()
