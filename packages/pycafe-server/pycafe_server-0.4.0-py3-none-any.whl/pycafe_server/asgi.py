import json
import logging
import os
from pathlib import Path
import sys
import typing
import subprocess

from starlette.applications import Starlette
from starlette.staticfiles import StaticFiles
from starlette.responses import PlainTextResponse, JSONResponse, Response
from starlette.routing import Route
from starlette.requests import Request
from starlette.types import Receive, Scope, Send
from starlette.responses import RedirectResponse
from starlette.applications import Starlette
from starlette.middleware import Middleware
from .session import SessionMiddleware
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.middleware import Middleware
from .uv_util import _run_resolve
from . import database

import uvicorn

from . import config
from . import auth
from . import license
from . import sign

HERE = Path(__file__).parent

logger = logging.getLogger(__name__)
trialmode = False
from .cookie import Cookie


session_cookie = Cookie(
    "pycafe_session",
    same_site="none",
    secure=True,
    secret_key=config.PYCAFE_SESSION_SECRET_KEY,
    max_age=int(config.PYCAFE_COOKIE_MAX_AGE),
)
middleware = []
if os.environ.get("ENV", "dev") == "dev":
    middleware = [
        Middleware(
            CORSMiddleware,
            allow_origins=["localhost"],
        ),
    ]
middleware += [
    Middleware(
        SessionMiddleware,
        cookie=session_cookie,
    ),
    Middleware(AuthenticationMiddleware, backend=auth.AuthBackend()),
]
app = Starlette(middleware=middleware)


static_dir = (HERE / "static").resolve()
print("static assets in", static_dir)


class StaticFilesNextJs(StaticFiles):
    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        request = Request(scope, receive=receive)
        if (
            config.auth_is_configured()
            and config.PYCAFE_SERVER_PRE_AUTH
            and not request.user.is_authenticated
        ):
            # redirect to /_login
            # TODO: url encode etc
            redirect_uri = str(request.url)
            url = f"/_login?next_url={redirect_uri}"
            await RedirectResponse(url)(scope, receive, send)
        else:
            await super().__call__(scope, receive, send)

    def lookup_path(
        self, path: str
    ) -> typing.Tuple[str, typing.Optional[os.stat_result]]:
        attempt1 = super().lookup_path(path)
        if attempt1[1] is not None:
            return attempt1
        # a path like /snippet/solara/v1 should be resolved to /snippet/solara/v1.html
        attempt2 = super().lookup_path(path + ".html")
        return attempt2

    def file_response(self, *args, **kwargs) -> Response:
        response = super().file_response(*args, **kwargs)
        # we don't want to cache html pages, since if we logout, it
        # should always fetch from the server, instead of using the cache
        response.headers["cache-control"] = "no-cache"
        return response


async def resolve_uv(request: Request):
    form = await request.form()

    # Retrieve the JSON body from the 'query' field
    body = form["query"]
    args = json.loads(body)

    # Process uploaded files from the 'wheels' field
    files: dict[str, bytes] = {}
    for file in form.getlist("wheels"):
        files[file.filename] = await file.read()

    requirements = args["requirements"]
    constraints = args["constraints"]
    python_version = args["python_version"]
    overrides = args["overrides"]
    universal = args["universal"] == "true"

    try:
        result = _run_resolve(
            requirements,
            constraints,
            overrides,
            python_version,
            universal=universal,
            files=files,
        )
    except subprocess.CalledProcessError as e:
        print("Failed to resolve", e.stderr)
        return PlainTextResponse(e.stderr, status_code=500)
    return PlainTextResponse(result, status_code=200)


def get_user_id(userinfo):
    id_field = config.get("PYCAFE_SERVER_USER_ID_FIELD", default="email")
    if id_field not in userinfo:
        logger.error(
            f"no value found in userinfo with key PYCAFE_SERVER_USER_ID_FIELD={id_field}, possible fields are {list(userinfo.keys())}"
        )
        return JSONResponse(
            {
                "error": "Could not find a field in the auth data to uniquely describe the user, see server logs and configuration"
            },
            status_code=500,
        )
    return userinfo[id_field]


async def logins(request: Request):
    # only admins can see logins

    if not trialmode:
        userinfo = auth.get_userinfo(request)
        if userinfo is None:
            return JSONResponse({"error": "Not authenticated"}, status_code=401)

        user_id = get_user_id(userinfo)
        is_admin = user_is_admin(user_id)
        if not is_admin:
            return JSONResponse({"error": "Not authorized"}, status_code=403)

    try:
        logins_db = database.get_logins()
        logins = [
            {
                "user_id": login.user_id,
                "datetime": login.datetime.isoformat(),
                "email": login.email,
                "is_editor": login.is_editor,
                "is_admin": login.is_admin,
                # "userinfo": login.userinfo,
            }
            for login in logins_db
        ]

        return JSONResponse({"logins": logins})
    except Exception:
        logger.exception("Failed to get logins")
        return JSONResponse({"error": "Failed to get logins"}, status_code=500)


async def info(request: Request):
    userinfo = auth.get_userinfo(request)
    # we should reply with the following type from types.ts
    """
    export type UserInfo = {
        user_id: string;
        full_name: string;
        username: string;
        email: string;
        avatar: string;
        is_editor: boolean;
        is_admin: boolean;
        meta: { maxFileSize: number } | null;
    };
    """

    settings = config.get_settings()
    settings["trialmode"] = trialmode
    if trialmode:
        settings["message"] = (
            "Auth is not configured, please set up auth, running in trial mode"
        )

    if userinfo is None:
        # if we do not have auth, we will always show the instance_id
        if not config.auth_is_configured():
            settings["instanceId"] = database.instance_id
        return JSONResponse({"user": None, "settings": settings})
    else:
        user_id = get_user_id(userinfo)
        is_editor = user_is_editor(user_id)
        is_admin = user_is_admin(user_id)

        if is_admin:
            settings["instanceId"] = database.instance_id
        try:
            email = userinfo.get("email", "")
            database.log_login(user_id, email, is_editor, is_admin, userinfo)
        except Exception:
            logger.exception(f"Failed to log login")

        return JSONResponse(
            {
                "user": {
                    "user_id": user_id,
                    "full_name": userinfo.get("name", ""),
                    "username": userinfo.get("preferred_username", ""),
                    "email": userinfo.get("email", ""),
                    "avatar": userinfo.get("picture", ""),
                    "is_editor": is_editor,
                    "is_admin": is_admin,
                    "meta": None,
                },
                "settings": settings,
            }
        )


def user_is_editor(user_id: str) -> bool:
    if trialmode and not config.PYCAFE_SERVER_EDITORS:
        logger.debug(
            f"user {user_id} is an editor, because we are in trialmode and PYCAFE_SERVER_EDITOR is not set"
        )
        return True
    is_editor = user_id in config.PYCAFE_SERVER_EDITORS
    if is_editor:
        logger.debug(
            f"user {user_id} is an editor, because they are in PYCAFE_SERVER_EDITORS"
        )
    else:
        logger.debug(
            f"user {user_id} is not an editor, because they are not in PYCAFE_SERVER_EDITORS"
        )
    return is_editor


def user_is_admin(user_id: str) -> bool:
    is_admin = user_id in config.PYCAFE_SERVER_ADMINS
    if is_admin:
        logger.debug(
            f"user {user_id} is an admin, because they are in PYCAFE_SERVER_ADMINS"
        )
    else:
        logger.debug(
            f"user {user_id} is not an admin, because they are not in PYCAFE_SERVER_ADMINS"
        )
    return is_admin


async def sign_hash(request: Request):
    # ensure login?
    # we only support ?hash=<hash> for now

    userinfo = auth.get_userinfo(request)
    user_id = get_user_id(userinfo) if userinfo is not None else None
    if not trialmode:
        if userinfo is None:
            return JSONResponse(
                {"error": "Not authenticated, please login"}, status_code=401
            )
        user_id = get_user_id(userinfo)
        if not user_is_editor(user_id):
            return JSONResponse(
                {"error": "Not authorized, not an editor"}, status_code=403
            )
    else:
        if user_id is None:
            user_id = "trailmode"  # just make it work in trial mode
    hash = request.query_params.get("hash")
    if hash is None:
        return JSONResponse({"error": "No hash provided"}, status_code=500)
    signature_jwt = sign.sign_hash(hash, user_id)
    return JSONResponse({"signatureJwt": signature_jwt})


app.add_route("/api/resolve", resolve_uv, methods=["POST"])
app.add_route("/api/info", info)
app.add_route("/api/logins", logins)
app.add_route("/api/sign", sign_hash)
# starlette does not seem to merge multiple routes at the common path
# so we manually add all routes from the auth app
for route in auth.app.routes:
    app.add_route(route.path, route.endpoint)
app.mount("/", StaticFilesNextJs(directory=static_dir, html=True), name="static")


if not config.PYCAFE_SERVER_INSECURE_MODE_DONT_USE_IN_PRODUCTION:
    if not config.auth_is_configured() and not config.auth_using_proxy():
        print(
            "ERROR: Insecure mode is not enabled, and auth is not configured. Please set up auth.",
            file=sys.stderr,
        )
        sys.exit(1)
    if config.PYCAFE_SERVER_ENABLE_EXPORT and not config.signing_is_configured():
        print(
            "ERROR: Insecure mode is not enabled, and signing is not configured. Please set up signing.",
            file=sys.stderr,
        )
        sys.exit(1)
else:
    print(
        "WARNING: Insecure mode is enabled. Do not use in production.", file=sys.stderr
    )

if license.license:
    if not config.auth_is_configured():
        print(
            "ERROR: Valid license found, but not auth is setup. Please set up auth. Entering trial mode",
            file=sys.stderr,
        )
        trialmode = True
    if license.license.sub != database.instance_id:
        print(
            f"ERROR: License is for {license.license.sub}, but this instance has id {database.instance_id}. Please obtain a new license.",
            file=sys.stderr,
        )
        if config.PYCAFE_SERVER_INSECURE_MODE_DONT_USE_IN_PRODUCTION:
            trialmode = True
            print("Entering trial mode.")
        else:
            sys.exit(1)
    if len(config.PYCAFE_SERVER_EDITORS) > license.license.max_editors:
        print(
            f"ERROR: License does not allow {len(config.PYCAFE_SERVER_EDITORS)} editors, only {license.license.max_editors}.",
            file=sys.stderr,
        )
        if config.PYCAFE_SERVER_INSECURE_MODE_DONT_USE_IN_PRODUCTION:
            trialmode = True
            print("Entering trial mode.")
        else:
            sys.exit(1)
else:
    if config.PYCAFE_SERVER_INSECURE_MODE_DONT_USE_IN_PRODUCTION:
        trialmode = True
        print("Entering trial mode.")
    else:
        print(
            "ERROR: No license set, and insecure mode is not enabled. Please obtain a license or set the environmental variable PYCAFE_SERVER_INSECURE_MODE_DONT_USE_IN_PRODUCTION=1",
            file=sys.stderr,
        )
        sys.exit(1)

if not trialmode:
    if not config.PYCAFE_SESSION_SECRET_KEY:
        print(
            "ERROR: PYCAFE_SESSION_SECRET_KEY is not set. Please set it to a random secret.",
            file=sys.stderr,
        )
        sys.exit(1)

    if not config.PYCAFE_SERVER_SIGN_PRIVATE_KEY:
        print(
            "ERROR: PYCAFE_SERVER_SIGN_PRIVATE_KEY is not set. Please set it to a private key.",
            file=sys.stderr,
        )
        sys.exit(1)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8001)
