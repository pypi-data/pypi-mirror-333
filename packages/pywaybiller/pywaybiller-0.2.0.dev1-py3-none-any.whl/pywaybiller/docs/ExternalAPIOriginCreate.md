# ExternalAPIOriginCreate


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** |  | [readonly] 
**name** | **str** |  | 
**location** | [**GeoLocation**](GeoLocation.md) |  | 
**assortments** | [**List[ExternalAPIOriginAssortment]**](ExternalAPIOriginAssortment.md) |  | 
**partner_companies** | **List[str]** | List of registry codes of partner companies. | [optional] 
**public** | **bool** |  | [optional] [default to False]
**active** | **bool** |  | [optional] [default to True]
**holding_base** | [**ExternalAPIHoldingBase**](ExternalAPIHoldingBase.md) | Holding base data is provided as is, in internal WB format. It may change at any time without warning and may have a different schema for old and new origins | [optional] 
**cadaster_number** | **str** | Cadaster number of the Origin in free form. Required if holding base is sent. | [optional] 
**extra_information** | **str** |  | [optional] 
**representative_name** | **str** |  | [optional] 
**representative_phone** | **str** |  | [optional] 
**waybill_created_emails** | **List[str]** | E-mail addresses, where you want to receive notification when waybill is created. | [optional] 
**waybill_accepted_emails** | **List[str]** | E-mail addresses, where you want to receive notification when waybill is accepted. | [optional] 
**waybill_reached_destination_emails** | **List[str]** | E-mail addresses, where you want to receive notification when waybill has arrived at destination. | [optional] 
**transport_order_created_emails** | **List[str]** | E-mail addresses, where you want to receive notification when transport order is created. | [optional] 
**waybill_created_emails_language** | [**ExternalAPIOriginCreateWaybillCreatedEmailsLanguage**](ExternalAPIOriginCreateWaybillCreatedEmailsLanguage.md) |  | [optional] 
**waybill_accepted_emails_language** | [**ExternalAPIOriginCreateWaybillCreatedEmailsLanguage**](ExternalAPIOriginCreateWaybillCreatedEmailsLanguage.md) |  | [optional] 
**waybill_reached_destination_emails_language** | [**ExternalAPIOriginCreateWaybillCreatedEmailsLanguage**](ExternalAPIOriginCreateWaybillCreatedEmailsLanguage.md) |  | [optional] 
**transport_order_created_emails_language** | [**ExternalAPIOriginCreateWaybillCreatedEmailsLanguage**](ExternalAPIOriginCreateWaybillCreatedEmailsLanguage.md) |  | [optional] 
**feature_single_transport_order_per_truck** | **bool** | Managers are not allowed to create transport orders for a vehicle if there is an active transport order for the vehicle from this origin | [optional] [default to False]
**feature_waybill_dispatched_amounts_changing_disabled** | **bool** | Drivers and receivers are not allowed to change dispatched amounts for waybills from this origin | [optional] [default to False]
**feature_waybill_destination_changing_disabled_for_drivers** | **bool** | Drivers are not allowed to change the destination of waybills from this origin | [optional] [default to False]
**company** | **str** | Registry code of the owner company. By default, API KEY company is used. Note, origin company can not be changed | [optional] 

## Example

```python
from openapi_client.models.external_api_origin_create import ExternalAPIOriginCreate

# TODO update the JSON string below
json = "{}"
# create an instance of ExternalAPIOriginCreate from a JSON string
external_api_origin_create_instance = ExternalAPIOriginCreate.from_json(json)
# print the JSON string representation of the object
print(ExternalAPIOriginCreate.to_json())

# convert the object into a dict
external_api_origin_create_dict = external_api_origin_create_instance.to_dict()
# create an instance of ExternalAPIOriginCreate from a dict
external_api_origin_create_from_dict = ExternalAPIOriginCreate.from_dict(external_api_origin_create_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


