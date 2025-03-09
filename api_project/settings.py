REST_FRAMEWORK = {
    'DEFAULTAUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ]
}

#rest_framework.permissions.IsAuthenticated