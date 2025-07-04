
.. image:: ./_static/logo.png
   :alt: Data.all Logo
   :align: center
   :scale: 30%

An `AWS Professional Service <https://aws.amazon.com/professional-services>`_ open source initiative | aws-proserve-opensource@amazon.com

AWS data.all SDK is a software development kit (SDK) tool for data.all which aims to provide users with a seamless and efficient means of interfacing with data.all programmatically. Users can leverage the  data.all SDK to enhance automation, develop scripting, and integrate data.all APIs into their existing workflows. The SDK tool encompasses a comprehensive set of commands and functions, enabling users to perform operations related to data.all features such as datasets, dataset share, environment, organization and consumption role through programmatic interfaces. The data.all SDK tool empowers developers and administrators to leverage data.all functionalities in a programmatic manner.

Quick Start
-----------

To install data.all SDK, check out the **Install** Page of the documentation.

.. code-block:: py3

    import dataall_sdk

    # # # USER A
    # # # __________________________________
    # Set Up Organization Client - UserA
    da_client = dataall_sdk.client(profile="UserA")

    # # List Org - Ensure Org Creatd
    list_org_response = da_client.list_organizations()

    print("\n\n ListOrg Response UserA: \n")
    print(list_org_response)

Read The Docs
-------------

.. toctree::
   :maxdepth: 2

   about
   install
   tutorials
   Community Resources <https://data-dot-all.github.io/dataall/deploy-aws/>
   Logging <https://data-dot-all.github.io/dataall/deploy-aws/>
   License <https://github.com/awslabs/aiops-modules/blob/main/LICENSE>
   Contributing <https://github.com/awslabs/aiops-modules/blob/main/CONTRIBUTING.md>


Dataall SDK
-------------

.. toctree::
   :maxdepth: 2

   modules
