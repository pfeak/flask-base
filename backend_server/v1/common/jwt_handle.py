from backend_server import jwt, redis


# @jwt.user_claims_loader
# def add_claims_to_access_token(identity):
#     # return {
#     #     'hello': identity,
#     #     'foo': ['bar', 'baz']
#     # }
#     return identity


# # create_access_token 时被调用
# @jwt.user_identity_loader
# def user_identity_lookup(user):
#     return user


# jwt_required 触发检测时调用
@jwt.token_in_blacklist_loader
def check_if_token_is_revoked(decrypted_token):
    jti = decrypted_token['jti']
    entry = redis.get(jti)
    if entry is None:
        return True
    return entry == 'true'
