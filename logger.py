import helpers
template_info = "{time}: {message}"
template_error = "{time}: ERROR: {message}"

def log(message):
    print(helpers.fill_template(template_info,time=helpers.get_today_minsk_time(),message=str(message)))

def log_user_action(user_message_text):
    log(helpers.fill_template(template_info,time=helpers.get_today_minsk_time(),message=user_message_text))

def log_error(error_message):
    log(helpers.fill_template(template_error,time=helpers.get_today_minsk_time(),message=error_message))