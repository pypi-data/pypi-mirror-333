import getpass
import logging
import sys
import webbrowser

import httpx
import keyring
from keyrings.alt.file import PlaintextKeyring

from .log import setup_logger
from .sets import Settings, get_console
from .util import ANSI, print_url

logger = logging.getLogger(f"{__name__.split('.')[0]}")
tag = "Auth"


def login(settings=Settings(), retry=False):
    setup_logger(settings)
    try:
        auth = keyring.get_password(f"{settings.tag}", f"{settings.tag}")
    except keyring.errors.NoKeyringError:  # fallback
        keyring.set_keyring(PlaintextKeyring())
        auth = keyring.get_password(f"{settings.tag}", f"{settings.tag}")
    if settings.auth is None:
        if auth == "":
            keyring.delete_password(f"{settings.tag}", f"{settings.tag}")
        elif auth is not None:
            settings.auth = auth
    if settings.auth == "":
        logger.critical(
            "%s: authentication failed: the provided token cannot be empty", tag
        )
        sys.exit()  # os._exit(1)
    client = httpx.Client(proxy=settings.http_proxy or settings.https_proxy or None)
    r = client.post(
        url=settings.url_login,
        headers={
            "Authorization": f"Bearer {settings.auth}",
        },
    )
    try:
        logger.info(f"{tag}: logged in as {r.json()['organization']['slug']}")
        keyring.set_password(f"{settings.tag}", f"{settings.tag}", f"{settings.auth}")
    except Exception as e:
        if retry:
            logger.warning("%s: authentication failed", tag)
        hint1 = f"{ANSI.cyan}- Please copy the API key provided in the web portal and paste it below"
        hint2 = f"- You can alternatively manually open {print_url(settings.url_token)}"
        hint3 = f"{ANSI.green}- You may exit at any time by pressing CTRL+C / ⌃+C"
        logger.info(
            f"{tag}: initializing authentication\n\n {hint1}\n\n {hint2}\n\n {hint3}\n"
        )
        webbrowser.open(url=settings.url_token)
        if get_console() == "jupyter":
            settings.auth = getpass.getpass(prompt="Enter API key: ")
        else:
            settings.auth = input(f"{ANSI.yellow}Enter API key: ")
        try:
            keyring.set_password(
                f"{settings.tag}", f"{settings.tag}", f"{settings.auth}"
            )
        except Exception as e:
            logger.critical(
                "%s: failed to save key to system keyring service: %s", tag, e
            )
        login(retry=True)


def logout(settings=Settings()):
    setup_logger(settings)
    try:
        keyring.delete_password(f"{settings.tag}", f"{settings.tag}")
    except keyring.errors.NoKeyringError:
        keyring.set_keyring(PlaintextKeyring())
        keyring.delete_password(f"{settings.tag}", f"{settings.tag}")
    except Exception as e:
        logger.warning(
            "%s: failed to delete key from system keyring service: %s", tag, e
        )
    logger.info(f"{tag}: logged out")
