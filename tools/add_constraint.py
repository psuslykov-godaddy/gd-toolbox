import argparse
import json
import os

from lake.client import LakeApiClient
from lake.generated.exceptions import (ApiException, ApiTypeError,
                                       ApiValueError, ForbiddenException)
from lake.model.constraint import NewConstraintTypeDef


def register_constraint(env: str, account_id: str, dex_config: str):
    with open(dex_config) as f:
        config = json.load(f)
        database_name = config["database"]
        table_name = config["table"]

        for constraint in config["constraints"]:
            try:
                response = LakeApiClient(env=env)\
                    .define_constraint(
                        database_name=database_name,
                        table_name=table_name,
                        account_id=account_id,
                        new_constraint=NewConstraintTypeDef(
                            column=constraint["column"],
                            code=constraint["code"],
                            description=constraint["description"]
                        )
                    )
                print(response)

            except (ForbiddenException, ApiException) as err:
                print(err.status)
                print(err.reason)
            except (ApiTypeError, ApiValueError) as err:
                print(str(err))


if __name__ == "__main__":
    # Parse arguments
    parser = argparse.ArgumentParser(description='Register constraints in DeX')
    parser.add_argument('-e', '--env', type=str, help='DeX environment to use', required=True)
    parser.add_argument('-a', '--account', type=str, help='AWS account ID', required=True)
    parser.add_argument('-c', '--config', type=str, help='Path to DeX constraint config files',
                        required=True)
    args = parser.parse_args()

    environment = args.env
    account_id = args.account
    dex_config_path = args.config

    # Register constraints
    for config in os.listdir(dex_config_path):
        if config.endswith(".json"):
            register_constraint(environment, account_id, os.path.join(dex_config_path, config))
