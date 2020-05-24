from .Implementations import Web, Android
from Web import web_client
from Android import android_client

clients = {"web": lambda  : Web.web_client(),
            "android": lambda  : Android.android_client()}

"""

            """
