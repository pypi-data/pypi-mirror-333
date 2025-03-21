"""Custom authentication classes"""

from mozilla_django_oidc.auth import OIDCAuthenticationBackend


class DryOIDCAuthBackend(OIDCAuthenticationBackend):
    """
    Custom authentication backend to be used with mozilla-django-oidc.
    The customizations center around using the user's NetId from the token
    for their username, rather than their email address.

    Subclass of mozilla_django_oidc.auth.OIDCAuthenticationBackend
    """

    def create_user(self, claims):
        """
        Create a new User with data from claims

        Overrides OIDCAuthenticationBackend.create_user

        Args:
            claims (dict): User claims

        Returns:
            User: The created User instance
        """
        user = self.UserModel()
        return self.update_user(user, claims)

    def update_user(self, user, claims):
        """
        Updates user with data from claims

        Overrides OIDCAuthenticationBackend.update_user

        Args:
            user (User): User instance
            claims (dict): User claims

        Returns:
            User: The updated User instance
        """
        user.username = claims.get('net_id', '')
        user.library_id = claims.get('library_id', '')
        user.email = claims.get('email', '')
        user.first_name = claims.get('given_name', '')
        user.last_name = claims.get('family_name', '')

        if not user.username:
            user.username = user.email.split('@')[0]

        user.save()
        return user

    def get_userinfo(self, access_token, id_token, payload):
        """
        This overrides OIDCAuthenticationBackend.get_userinfo to get the user
        information directly from the payload rather than calling the endpoint
        specified in OIDC_OP_USER_ENDPOINT.

        As of this implementation `net_id` is found in the token payload, but
        not in the data returned by the OIDC_OP_USER_ENDPOINT. On the other hand,
        we don't get the 'realm_access' claim which includes the user roles.

        This may need to change in the future based what is available in the token
        vs the OP user endpoint.

        Args:
            access_token (str): The access token
            id_token (str): The identity token
            payload (dict): The decoded payload of the identity token

        Returns:
            dict: Dictionary of user claims
        """
        return payload

    def filter_users_by_claims(self, claims):
        """
        Return all users matching the specified net_id.

        Overrides OIDCAuthenticationBackend.filter_users_by_claims
        """
        net_id = claims.get('net_id')

        if not net_id:
            net_id = claims.get('email', '').split('@')[0]
            if not net_id:
                return self.UserModel.objects.none()

        return self.UserModel.objects.filter(username__iexact=net_id)

    def describe_user_by_claims(self, claims):
        """
        Describe a user, based on user claims.

        Overrides OIDCAuthenticationBackend.describe_user_by_claims
        """
        email = claims.get('email')
        net_id = claims.get('net_id')
        return f'net_id {net_id} and email {email}'
