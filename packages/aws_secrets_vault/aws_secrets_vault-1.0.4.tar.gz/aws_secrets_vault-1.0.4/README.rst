=====================
**aws_secrets_vault**
=====================

Overview
--------

Manage secrets vaults in AWS Secrets Manager.  

This module helps to manage secrets in AWS Secrets Manager. The secrets are stored as dictionaries, allowing for each secret to have multiple key-value pairs. There is the option to use default AWS KMS keys for encryption or create / specify a Customer-Manager Key (CMK).  

aws_authenticate module is used to authenticate with AWS Security Token Service (STS) using AWS IAM access key credentials for the interactive mode. You can customize this to use named profiles or Single Sign-On (SSO) instead.  

The following functions are available:

- get_caller_identity
    - Get user identity from AWS Security Token Service (STS).
- list_kms_keys
    - List all keys in AWS Key Management Service (KMS).
- create_kms_key
    - Create key in AWS Key Management Service (KMS).
- delete_kms_key
    - Delete key in AWS Key Management Service (KMS).
- create_secrets_vault
    - Create secrets vault in AWS Secrets Manager.
- list_secrets_vaults
    - List all secrets vaults in AWS Secrets Manager.
- check_secrets_vault
    - Check if secrets vault exists in AWS Secrets Manager.
- get_secrets_vault
    - Get secrets from AWS Secrets Manager.
- update_secrets_vault
    - Update secrets vault in AWS Secrets Manager.
- delete_secrets_vault
    - Delete secrets vault from AWS Secrets Manager.
- create_secrets_dictionary
    - Create secrets dictionary from interactive inputs.
- create_secrets_vault_arn
    - Create secrets vault Amazon Resource Name (ARN) from vault name.

Usage
------

Installation:

.. code-block:: BASH

    pip3 install aws_secrets_vault
    # or
    python3 -m pip install aws_secrets_vault

To use the module interactively:

- Set environment variables in BASH.

.. code-block:: BASH

    export AWS_ACCESS_KEY_ID = <AWS_access_key_id>
    export AWS_SECRET_ACCESS_KEY = <AWS_secret_access_key>
    export AWS_SESSION_TOKEN = <AWS_session_token, default is None>
    export AWS_REGION = <AWS_region, default is us-east-1>
    export AWS_PARTITION = <AWS_partition, default is aws>

- Import the module and execute the main function in Python3.

.. code-block:: PYTHON

    import aws_secrets_vault
    aws_secrets_vault.main()
