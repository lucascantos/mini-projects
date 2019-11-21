import serverless_sdk
sdk = serverless_sdk.SDK(
    tenant_id='lucascantos',
    application_name='myapp',
    app_uid='SpHSHgLCjg8QDzR1NN',
    tenant_uid='BczkXMC16ZQcZjm0TY',
    deployment_uid='27c88a5a-2247-4acc-be08-b695bcc51131',
    service_name='websocket-api',
    stage_name='dev',
    plugin_version='2.0.0'
)
handler_wrapper_kwargs = {'function_name': 'websocket-api-dev-default', 'timeout': 6}
try:
    user_handler = serverless_sdk.get_user_handler('handler.default')
    handler = sdk.handler(user_handler, **handler_wrapper_kwargs)
except Exception as error:
    e = error
    def error_handler(event, context):
        raise e
    handler = sdk.handler(error_handler, **handler_wrapper_kwargs)
