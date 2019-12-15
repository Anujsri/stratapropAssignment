import mandrill
from strataprop_server import app


def send_template_mail(template_name=None, template_content=None, to=None, subject='', from_email='', from_name='',
                       merge=False, global_merge_vars=None, merge_vars=None, attachments=None, reply_to=None):
    if to:
        try:
            mandrill_client = mandrill.Mandrill(app.config['MANDRILL_API_KEY'])
            message = {
                'subject': subject,
                'from_email': from_email,
                'from_name': from_name,
                'to': to,
                'track_opens': True,
                'important': True,
                'inline_css': True,
                'auto_html': True
            }
            if reply_to:
                message['headers'] = {"Reply-To": reply_to}
            if merge:
                message['merge'] = True
                message['merge_language'] = 'handlebars'
                if merge_vars:
                    message['merge_vars'] = merge_vars
                if global_merge_vars:
                    message['global_merge_vars'] = global_merge_vars
            if attachments:
                message['attachments'] = attachments
            if template_name is not None:
                if template_content is None:
                    template_content = {}
                mandrill_client.messages.send_template(
                    template_name=template_name,
                    template_content=template_content,
                    message=message,
                    async=False,
                    ip_pool='Main Pool'
                )
        except mandrill.Error, e:
            # Mandrill errors are thrown as exceptions
            app.logger.error('A mandrill error occurred: %s - %s' % (e.__class__, e))
            raise


def list_mail_templates():
    mandrill_client = mandrill.Mandrill(app.config['MANDRILL_API_KEY'])
    result = mandrill_client.templates.list()
    app.logger.info("Available email templates in mandrill: %s" % result)
