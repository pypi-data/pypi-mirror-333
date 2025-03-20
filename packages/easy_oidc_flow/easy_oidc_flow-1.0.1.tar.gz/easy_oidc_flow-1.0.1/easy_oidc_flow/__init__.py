from uuid import uuid4
import requests
import traceback
from flask import Flask, request, redirect, session, url_for
import jwt
import os
from jwt import PyJWKClient
from jwt.exceptions import DecodeError
from werkzeug.exceptions import Unauthorized
from requests_oauthlib import OAuth2Session

class EasyOIDCFlow(Flask):
  def __init__(self, context):
    envvars_not_set = []
    for envvar in [
      "IDP_WELL_KNOWN_URL",
      "IDP_CLIENT_ID",
      "IDP_CLIENT_SECRET",
      "IDP_OIDC_SCOPES",
      ]:
      if os.environ.get(envvar) is None:
        envvars_not_set.append(envvar)
    if len(envvars_not_set) != 0:
      raise Exception(f"Please set the following environment variables: {envvars_not_set}")
    super().__init__(context.import_name)
    self.config["SECRET_KEY"] = str(uuid4())

    IDP_CONFIG = {
      "well_known_url": os.environ.get("IDP_WELL_KNOWN_URL"),
      "client_id": os.environ.get("IDP_CLIENT_ID"),
      "client_secret": os.environ.get("IDP_CLIENT_SECRET"),
      "scope": os.environ.get("IDP_OIDC_SCOPES").split(",")
    }

    @self.before_request
    def verify_and_decode_token():
      if request.endpoint not in {"login", "callback"}:
        if "Authorization" in request.headers:
          token = request.headers["Authorization"].split()[1]
        elif "oauth_token" in session:
          token = session["oauth_token"]
        else:
          return redirect('/login')

        try:
          signing_key = jwks_client.get_signing_key_from_jwt(token)
          header_data = jwt.get_unverified_header(token)
          request.user_data = jwt.decode(token,
                        signing_key.key,
                        algorithms=[header_data['alg']],
                        audience=IDP_CONFIG["client_id"])
        except DecodeError:
          return Unauthorized("Authorization token is invalid")
        except Exception as e:
          print(f'ERROR: {e}')
          print(traceback.format_exc())
          return redirect('/login')

    @self.route("/login")
    def login():
      well_known_metadata = get_well_known_metadata()
      oauth2_session = get_oauth2_session()
      authorization_url, state = oauth2_session.authorization_url(well_known_metadata["authorization_endpoint"])
      session["oauth_state"] = state
      return redirect(authorization_url)

    @self.route("/callback")
    def callback():
      well_known_metadata = get_well_known_metadata()
      oauth2_session = get_oauth2_session(state=session["oauth_state"])
      session["oauth_token"] = oauth2_session.fetch_token(well_known_metadata["token_endpoint"],
                                                          client_secret=IDP_CONFIG["client_secret"],
                                                          code=request.args["code"])["id_token"]
      return redirect('/')

    def get_well_known_metadata():
        response = requests.get(IDP_CONFIG["well_known_url"])
        response.raise_for_status()
        return response.json()

    def get_jwks_client():
        well_known_metadata = get_well_known_metadata()
        jwks_client = PyJWKClient(well_known_metadata["jwks_uri"], headers={"User-Agent": "Authentik kheiden.com request v1.0"})
        return jwks_client

    jwks_client = get_jwks_client()

    def get_oauth2_session(**kwargs):
        oauth2_session = OAuth2Session(IDP_CONFIG["client_id"],
                                      scope=IDP_CONFIG["scope"],
                                      redirect_uri=url_for(".callback", _external=True, _scheme=os.environ.get("REDIRECT_PROTOCOL")),
                                      **kwargs)
        return oauth2_session

