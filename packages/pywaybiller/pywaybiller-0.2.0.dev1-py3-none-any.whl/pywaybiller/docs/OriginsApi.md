# openapi_client.OriginsApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**origins_create**](OriginsApi.md#origins_create) | **POST** /external-api/origins/ | Creation of an origin
[**origins_list**](OriginsApi.md#origins_list) | **GET** /external-api/origins/ | Querying of origins
[**origins_retrieve**](OriginsApi.md#origins_retrieve) | **GET** /external-api/origins/{id}/ | Querying of a single origin
[**origins_update**](OriginsApi.md#origins_update) | **PUT** /external-api/origins/{id}/ | Editing of an origin


# **origins_create**
> ExternalAPIOriginCreate origins_create(external_api_origin_create_request)

Creation of an origin

Creates a new origin.<br><br>
        **NB!** All posted IDs are Waybiller IDs.
        

### Example

* Api Key Authentication (ApiKeyAuth):

```python
import openapi_client
from openapi_client.models.external_api_origin_create import ExternalAPIOriginCreate
from openapi_client.models.external_api_origin_create_request import ExternalAPIOriginCreateRequest
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration.api_key['ApiKeyAuth'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['ApiKeyAuth'] = 'Bearer'

# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.OriginsApi(api_client)
    external_api_origin_create_request = openapi_client.ExternalAPIOriginCreateRequest() # ExternalAPIOriginCreateRequest | 

    try:
        # Creation of an origin
        api_response = api_instance.origins_create(external_api_origin_create_request)
        print("The response of OriginsApi->origins_create:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OriginsApi->origins_create: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **external_api_origin_create_request** | [**ExternalAPIOriginCreateRequest**](ExternalAPIOriginCreateRequest.md)|  | 

### Return type

[**ExternalAPIOriginCreate**](ExternalAPIOriginCreate.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** |  |  -  |
**403** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **origins_list**
> PaginatedExternalAPIOriginListList origins_list(company__reg_code=company__reg_code, company__reg_code__contains=company__reg_code__contains, company__reg_code__icontains=company__reg_code__icontains, company__reg_code__iexact=company__reg_code__iexact, explicitly_viewable=explicitly_viewable, limit=limit, location__address=location__address, location__address__contains=location__address__contains, location__address__icontains=location__address__icontains, location__address__iexact=location__address__iexact, name=name, name__contains=name__contains, name__icontains=name__icontains, name__iexact=name__iexact, offset=offset)

Querying of origins

Returns all origins associated with your company, according to the specified filters.

### Example

* Api Key Authentication (ApiKeyAuth):

```python
import openapi_client
from openapi_client.models.paginated_external_api_origin_list_list import PaginatedExternalAPIOriginListList
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration.api_key['ApiKeyAuth'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['ApiKeyAuth'] = 'Bearer'

# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.OriginsApi(api_client)
    company__reg_code = 'company__reg_code_example' # str | Filters origins belonging to the company with the specified register code (case sensitive). (optional)
    company__reg_code__contains = 'company__reg_code__contains_example' # str | Filters origins belonging to the company of which register codes contain this keyword (case sensitive). (optional)
    company__reg_code__icontains = 'company__reg_code__icontains_example' # str | Filters origins belonging to the company of which register codes contain this keyword (case insensitive). (optional)
    company__reg_code__iexact = 'company__reg_code__iexact_example' # str | Filters origins belonging to the company with the specified register code (case insensitive). (optional)
    explicitly_viewable = True # bool | Filters origins that belong to your company or where your company was added as a partner. (optional)
    limit = 30 # int | Maximum number of objects to return per page (optional) (default to 30)
    location__address = 'location__address_example' # str | Filters origins with specified address (case sensitive). (optional)
    location__address__contains = 'location__address__contains_example' # str | Filters origins of which addresses contain this keyword (case sensitive). (optional)
    location__address__icontains = 'location__address__icontains_example' # str | Filters origins of which addresses contain this keyword (case insensitive). (optional)
    location__address__iexact = 'location__address__iexact_example' # str | Filters origins with specified address (case insensitive). (optional)
    name = 'name_example' # str | Filters origins with specified name (case sensitive). (optional)
    name__contains = 'name__contains_example' # str | Filters origins of which names contain this keyword (case sensitive). (optional)
    name__icontains = 'name__icontains_example' # str | Filters origins of which names contain this keyword (case insensitive). (optional)
    name__iexact = 'name__iexact_example' # str | Filters origins with specified name (case insensitive). (optional)
    offset = 0 # int | The initial index from which to return the results (optional) (default to 0)

    try:
        # Querying of origins
        api_response = api_instance.origins_list(company__reg_code=company__reg_code, company__reg_code__contains=company__reg_code__contains, company__reg_code__icontains=company__reg_code__icontains, company__reg_code__iexact=company__reg_code__iexact, explicitly_viewable=explicitly_viewable, limit=limit, location__address=location__address, location__address__contains=location__address__contains, location__address__icontains=location__address__icontains, location__address__iexact=location__address__iexact, name=name, name__contains=name__contains, name__icontains=name__icontains, name__iexact=name__iexact, offset=offset)
        print("The response of OriginsApi->origins_list:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OriginsApi->origins_list: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **company__reg_code** | **str**| Filters origins belonging to the company with the specified register code (case sensitive). | [optional] 
 **company__reg_code__contains** | **str**| Filters origins belonging to the company of which register codes contain this keyword (case sensitive). | [optional] 
 **company__reg_code__icontains** | **str**| Filters origins belonging to the company of which register codes contain this keyword (case insensitive). | [optional] 
 **company__reg_code__iexact** | **str**| Filters origins belonging to the company with the specified register code (case insensitive). | [optional] 
 **explicitly_viewable** | **bool**| Filters origins that belong to your company or where your company was added as a partner. | [optional] 
 **limit** | **int**| Maximum number of objects to return per page | [optional] [default to 30]
 **location__address** | **str**| Filters origins with specified address (case sensitive). | [optional] 
 **location__address__contains** | **str**| Filters origins of which addresses contain this keyword (case sensitive). | [optional] 
 **location__address__icontains** | **str**| Filters origins of which addresses contain this keyword (case insensitive). | [optional] 
 **location__address__iexact** | **str**| Filters origins with specified address (case insensitive). | [optional] 
 **name** | **str**| Filters origins with specified name (case sensitive). | [optional] 
 **name__contains** | **str**| Filters origins of which names contain this keyword (case sensitive). | [optional] 
 **name__icontains** | **str**| Filters origins of which names contain this keyword (case insensitive). | [optional] 
 **name__iexact** | **str**| Filters origins with specified name (case insensitive). | [optional] 
 **offset** | **int**| The initial index from which to return the results | [optional] [default to 0]

### Return type

[**PaginatedExternalAPIOriginListList**](PaginatedExternalAPIOriginListList.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |
**403** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **origins_retrieve**
> ExternalAPIOriginRead origins_retrieve(id)

Querying of a single origin

Returns an origin with the specified ID. Only owner company and partner companies can query non-public origins. Public origins are available for everyone.

### Example

* Api Key Authentication (ApiKeyAuth):

```python
import openapi_client
from openapi_client.models.external_api_origin_read import ExternalAPIOriginRead
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration.api_key['ApiKeyAuth'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['ApiKeyAuth'] = 'Bearer'

# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.OriginsApi(api_client)
    id = 56 # int | A unique integer value identifying this origin.

    try:
        # Querying of a single origin
        api_response = api_instance.origins_retrieve(id)
        print("The response of OriginsApi->origins_retrieve:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OriginsApi->origins_retrieve: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **int**| A unique integer value identifying this origin. | 

### Return type

[**ExternalAPIOriginRead**](ExternalAPIOriginRead.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |
**403** |  |  -  |
**404** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **origins_update**
> ExternalAPIOriginUpdate origins_update(id, external_api_origin_update_request=external_api_origin_update_request)

Editing of an origin

Edits origin. It is allowed to be used by origin's owner company.<br><br>
        **NB!** All posted IDs are Waybiller IDs.
        

### Example

* Api Key Authentication (ApiKeyAuth):

```python
import openapi_client
from openapi_client.models.external_api_origin_update import ExternalAPIOriginUpdate
from openapi_client.models.external_api_origin_update_request import ExternalAPIOriginUpdateRequest
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration.api_key['ApiKeyAuth'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['ApiKeyAuth'] = 'Bearer'

# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.OriginsApi(api_client)
    id = 56 # int | A unique integer value identifying this origin.
    external_api_origin_update_request = openapi_client.ExternalAPIOriginUpdateRequest() # ExternalAPIOriginUpdateRequest |  (optional)

    try:
        # Editing of an origin
        api_response = api_instance.origins_update(id, external_api_origin_update_request=external_api_origin_update_request)
        print("The response of OriginsApi->origins_update:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OriginsApi->origins_update: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **int**| A unique integer value identifying this origin. | 
 **external_api_origin_update_request** | [**ExternalAPIOriginUpdateRequest**](ExternalAPIOriginUpdateRequest.md)|  | [optional] 

### Return type

[**ExternalAPIOriginUpdate**](ExternalAPIOriginUpdate.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |
**403** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

