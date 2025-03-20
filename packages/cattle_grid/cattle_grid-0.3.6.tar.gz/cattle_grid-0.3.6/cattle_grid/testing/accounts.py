import logging

from cattle_grid.account.account import AccountAlreadyExists, create_account
from cattle_grid.dependencies.globals import global_container

logger = logging.getLogger(__name__)


async def create_test_accounts():
    config = global_container.get_config().testing

    if not config.enable:  # type:ignore
        return

    logger.warning("running in testing mode")
    logger.warning(
        "\n   __            __  _            \n  / /____  _____/ /_(_)___  ____ _\n / __/ _ \\/ ___/ __/ / __ \\/ __ `/\n/ /_/  __(__  ) /_/ / / / / /_/ / \n\\__/\\___/____/\\__/_/_/ /_/\\__, /  \n                         /____/   \n"
    )
    accounts: list[dict] = config.accounts  # type:ignore

    for account in accounts:
        try:
            await create_account(
                account["name"],
                account["password"],
                permissions=account.get("permissions", []),
                meta_information=account.get(
                    "meta_information", {"testing": "created by testing"}
                ),
            )
            logger.info("created account %s", account["name"])
        except AccountAlreadyExists:
            pass
