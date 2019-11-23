def authenticating_decorator(func):
    def wrapper(*args, **kw):
        try:
             '''
            auth user before execution of the required code
            if user is not authenticated bottle.HTTPError is raised
            '''
            auth()  
            return func(*args, **kw) #calling func here
        except HTTPError as e:
            return handle_auth_error(e)  #calling the handle_auto_error here

return wrapper #notice - no call here, just return the wrapper