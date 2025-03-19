# ExternalAPIHoldingBaseRead


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**type** | **str** |  | [optional] 
**contract_number** | **str** |  | [optional] 
**contract_date** | **str** |  | [optional] 
**previous_owner** | [**ExternalAPIHoldingBasePreviousOwner**](ExternalAPIHoldingBasePreviousOwner.md) |  | [optional] 

## Example

```python
from openapi_client.models.external_api_holding_base_read import ExternalAPIHoldingBaseRead

# TODO update the JSON string below
json = "{}"
# create an instance of ExternalAPIHoldingBaseRead from a JSON string
external_api_holding_base_read_instance = ExternalAPIHoldingBaseRead.from_json(json)
# print the JSON string representation of the object
print(ExternalAPIHoldingBaseRead.to_json())

# convert the object into a dict
external_api_holding_base_read_dict = external_api_holding_base_read_instance.to_dict()
# create an instance of ExternalAPIHoldingBaseRead from a dict
external_api_holding_base_read_from_dict = ExternalAPIHoldingBaseRead.from_dict(external_api_holding_base_read_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


