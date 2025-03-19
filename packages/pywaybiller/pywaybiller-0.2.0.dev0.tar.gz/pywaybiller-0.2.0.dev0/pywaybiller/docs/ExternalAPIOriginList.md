# ExternalAPIOriginList


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** |  | 
**name** | **str** |  | 
**address** | **str** |  | 
**latitude** | **float** |  | 
**longitude** | **float** |  | 
**raw_data** | [**ExternalAPIOriginRawData**](ExternalAPIOriginRawData.md) | The IDs of the Waybiller internal objects | [readonly] 

## Example

```python
from openapi_client.models.external_api_origin_list import ExternalAPIOriginList

# TODO update the JSON string below
json = "{}"
# create an instance of ExternalAPIOriginList from a JSON string
external_api_origin_list_instance = ExternalAPIOriginList.from_json(json)
# print the JSON string representation of the object
print(ExternalAPIOriginList.to_json())

# convert the object into a dict
external_api_origin_list_dict = external_api_origin_list_instance.to_dict()
# create an instance of ExternalAPIOriginList from a dict
external_api_origin_list_from_dict = ExternalAPIOriginList.from_dict(external_api_origin_list_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


