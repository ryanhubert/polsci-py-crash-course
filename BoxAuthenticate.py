#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Ryan Hübert
# Department of Political Science
# University of California, Davis

# Website: https://www.ryanhubert.com/

"""
Authenticate to Box.com
"""

import os
import keyring
from boxsdk import Client, OAuth2

def BoxAuth(boxuser, directory=None):
    warn = input(
        "Warning: this function will access your local keychain and/or store passwords. Do you want to proceed? [y/n] ")

    if warn in ["y", "yes", "Yes", "YES"]:

        # What is your Box User ID?
        boxid = boxuser

        # Define client ID and client secret
        CLIENT_ID = None
        CLIENT_SECRET = None

        if directory == None:
            wdir = os.path.dirname(os.path.abspath(__file__))
        else:
            wdir = directory

        try:
            # Read app info from text file
            with open(wdir + '/boxapp.cfg', 'r') as app_cfg:
                CLIENT_ID = app_cfg.readline()[:-1]
                CLIENT_SECRET = app_cfg.readline()[:-1]
        except:
            print("\nCONFIGURATION ERROR \n\nYou have not set up the Box Python SDK.\n\n" +
                  "Before calling this function, please follow the instructions at:\n" +
                  "http://opensource.box.com/box-python-sdk/tutorials/intro.html\n\n" +
                  "NOTE: Please name your `.cfg` file `boxapp.cfg` and place in this directory:\n" +
                  wdir + '\n')

        def read_tokens():
            """Reads authorization tokens from system keychain"""
            auth_token = keyring.get_password('box_python_sdk_auth', boxid)
            refresh_token = keyring.get_password('box_python_sdk_refr', boxid)
            return (auth_token, refresh_token)

        def store_tokens(access_token, refresh_token):
            """Callback function when Box SDK refreshes tokens"""
            # Use keyring to store the tokens
            keyring.set_password('box_python_sdk_auth', boxid, access_token)
            keyring.set_password('box_python_sdk_refr', boxid, refresh_token)

        # Authenticate with stored tokens
        access_token, refresh_token = read_tokens()

        if access_token != None:
            # Set up authorisation using the tokens we've retrieved
            oauth = OAuth2(
                client_id=CLIENT_ID,
                client_secret=CLIENT_SECRET,
                access_token=access_token,
                refresh_token=refresh_token,
                store_tokens=store_tokens,
            )

        else:
            # Authenticate for first time and store tokens
            oauth = OAuth2(
                client_id=CLIENT_ID,
                client_secret=CLIENT_SECRET,
                store_tokens=store_tokens,
            )
            print("To authorize access to your Box account please do the following:\n\n" +
                  "1. Navigate to the following URL in a browser:\n")
            print(oauth.get_authorization_url('http://localhost')[0])
            print("\n2. Select 'Grant Access to Box'.\n")
            print(
                "3. Extract the access code from the resulting URL (in your browser's address bar, the string after 'code=').\n")
            boxcode = input("4. Paste it here: ")
            access_token, refresh_token = oauth.authenticate(boxcode)
            keyring.set_password('box_python_sdk_auth', boxuser, access_token)
            keyring.set_password('box_python_sdk_refr', boxuser, refresh_token)

            # Create the SDK client
            
        client = Client(oauth)

        # Get information about the logged in user (that's whoever owns the developer token)
        boxusr = client.user(user_id='me').get()
        print("You are now logged into Box as: " + boxusr.name + ' (' + boxusr.login + ')')
        return client