#!/usr/bin/env python3
# -*- coding: latin-1 -*-

"""Manage secrets vaults in AWS Secrets Manager."""
import os
import json
from aws_authenticator import AWSAuthenticator as aws_auth
from typing import Union
from getpass import getpass as gp
from pprint import pprint as pp


__version__ = "1.0.4"
__author__ = "Ahmad Ferdaus Abd Razak"


def get_caller_identity(
    session
) -> dict:
    """Get user identity from AWS Security Token Service (STS)."""
    client = session.client("sts")
    response = client.get_caller_identity()

    return response


def list_kms_keys(
    session
) -> list:
    """List all keys in AWS Key Management Service (KMS)."""
    client = session.client("kms")
    paginator = client.get_paginator("list_keys")
    response_iterator = paginator.paginate()

    for page in response_iterator:
        keys = [key["KeyArn"] for key in page["Keys"]]

    key_descriptions = []
    for key in keys:
        response = client.describe_key(
            KeyId=key
        )
        paginator = client.get_paginator('list_aliases')
        response_iterator = paginator.paginate(
            KeyId=key
        )
        for page in response_iterator:
            aliases = [alias["AliasName"] for alias in page["Aliases"]]
        key_descriptions.append(
            {
                "arn": key,
                "description": response["KeyMetadata"]["Description"],
                "state": response["KeyMetadata"]["KeyState"],
                "aliases": aliases
            }
        )

    return key_descriptions


def create_kms_key(
    session,
    caller_arn: str,
    account_id: str,
    description: str,
    alias: Union[str, None] = None
) -> str:
    """Create key in AWS Key Management Service (KMS)."""
    key_policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "AllowKeyUsage",
                "Effect": "Allow",
                "Principal": {
                    "AWS": caller_arn
                },
                "Action": [
                    "kms:Encrypt",
                    "kms:Decrypt",
                    "kms:ReEncrypt*",
                    "kms:GenerateDataKey*",
                    "kms:DescribeKey"
                ],
                "Resource": "*",
                "Condition": {
                    "StringEquals": {
                        "kms:CallerAccount": str(account_id)
                    }
                }
            },
            {
                "Sid": "AllowKeyAdmin",
                "Effect": "Allow",
                "Principal": {
                    "AWS": caller_arn
                },
                "Action": "kms:*",
                "Resource": "*",
                "Condition": {
                    "StringEquals": {
                        "kms:CallerAccount": str(account_id)
                    }
                }
            }
        ]
    }
    client = session.client("kms")
    response = client.create_key(
        Policy=json.dumps(key_policy),
        Description=description,
        KeyUsage="ENCRYPT_DECRYPT",
        KeySpec="SYMMETRIC_DEFAULT",
        Origin="AWS_KMS",
        BypassPolicyLockoutSafetyCheck=False,
        MultiRegion=False
    )

    if alias:
        client.create_alias(
            AliasName=f"alias/{alias}",
            TargetKeyId=response["KeyMetadata"]["Arn"]
        )

    return response["KeyMetadata"]["Arn"]


def delete_kms_key(
    session,
    key_arn: str
) -> str:
    """Delete key in AWS Key Management Service (KMS)."""
    client = session.client("kms")
    response = client.schedule_key_deletion(
        KeyId=key_arn,
        PendingWindowInDays=7  # 7 - 30
    )

    return response["DeletionDate"]


def create_secrets_vault(
    session,
    secret_name: str,
    secrets: dict,
    description: str,
    kms_key_arn: Union[str, None] = None
) -> str:
    """Create secrets vault in AWS Secrets Manager."""
    client = session.client("secretsmanager")

    if kms_key_arn:
        response = client.create_secret(
            Name=secret_name,
            Description=description,
            KmsKeyId=kms_key_arn,
            SecretString=json.dumps(secrets)
        )
    else:
        response = client.create_secret(
            Name=secret_name,
            Description=description,
            SecretString=json.dumps(secrets)
        )

    return response["ARN"]


def list_secrets_vaults(
    session
) -> list:
    """List all secrets vaults in AWS Secrets Manager."""
    client = session.client("secretsmanager")
    paginator = client.get_paginator("list_secrets")
    response_iterator = paginator.paginate(
        IncludePlannedDeletion=False,
        SortOrder="asc"
    )

    for page in response_iterator:
        secrets = [secret["ARN"] for secret in page["SecretList"]]

    secrets_vaults = []
    for secret in secrets:
        response = client.describe_secret(
            SecretId=secret
        )
        try:
            secrets_vaults.append(
                {
                    "arn": secret,
                    "description": response["Description"]
                }
            )
        except KeyError:
            secrets_vaults.append(
                {
                    "arn": secret,
                    "description": "No description"
                }
            )

    return secrets_vaults


def check_secrets_vault(
    session,
    secrets_vault_arn: str
) -> bool:
    """Check if secrets vault exists in AWS Secrets Manager."""
    client = session.client("secretsmanager")

    try:
        client.describe_secret(
            SecretId=secrets_vault_arn
        )
        vault_exists = True
    except client.exceptions.ResourceNotFoundException:
        vault_exists = False

    return vault_exists


def get_secrets_vault(
    session,
    secrets_vault_arn: str
) -> dict:
    """Get secrets from AWS Secrets Manager."""
    client = session.client("secretsmanager")
    response = client.get_secret_value(
        SecretId=secrets_vault_arn,
        # VersionId="uuid",
        VersionStage="AWSCURRENT"  # | AWSPREVIOUS | AWSPENDING
    )

    return json.loads(response["SecretString"])


def update_secrets_vault(
    session,
    secrets_vault_arn: str,
    secrets: dict,
    description: Union[str, None] = None,
    kms_key_arn: Union[str, None] = None
) -> dict:
    """Update secrets vault in AWS Secrets Manager."""
    client = session.client("secretsmanager")

    if description and kms_key_arn:
        response = client.update_secret(
            SecretId=secrets_vault_arn,
            Description=description,
            KmsKeyId=kms_key_arn,
            SecretString=json.dumps(secrets)
        )
    elif description:
        response = client.update_secret(
            SecretId=secrets_vault_arn,
            Description=description,
            SecretString=json.dumps(secrets)
        )
    elif kms_key_arn:
        response = client.update_secret(
            SecretId=secrets_vault_arn,
            KmsKeyId=kms_key_arn,
            SecretString=json.dumps(secrets)
        )
    else:
        response = client.update_secret(
            SecretId=secrets_vault_arn,
            SecretString=json.dumps(secrets)
        )

    return response["ARN"]


def delete_secrets_vault(
    session,
    secrets_vault_arn: str
) -> str:
    """Delete secrets vault from AWS Secrets Manager."""
    client = session.client("secretsmanager")
    response = client.delete_secret(
        SecretId=secrets_vault_arn,
        # RecoveryWindowInDays=7  # 7 - 30
        ForceDeleteWithoutRecovery=True
    )

    return response["DeletionDate"]


def create_secrets_dictionary() -> dict:
    """Create secrets dictionary from interactive inputs."""
    # Initialize secrets dictionary.
    secrets = {}

    # Get secret keys and values.
    # Repeat until no secret key is specified.
    secret_key = input("Secret key: ")
    while secret_key:
        secret_value = gp("Secret value: ")
        secrets[secret_key] = secret_value
        secret_key = input("Next secret key (leave blank to skip): ")
    description = input("Description: ")

    return {
        "secrets": secrets,
        "description": description
    }


def create_secrets_vault_arn(
    account_id: str,
    region: str,
    secret_name: str,
    aws_partition: str
) -> str:
    """Create secrets vault Amazon Resource Name (ARN) from vault name."""
    return f"arn:{aws_partition}:secretsmanager:{region}:{account_id}:secret:{secret_name}"


def main():
    """Execute main function."""
    # Get parameters from environment variables.
    aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID")
    aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
    aws_session_token = os.environ.get("AWS_SESSION_TOKEN", None)
    aws_region = os.environ.get("AWS_REGION", "us-east-1")
    aws_partition = os.environ.get("AWS_PARTITION", "aws")

    # Authenticate to AWS.
    auth = aws_auth(
        access_key_id=aws_access_key_id,
        secret_access_key=aws_secret_access_key,
        session_token=aws_session_token
    )
    session = auth.iam()

    print()
    print("Caller identity.")

    # Get caller identity.
    caller_identity = get_caller_identity(session)
    pp(
        {
            "account_id": caller_identity["Account"],
            "user_id": caller_identity["UserId"],
            "arn": caller_identity["Arn"]
        }
    )

    print()
    print("KMS keys:")

    # List all keys in the specified account.
    kms_keys = list_kms_keys(session)
    pp(kms_keys)

    print()
    print("Create a new KMS key.")

    # Create a new KMS key.
    key_description = input("Key description (leave blank to skip): ")

    if key_description:

        key_alias = input("Key alias: ")

        # Create KMS key.
        kms_key_arn = create_kms_key(
            session,
            caller_identity["Arn"],
            caller_identity["Account"],
            key_description,
            key_alias
        )
        print(kms_key_arn)

    print()
    print("Secrets vaults:")

    # List all secrets vaults in the specified account.
    secrets_vaults = list_secrets_vaults(session)
    pp(secrets_vaults)

    print()
    print("Create a new secrets vault.")

    # Create a new secrets vault.
    vault_name = input("Vault name (leave blank to skip): ")

    if vault_name:

        # Check if secrets vault exists.
        vault_exists = check_secrets_vault(
            session,
            create_secrets_vault_arn(
                caller_identity["Account"],
                aws_region,
                vault_name,
                aws_partition
            )
        )

        # Proceed if secrets vault does not exist.
        if not vault_exists:

            kms_key_arn = input("KMS key ARN (leave blank to skip): ")

            # Create secrets dictionary.
            secrets = create_secrets_dictionary()

            # Create secrets vault.
            secrets_vault_arn = create_secrets_vault(
                session,
                vault_name,
                secrets["secrets"],
                secrets["description"],
                kms_key_arn
            )
            print(secrets_vault_arn)

    print()
    print("View secrets.")

    # View secrets in a secrets vault.
    vault_arn = input("Vault ARN (leave blank to skip): ")

    if vault_arn:

        # Get secrets from secrets vault.
        secrets = get_secrets_vault(session, vault_arn)

        # Print secrets keys and values.
        for key, value in secrets.items():
            print(f"{key}: {value}")

    print()
    print("Update secrets.")

    # Update secrets in a secrets vault.
    vault_arn = input("Vault ARN (leave blank to skip): ")

    if vault_arn:

        kms_key_arn = input("KMS key ARN (leave blank to skip): ")

        # Create secrets dictionary.
        secrets = create_secrets_dictionary()

        # Update secrets vault.
        secrets_vault_arn = update_secrets_vault(
            session,
            vault_arn,
            secrets["secrets"],
            secrets["description"],
            kms_key_arn
        )
        print(secrets_vault_arn)

    print()
    print("Delete secrets.")

    # Delete secrets vault.
    vault_arn = input("Vault ARN (leave blank to skip): ")

    if vault_arn:

        # Delete secrets vault.
        deletion_date = delete_secrets_vault(session, vault_arn)
        print(deletion_date)

    print()
    print("Delete a KMS key.")

    # Delete a KMS key.
    key_arn = input("Key ARN (leave blank to skip): ")

    if key_arn:

        # Delete KMS key.
        deletion_date = delete_kms_key(session, key_arn)
        print(deletion_date)

    print()
