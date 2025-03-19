# GeoLocationRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**address** | **str** |  | 
**lat** | **float** |  | 
**lng** | **float** |  | 

## Example

```python
from openapi_client.models.geo_location_request import GeoLocationRequest

# TODO update the JSON string below
json = "{}"
# create an instance of GeoLocationRequest from a JSON string
geo_location_request_instance = GeoLocationRequest.from_json(json)
# print the JSON string representation of the object
print(GeoLocationRequest.to_json())

# convert the object into a dict
geo_location_request_dict = geo_location_request_instance.to_dict()
# create an instance of GeoLocationRequest from a dict
geo_location_request_from_dict = GeoLocationRequest.from_dict(geo_location_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


