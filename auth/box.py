from boxsdk import JWTAuth, Client

import box_config as config

auth = JWTAuth(
    client_id=config.client_id,
    client_secret=config.client_secret,
    enterprise_id=config.enterprise_id,
    jwt_key_id=config.jwt_key_id,
    rsa_private_key_file_sys_path=config.rsa_private_key_file_sys_path
)


def box_user(userId=config.user_id):
    client = Client(auth)

    owner = client.user(user_id=userId)

    auth.authenticate_app_user(owner)

    return client


def box_access_token():
    auth.authenticate_instance()

    client = Client(auth)

    return client
