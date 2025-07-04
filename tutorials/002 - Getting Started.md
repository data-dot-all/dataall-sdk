
# 2 - Getting Started

## How does dataall_sdk handle data.all user credentials and profiles?

Dataall's SDK requires user profile information to be stored either in a local file or in AWS Secrets Manager. The user information required includes:

- auth_type: Either `CognitoAuth` or `CustomAuth`
- client_id: The App Client ID
- api_endpoint_url: The URL data.all API Gateway Endpoint 
- redirect_uri: The data.all domain URL
- idp_domain_url: The Identity Providers URL
- client_secret (optional): The client secret used for the data.all App Client
- auth_server (optional, used for CustomAuth): The Custom Authorization Server used if applicable
- session_token_endpoint (optional, required for CustomAuth): The Identity Provider API endpoint to retrieve session tokens
- profile:  The Profile Name

Data.all's SDK uses the profile information to fetch and save tokens from the data.all application. 

By default the user information is provided at `~/.dataall/config.yaml` and the token information is saved at `~/.dataall/credentials.yaml`

If a valid token or refresh token exists for the given user, that will be used to fetch a new token and authenticate the profile. Otherwise, the user will be prompted for username and password when running an API request and the fetched tokens will be saved.


### Configuring your first data.all User profile

Below is an example of what a configured user profile typically looks like in `~/.dataall/config.yaml`:

```
TestCognitoProfile:
  auth_type: CognitoAuth
  client_id: testclient
  api_endpoint_url: https://API_GATEWAY_URL/prod
  redirect_uri: https://DATAALL_DOMAIN_URL
  idp_domain_url: https://IDP_DOMAIN_URL
```

### Configuring a Custom Auth User

If your data.all application is using custom auth, below is an example of a custom auth user configuration in `~/.dataall/config.yaml`: 
```
TestCustomProfile:
  auth_type: CustomAuth
  client_id: testclient
  client_secret: testsecret
  api_endpoint_url: https://API_GATEWAY_URL/prod
  redirect_uri: https://DATAALL_DOMAIN_URL
  idp_domain_url: https://IDP_DOMAIN_URL
  session_token_endpoint: testtokenendpoint
```

### Specifying your user profile

Once you have configured your user profile appropriately, you can begin running data.all API requests via the SDK using your configured profile(s) such as:

  ```py3
  import dataall_sdk as dataall

  # Profile w/ TestCustomProfile (assuming TestCustomProfile profile configured in ~/.dataall/config.yaml)
  da_client = dataall.client(profile="TestCustomProfile") 

  list_org_response = da_client.list_organizations()
  print(list_org_response)
  ```

  By default, a profile of name `default` is used if none if provided



## Configuring data.all User profiles with AWS Secrets Manager

Similarly, one can specify user profile information in AWS Secrets Manager as Key Value pairs rather than at `~/.dataall/config.yaml`

To do so:
1. Navigate to AWS Secrets Manager in your AWS Account
2. Select "Store a new secret" 
    a. For secret Type select "Other type of secret"
    b. For key/value pairs, enter key-values same as ones specified in local `~/.dataall/config.yaml` file such as:
```json
{
  "auth_type": "CognitoAuth",
  "client_id":"testclient",
  "api_endpoint_url":"https://API_GATEWAY_URL/prod",
  "redirect_uri": "https://DATAALL_DOMAIN_URL",
  "idp_domain_url": "https://IDP_DOMAIN_URL"
}
```
3. Select an Encryption Key (or use default), and chose "Next"
4. Give a Secret name, Description (optional), and chose "Next"
5. Provide any additional configuration details (i.e. Key Rotation, Tags, etc.) and finally chose "Store"
6. Once the secret is created, copy the secret ARN and provide it when initializing the dataall SDK client as such:

```py3
import dataall_sdk as dataall

da_client = dataall.client(profile="SecretProfile", secret_arn="arn:aws:secretsmanager:REGION:ACCOUNT:secret:SECRET_NAME-XXXXXX") 
list_org_response = da_client.list_organizations()
```

_NOTE: You need IAM access to retrieve the secret value from the specific AWS Account in order to run the data.all SDK properly using this method._

_NOTE: If required, you can store the username nad password information as additional key-value pairs in the AWS Secret to be used to fetch the token rather than being prompted for the user's username/password on new token retrieval_



## Additional Configuration Options

### Specifying a separate Config YAML paths

If you would rather store your user information in a separate file, you can provide an additional parameter to specify the `config_path` of the profile provided:

```py3
import dataall_sdk as dataall

da_client = dataall.client(profile="NewProfile", config_path="~/PATH/TO/NEW/PROFILE.yaml") 
```

Additionally, you can provide a different `credentials.yaml` path for each User Profile by specifying a new `creds_path` key value pair in the configuration of each user (default is `~/.dataall/credentials.yaml`)
