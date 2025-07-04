
# 3 - Running a Command

## Running a SDK Command

To run an SDK command it is as simple as initializing a new client with your repective user profile and running the supported command.

For instance:
```py3

import dataall_sdk as dataall

client = dataall.client(profile="MyProfile")

client.list_organizations()
```


## Specifying a New Schema Version 

By default, data.all uses the latest schema present in the the dataall_core PyPi repositories library, under path `dataall_core/dataall_core/schema/v2_6.json`.

Each one of the schemas listed in the `schema/` directory are the GraphQL Schema files generated from that version of data.all (a.k.a the value of the release tag of the version). 

To specify a separate schema version to use, you can do the following:

```py3

import dataall_sdk as dataall

client = dataall.client(profile="MyProfile", schema_version="v2_5")

client.list_organizations()
```


## Specifying a New Schema Path 

Going further, if you want to provide your own GraphQL Schema specific to your data.all application you can do that as well. 

By specifying the `schema_path` when initializing your client you can point the DataallClient to load some other GraphQL Schema that is custom to you deployment, for example:

```py3

import dataall_sdk as dataall

client = dataall.client(schema_path="/Path/To/Custom/dataall/schema.json")

client.custom_query()
```