import traceback

def log_err(app, msg, expection, send_mail):
    """Loggea un error.
    app es el objecto app/current_app
    msg el texto a loggear
    expection la Exception (o None)
    send_mail un boolean (si envía mail o no)
    """
    try:
        err_log_msg = msg
        if expection:
            tb = traceback.format_exc()
            err_log_msg += ' ' + str(expection or '') + '\n' + tb
        app.logger.error(err_log_msg)
    except Exception as e:
        print('ERROR: El logger no está funcionando!!', e)
    if send_mail and app.config.get('_using_mailer'):
        try:
            app._mailer.send_error_mail(err_log_msg)
        except Exception as e:
            log_err(app, 'No se pudo enviar el mail con el error:', e, False)
