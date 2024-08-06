from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import json
import streamlit as st

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

token_data = {
    "token": st.secrets["token"],
    "refresh_token": st.secrets["refresh_token"],
    "token_uri": st.secrets["token_uri"],
    "client_id": st.secrets["client_id"],
    "client_secret": st.secrets["client_secret"],
    "scopes": ["https://www.googleapis.com/auth/spreadsheets"],
    "universe_domain": "googleapis.com",
    "account": "",
    "expiry": "2024-08-06T08:36:06.391636Z",
}

json_data = json.dumps(token_data)
json_data = json.loads(json_data)

def append_values(spreadsheet_id, range_name, value_input_option, _values):
  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  #creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  print(json_data)
  creds = Credentials.from_authorized_user_info(json_data)
  """
  Creates the batch_update the user has access to.
  Load pre-authorized user credentials from the environment.
  TODO(developer) - See https://developers.google.com/identity
  for guides on implementing OAuth2 for the application.
  """
  # creds, _ = google.auth.default()
  # pylint: disable=maybe-no-member
  try:
    service = build("sheets", "v4", credentials=creds)

    values = [
        [
            # Cell values ...
        ],
        # Additional rows ...
    ]
    body = {"values": _values}
    result = (
        service.spreadsheets()
        .values()
        .append(
            spreadsheetId=spreadsheet_id,
            range=range_name,
            valueInputOption=value_input_option,
            body=body,
        )
        .execute()
    )
    print(f"{(result.get('updates').get('updatedCells'))} cells appended.")
    return result

  except HttpError as error:
    print(f"An error occurred: {error}")
    return error

