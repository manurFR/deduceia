def ask_for(prompt, wanted_type=unicode, allowed=[]):
    while True:
        response = raw_input(prompt)
        if len(allowed) > 0 and response not in allowed:
            print '> Invalid answer (allowed : {0})'.format('/'.join(allowed))
        else:
            return wanted_type(response)