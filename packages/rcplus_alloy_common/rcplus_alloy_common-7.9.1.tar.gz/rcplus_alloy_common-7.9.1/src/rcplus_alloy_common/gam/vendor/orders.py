# ruff: noqa: E501
"""
This XML file does not appear to have any style information associated with it. The document tree is shown below.
<!--  Generated file, do not edit  -->
<!--  Copyright 2024 Google Inc. All Rights Reserved  -->
<wsdl:definitions xmlns:tns="https://www.google.com/apis/ads/publisher/v202305" xmlns:wsdl="http://schemas.xmlsoap.org/wsdl/" xmlns:wsdlsoap="http://schemas.xmlsoap.org/wsdl/soap/" xmlns:xsd="http://www.w3.org/2001/XMLSchema" targetNamespace="https://www.google.com/apis/ads/publisher/v202305">
<wsdl:types>
<schema xmlns="http://www.w3.org/2001/XMLSchema" xmlns:jaxb="http://java.sun.com/xml/ns/jaxb" xmlns:tns="https://www.google.com/apis/ads/publisher/v202305" elementFormDefault="qualified" jaxb:version="1.0" targetNamespace="https://www.google.com/apis/ads/publisher/v202305">
<annotation>
<appinfo>
<jaxb:globalBindings typesafeEnumMaxMembers="999999"/>
</appinfo>
</annotation>
<complexType abstract="true" name="ObjectValue">
<annotation>
<documentation> Contains an object value. <p> <b>This object is experimental! <code>ObjectValue</code> is an experimental, innovative, and rapidly changing new feature for Ad Manager. Unfortunately, being on the bleeding edge means that we may make backwards-incompatible changes to <code>ObjectValue</code>. We will inform the community when this feature is no longer experimental.</b> </documentation>
</annotation>
<complexContent>
<extension base="tns:Value">
<sequence/>
</extension>
</complexContent>
</complexType>
<complexType abstract="true" name="ApiError">
<annotation>
<documentation> The API error base class that provides details about an error that occurred while processing a service request. <p>The OGNL field path is provided for parsers to identify the request data element that may have caused the error.</p> </documentation>
</annotation>
<sequence>
<element maxOccurs="1" minOccurs="0" name="fieldPath" type="xsd:string">
<annotation>
<documentation> The OGNL field path to identify cause of error. </documentation>
</annotation>
</element>
<element maxOccurs="unbounded" minOccurs="0" name="fieldPathElements" type="tns:FieldPathElement">
<annotation>
<documentation> A parsed copy of the field path. For example, the field path "operations[1].operand" corresponds to this list: {FieldPathElement(field = "operations", index = 1), FieldPathElement(field = "operand", index = null)}. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="trigger" type="xsd:string">
<annotation>
<documentation> The data that caused the error. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="errorString" type="xsd:string">
<annotation>
<documentation> A simple string representation of the error and reason. </documentation>
</annotation>
</element>
</sequence>
</complexType>
<complexType name="ApiException">
<annotation>
<documentation> Exception class for holding a list of service errors. </documentation>
</annotation>
<complexContent>
<extension base="tns:ApplicationException">
<sequence>
<element maxOccurs="unbounded" minOccurs="0" name="errors" type="tns:ApiError">
<annotation>
<documentation> List of errors. </documentation>
</annotation>
</element>
</sequence>
</extension>
</complexContent>
</complexType>
<complexType name="ApiVersionError">
<annotation>
<documentation> Errors related to the usage of API versions. </documentation>
</annotation>
<complexContent>
<extension base="tns:ApiError">
<sequence>
<element maxOccurs="1" minOccurs="0" name="reason" type="tns:ApiVersionError.Reason"/>
</sequence>
</extension>
</complexContent>
</complexType>
<complexType name="ApplicationException">
<annotation>
<documentation> Base class for exceptions. </documentation>
</annotation>
<sequence>
<element maxOccurs="1" minOccurs="0" name="message" type="xsd:string">
<annotation>
<documentation> Error message. </documentation>
</annotation>
</element>
</sequence>
</complexType>
<complexType name="AppliedLabel">
<annotation>
<documentation> Represents a {@link Label} that can be applied to an entity. To negate an inherited label, create an {@code AppliedLabel} with {@code labelId} as the inherited label's ID and {@code isNegated} set to true. </documentation>
</annotation>
<sequence>
<element maxOccurs="1" minOccurs="0" name="labelId" type="xsd:long">
<annotation>
<documentation> The ID of a created {@link Label}. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="isNegated" type="xsd:boolean">
<annotation>
<documentation> {@code isNegated} should be set to {@code true} to negate the effects of {@code labelId}. </documentation>
</annotation>
</element>
</sequence>
</complexType>
<complexType name="ApproveAndOverbookOrders">
<annotation>
<documentation> The action used for approving and overbooking {@link Order} objects. All {@link LineItem} objects within the order will be approved as well. For more information on what happens to an order and its line items when it is approved and overbooked, see the <a href="https://support.google.com/admanager/answer/177334">Ad Manager Help Center</a>. </documentation>
</annotation>
<complexContent>
<extension base="tns:ApproveOrders">
<sequence/>
</extension>
</complexContent>
</complexType>
<complexType name="ApproveOrders">
<annotation>
<documentation> The action used for approving {@link Order} objects. All {@link LineItem} objects within the order will be approved as well. For more information on what happens to an order and its line items when it is approved, see the <a href="https://support.google.com/admanager/answer/177334">Ad Manager Help Center</a>. </p> </documentation>
</annotation>
<complexContent>
<extension base="tns:OrderAction">
<sequence>
<element maxOccurs="1" minOccurs="0" name="skipInventoryCheck" type="xsd:boolean">
<annotation>
<documentation> Indicates whether the inventory check should be skipped when performing this action. The default value is false. </documentation>
</annotation>
</element>
</sequence>
</extension>
</complexContent>
</complexType>
<complexType name="ApproveOrdersWithoutReservationChanges">
<annotation>
<documentation> The action used for approving {@link Order} objects. All {@link LineItem} objects within the order will be approved as well. This action does not make any changes to the {@link LineItem#reservationStatus} of the line items within the order. If there are reservable line items that have not been reserved the operation will not succeed. </documentation>
</annotation>
<complexContent>
<extension base="tns:OrderAction">
<sequence/>
</extension>
</complexContent>
</complexType>
<complexType name="ArchiveOrders">
<annotation>
<documentation> The action used for archiving {@link Order} objects. </documentation>
</annotation>
<complexContent>
<extension base="tns:OrderAction">
<sequence/>
</extension>
</complexContent>
</complexType>
<complexType name="AssetError">
<annotation>
<documentation> Lists all errors associated with assets. </documentation>
</annotation>
<complexContent>
<extension base="tns:ApiError">
<sequence>
<element maxOccurs="1" minOccurs="0" name="reason" type="tns:AssetError.Reason">
<annotation>
<documentation> The error reason represented by an enum. </documentation>
</annotation>
</element>
</sequence>
</extension>
</complexContent>
</complexType>
<complexType name="AudienceExtensionError">
<annotation>
<documentation> Errors associated with audience extension enabled line items </documentation>
</annotation>
<complexContent>
<extension base="tns:ApiError">
<sequence>
<element maxOccurs="1" minOccurs="0" name="reason" type="tns:AudienceExtensionError.Reason">
<annotation>
<documentation> The error reason represented by an enum. </documentation>
</annotation>
</element>
</sequence>
</extension>
</complexContent>
</complexType>
<complexType name="AuthenticationError">
<annotation>
<documentation> An error for an exception that occurred when authenticating. </documentation>
</annotation>
<complexContent>
<extension base="tns:ApiError">
<sequence>
<element maxOccurs="1" minOccurs="0" name="reason" type="tns:AuthenticationError.Reason"/>
</sequence>
</extension>
</complexContent>
</complexType>
<complexType abstract="true" name="BaseCustomFieldValue">
<annotation>
<documentation> The value of a {@link CustomField} for a particular entity. </documentation>
</annotation>
<sequence>
<element maxOccurs="1" minOccurs="0" name="customFieldId" type="xsd:long">
<annotation>
<documentation> Id of the {@code CustomField} to which this value belongs. This attribute is required. </documentation>
</annotation>
</element>
</sequence>
</complexType>
<complexType name="BooleanValue">
<annotation>
<documentation> Contains a boolean value. </documentation>
</annotation>
<complexContent>
<extension base="tns:Value">
<sequence>
<element maxOccurs="1" minOccurs="0" name="value" type="xsd:boolean">
<annotation>
<documentation> The boolean value. </documentation>
</annotation>
</element>
</sequence>
</extension>
</complexContent>
</complexType>
<complexType name="ClickTrackingLineItemError">
<annotation>
<documentation> Click tracking is a special line item type with a number of unique errors as described below. </documentation>
</annotation>
<complexContent>
<extension base="tns:ApiError">
<sequence>
<element maxOccurs="1" minOccurs="0" name="reason" type="tns:ClickTrackingLineItemError.Reason">
<annotation>
<documentation> The error reason represented by an enum. </documentation>
</annotation>
</element>
</sequence>
</extension>
</complexContent>
</complexType>
<complexType name="CollectionSizeError">
<annotation>
<documentation> Error for the size of the collection being too large </documentation>
</annotation>
<complexContent>
<extension base="tns:ApiError">
<sequence>
<element maxOccurs="1" minOccurs="0" name="reason" type="tns:CollectionSizeError.Reason"/>
</sequence>
</extension>
</complexContent>
</complexType>
<complexType name="CommonError">
<annotation>
<documentation> A place for common errors that can be used across services. </documentation>
</annotation>
<complexContent>
<extension base="tns:ApiError">
<sequence>
<element maxOccurs="1" minOccurs="0" name="reason" type="tns:CommonError.Reason"/>
</sequence>
</extension>
</complexContent>
</complexType>
<complexType name="CompanyCreditStatusError">
<annotation>
<documentation> Lists all errors due to {@link Company#creditStatus}. </documentation>
</annotation>
<complexContent>
<extension base="tns:ApiError">
<sequence>
<element maxOccurs="1" minOccurs="0" name="reason" type="tns:CompanyCreditStatusError.Reason">
<annotation>
<documentation> The error reason represented by an enum. </documentation>
</annotation>
</element>
</sequence>
</extension>
</complexContent>
</complexType>
<complexType name="CreativeError">
<annotation>
<documentation> Lists all errors associated with creatives. </documentation>
</annotation>
<complexContent>
<extension base="tns:ApiError">
<sequence>
<element maxOccurs="1" minOccurs="0" name="reason" type="tns:CreativeError.Reason">
<annotation>
<documentation> The error reason represented by an enum. </documentation>
</annotation>
</element>
</sequence>
</extension>
</complexContent>
</complexType>
<complexType name="CrossSellError">
<annotation>
<documentation> Lists all errors associated with cross selling. </documentation>
</annotation>
<complexContent>
<extension base="tns:ApiError">
<sequence>
<element maxOccurs="1" minOccurs="0" name="reason" type="tns:CrossSellError.Reason">
<annotation>
<documentation> The error reason represented by an enum. </documentation>
</annotation>
</element>
</sequence>
</extension>
</complexContent>
</complexType>
<complexType name="CurrencyCodeError">
<annotation>
<documentation> Errors related to currency codes. </documentation>
</annotation>
<complexContent>
<extension base="tns:ApiError">
<sequence>
<element maxOccurs="1" minOccurs="0" name="reason" type="tns:CurrencyCodeError.Reason"/>
</sequence>
</extension>
</complexContent>
</complexType>
<complexType name="CustomFieldValue">
<annotation>
<documentation> The value of a {@link CustomField} that does not have a {@link CustomField#dataType} of {@link CustomFieldDataType#DROP_DOWN}. </documentation>
</annotation>
<complexContent>
<extension base="tns:BaseCustomFieldValue">
<sequence>
<element maxOccurs="1" minOccurs="0" name="value" type="tns:Value">
<annotation>
<documentation> The value for this field. The appropriate type of {@code Value} is determined by the {@link CustomField#dataType} of the {@code CustomField} that this conforms to. <table> <tr><th>{@link CustomFieldDataType}</th><th>{@link Value} type</th></tr> <tr><td>{@link CustomFieldDataType#STRING STRING}</td><td>{@link TextValue}</td></tr> <tr><td>{@link CustomFieldDataType#NUMBER NUMBER}</td><td>{@link NumberValue}</td></tr> <tr><td>{@link CustomFieldDataType#TOGGLE TOGGLE}</td><td>{@link BooleanValue}</td></tr> </table> </documentation>
</annotation>
</element>
</sequence>
</extension>
</complexContent>
</complexType>
<complexType name="CustomFieldValueError">
<annotation>
<documentation> Errors specific to editing custom field values </documentation>
</annotation>
<complexContent>
<extension base="tns:ApiError">
<sequence>
<element maxOccurs="1" minOccurs="0" name="reason" type="tns:CustomFieldValueError.Reason">
<annotation>
<documentation> The error reason represented by an enum. </documentation>
</annotation>
</element>
</sequence>
</extension>
</complexContent>
</complexType>
<complexType name="CustomTargetingError">
<annotation>
<documentation> Lists all errors related to {@link CustomTargetingKey} and {@link CustomTargetingValue} objects. </documentation>
</annotation>
<complexContent>
<extension base="tns:ApiError">
<sequence>
<element maxOccurs="1" minOccurs="0" name="reason" type="tns:CustomTargetingError.Reason"/>
</sequence>
</extension>
</complexContent>
</complexType>
<complexType name="Date">
<annotation>
<documentation> Represents a date. </documentation>
</annotation>
<sequence>
<element maxOccurs="1" minOccurs="0" name="year" type="xsd:int">
<annotation>
<documentation> Year (e.g., 2009) </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="month" type="xsd:int">
<annotation>
<documentation> Month (1..12) </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="day" type="xsd:int">
<annotation>
<documentation> Day (1..31) </documentation>
</annotation>
</element>
</sequence>
</complexType>
<complexType name="DateTime">
<annotation>
<documentation> Represents a date combined with the time of day. </documentation>
</annotation>
<sequence>
<element maxOccurs="1" minOccurs="0" name="date" type="tns:Date"/>
<element maxOccurs="1" minOccurs="0" name="hour" type="xsd:int"/>
<element maxOccurs="1" minOccurs="0" name="minute" type="xsd:int"/>
<element maxOccurs="1" minOccurs="0" name="second" type="xsd:int"/>
<element maxOccurs="1" minOccurs="0" name="timeZoneId" type="xsd:string"/>
</sequence>
</complexType>
<complexType name="DateTimeRangeTargetingError">
<annotation>
<documentation> Lists all date time range errors caused by associating a line item with a targeting expression. </documentation>
</annotation>
<complexContent>
<extension base="tns:ApiError">
<sequence>
<element maxOccurs="1" minOccurs="0" name="reason" type="tns:DateTimeRangeTargetingError.Reason">
<annotation>
<documentation> The error reason represented by an enum. </documentation>
</annotation>
</element>
</sequence>
</extension>
</complexContent>
</complexType>
<complexType name="DateTimeValue">
<annotation>
<documentation> Contains a date-time value. </documentation>
</annotation>
<complexContent>
<extension base="tns:Value">
<sequence>
<element maxOccurs="1" minOccurs="0" name="value" type="tns:DateTime">
<annotation>
<documentation> The {@code DateTime} value. </documentation>
</annotation>
</element>
</sequence>
</extension>
</complexContent>
</complexType>
<complexType name="DateValue">
<annotation>
<documentation> Contains a date value. </documentation>
</annotation>
<complexContent>
<extension base="tns:Value">
<sequence>
<element maxOccurs="1" minOccurs="0" name="value" type="tns:Date">
<annotation>
<documentation> The {@code Date} value. </documentation>
</annotation>
</element>
</sequence>
</extension>
</complexContent>
</complexType>
<complexType name="DayPartTargetingError">
<annotation>
<documentation> Lists all errors associated with day-part targeting for a line item. </documentation>
</annotation>
<complexContent>
<extension base="tns:ApiError">
<sequence>
<element maxOccurs="1" minOccurs="0" name="reason" type="tns:DayPartTargetingError.Reason">
<annotation>
<documentation> The error reason represented by an enum. </documentation>
</annotation>
</element>
</sequence>
</extension>
</complexContent>
</complexType>
<complexType name="DeleteOrders">
<annotation>
<documentation> The action used for deleting {@link Order} objects. All line items within that order are also deleted. Orders can only be deleted if none of its line items have been eligible to serve. This action can be used to delete proposed orders and line items if they are no longer valid. </documentation>
</annotation>
<complexContent>
<extension base="tns:OrderAction">
<sequence/>
</extension>
</complexContent>
</complexType>
<complexType name="DisapproveOrders">
<annotation>
<documentation> The action used for disapproving {@link Order} objects. All {@link LineItem} objects within the order will be disapproved as well. </documentation>
</annotation>
<complexContent>
<extension base="tns:OrderAction">
<sequence/>
</extension>
</complexContent>
</complexType>
<complexType name="DisapproveOrdersWithoutReservationChanges">
<annotation>
<documentation> The action used for disapproving {@link Order} objects. All {@link LineItem} objects within the order will be disapproved as well. This action does not make any changes to the {@link LineItem#reservationStatus} of the line items within the order. </documentation>
</annotation>
<complexContent>
<extension base="tns:OrderAction">
<sequence/>
</extension>
</complexContent>
</complexType>
<complexType name="DropDownCustomFieldValue">
<annotation>
<documentation> A {@link CustomFieldValue} for a {@link CustomField} that has a {@link CustomField#dataType} of {@link CustomFieldDataType#DROP_DOWN} </documentation>
</annotation>
<complexContent>
<extension base="tns:BaseCustomFieldValue">
<sequence>
<element maxOccurs="1" minOccurs="0" name="customFieldOptionId" type="xsd:long">
<annotation>
<documentation> The {@link CustomFieldOption#id ID} of the {@link CustomFieldOption} for this value. </documentation>
</annotation>
</element>
</sequence>
</extension>
</complexContent>
</complexType>
<complexType name="EntityChildrenLimitReachedError">
<annotation>
<documentation> Lists errors relating to having too many children on an entity. </documentation>
</annotation>
<complexContent>
<extension base="tns:ApiError">
<sequence>
<element maxOccurs="1" minOccurs="0" name="reason" type="tns:EntityChildrenLimitReachedError.Reason"/>
</sequence>
</extension>
</complexContent>
</complexType>
<complexType name="EntityLimitReachedError">
<annotation>
<documentation> An error that occurs when creating an entity if the limit on the number of allowed entities for a network has already been reached. </documentation>
</annotation>
<complexContent>
<extension base="tns:ApiError">
<sequence>
<element maxOccurs="1" minOccurs="0" name="reason" type="tns:EntityLimitReachedError.Reason"/>
</sequence>
</extension>
</complexContent>
</complexType>
<complexType name="FeatureError">
<annotation>
<documentation> Errors related to feature management. If you attempt using a feature that is not available to the current network you'll receive a FeatureError with the missing feature as the trigger. </documentation>
</annotation>
<complexContent>
<extension base="tns:ApiError">
<sequence>
<element maxOccurs="1" minOccurs="0" name="reason" type="tns:FeatureError.Reason"/>
</sequence>
</extension>
</complexContent>
</complexType>
<complexType name="FieldPathElement">
<annotation>
<documentation> A segment of a field path. Each dot in a field path defines a new segment. </documentation>
</annotation>
<sequence>
<element maxOccurs="1" minOccurs="0" name="field" type="xsd:string">
<annotation>
<documentation> The name of a field in lower camelcase. (e.g. "biddingStrategy") </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="index" type="xsd:int">
<annotation>
<documentation> For list fields, this is a 0-indexed position in the list. Null for non-list fields. </documentation>
</annotation>
</element>
</sequence>
</complexType>
<complexType name="ForecastError">
<annotation>
<documentation> Errors that can result from a forecast request. </documentation>
</annotation>
<complexContent>
<extension base="tns:ApiError">
<sequence>
<element maxOccurs="1" minOccurs="0" name="reason" type="tns:ForecastError.Reason">
<annotation>
<documentation> The reason for the forecast error. </documentation>
</annotation>
</element>
</sequence>
</extension>
</complexContent>
</complexType>
<complexType name="FrequencyCapError">
<annotation>
<documentation> Lists all errors associated with frequency caps. </documentation>
</annotation>
<complexContent>
<extension base="tns:ApiError">
<sequence>
<element maxOccurs="1" minOccurs="0" name="reason" type="tns:FrequencyCapError.Reason">
<annotation>
<documentation> The error reason represented by an enum. </documentation>
</annotation>
</element>
</sequence>
</extension>
</complexContent>
</complexType>
<complexType name="GenericTargetingError">
<annotation>
<documentation> Targeting validation errors that can be used by different targeting types. </documentation>
</annotation>
<complexContent>
<extension base="tns:ApiError">
<sequence>
<element maxOccurs="1" minOccurs="0" name="reason" type="tns:GenericTargetingError.Reason"/>
</sequence>
</extension>
</complexContent>
</complexType>
<complexType name="GeoTargetingError">
<annotation>
<documentation> Lists all errors associated with geographical targeting for a {@link LineItem}. </documentation>
</annotation>
<complexContent>
<extension base="tns:ApiError">
<sequence>
<element maxOccurs="1" minOccurs="0" name="reason" type="tns:GeoTargetingError.Reason">
<annotation>
<documentation> The error reason represented by an enum. </documentation>
</annotation>
</element>
</sequence>
</extension>
</complexContent>
</complexType>
<complexType name="GrpSettingsError">
<annotation>
<documentation> Errors associated with line items with GRP settings. </documentation>
</annotation>
<complexContent>
<extension base="tns:ApiError">
<sequence>
<element maxOccurs="1" minOccurs="0" name="reason" type="tns:GrpSettingsError.Reason">
<annotation>
<documentation> The error reason represented by an enum. </documentation>
</annotation>
</element>
</sequence>
</extension>
</complexContent>
</complexType>
<complexType name="ImageError">
<annotation>
<documentation> Lists all errors associated with images. </documentation>
</annotation>
<complexContent>
<extension base="tns:ApiError">
<sequence>
<element maxOccurs="1" minOccurs="0" name="reason" type="tns:ImageError.Reason">
<annotation>
<documentation> The error reason represented by an enum. </documentation>
</annotation>
</element>
</sequence>
</extension>
</complexContent>
</complexType>
<complexType name="InternalApiError">
<annotation>
<documentation> Indicates that a server-side error has occured. {@code InternalApiError}s are generally not the result of an invalid request or message sent by the client. </documentation>
</annotation>
<complexContent>
<extension base="tns:ApiError">
<sequence>
<element maxOccurs="1" minOccurs="0" name="reason" type="tns:InternalApiError.Reason">
<annotation>
<documentation> The error reason represented by an enum. </documentation>
</annotation>
</element>
</sequence>
</extension>
</complexContent>
</complexType>
<complexType name="InvalidEmailError">
<annotation>
<documentation> Caused by supplying a value for an email attribute that is not a valid email address. </documentation>
</annotation>
<complexContent>
<extension base="tns:ApiError">
<sequence>
<element maxOccurs="1" minOccurs="0" name="reason" type="tns:InvalidEmailError.Reason"/>
</sequence>
</extension>
</complexContent>
</complexType>
<complexType name="InvalidUrlError">
<annotation>
<documentation> Lists all errors associated with URLs. </documentation>
</annotation>
<complexContent>
<extension base="tns:ApiError">
<sequence>
<element maxOccurs="1" minOccurs="0" name="reason" type="tns:InvalidUrlError.Reason"/>
</sequence>
</extension>
</complexContent>
</complexType>
<complexType name="InventoryTargetingError">
<annotation>
<documentation> Lists all inventory errors caused by associating a line item with a targeting expression. </documentation>
</annotation>
<complexContent>
<extension base="tns:ApiError">
<sequence>
<element maxOccurs="1" minOccurs="0" name="reason" type="tns:InventoryTargetingError.Reason">
<annotation>
<documentation> The error reason represented by an enum. </documentation>
</annotation>
</element>
</sequence>
</extension>
</complexContent>
</complexType>
<complexType name="LabelEntityAssociationError">
<annotation>
<documentation> Errors specific to creating label entity associations. </documentation>
</annotation>
<complexContent>
<extension base="tns:ApiError">
<sequence>
<element maxOccurs="1" minOccurs="0" name="reason" type="tns:LabelEntityAssociationError.Reason">
<annotation>
<documentation> The error reason represented by an enum. </documentation>
</annotation>
</element>
</sequence>
</extension>
</complexContent>
</complexType>
<complexType name="LineItemActivityAssociationError">
<annotation>
<documentation> Errors specific to associating activities to line items. </documentation>
</annotation>
<complexContent>
<extension base="tns:ApiError">
<sequence>
<element maxOccurs="1" minOccurs="0" name="reason" type="tns:LineItemActivityAssociationError.Reason">
<annotation>
<documentation> The error reason represented by an enum. </documentation>
</annotation>
</element>
</sequence>
</extension>
</complexContent>
</complexType>
<complexType name="LineItemCreativeAssociationError">
<annotation>
<documentation> Lists all errors associated with line item-to-creative association dates. </documentation>
</annotation>
<complexContent>
<extension base="tns:ApiError">
<sequence>
<element maxOccurs="1" minOccurs="0" name="reason" type="tns:LineItemCreativeAssociationError.Reason">
<annotation>
<documentation> The error reason represented by an enum. </documentation>
</annotation>
</element>
</sequence>
</extension>
</complexContent>
</complexType>
<complexType name="LineItemError">
<annotation>
<documentation> A catch-all error that lists all generic errors associated with LineItem. </documentation>
</annotation>
<complexContent>
<extension base="tns:ApiError">
<sequence>
<element maxOccurs="1" minOccurs="0" name="reason" type="tns:LineItemError.Reason">
<annotation>
<documentation> The error reason represented by an enum. </documentation>
</annotation>
</element>
</sequence>
</extension>
</complexContent>
</complexType>
<complexType name="LineItemFlightDateError">
<annotation>
<documentation> Lists all errors associated with LineItem start and end dates. </documentation>
</annotation>
<complexContent>
<extension base="tns:ApiError">
<sequence>
<element maxOccurs="1" minOccurs="0" name="reason" type="tns:LineItemFlightDateError.Reason">
<annotation>
<documentation> The error reason represented by an enum. </documentation>
</annotation>
</element>
</sequence>
</extension>
</complexContent>
</complexType>
<complexType name="LineItemOperationError">
<annotation>
<documentation> Lists all errors for executing operations on line items </documentation>
</annotation>
<complexContent>
<extension base="tns:ApiError">
<sequence>
<element maxOccurs="1" minOccurs="0" name="reason" type="tns:LineItemOperationError.Reason">
<annotation>
<documentation> The error reason represented by an enum. </documentation>
</annotation>
</element>
</sequence>
</extension>
</complexContent>
</complexType>
<complexType name="MobileApplicationTargetingError">
<annotation>
<documentation> Lists all errors related to mobile application targeting for a line item. </documentation>
</annotation>
<complexContent>
<extension base="tns:ApiError">
<sequence>
<element maxOccurs="1" minOccurs="0" name="reason" type="tns:MobileApplicationTargetingError.Reason"/>
</sequence>
</extension>
</complexContent>
</complexType>
<complexType name="Money">
<annotation>
<documentation> Represents a money amount. </documentation>
</annotation>
<sequence>
<element maxOccurs="1" minOccurs="0" name="currencyCode" type="xsd:string">
<annotation>
<documentation> Three letter currency code in string format. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="microAmount" type="xsd:long">
<annotation>
<documentation> Money values are always specified in terms of micros which are a millionth of the fundamental currency unit. For US dollars, $1 is 1,000,000 micros. </documentation>
</annotation>
</element>
</sequence>
</complexType>
<complexType name="NotNullError">
<annotation>
<documentation> Caused by supplying a null value for an attribute that cannot be null. </documentation>
</annotation>
<complexContent>
<extension base="tns:ApiError">
<sequence>
<element maxOccurs="1" minOccurs="0" name="reason" type="tns:NotNullError.Reason">
<annotation>
<documentation> The error reason represented by an enum. </documentation>
</annotation>
</element>
</sequence>
</extension>
</complexContent>
</complexType>
<complexType name="NullError">
<annotation>
<documentation> Errors associated with violation of a NOT NULL check. </documentation>
</annotation>
<complexContent>
<extension base="tns:ApiError">
<sequence>
<element maxOccurs="1" minOccurs="0" name="reason" type="tns:NullError.Reason">
<annotation>
<documentation> The error reason represented by an enum. </documentation>
</annotation>
</element>
</sequence>
</extension>
</complexContent>
</complexType>
<complexType name="NumberValue">
<annotation>
<documentation> Contains a numeric value. </documentation>
</annotation>
<complexContent>
<extension base="tns:Value">
<sequence>
<element maxOccurs="1" minOccurs="0" name="value" type="xsd:string">
<annotation>
<documentation> The numeric value represented as a string. </documentation>
</annotation>
</element>
</sequence>
</extension>
</complexContent>
</complexType>
<complexType abstract="true" name="OrderAction">
<annotation>
<documentation> Represents the actions that can be performed on {@link Order} objects. </documentation>
</annotation>
<sequence/>
</complexType>
<complexType name="OrderActionError">
<annotation>
<documentation> Lists all errors associated with performing actions on {@link Order} objects. </documentation>
</annotation>
<complexContent>
<extension base="tns:ApiError">
<sequence>
<element maxOccurs="1" minOccurs="0" name="reason" type="tns:OrderActionError.Reason">
<annotation>
<documentation> The error reason represented by an enum. </documentation>
</annotation>
</element>
</sequence>
</extension>
</complexContent>
</complexType>
<complexType name="Order">
<annotation>
<documentation> An {@code Order} represents a grouping of individual {@link LineItem} objects, each of which fulfill an ad request from a particular advertiser. </documentation>
</annotation>
<sequence>
<element maxOccurs="1" minOccurs="0" name="id" type="xsd:long">
<annotation>
<documentation> The unique ID of the {@code Order}. This value is readonly and is assigned by Google. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="name" type="xsd:string">
<annotation>
<documentation> The name of the {@code Order}. This value is required to create an order and has a maximum length of 255 characters. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="startDateTime" type="tns:DateTime">
<annotation>
<documentation> The date and time at which the {@code Order} and its associated line items are eligible to begin serving. This attribute is readonly and is derived from the line item of the order which has the earliest {@link LineItem#startDateTime}. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="endDateTime" type="tns:DateTime">
<annotation>
<documentation> The date and time at which the {@code Order} and its associated line items stop being served. This attribute is readonly and is derived from the line item of the order which has the latest {@link LineItem#endDateTime}. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="unlimitedEndDateTime" type="xsd:boolean">
<annotation>
<documentation> Specifies whether or not the {@code Order} has an unlimited end date. This attribute is readonly and is {@code true} if any of the order's line items has {@link LineItem#unlimitedEndDateTime} set to {@code true}. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="status" type="tns:OrderStatus">
<annotation>
<documentation> The status of the {@code Order}. This attribute is read-only. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="isArchived" type="xsd:boolean">
<annotation>
<documentation> The archival status of the {@code Order}. This attribute is readonly. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="notes" type="xsd:string">
<annotation>
<documentation> Provides any additional notes that may annotate the {@code Order}. This attribute is optional and has a maximum length of 65,535 characters. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="externalOrderId" type="xsd:int">
<annotation>
<documentation> An arbitrary ID to associate to the {@code Order}, which can be used as a key to an external system. This value is optional. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="poNumber" type="xsd:string">
<annotation>
<documentation> The purchase order number for the {@code Order}. This value is optional and has a maximum length of 63 characters. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="currencyCode" type="xsd:string">
<annotation>
<documentation> The ISO currency code for the currency used by the {@code Order}. This value is read-only and is the network's currency code. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="advertiserId" type="xsd:long">
<annotation>
<documentation> The unique ID of the {@link Company}, which is of type {@link Company.Type#ADVERTISER}, to which this order belongs. This attribute is required. </documentation>
</annotation>
</element>
<element maxOccurs="unbounded" minOccurs="0" name="advertiserContactIds" type="xsd:long">
<annotation>
<documentation> List of IDs for advertiser contacts of the order. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="agencyId" type="xsd:long">
<annotation>
<documentation> The unique ID of the {@link Company}, which is of type {@link Company.Type#AGENCY}, with which this order is associated. This attribute is optional. </documentation>
</annotation>
</element>
<element maxOccurs="unbounded" minOccurs="0" name="agencyContactIds" type="xsd:long">
<annotation>
<documentation> List of IDs for agency contacts of the order. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="creatorId" type="xsd:long">
<annotation>
<documentation> The unique ID of the {@link User} who created the {@code Order} on behalf of the advertiser. This value is readonly and is assigned by Google. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="traffickerId" type="xsd:long">
<annotation>
<documentation> The unique ID of the {@link User} responsible for trafficking the {@code Order}. This value is required for creating an order. </documentation>
</annotation>
</element>
<element maxOccurs="unbounded" minOccurs="0" name="secondaryTraffickerIds" type="xsd:long">
<annotation>
<documentation> The IDs of the secondary traffickers associated with the order. This value is optional. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="salespersonId" type="xsd:long">
<annotation>
<documentation> The unique ID of the {@link User} responsible for the sales of the {@code Order}. This value is optional. </documentation>
</annotation>
</element>
<element maxOccurs="unbounded" minOccurs="0" name="secondarySalespersonIds" type="xsd:long">
<annotation>
<documentation> The IDs of the secondary salespeople associated with the order. This value is optional. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="totalImpressionsDelivered" type="xsd:long">
<annotation>
<documentation> Total impressions delivered for all line items of this {@code Order}. This value is read-only and is assigned by Google. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="totalClicksDelivered" type="xsd:long">
<annotation>
<documentation> Total clicks delivered for all line items of this {@code Order}. This value is read-only and is assigned by Google. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="totalViewableImpressionsDelivered" type="xsd:long">
<annotation>
<documentation> Total viewable impressions delivered for all line items of this {@code Order}. This value is read-only and is assigned by Google. Starting in v201705, this will be {@code null} when the order does not have line items trafficked against a viewable impressions goal. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="totalBudget" type="tns:Money">
<annotation>
<documentation> Total budget for all line items of this {@code Order}. This value is a readonly field assigned by Google and is calculated from the associated {@link LineItem#costPerUnit} values. </documentation>
</annotation>
</element>
<element maxOccurs="unbounded" minOccurs="0" name="appliedLabels" type="tns:AppliedLabel">
<annotation>
<documentation> The set of labels applied directly to this order. </documentation>
</annotation>
</element>
<element maxOccurs="unbounded" minOccurs="0" name="effectiveAppliedLabels" type="tns:AppliedLabel">
<annotation>
<documentation> Contains the set of labels applied directly to the order as well as those inherited from the company that owns the order. If a label has been negated, only the negated label is returned. This field is readonly and is assigned by Google. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="lastModifiedByApp" type="xsd:string">
<annotation>
<documentation> The application which modified this order. This attribute is read only and is assigned by Google. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="isProgrammatic" type="xsd:boolean">
<annotation>
<documentation> Specifies whether or not the {@code Order} is a programmatic order. This value is optional and defaults to false. </documentation>
</annotation>
</element>
<element maxOccurs="unbounded" minOccurs="0" name="appliedTeamIds" type="xsd:long">
<annotation>
<documentation> The IDs of all teams that this order is on directly. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="lastModifiedDateTime" type="tns:DateTime">
<annotation>
<documentation> The date and time this order was last modified. </documentation>
</annotation>
</element>
<element maxOccurs="unbounded" minOccurs="0" name="customFieldValues" type="tns:BaseCustomFieldValue">
<annotation>
<documentation> The values of the custom fields associated with this order. </documentation>
</annotation>
</element>
</sequence>
</complexType>
<complexType name="OrderError">
<annotation>
<documentation> Lists all errors associated with orders. </documentation>
</annotation>
<complexContent>
<extension base="tns:ApiError">
<sequence>
<element maxOccurs="1" minOccurs="0" name="reason" type="tns:OrderError.Reason">
<annotation>
<documentation> The error reason represented by an enum. </documentation>
</annotation>
</element>
</sequence>
</extension>
</complexContent>
</complexType>
<complexType name="OrderPage">
<annotation>
<documentation> Captures a page of {@link Order} objects. </documentation>
</annotation>
<sequence>
<element maxOccurs="1" minOccurs="0" name="totalResultSetSize" type="xsd:int">
<annotation>
<documentation> The size of the total result set to which this page belongs. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="startIndex" type="xsd:int">
<annotation>
<documentation> The absolute index in the total result set on which this page begins. </documentation>
</annotation>
</element>
<element maxOccurs="unbounded" minOccurs="0" name="results" type="tns:Order">
<annotation>
<documentation> The collection of orders contained within this page. </documentation>
</annotation>
</element>
</sequence>
</complexType>
<complexType name="ParseError">
<annotation>
<documentation> Lists errors related to parsing. </documentation>
</annotation>
<complexContent>
<extension base="tns:ApiError">
<sequence>
<element maxOccurs="1" minOccurs="0" name="reason" type="tns:ParseError.Reason">
<annotation>
<documentation> The error reason represented by an enum. </documentation>
</annotation>
</element>
</sequence>
</extension>
</complexContent>
</complexType>
<complexType name="PauseOrders">
<annotation>
<documentation> The action used for pausing all {@link LineItem} objects within an order. </documentation>
</annotation>
<complexContent>
<extension base="tns:OrderAction">
<sequence/>
</extension>
</complexContent>
</complexType>
<complexType name="PermissionError">
<annotation>
<documentation> Errors related to incorrect permission. </documentation>
</annotation>
<complexContent>
<extension base="tns:ApiError">
<sequence>
<element maxOccurs="1" minOccurs="0" name="reason" type="tns:PermissionError.Reason"/>
</sequence>
</extension>
</complexContent>
</complexType>
<complexType name="ProgrammaticError">
<annotation>
<documentation> Errors associated with programmatic line items. </documentation>
</annotation>
<complexContent>
<extension base="tns:ApiError">
<sequence>
<element maxOccurs="1" minOccurs="0" name="reason" type="tns:ProgrammaticError.Reason">
<annotation>
<documentation> The error reason represented by an enum. </documentation>
</annotation>
</element>
</sequence>
</extension>
</complexContent>
</complexType>
<complexType name="PublisherQueryLanguageContextError">
<annotation>
<documentation> An error that occurs while executing a PQL query contained in a {@link Statement} object. </documentation>
</annotation>
<complexContent>
<extension base="tns:ApiError">
<sequence>
<element maxOccurs="1" minOccurs="0" name="reason" type="tns:PublisherQueryLanguageContextError.Reason">
<annotation>
<documentation> The error reason represented by an enum. </documentation>
</annotation>
</element>
</sequence>
</extension>
</complexContent>
</complexType>
<complexType name="PublisherQueryLanguageSyntaxError">
<annotation>
<documentation> An error that occurs while parsing a PQL query contained in a {@link Statement} object. </documentation>
</annotation>
<complexContent>
<extension base="tns:ApiError">
<sequence>
<element maxOccurs="1" minOccurs="0" name="reason" type="tns:PublisherQueryLanguageSyntaxError.Reason">
<annotation>
<documentation> The error reason represented by an enum. </documentation>
</annotation>
</element>
</sequence>
</extension>
</complexContent>
</complexType>
<complexType name="QuotaError">
<annotation>
<documentation> Describes a client-side error on which a user is attempting to perform an action to which they have no quota remaining. </documentation>
</annotation>
<complexContent>
<extension base="tns:ApiError">
<sequence>
<element maxOccurs="1" minOccurs="0" name="reason" type="tns:QuotaError.Reason"/>
</sequence>
</extension>
</complexContent>
</complexType>
<complexType name="RangeError">
<annotation>
<documentation> A list of all errors associated with the Range constraint. </documentation>
</annotation>
<complexContent>
<extension base="tns:ApiError">
<sequence>
<element maxOccurs="1" minOccurs="0" name="reason" type="tns:RangeError.Reason"/>
</sequence>
</extension>
</complexContent>
</complexType>
<complexType name="RegExError">
<annotation>
<documentation> Caused by supplying a value for an object attribute that does not conform to a documented valid regular expression. </documentation>
</annotation>
<complexContent>
<extension base="tns:ApiError">
<sequence>
<element maxOccurs="1" minOccurs="0" name="reason" type="tns:RegExError.Reason">
<annotation>
<documentation> The error reason represented by an enum. </documentation>
</annotation>
</element>
</sequence>
</extension>
</complexContent>
</complexType>
<complexType name="RequestPlatformTargetingError">
<annotation>
<documentation> Errors related to request platform targeting. </documentation>
</annotation>
<complexContent>
<extension base="tns:ApiError">
<sequence>
<element maxOccurs="1" minOccurs="0" name="reason" type="tns:RequestPlatformTargetingError.Reason">
<annotation>
<documentation> The error reason represented by an enum. </documentation>
</annotation>
</element>
</sequence>
</extension>
</complexContent>
</complexType>
<complexType name="RequiredCollectionError">
<annotation>
<documentation> A list of all errors to be used for validating sizes of collections. </documentation>
</annotation>
<complexContent>
<extension base="tns:ApiError">
<sequence>
<element maxOccurs="1" minOccurs="0" name="reason" type="tns:RequiredCollectionError.Reason"/>
</sequence>
</extension>
</complexContent>
</complexType>
<complexType name="RequiredError">
<annotation>
<documentation> Errors due to missing required field. </documentation>
</annotation>
<complexContent>
<extension base="tns:ApiError">
<sequence>
<element maxOccurs="1" minOccurs="0" name="reason" type="tns:RequiredError.Reason">
<annotation>
<documentation> The error reason represented by an enum. </documentation>
</annotation>
</element>
</sequence>
</extension>
</complexContent>
</complexType>
<complexType name="RequiredNumberError">
<annotation>
<documentation> A list of all errors to be used in conjunction with required number validators. </documentation>
</annotation>
<complexContent>
<extension base="tns:ApiError">
<sequence>
<element maxOccurs="1" minOccurs="0" name="reason" type="tns:RequiredNumberError.Reason"/>
</sequence>
</extension>
</complexContent>
</complexType>
<complexType name="RequiredSizeError">
<annotation>
<documentation> A list of all errors to be used for validating {@link Size}. </documentation>
</annotation>
<complexContent>
<extension base="tns:ApiError">
<sequence>
<element maxOccurs="1" minOccurs="0" name="reason" type="tns:RequiredSizeError.Reason"/>
</sequence>
</extension>
</complexContent>
</complexType>
<complexType name="ReservationDetailsError">
<annotation>
<documentation> Lists all errors associated with LineItem's reservation details. </documentation>
</annotation>
<complexContent>
<extension base="tns:ApiError">
<sequence>
<element maxOccurs="1" minOccurs="0" name="reason" type="tns:ReservationDetailsError.Reason">
<annotation>
<documentation> The error reason represented by an enum. </documentation>
</annotation>
</element>
</sequence>
</extension>
</complexContent>
</complexType>
<complexType name="ResumeAndOverbookOrders">
<annotation>
<documentation> The action used for resuming and overbooking {@link Order} objects. All {@link LineItem} objects within the order will resume as well. </documentation>
</annotation>
<complexContent>
<extension base="tns:ResumeOrders">
<sequence/>
</extension>
</complexContent>
</complexType>
<complexType name="ResumeOrders">
<annotation>
<documentation> The action used for resuming {@link Order} objects. {@link LineItem} objects within the order that are eligble to resume will resume as well. </documentation>
</annotation>
<complexContent>
<extension base="tns:OrderAction">
<sequence>
<element maxOccurs="1" minOccurs="0" name="skipInventoryCheck" type="xsd:boolean">
<annotation>
<documentation> Indicates whether the inventory check should be skipped when performing this action. The default value is false. </documentation>
</annotation>
</element>
</sequence>
</extension>
</complexContent>
</complexType>
<complexType name="RetractOrders">
<annotation>
<documentation> The action used for retracting {@link Order} objects. </documentation>
</annotation>
<complexContent>
<extension base="tns:OrderAction">
<sequence/>
</extension>
</complexContent>
</complexType>
<complexType name="RetractOrdersWithoutReservationChanges">
<annotation>
<documentation> The action used for retracting {@link Order} objects. This action does not make any changes to the {@link LineItem#reservationStatus} of the line items within the order. </documentation>
</annotation>
<complexContent>
<extension base="tns:OrderAction">
<sequence/>
</extension>
</complexContent>
</complexType>
<complexType name="AudienceSegmentError">
<annotation>
<documentation> Errors that could occur on audience segment related requests. </documentation>
</annotation>
<complexContent>
<extension base="tns:ApiError">
<sequence>
<element maxOccurs="1" minOccurs="0" name="reason" type="tns:AudienceSegmentError.Reason"/>
</sequence>
</extension>
</complexContent>
</complexType>
<complexType name="ServerError">
<annotation>
<documentation> Errors related to the server. </documentation>
</annotation>
<complexContent>
<extension base="tns:ApiError">
<sequence>
<element maxOccurs="1" minOccurs="0" name="reason" type="tns:ServerError.Reason"/>
</sequence>
</extension>
</complexContent>
</complexType>
<complexType name="SetTopBoxLineItemError">
<annotation>
<documentation> Errors associated with set-top box {@link LineItem line items}. </documentation>
</annotation>
<complexContent>
<extension base="tns:ApiError">
<sequence>
<element maxOccurs="1" minOccurs="0" name="reason" type="tns:SetTopBoxLineItemError.Reason">
<annotation>
<documentation> The error reason represented by an enum. </documentation>
</annotation>
</element>
</sequence>
</extension>
</complexContent>
</complexType>
<complexType name="SetValue">
<annotation>
<documentation> Contains a set of {@link Value Values}. May not contain duplicates. </documentation>
</annotation>
<complexContent>
<extension base="tns:Value">
<sequence>
<element maxOccurs="unbounded" minOccurs="0" name="values" type="tns:Value">
<annotation>
<documentation> The values. They must all be the same type of {@code Value} and not contain duplicates. </documentation>
</annotation>
</element>
</sequence>
</extension>
</complexContent>
</complexType>
<complexType name="SoapRequestHeader">
<annotation>
<documentation> Represents the SOAP request header used by API requests. </documentation>
</annotation>
<sequence>
<element maxOccurs="1" minOccurs="0" name="networkCode" type="xsd:string">
<annotation>
<documentation> The network code to use in the context of a request. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="applicationName" type="xsd:string">
<annotation>
<documentation> The name of client library application. </documentation>
</annotation>
</element>
</sequence>
</complexType>
<complexType name="SoapResponseHeader">
<annotation>
<documentation> Represents the SOAP request header used by API responses. </documentation>
</annotation>
<sequence>
<element maxOccurs="1" minOccurs="0" name="requestId" type="xsd:string"/>
<element maxOccurs="1" minOccurs="0" name="responseTime" type="xsd:long"/>
</sequence>
</complexType>
<complexType name="Statement">
<annotation>
<documentation> Captures the {@code WHERE}, {@code ORDER BY} and {@code LIMIT} clauses of a PQL query. Statements are typically used to retrieve objects of a predefined domain type, which makes SELECT clause unnecessary. <p> An example query text might be {@code "WHERE status = 'ACTIVE' ORDER BY id LIMIT 30"}. </p> <p> Statements support bind variables. These are substitutes for literals and can be thought of as input parameters to a PQL query. </p> <p> An example of such a query might be {@code "WHERE id = :idValue"}. </p> <p> Statements also support use of the LIKE keyword. This provides wildcard string matching. </p> <p> An example of such a query might be {@code "WHERE name LIKE '%searchString%'"}. </p> The value for the variable idValue must then be set with an object of type {@link Value}, e.g., {@link NumberValue}, {@link TextValue} or {@link BooleanValue}. </documentation>
</annotation>
<sequence>
<element maxOccurs="1" minOccurs="0" name="query" type="xsd:string">
<annotation>
<documentation> Holds the query in PQL syntax. The syntax is:<br> <code>[WHERE <condition> {[AND | OR] <condition> ...}]</code><br> <code>[ORDER BY <property> [ASC | DESC]]</code><br> <code>[LIMIT {[<offset>,] <count>} | {<count> OFFSET <offset>}]</code><br> <p> <code><condition></code><br> &nbsp;&nbsp;&nbsp;&nbsp; <code>:= <property> {< | <= | > | >= | = | != } <value></code><br> <code><condition></code><br> &nbsp;&nbsp;&nbsp;&nbsp; <code>:= <property> {< | <= | > | >= | = | != } <bind variable></code><br> <code><condition> := <property> IN <list></code><br> <code><condition> := <property> IS NULL</code><br> <code><condition> := <property> LIKE <wildcard%match></code><br> <code><bind variable> := :<name></code><br> </p> </documentation>
</annotation>
</element>
<element maxOccurs="unbounded" minOccurs="0" name="values" type="tns:String_ValueMapEntry">
<annotation>
<documentation> Holds keys and values for bind variables and their values. The key is the name of the bind variable. The value is the literal value of the variable. <p> In the example {@code "WHERE status = :bindStatus ORDER BY id LIMIT 30"}, the bind variable, represented by {@code :bindStatus} is named {@code bindStatus}, which would also be the parameter map key. The bind variable's value would be represented by a parameter map value of type {@link TextValue}. The final result, for example, would be an entry of {@code "bindStatus" => StringParam("ACTIVE")}. </p> </documentation>
</annotation>
</element>
</sequence>
</complexType>
<complexType name="StatementError">
<annotation>
<documentation> An error that occurs while parsing {@link Statement} objects. </documentation>
</annotation>
<complexContent>
<extension base="tns:ApiError">
<sequence>
<element maxOccurs="1" minOccurs="0" name="reason" type="tns:StatementError.Reason">
<annotation>
<documentation> The error reason represented by an enum. </documentation>
</annotation>
</element>
</sequence>
</extension>
</complexContent>
</complexType>
<complexType name="StringFormatError">
<annotation>
<documentation> A list of error code for reporting invalid content of input strings. </documentation>
</annotation>
<complexContent>
<extension base="tns:ApiError">
<sequence>
<element maxOccurs="1" minOccurs="0" name="reason" type="tns:StringFormatError.Reason"/>
</sequence>
</extension>
</complexContent>
</complexType>
<complexType name="StringLengthError">
<annotation>
<documentation> Errors for Strings which do not meet given length constraints. </documentation>
</annotation>
<complexContent>
<extension base="tns:ApiError">
<sequence>
<element maxOccurs="1" minOccurs="0" name="reason" type="tns:StringLengthError.Reason"/>
</sequence>
</extension>
</complexContent>
</complexType>
<complexType name="String_ValueMapEntry">
<annotation>
<documentation> This represents an entry in a map with a key of type String and value of type Value. </documentation>
</annotation>
<sequence>
<element maxOccurs="1" minOccurs="0" name="key" type="xsd:string"/>
<element maxOccurs="1" minOccurs="0" name="value" type="tns:Value"/>
</sequence>
</complexType>
<complexType name="SubmitOrdersForApproval">
<annotation>
<documentation> The action used for submitting {@link Order} objects for approval. </documentation>
</annotation>
<complexContent>
<extension base="tns:OrderAction">
<sequence>
<element maxOccurs="1" minOccurs="0" name="skipInventoryCheck" type="xsd:boolean">
<annotation>
<documentation> Indicates whether the inventory check should be skipped when performing this action. The default value is false. </documentation>
</annotation>
</element>
</sequence>
</extension>
</complexContent>
</complexType>
<complexType name="SubmitOrdersForApprovalAndOverbook">
<annotation>
<documentation> The action used for submitting and overbooking {@link Order} objects for approval. </documentation>
</annotation>
<complexContent>
<extension base="tns:SubmitOrdersForApproval">
<sequence/>
</extension>
</complexContent>
</complexType>
<complexType name="SubmitOrdersForApprovalWithoutReservationChanges">
<annotation>
<documentation> The action used for submitting {@link Order} objects for approval. This action does not make any changes to the {@link LineItem#reservationStatus} of the line items within the order. </documentation>
</annotation>
<complexContent>
<extension base="tns:OrderAction">
<sequence/>
</extension>
</complexContent>
</complexType>
<complexType name="TeamError">
<annotation>
<documentation> Errors related to a Team. </documentation>
</annotation>
<complexContent>
<extension base="tns:ApiError">
<sequence>
<element maxOccurs="1" minOccurs="0" name="reason" type="tns:TeamError.Reason">
<annotation>
<documentation> The error reason represented by an enum. </documentation>
</annotation>
</element>
</sequence>
</extension>
</complexContent>
</complexType>
<complexType name="TechnologyTargetingError">
<annotation>
<documentation> Technology targeting validation errors. </documentation>
</annotation>
<complexContent>
<extension base="tns:ApiError">
<sequence>
<element maxOccurs="1" minOccurs="0" name="reason" type="tns:TechnologyTargetingError.Reason"/>
</sequence>
</extension>
</complexContent>
</complexType>
<complexType name="TemplateInstantiatedCreativeError">
<annotation>
<documentation> Lists all errors associated with template instantiated creatives. </documentation>
</annotation>
<complexContent>
<extension base="tns:ApiError">
<sequence>
<element maxOccurs="1" minOccurs="0" name="reason" type="tns:TemplateInstantiatedCreativeError.Reason">
<annotation>
<documentation> The error reason represented by an enum. </documentation>
</annotation>
</element>
</sequence>
</extension>
</complexContent>
</complexType>
<complexType name="TextValue">
<annotation>
<documentation> Contains a string value. </documentation>
</annotation>
<complexContent>
<extension base="tns:Value">
<sequence>
<element maxOccurs="1" minOccurs="0" name="value" type="xsd:string">
<annotation>
<documentation> The string value. </documentation>
</annotation>
</element>
</sequence>
</extension>
</complexContent>
</complexType>
<complexType name="TimeZoneError">
<annotation>
<documentation> Errors related to timezones. </documentation>
</annotation>
<complexContent>
<extension base="tns:ApiError">
<sequence>
<element maxOccurs="1" minOccurs="0" name="reason" type="tns:TimeZoneError.Reason"/>
</sequence>
</extension>
</complexContent>
</complexType>
<complexType name="TranscodingError">
<annotation>
<documentation> Errors associated with the video and audio transcoding flow. </documentation>
</annotation>
<complexContent>
<extension base="tns:ApiError">
<sequence>
<element maxOccurs="1" minOccurs="0" name="reason" type="tns:TranscodingError.Reason"/>
</sequence>
</extension>
</complexContent>
</complexType>
<complexType name="TypeError">
<annotation>
<documentation> An error for a field which is an invalid type. </documentation>
</annotation>
<complexContent>
<extension base="tns:ApiError">
<sequence/>
</extension>
</complexContent>
</complexType>
<complexType name="UnarchiveOrders">
<annotation>
<documentation> The action used for unarchiving {@link Order} objects. </documentation>
</annotation>
<complexContent>
<extension base="tns:OrderAction">
<sequence/>
</extension>
</complexContent>
</complexType>
<complexType name="UniqueError">
<annotation>
<documentation> An error for a field which must satisfy a uniqueness constraint </documentation>
</annotation>
<complexContent>
<extension base="tns:ApiError">
<sequence/>
</extension>
</complexContent>
</complexType>
<complexType name="UpdateResult">
<annotation>
<documentation> Represents the result of performing an action on objects. </documentation>
</annotation>
<sequence>
<element maxOccurs="1" minOccurs="0" name="numChanges" type="xsd:int">
<annotation>
<documentation> The number of objects that were changed as a result of performing the action. </documentation>
</annotation>
</element>
</sequence>
</complexType>
<complexType name="UserDomainTargetingError">
<annotation>
<documentation> Lists all errors related to user domain targeting for a line item. </documentation>
</annotation>
<complexContent>
<extension base="tns:ApiError">
<sequence>
<element maxOccurs="1" minOccurs="0" name="reason" type="tns:UserDomainTargetingError.Reason"/>
</sequence>
</extension>
</complexContent>
</complexType>
<complexType abstract="true" name="Value">
<annotation>
<documentation> {@code Value} represents a value. </documentation>
</annotation>
<sequence/>
</complexType>
<complexType name="VideoPositionTargetingError">
<annotation>
<documentation> Lists all errors related to {@link VideoPositionTargeting}. </documentation>
</annotation>
<complexContent>
<extension base="tns:ApiError">
<sequence>
<element maxOccurs="1" minOccurs="0" name="reason" type="tns:VideoPositionTargetingError.Reason"/>
</sequence>
</extension>
</complexContent>
</complexType>
<simpleType name="ApiVersionError.Reason">
<restriction base="xsd:string">
<enumeration value="UPDATE_TO_NEWER_VERSION">
<annotation>
<documentation> Indicates that the operation is not allowed in the version the request was made in. </documentation>
</annotation>
</enumeration>
<enumeration value="UNKNOWN">
<annotation>
<documentation> The value returned if the actual value is not exposed by the requested API version. </documentation>
</annotation>
</enumeration>
</restriction>
</simpleType>
<simpleType name="AssetError.Reason">
<annotation>
<documentation> The reasons for the target error. </documentation>
</annotation>
<restriction base="xsd:string">
<enumeration value="NON_UNIQUE_NAME">
<annotation>
<documentation> An asset name must be unique across advertiser. </documentation>
</annotation>
</enumeration>
<enumeration value="FILE_NAME_TOO_LONG">
<annotation>
<documentation> The file name is too long. </documentation>
</annotation>
</enumeration>
<enumeration value="FILE_SIZE_TOO_LARGE">
<annotation>
<documentation> The file size is too large. </documentation>
</annotation>
</enumeration>
<enumeration value="MISSING_REQUIRED_DYNAMIC_ALLOCATION_CLIENT">
<annotation>
<documentation> Required client code is not present in the code snippet. </documentation>
</annotation>
</enumeration>
<enumeration value="MISSING_REQUIRED_DYNAMIC_ALLOCATION_HEIGHT">
<annotation>
<documentation> Required height is not present in the code snippet. </documentation>
</annotation>
</enumeration>
<enumeration value="MISSING_REQUIRED_DYNAMIC_ALLOCATION_WIDTH">
<annotation>
<documentation> Required width is not present in the code snippet. </documentation>
</annotation>
</enumeration>
<enumeration value="MISSING_REQUIRED_DYNAMIC_ALLOCATION_FORMAT">
<annotation>
<documentation> Required format is not present in the mobile code snippet. </documentation>
</annotation>
</enumeration>
<enumeration value="INVALID_CODE_SNIPPET_PARAMETER_VALUE">
<annotation>
<documentation> The parameter value in the code snippet is invalid. </documentation>
</annotation>
</enumeration>
<enumeration value="INVALID_ASSET_ID">
<annotation>
<documentation> Invalid asset Id. </documentation>
</annotation>
</enumeration>
<enumeration value="UNKNOWN">
<annotation>
<documentation> The value returned if the actual value is not exposed by the requested API version. </documentation>
</annotation>
</enumeration>
</restriction>
</simpleType>
<simpleType name="AudienceExtensionError.Reason">
<annotation>
<documentation> Specific audience extension error reasons. </documentation>
</annotation>
<restriction base="xsd:string">
<enumeration value="FREQUENCY_CAPS_NOT_SUPPORTED">
<annotation>
<documentation> Frequency caps are not supported by audience extension line items </documentation>
</annotation>
</enumeration>
<enumeration value="INVALID_TARGETING">
<annotation>
<documentation> Audience extension line items can only target geography </documentation>
</annotation>
</enumeration>
<enumeration value="INVENTORY_UNIT_TARGETING_INVALID">
<annotation>
<documentation> Audience extension line items can only target audience extension inventory units </documentation>
</annotation>
</enumeration>
<enumeration value="INVALID_CREATIVE_ROTATION">
<annotation>
<documentation> Audience extension line items do not support {@link CreativeRotationType#SEQUENTIAL}. </documentation>
</annotation>
</enumeration>
<enumeration value="INVALID_EXTERNAL_ENTITY_ID">
<annotation>
<documentation> The given ID of the external entity is not valid </documentation>
</annotation>
</enumeration>
<enumeration value="INVALID_LINE_ITEM_TYPE">
<annotation>
<documentation> Audience extension line items only support {@link LineItemType#STANDARD}. </documentation>
</annotation>
</enumeration>
<enumeration value="INVALID_MAX_BID">
<annotation>
<documentation> Audience extension max bid is invalid when it is greater then the max budget. </documentation>
</annotation>
</enumeration>
<enumeration value="AUDIENCE_EXTENSION_BULK_UPDATE_NOT_ALLOWED">
<annotation>
<documentation> Bulk update for audience extension line items is not allowed. </documentation>
</annotation>
</enumeration>
<enumeration value="UNEXPECTED_AUDIENCE_EXTENSION_ERROR">
<annotation>
<documentation> An unexpected error occurred. </documentation>
</annotation>
</enumeration>
<enumeration value="MAX_DAILY_BUDGET_AMOUNT_EXCEEDED">
<annotation>
<documentation> The value entered for the maximum daily budget on an audience extension line item exceeds the maximum allowed. </documentation>
</annotation>
</enumeration>
<enumeration value="EXTERNAL_CAMPAIGN_ALREADY_EXISTS">
<annotation>
<documentation> Creating a campaign for a line item that already has an associated campaign is not allowed. </documentation>
</annotation>
</enumeration>
<enumeration value="AUDIENCE_EXTENSION_WITHOUT_FEATURE">
<annotation>
<documentation> Audience extension was specified on a line item but the feature was not enabled. </documentation>
</annotation>
</enumeration>
<enumeration value="AUDIENCE_EXTENSION_WITHOUT_LINKED_ACCOUNT">
<annotation>
<documentation> Audience extension was specified on a line item but no audience extension account has been linked. </documentation>
</annotation>
</enumeration>
<enumeration value="CANNOT_OVERRIDE_CREATIVE_SIZE_WITH_AUDIENCE_EXTENSION">
<annotation>
<documentation> Assocation creative size overrides are not allowed with audience extension. </documentation>
</annotation>
</enumeration>
<enumeration value="CANNOT_OVERRIDE_FIELD_WITH_AUDIENCE_EXTENSION">
<annotation>
<documentation> Some association overrides are not allowed with audience extension. </documentation>
</annotation>
</enumeration>
<enumeration value="ONLY_ONE_CREATIVE_PLACEHOLDER_ALLOWED">
<annotation>
<documentation> Only one creative placeholder is allowed for an audience extension line item. </documentation>
</annotation>
</enumeration>
<enumeration value="MULTIPLE_AUDIENCE_EXTENSION_LINE_ITEMS_ON_ORDER">
<annotation>
<documentation> Only one audience extension line item can be associated with a given order. </documentation>
</annotation>
</enumeration>
<enumeration value="CANNOT_COPY_AUDIENCE_EXTENSION_LINE_ITEMS_AND_CREATIVES_TOGETHER">
<annotation>
<documentation> Audience extension line items must be copied separately from their associated creatives. </documentation>
</annotation>
</enumeration>
<enumeration value="FEATURE_DEPRECATED">
<annotation>
<documentation> Audience extension is no longer supported and cannot be used. </documentation>
</annotation>
</enumeration>
<enumeration value="UNKNOWN">
<annotation>
<documentation> The value returned if the actual value is not exposed by the requested API version. </documentation>
</annotation>
</enumeration>
</restriction>
</simpleType>
<simpleType name="AuthenticationError.Reason">
<restriction base="xsd:string">
<enumeration value="AMBIGUOUS_SOAP_REQUEST_HEADER">
<annotation>
<documentation> The SOAP message contains a request header with an ambiguous definition of the authentication header fields. This means either the {@code authToken} and {@code oAuthToken} fields were both null or both were specified. Exactly one value should be specified with each request. </documentation>
</annotation>
</enumeration>
<enumeration value="INVALID_EMAIL">
<annotation>
<documentation> The login provided is invalid. </documentation>
</annotation>
</enumeration>
<enumeration value="AUTHENTICATION_FAILED">
<annotation>
<documentation> Tried to authenticate with provided information, but failed. </documentation>
</annotation>
</enumeration>
<enumeration value="INVALID_OAUTH_SIGNATURE">
<annotation>
<documentation> The OAuth provided is invalid. </documentation>
</annotation>
</enumeration>
<enumeration value="INVALID_SERVICE">
<annotation>
<documentation> The specified service to use was not recognized. </documentation>
</annotation>
</enumeration>
<enumeration value="MISSING_SOAP_REQUEST_HEADER">
<annotation>
<documentation> The SOAP message is missing a request header with an {@code authToken} and optional {@code networkCode}. </documentation>
</annotation>
</enumeration>
<enumeration value="MISSING_AUTHENTICATION_HTTP_HEADER">
<annotation>
<documentation> The HTTP request is missing a request header with an {@code authToken} </documentation>
</annotation>
</enumeration>
<enumeration value="MISSING_AUTHENTICATION">
<annotation>
<documentation> The request is missing an {@code authToken} </documentation>
</annotation>
</enumeration>
<enumeration value="NETWORK_API_ACCESS_DISABLED">
<annotation>
<documentation> The network does not have API access enabled. </documentation>
</annotation>
</enumeration>
<enumeration value="NO_NETWORKS_TO_ACCESS">
<annotation>
<documentation> The user is not associated with any network. </documentation>
</annotation>
</enumeration>
<enumeration value="NETWORK_NOT_FOUND">
<annotation>
<documentation> No network for the given {@code networkCode} was found. </documentation>
</annotation>
</enumeration>
<enumeration value="NETWORK_CODE_REQUIRED">
<annotation>
<documentation> The user has access to more than one network, but did not provide a {@code networkCode}. </documentation>
</annotation>
</enumeration>
<enumeration value="CONNECTION_ERROR">
<annotation>
<documentation> An error happened on the server side during connection to authentication service. </documentation>
</annotation>
</enumeration>
<enumeration value="GOOGLE_ACCOUNT_ALREADY_ASSOCIATED_WITH_NETWORK">
<annotation>
<documentation> The user tried to create a test network using an account that already is associated with a network. </documentation>
</annotation>
</enumeration>
<enumeration value="UNDER_INVESTIGATION">
<annotation>
<documentation> The account is blocked and under investigation by the collections team. Please contact Google for more information. </documentation>
</annotation>
</enumeration>
<enumeration value="UNKNOWN">
<annotation>
<documentation> The value returned if the actual value is not exposed by the requested API version. </documentation>
</annotation>
</enumeration>
</restriction>
</simpleType>
<simpleType name="ClickTrackingLineItemError.Reason">
<annotation>
<documentation> The reasons for the target error. </documentation>
</annotation>
<restriction base="xsd:string">
<enumeration value="TYPE_IMMUTABLE">
<annotation>
<documentation> The line item type cannot be changed once created. </documentation>
</annotation>
</enumeration>
<enumeration value="INVALID_TARGETING_TYPE">
<annotation>
<documentation> Click tracking line items can only be targeted at ad unit inventory, all other types are invalid, as well as placements. </documentation>
</annotation>
</enumeration>
<enumeration value="INVALID_ROADBLOCKING_TYPE">
<annotation>
<documentation> Click tracking line items do not allow us to control creative delivery so are by nature one or more as entered by the third party. </documentation>
</annotation>
</enumeration>
<enumeration value="INVALID_CREATIVEROTATION_TYPE">
<annotation>
<documentation> Click tracking line items do not support the {@link CreativeRotationType#OPTIMIZED} creative rotation type. </documentation>
</annotation>
</enumeration>
<enumeration value="INVALID_DELIVERY_RATE_TYPE">
<annotation>
<documentation> Click tracking line items do not allow us to control line item delivery so we can not control the rate at which they are served. </documentation>
</annotation>
</enumeration>
<enumeration value="UNSUPPORTED_FIELD">
<annotation>
<documentation> Not all fields are supported by the click tracking line items. </documentation>
</annotation>
</enumeration>
<enumeration value="UNKNOWN">
<annotation>
<documentation> The value returned if the actual value is not exposed by the requested API version. </documentation>
</annotation>
</enumeration>
</restriction>
</simpleType>
<simpleType name="CollectionSizeError.Reason">
<restriction base="xsd:string">
<enumeration value="TOO_LARGE"/>
<enumeration value="UNKNOWN">
<annotation>
<documentation> The value returned if the actual value is not exposed by the requested API version. </documentation>
</annotation>
</enumeration>
</restriction>
</simpleType>
<simpleType name="CommonError.Reason">
<annotation>
<documentation> Describes reasons for common errors </documentation>
</annotation>
<restriction base="xsd:string">
<enumeration value="NOT_FOUND">
<annotation>
<documentation> Indicates that an attempt was made to retrieve an entity that does not exist. </documentation>
</annotation>
</enumeration>
<enumeration value="ALREADY_EXISTS">
<annotation>
<documentation> Indicates that an attempt was made to create an entity that already exists. </documentation>
</annotation>
</enumeration>
<enumeration value="NOT_APPLICABLE">
<annotation>
<documentation> Indicates that a value is not applicable for given use case. </documentation>
</annotation>
</enumeration>
<enumeration value="DUPLICATE_OBJECT">
<annotation>
<documentation> Indicates that two elements in the collection were identical. </documentation>
</annotation>
</enumeration>
<enumeration value="CANNOT_UPDATE">
<annotation>
<documentation> Indicates that an attempt was made to change an immutable field. </documentation>
</annotation>
</enumeration>
<enumeration value="UNSUPPORTED_OPERATION">
<annotation>
<documentation> Indicates that the requested operation is not supported. </documentation>
</annotation>
</enumeration>
<enumeration value="CONCURRENT_MODIFICATION">
<annotation>
<documentation> Indicates that another request attempted to update the same data in the same network at about the same time. Please wait and try the request again. </documentation>
</annotation>
</enumeration>
<enumeration value="UNKNOWN">
<annotation>
<documentation> The value returned if the actual value is not exposed by the requested API version. </documentation>
</annotation>
</enumeration>
</restriction>
</simpleType>
<simpleType name="CompanyCreditStatusError.Reason">
<annotation>
<documentation> The reasons for the target error. </documentation>
</annotation>
<restriction base="xsd:string">
<enumeration value="COMPANY_CREDIT_STATUS_CHANGE_NOT_ALLOWED">
<annotation>
<documentation> The user's role does not have permission to change {@link Company#creditStatus} from the default value. The default value is {@link Company.CreditStatus#ACTIVE} for the Basic credit status setting and {@link Company.CreditStatus#ON_HOLD} for the Advanced credit status setting. </documentation>
</annotation>
</enumeration>
<enumeration value="CANNOT_USE_CREDIT_STATUS_SETTING">
<annotation>
<documentation> The network has not been enabled for editing credit status settings for companies. </documentation>
</annotation>
</enumeration>
<enumeration value="CANNOT_USE_ADVANCED_CREDIT_STATUS_SETTING">
<annotation>
<documentation> The network has not been enabled for the Advanced credit status settings for companies. {@link Company#creditStatus} must be either {@code ACTIVE} or {@code INACTIVE}. </documentation>
</annotation>
</enumeration>
<enumeration value="UNACCEPTABLE_COMPANY_CREDIT_STATUS_FOR_ORDER">
<annotation>
<documentation> An order cannot be created or updated because the {@link Order#advertiserId} or the {@link Order#agencyId} it is associated with has {@link Company#creditStatus} that is not {@code ACTIVE} or {@code ON_HOLD}. </documentation>
</annotation>
</enumeration>
<enumeration value="UNACCEPTABLE_COMPANY_CREDIT_STATUS_FOR_LINE_ITEM">
<annotation>
<documentation> A line item cannot be created for the order because the {@link Order#advertiserId} or {Order#agencyId} it is associated with has {@link Company#creditStatus} that is not {@code ACTIVE} or {@code ON_HOLD}. </documentation>
</annotation>
</enumeration>
<enumeration value="CANNOT_BLOCK_COMPANY_TOO_MANY_APPROVED_ORDERS">
<annotation>
<documentation> The company cannot be blocked because there are more than 200 approved orders of the company. Archive some, so that there are less than 200 of them. </documentation>
</annotation>
</enumeration>
<enumeration value="UNKNOWN">
<annotation>
<documentation> The value returned if the actual value is not exposed by the requested API version. </documentation>
</annotation>
</enumeration>
</restriction>
</simpleType>
<simpleType name="CreativeError.Reason">
<annotation>
<documentation> The reasons for the target error. </documentation>
</annotation>
<restriction base="xsd:string">
<enumeration value="FLASH_AND_FALLBACK_URL_ARE_SAME">
<annotation>
<documentation> {@link FlashRedirectCreative#flashUrl} and {@link FlashRedirectCreative#fallbackUrl} are the same. The fallback URL is used when the flash URL does not work and must be different from it. </documentation>
</annotation>
</enumeration>
<enumeration value="INVALID_INTERNAL_REDIRECT_URL">
<annotation>
<documentation> The internal redirect URL was invalid. The URL must have the following syntax http://ad.doubleclick.net/ad/sitename/;sz=size. </documentation>
</annotation>
</enumeration>
<enumeration value="DESTINATION_URL_REQUIRED">
<annotation>
<documentation> {@link HasDestinationUrlCreative#destinationUrl} is required. </documentation>
</annotation>
</enumeration>
<enumeration value="DESTINATION_URL_NOT_EMPTY">
<annotation>
<documentation> {@link HasDestinationUrlCreative#destinationUrl} must be empty when its type is {@link DestinationUrlType#NONE}. </documentation>
</annotation>
</enumeration>
<enumeration value="DESTINATION_URL_TYPE_NOT_SUPPORTED">
<annotation>
<documentation> The provided {@link DestinationUrlType} is not supported for the creative type it is being used on. </documentation>
</annotation>
</enumeration>
<enumeration value="CANNOT_CREATE_OR_UPDATE_LEGACY_DFP_CREATIVE">
<annotation>
<documentation> Cannot create or update legacy DART For Publishers creative. </documentation>
</annotation>
</enumeration>
<enumeration value="CANNOT_CREATE_OR_UPDATE_LEGACY_DFP_MOBILE_CREATIVE">
<annotation>
<documentation> Cannot create or update legacy mobile creative. </documentation>
</annotation>
</enumeration>
<enumeration value="MISSING_FEATURE">
<annotation>
<documentation> The user is missing a necessary feature. </documentation>
</annotation>
</enumeration>
<enumeration value="INVALID_COMPANY_TYPE">
<annotation>
<documentation> Company type should be one of Advertisers, House Advertisers and Ad Networks. </documentation>
</annotation>
</enumeration>
<enumeration value="INVALID_ADSENSE_CREATIVE_SIZE">
<annotation>
<documentation> Invalid size for AdSense dynamic allocation creative. Only valid AFC sizes are allowed. </documentation>
</annotation>
</enumeration>
<enumeration value="INVALID_AD_EXCHANGE_CREATIVE_SIZE">
<annotation>
<documentation> Invalid size for Ad Exchange dynamic allocation creative. Only valid Ad Exchange sizes are allowed. </documentation>
</annotation>
</enumeration>
<enumeration value="DUPLICATE_ASSET_IN_CREATIVE">
<annotation>
<documentation> Assets associated with the same creative must be unique. </documentation>
</annotation>
</enumeration>
<enumeration value="CREATIVE_ASSET_CANNOT_HAVE_ID_AND_BYTE_ARRAY">
<annotation>
<documentation> A creative asset cannot contain an asset ID and a byte array. </documentation>
</annotation>
</enumeration>
<enumeration value="CANNOT_CREATE_OR_UPDATE_UNSUPPORTED_CREATIVE">
<annotation>
<documentation> Cannot create or update unsupported creative. </documentation>
</annotation>
</enumeration>
<enumeration value="CANNOT_CREATE_PROGRAMMATIC_CREATIVES">
<annotation>
<documentation> Cannot create programmatic creatives. </documentation>
</annotation>
</enumeration>
<enumeration value="INVALID_SIZE_FOR_THIRD_PARTY_IMPRESSION_TRACKER">
<annotation>
<documentation> A creative must have valid size to use the third-party impression tracker. </documentation>
</annotation>
</enumeration>
<enumeration value="CANNOT_DEACTIVATE_CREATIVES_IN_CREATIVE_SETS">
<annotation>
<documentation> Ineligible creatives can not be deactivated. </documentation>
</annotation>
</enumeration>
<enumeration value="HOSTED_VIDEO_CREATIVE_REQUIRES_VIDEO_ASSET">
<annotation>
<documentation> Ad Manager hosted video creatives must contain a video asset. </documentation>
</annotation>
</enumeration>
<enumeration value="CANNOT_SET_MULTIPLE_IMPRESSION_TRACKING_URLS">
<annotation>
<documentation> {@link ImageCreative#thirdPartyImpressionTrackingUrls} should not contain more than one url. </documentation>
</annotation>
</enumeration>
<enumeration value="UNKNOWN">
<annotation>
<documentation> The value returned if the actual value is not exposed by the requested API version. </documentation>
</annotation>
</enumeration>
</restriction>
</simpleType>
<simpleType name="CrossSellError.Reason">
<annotation>
<documentation> The reason of the error. </documentation>
</annotation>
<restriction base="xsd:string">
<enumeration value="COMPANY_IS_NOT_DISTRIBUTION_PARTNER">
<annotation>
<documentation> A company for cross-sell partner must be of type {@link Company.Type#PARTNER}. </documentation>
</annotation>
</enumeration>
<enumeration value="CHANGING_PARTNER_NETWORK_IS_NOT_SUPPORTED">
<annotation>
<documentation> The network code of a cross-sell partner cannot be changed. </documentation>
</annotation>
</enumeration>
<enumeration value="MISSING_DISTRIBUTOR_PARTNER_NAME">
<annotation>
<documentation> A cross-sell partner must have a partner name. </documentation>
</annotation>
</enumeration>
<enumeration value="DISTRIBUTOR_NETWORK_MISSING_PUBLISHER_FEATURE">
<annotation>
<documentation> The cross-sell distributor publisher feature must be enabled. </documentation>
</annotation>
</enumeration>
<enumeration value="CONTENT_PROVIDER_NETWORK_MISSING_PUBLISHER_FEATURE">
<annotation>
<documentation> The cross-sell publisher features must be enabled on the partner's network. </documentation>
</annotation>
</enumeration>
<enumeration value="INVALID_DISTRIBUTOR_PARTNER_NAME">
<annotation>
<documentation> The cross-sell partner name conflicts with an ad unit name on the partner's network. </documentation>
</annotation>
</enumeration>
<enumeration value="INVALID_CONTENT_PROVIDER_NETWORK">
<annotation>
<documentation> The network code of a cross-sell partner is invalid. </documentation>
</annotation>
</enumeration>
<enumeration value="CONTENT_PROVIDER_NETWORK_CANNOT_BE_ACTIVE_NETWORK">
<annotation>
<documentation> The content provider network must be different than the distributor network. </documentation>
</annotation>
</enumeration>
<enumeration value="CONTENT_PROVIDER_NETWORK_ALREADY_ENABLED_FOR_CROSS_SELLING">
<annotation>
<documentation> The same network code was already enabled for cross-sell in a different company. </documentation>
</annotation>
</enumeration>
<enumeration value="DISTRIBUTOR_RULE_VIOLATION_ERROR">
<annotation>
<documentation> A rule defined by the cross selling distributor has been violated by a line item targeting a shared ad unit. Violating this rule is an error. </documentation>
</annotation>
</enumeration>
<enumeration value="DISTRIBUTOR_RULE_VIOLATION_WARNING">
<annotation>
<documentation> A rule defined by the cross selling distributor has been violated by a line item targeting a shared ad unit. Violating this rule is a warning. <p>By setting {@link LineItem#skipCrossSellingRuleWarningChecks}, the content partner can suppress the warning (and create or save the line item). <p>This flag is available beginning in V201411. </documentation>
</annotation>
</enumeration>
<enumeration value="UNKNOWN">
<annotation>
<documentation> The value returned if the actual value is not exposed by the requested API version. </documentation>
</annotation>
</enumeration>
</restriction>
</simpleType>
<simpleType name="CurrencyCodeError.Reason">
<annotation>
<documentation> The reason behind the currency code error. </documentation>
</annotation>
<restriction base="xsd:string">
<enumeration value="INVALID">
<annotation>
<documentation> The currency code is invalid and does not follow ISO 4217. </documentation>
</annotation>
</enumeration>
<enumeration value="UNSUPPORTED">
<annotation>
<documentation> The currency code is valid, but is not supported. </documentation>
</annotation>
</enumeration>
<enumeration value="DEPRECATED_CURRENCY_USED">
<annotation>
<documentation> The currency has been used for entity creation after its deprecation </documentation>
</annotation>
</enumeration>
</restriction>
</simpleType>
<simpleType name="CustomFieldValueError.Reason">
<annotation>
<documentation> The reasons for the target error. </documentation>
</annotation>
<restriction base="xsd:string">
<enumeration value="CUSTOM_FIELD_NOT_FOUND">
<annotation>
<documentation> An attempt was made to modify or create a {@link CustomFieldValue} for a {@link CustomField} that does not exist. </documentation>
</annotation>
</enumeration>
<enumeration value="CUSTOM_FIELD_INACTIVE">
<annotation>
<documentation> An attempt was made to create a new value for a custom field that is inactive. </documentation>
</annotation>
</enumeration>
<enumeration value="CUSTOM_FIELD_OPTION_NOT_FOUND">
<annotation>
<documentation> An attempt was made to modify or create a {@link CustomFieldValue} corresponding to a {@link CustomFieldOption} that could not be found. </documentation>
</annotation>
</enumeration>
<enumeration value="INVALID_ENTITY_TYPE">
<annotation>
<documentation> An attempt was made to modify or create a {@link CustomFieldValue} with an association to an entity of the wrong type for its field. </documentation>
</annotation>
</enumeration>
<enumeration value="UNKNOWN">
<annotation>
<documentation> The value returned if the actual value is not exposed by the requested API version. </documentation>
</annotation>
</enumeration>
</restriction>
</simpleType>
<simpleType name="CustomTargetingError.Reason">
<annotation>
<documentation> The reasons for the target error. </documentation>
</annotation>
<restriction base="xsd:string">
<enumeration value="KEY_NOT_FOUND">
<annotation>
<documentation> Requested {@link CustomTargetingKey} is not found. </documentation>
</annotation>
</enumeration>
<enumeration value="KEY_COUNT_TOO_LARGE">
<annotation>
<documentation> Number of {@link CustomTargetingKey} objects created exceeds the limit allowed for the network. </documentation>
</annotation>
</enumeration>
<enumeration value="KEY_NAME_DUPLICATE">
<annotation>
<documentation> {@link CustomTargetingKey} with the same {@link CustomTargetingKey#name} already exists. </documentation>
</annotation>
</enumeration>
<enumeration value="KEY_NAME_EMPTY">
<annotation>
<documentation> {@link CustomTargetingKey#name} is empty. </documentation>
</annotation>
</enumeration>
<enumeration value="KEY_NAME_INVALID_LENGTH">
<annotation>
<documentation> {@link CustomTargetingKey#name} is too long. </documentation>
</annotation>
</enumeration>
<enumeration value="KEY_NAME_INVALID_CHARS">
<annotation>
<documentation> {@link CustomTargetingKey#name} contains unsupported or reserved characters. </documentation>
</annotation>
</enumeration>
<enumeration value="KEY_NAME_RESERVED">
<annotation>
<documentation> {@link CustomTargetingKey#name} matches one of the reserved custom targeting key names. </documentation>
</annotation>
</enumeration>
<enumeration value="KEY_DISPLAY_NAME_INVALID_LENGTH">
<annotation>
<documentation> {@link CustomTargetingKey#displayName} is too long. </documentation>
</annotation>
</enumeration>
<enumeration value="KEY_STATUS_NOT_ACTIVE">
<annotation>
<documentation> Key is not active. </documentation>
</annotation>
</enumeration>
<enumeration value="VALUE_NOT_FOUND">
<annotation>
<documentation> Requested {@link CustomTargetingValue} is not found. </documentation>
</annotation>
</enumeration>
<enumeration value="GET_VALUES_BY_STATEMENT_MUST_CONTAIN_KEY_ID">
<annotation>
<documentation> The {@code WHERE} clause in the {@link Statement#query} must always contain {@link CustomTargetingValue#customTargetingKeyId} as one of its columns in a way that it is AND'ed with the rest of the query. </documentation>
</annotation>
</enumeration>
<enumeration value="VALUE_COUNT_FOR_KEY_TOO_LARGE">
<annotation>
<documentation> The number of {@link CustomTargetingValue} objects associated with a {@link CustomTargetingKey} exceeds the network limit. This is only applicable for keys of type {@code CustomTargetingKey.Type#PREDEFINED}. </documentation>
</annotation>
</enumeration>
<enumeration value="VALUE_NAME_DUPLICATE">
<annotation>
<documentation> {@link CustomTargetingValue} with the same {@link CustomTargetingValue#name} already exists. </documentation>
</annotation>
</enumeration>
<enumeration value="VALUE_NAME_EMPTY">
<annotation>
<documentation> {@link CustomTargetingValue#name} is empty. </documentation>
</annotation>
</enumeration>
<enumeration value="VALUE_NAME_INVALID_LENGTH">
<annotation>
<documentation> {@link CustomTargetingValue#name} is too long. </documentation>
</annotation>
</enumeration>
<enumeration value="VALUE_NAME_INVALID_CHARS">
<annotation>
<documentation> {@link CustomTargetingValue#name} contains unsupported or reserved characters. </documentation>
</annotation>
</enumeration>
<enumeration value="VALUE_DISPLAY_NAME_INVALID_LENGTH">
<annotation>
<documentation> {@link CustomTargetingValue#displayName} is too long. </documentation>
</annotation>
</enumeration>
<enumeration value="VALUE_MATCH_TYPE_NOT_ALLOWED">
<annotation>
<documentation> Only Ad Manager 360 networks can have {@link CustomTargetingValue#matchType} other than {@link CustomTargetingValue.MatchType#EXACT}. </documentation>
</annotation>
</enumeration>
<enumeration value="VALUE_MATCH_TYPE_NOT_EXACT_FOR_PREDEFINED_KEY">
<annotation>
<documentation> You can only create {@link CustomTargetingValue} objects with match type {@link CustomTargetingValue.MatchType#EXACT} when associating with {@link CustomTargetingKey} objects of type {@link CustomTargetingKey.Type#PREDEFINED} </documentation>
</annotation>
</enumeration>
<enumeration value="SUFFIX_MATCH_TYPE_NOT_ALLOWED">
<annotation>
<documentation> {@link CustomTargetingValue} object cannot have match type of {@link CustomTargetingValue.MatchType#SUFFIX} when adding a {@link CustomTargetingValue} to a line item. </documentation>
</annotation>
</enumeration>
<enumeration value="CONTAINS_MATCH_TYPE_NOT_ALLOWED">
<annotation>
<documentation> {@link CustomTargetingValue} object cannot have match type of {@link CustomTargetingValue.MatchType#CONTAINS} when adding a {@link CustomTargetingValue} to targeting expression of a line item. </documentation>
</annotation>
</enumeration>
<enumeration value="VALUE_STATUS_NOT_ACTIVE">
<annotation>
<documentation> Value is not active. </documentation>
</annotation>
</enumeration>
<enumeration value="KEY_WITH_MISSING_VALUES">
<annotation>
<documentation> The {@link CustomTargetingKey} does not have any {@link CustomTargetingValue} associated with it. </documentation>
</annotation>
</enumeration>
<enumeration value="INVALID_VALUE_FOR_KEY">
<annotation>
<documentation> The {@link CustomTargetingKey} has a {@link CustomTargetingValue} specified for which the value is not a valid child. </documentation>
</annotation>
</enumeration>
<enumeration value="CANNOT_OR_DIFFERENT_KEYS">
<annotation>
<documentation> {@link CustomCriteriaSet.LogicalOperator#OR} operation cannot be applied to values with different keys. </documentation>
</annotation>
</enumeration>
<enumeration value="INVALID_TARGETING_EXPRESSION">
<annotation>
<documentation> Targeting expression is invalid. This can happen if the sequence of operators is wrong, or a node contains invalid number of children. </documentation>
</annotation>
</enumeration>
<enumeration value="DELETED_KEY_CANNOT_BE_USED_FOR_TARGETING">
<annotation>
<documentation> The key has been deleted. {@link CustomCriteria} cannot have deleted keys. </documentation>
</annotation>
</enumeration>
<enumeration value="DELETED_VALUE_CANNOT_BE_USED_FOR_TARGETING">
<annotation>
<documentation> The value has been deleted. {@link CustomCriteria} cannot have deleted values. </documentation>
</annotation>
</enumeration>
<enumeration value="VIDEO_BROWSE_BY_KEY_CANNOT_BE_USED_FOR_CUSTOM_TARGETING">
<annotation>
<documentation> The key is set as the video browse-by key, which cannot be used for custom targeting. </documentation>
</annotation>
</enumeration>
<enumeration value="CANNOT_DELETE_CUSTOM_KEY_USED_IN_CONTENT_METADATA_MAPPING">
<annotation>
<documentation> Only active custom-criteria keys are supported in content metadata mapping. </documentation>
</annotation>
</enumeration>
<enumeration value="CANNOT_DELETE_CUSTOM_VALUE_USED_IN_CONTENT_METADATA_MAPPING">
<annotation>
<documentation> Only active custom-criteria values are supported in content metadata mapping. </documentation>
</annotation>
</enumeration>
<enumeration value="CANNOT_DELETE_CUSTOM_KEY_USED_IN_PARTNER_ASSIGNMENT_TARGETING">
<annotation>
<documentation> Cannot delete a custom criteria key that is targeted by an active partner assignment. </documentation>
</annotation>
</enumeration>
<enumeration value="CANNOT_DELETE_CUSTOM_VALUE_USED_IN_PARTNER_ASSIGNMENT_TARGETING">
<annotation>
<documentation> Cannot delete a custom criteria value that is targeted by an active partner assignment. </documentation>
</annotation>
</enumeration>
<enumeration value="CANNOT_TARGET_AUDIENCE_SEGMENT">
<annotation>
<documentation> {@link AudienceSegment} object cannot be targeted. </documentation>
</annotation>
</enumeration>
<enumeration value="CANNOT_TARGET_THIRD_PARTY_AUDIENCE_SEGMENT">
<annotation>
<documentation> Third party {@link AudienceSegment} cannot be targeted. </documentation>
</annotation>
</enumeration>
<enumeration value="CANNOT_TARGET_INACTIVE_AUDIENCE_SEGMENT">
<annotation>
<documentation> Inactive {@link AudienceSegment} object cannot be targeted. </documentation>
</annotation>
</enumeration>
<enumeration value="INVALID_AUDIENCE_SEGMENTS">
<annotation>
<documentation> Targeted {@link AudienceSegment} object is not valid. </documentation>
</annotation>
</enumeration>
<enumeration value="CANNOT_TARGET_MAPPED_METADATA">
<annotation>
<documentation> Mapped metadata key-values are deprecated and cannot be targeted. </documentation>
</annotation>
</enumeration>
<enumeration value="ONLY_APPROVED_AUDIENCE_SEGMENTS_CAN_BE_TARGETED">
<annotation>
<documentation> Targeted {@link AudienceSegment} objects have not been approved. </documentation>
</annotation>
</enumeration>
<enumeration value="UNKNOWN">
<annotation>
<documentation> The value returned if the actual value is not exposed by the requested API version. </documentation>
</annotation>
</enumeration>
</restriction>
</simpleType>
<simpleType name="DateTimeRangeTargetingError.Reason">
<annotation>
<documentation> {@link ApiErrorReason} enum for date time range targeting error. </documentation>
</annotation>
<restriction base="xsd:string">
<enumeration value="EMPTY_RANGES">
<annotation>
<documentation> No targeted ranges exists. </documentation>
</annotation>
</enumeration>
<enumeration value="NOT_SPONSORSHIP_LINEITEM">
<annotation>
<documentation> Type of lineitem is not sponsorship. </documentation>
</annotation>
</enumeration>
<enumeration value="NOT_SPONSORSHIP_OR_STANDARD_LINEITEM">
<annotation>
<documentation> Type of lineitem is not sponsorship or standard. </documentation>
</annotation>
</enumeration>
<enumeration value="UNSUPPORTED_LINEITEM_RESERVATION_TYPE">
<annotation>
<documentation> Line item must have a reservation type of sponsorship, standard or preferred deal to use date time range targeting. </documentation>
</annotation>
</enumeration>
<enumeration value="PAST_RANGES_CHANGED">
<annotation>
<documentation> Past ranges are changed. </documentation>
</annotation>
</enumeration>
<enumeration value="RANGES_OVERLAP">
<annotation>
<documentation> Targeted date time ranges overlap. </documentation>
</annotation>
</enumeration>
<enumeration value="FIRST_DATE_TIME_DOES_NOT_MATCH_START_TIME">
<annotation>
<documentation> First date time does not match line item's start time. </documentation>
</annotation>
</enumeration>
<enumeration value="LAST_DATE_TIME_DOES_NOT_MATCH_END_TIME">
<annotation>
<documentation> Last date time does not match line item's end time. </documentation>
</annotation>
</enumeration>
<enumeration value="RANGES_OUT_OF_LINEITEM_ACTIVE_PERIOD">
<annotation>
<documentation> Targeted date time ranges fall out the active period of lineitem. </documentation>
</annotation>
</enumeration>
<enumeration value="START_TIME_IS_NOT_START_OF_DAY">
<annotation>
<documentation> Start time of range (except the earliest range) is not at start of day. Start of day is 00:00:00. </documentation>
</annotation>
</enumeration>
<enumeration value="END_TIME_IS_NOT_END_OF_DAY">
<annotation>
<documentation> End time of range (except the latest range) is not at end of day. End of day is 23:59:59. </documentation>
</annotation>
</enumeration>
<enumeration value="START_DATE_TIME_IS_IN_PAST">
<annotation>
<documentation> Start date time of earliest targeted ranges is in past. </documentation>
</annotation>
</enumeration>
<enumeration value="MODIFY_START_DATE_TIME_TO_PAST">
<annotation>
<documentation> Cannot modify the start date time for date time targeting to the past. </documentation>
</annotation>
</enumeration>
<enumeration value="RANGE_END_TIME_BEFORE_START_TIME">
<annotation>
<documentation> The end time of range is before the start time. Could happen when start type is IMMEDIATE or ONE_HOUR_LATER. </documentation>
</annotation>
</enumeration>
<enumeration value="END_DATE_TIME_IS_TOO_LATE">
<annotation>
<documentation> End date time of latest targeted ranges is too late. </documentation>
</annotation>
</enumeration>
<enumeration value="LIMITED_RANGES_IN_UNLIMITED_LINEITEM"/>
<enumeration value="UNKNOWN">
<annotation>
<documentation> The value returned if the actual value is not exposed by the requested API version. </documentation>
</annotation>
</enumeration>
</restriction>
</simpleType>
<simpleType name="DayPartTargetingError.Reason">
<annotation>
<documentation> The reasons for the target error. </documentation>
</annotation>
<restriction base="xsd:string">
<enumeration value="INVALID_HOUR">
<annotation>
<documentation> Hour of day must be between 0 and 24, inclusive. </documentation>
</annotation>
</enumeration>
<enumeration value="INVALID_MINUTE">
<annotation>
<documentation> Minute of hour must be one of 0, 15,30, 45. </documentation>
</annotation>
</enumeration>
<enumeration value="END_TIME_NOT_AFTER_START_TIME">
<annotation>
<documentation> The {@link DayPart#endTime} cannot be after {@link DayPart#startTime}. </documentation>
</annotation>
</enumeration>
<enumeration value="TIME_PERIODS_OVERLAP">
<annotation>
<documentation> Cannot create day-parts that overlap. </documentation>
</annotation>
</enumeration>
<enumeration value="UNKNOWN">
<annotation>
<documentation> The value returned if the actual value is not exposed by the requested API version. </documentation>
</annotation>
</enumeration>
</restriction>
</simpleType>
<simpleType name="EntityChildrenLimitReachedError.Reason">
<annotation>
<documentation> The reasons for the entity children limit reached error. </documentation>
</annotation>
<restriction base="xsd:string">
<enumeration value="LINE_ITEM_LIMIT_FOR_ORDER_REACHED">
<annotation>
<documentation> The number of line items on the order exceeds the max number of line items allowed per order in the network. </documentation>
</annotation>
</enumeration>
<enumeration value="CREATIVE_ASSOCIATION_LIMIT_FOR_LINE_ITEM_REACHED">
<annotation>
<documentation> The number of creatives associated with the line item exceeds the max number of creatives allowed to be associated with a line item in the network. </documentation>
</annotation>
</enumeration>
<enumeration value="AD_UNIT_LIMIT_FOR_PLACEMENT_REACHED">
<annotation>
<documentation> The number of ad units on the placement exceeds the max number of ad units allowed per placement in the network. </documentation>
</annotation>
</enumeration>
<enumeration value="TARGETING_EXPRESSION_LIMIT_FOR_LINE_ITEM_REACHED">
<annotation>
<documentation> The number of targeting expressions on the line item exceeds the max number of targeting expressions allowed per line item in the network. </documentation>
</annotation>
</enumeration>
<enumeration value="TARGETING_EXPRESSION_SIZE_LIMIT_REACHED">
<annotation>
<documentation> The size of a single targeting expression tree exceeds the max size allowed by the network. </documentation>
</annotation>
</enumeration>
<enumeration value="CUSTOM_TARGETING_VALUES_FOR_KEY_LIMIT_REACHED">
<annotation>
<documentation> The number of custom targeting values for the free-form or predefined custom targeting key exceeds the max number allowed. </documentation>
</annotation>
</enumeration>
<enumeration value="TARGETING_EXPRESSION_LIMIT_FOR_CREATIVES_ON_LINE_ITEM_REACHED">
<annotation>
<documentation> The total number of targeting expressions on the creatives for the line item exceeds the max number allowed per line item in the network. </documentation>
</annotation>
</enumeration>
<enumeration value="ATTACHMENT_LIMIT_FOR_PROPOSAL_REACHED">
<annotation>
<documentation> The number of attachments added to the proposal exceeds the max number allowed per proposal in the network. </documentation>
</annotation>
</enumeration>
<enumeration value="PROPOSAL_LINE_ITEM_LIMIT_FOR_PROPOSAL_REACHED">
<annotation>
<documentation> The number of proposal line items on the proposal exceeds the max number allowed per proposal in the network. </documentation>
</annotation>
</enumeration>
<enumeration value="PRODUCT_LIMIT_FOR_PRODUCT_PACKAGE_REACHED">
<annotation>
<documentation> The number of product package items on the product package exceeds the max number allowed per product package in the network. </documentation>
</annotation>
</enumeration>
<enumeration value="PRODUCT_TEMPLATE_AND_PRODUCT_BASE_RATE_LIMIT_FOR_RATE_CARD_REACHED">
<annotation>
<documentation> The number of product template and product base rates on the rate card (including excluded product base rates) exceeds the max number allowed per rate card in the network. </documentation>
</annotation>
</enumeration>
<enumeration value="PRODUCT_PACKAGE_ITEM_BASE_RATE_LIMIT_FOR_RATE_CARD_REACHED">
<annotation>
<documentation> The number of product package item base rates on the rate card exceeds the max number allowed per rate card in the network. </documentation>
</annotation>
</enumeration>
<enumeration value="PREMIUM_LIMIT_FOR_RATE_CARD_REACHED">
<annotation>
<documentation> The number of premiums of the rate card exceeds the max number allowed per rate card in the network. </documentation>
</annotation>
</enumeration>
<enumeration value="AD_UNIT_LIMIT_FOR_AD_EXCLUSION_RULE_TARGETING_REACHED">
<annotation>
<documentation> The number of ad units on {@link AdExclusionRule#inventoryTargeting} exceeds the max number of ad units allowed per ad exclusion rule inventory targeting in the network. </documentation>
</annotation>
</enumeration>
<enumeration value="NATIVE_STYLE_LIMIT_FOR_NATIVE_AD_FORMAT_REACHED">
<annotation>
<documentation> The number of native styles under the native creative template exceeds the max number of native styles allowed per native creative template in the network. </documentation>
</annotation>
</enumeration>
<enumeration value="TARGETING_EXPRESSION_LIMIT_FOR_PRESENTATION_ASSIGNMENT_REACHED">
<annotation>
<documentation> The number of targeting expressions on the native style exceeds the max number of targeting expressions allowed per native style in the network. </documentation>
</annotation>
</enumeration>
<enumeration value="UNKNOWN">
<annotation>
<documentation> The value returned if the actual value is not exposed by the requested API version. </documentation>
</annotation>
</enumeration>
</restriction>
</simpleType>
<simpleType name="EntityLimitReachedError.Reason">
<annotation>
<documentation> The reasons for the entity limit reached error. </documentation>
</annotation>
<restriction base="xsd:string">
<enumeration value="CUSTOM_TARGETING_VALUES_LIMIT_REACHED">
<annotation>
<documentation> The number of custom targeting values exceeds the max number allowed in the network. </documentation>
</annotation>
</enumeration>
<enumeration value="AD_EXCLUSION_RULES_LIMIT_REACHED">
<annotation>
<documentation> The number of ad exclusion rules exceeds the max number allowed in the network. </documentation>
</annotation>
</enumeration>
<enumeration value="FIRST_PARTY_AUDIENCE_SEGMENTS_LIMIT_REACHED">
<annotation>
<documentation> The number of first party audience segments exceeds the max number allowed in the network. </documentation>
</annotation>
</enumeration>
<enumeration value="PLACEMENTS_LIMIT_REACHED">
<annotation>
<documentation> The number of active placements exceeds the max number allowed in the network. </documentation>
</annotation>
</enumeration>
<enumeration value="LINE_ITEMS_LIMIT_REACHED">
<annotation>
<documentation> The number of line items excceeds the max number allowed in the network. </documentation>
</annotation>
</enumeration>
<enumeration value="ACTIVE_LINE_ITEMS_LIMIT_REACHED">
<annotation>
<documentation> The number of active line items exceeds the max number allowed in the network. </documentation>
</annotation>
</enumeration>
<enumeration value="DAI_ENCODING_PROFILES_LIMIT_REACHED">
<annotation>
<documentation> The number of not-archived encoding profiles exceeds the max number allowed in the network. </documentation>
</annotation>
</enumeration>
<enumeration value="TRAFFIC_FORECAST_SEGMENTS_LIMIT_REACHED">
<annotation>
<documentation> The number of traffic forecast segments exceeds the max number allowed in the network. </documentation>
</annotation>
</enumeration>
<enumeration value="FORECAST_ADJUSTMENTS_LIMIT_REACHED">
<annotation>
<documentation> The number of forecast adjustments exceeds the max number allowed in the network. </documentation>
</annotation>
</enumeration>
<enumeration value="ACTIVE_EXPERIMENTS_LIMIT_REACHED">
<annotation>
<documentation> The number of active experiments exceeds the max number allowed in the network. </documentation>
</annotation>
</enumeration>
<enumeration value="SITES_LIMIT_REACHED">
<annotation>
<documentation> The number of sites exceeds the max number allowed in the network. </documentation>
</annotation>
</enumeration>
<enumeration value="UNKNOWN">
<annotation>
<documentation> The value returned if the actual value is not exposed by the requested API version. </documentation>
</annotation>
</enumeration>
</restriction>
</simpleType>
<simpleType name="FeatureError.Reason">
<restriction base="xsd:string">
<enumeration value="MISSING_FEATURE">
<annotation>
<documentation> A feature is being used that is not enabled on the current network. </documentation>
</annotation>
</enumeration>
<enumeration value="UNKNOWN">
<annotation>
<documentation> The value returned if the actual value is not exposed by the requested API version. </documentation>
</annotation>
</enumeration>
</restriction>
</simpleType>
<simpleType name="ForecastError.Reason">
<annotation>
<documentation> Reason why a forecast could not be retrieved. </documentation>
</annotation>
<restriction base="xsd:string">
<enumeration value="SERVER_NOT_AVAILABLE">
<annotation>
<documentation> The forecast could not be retrieved due to a server side connection problem. Please try again soon. </documentation>
</annotation>
</enumeration>
<enumeration value="INTERNAL_ERROR">
<annotation>
<documentation> There was an unexpected internal error. </documentation>
</annotation>
</enumeration>
<enumeration value="NO_FORECAST_YET">
<annotation>
<documentation> The forecast could not be retrieved because there is not enough forecasting data available yet. It may take up to one week before enough data is available. </documentation>
</annotation>
</enumeration>
<enumeration value="NOT_ENOUGH_INVENTORY">
<annotation>
<documentation> There's not enough inventory for the requested reservation. </documentation>
</annotation>
</enumeration>
<enumeration value="SUCCESS">
<annotation>
<documentation> No error from forecast. </documentation>
</annotation>
</enumeration>
<enumeration value="ZERO_LENGTH_RESERVATION">
<annotation>
<documentation> The requested reservation is of zero length. No forecast is returned. </documentation>
</annotation>
</enumeration>
<enumeration value="EXCEEDED_QUOTA">
<annotation>
<documentation> The number of requests made per second is too high and has exceeded the allowable limit. The recommended approach to handle this error is to wait about 5 seconds and then retry the request. Note that this does not guarantee the request will succeed. If it fails again, try increasing the wait time. <p> Another way to mitigate this error is to limit requests to 2 per second. Once again this does not guarantee that every request will succeed, but may help reduce the number of times you receive this error. </p> </documentation>
</annotation>
</enumeration>
<enumeration value="OUTSIDE_AVAILABLE_DATE_RANGE">
<annotation>
<documentation> The request falls outside the date range of the available data. </documentation>
</annotation>
</enumeration>
<enumeration value="UNKNOWN">
<annotation>
<documentation> The value returned if the actual value is not exposed by the requested API version. </documentation>
</annotation>
</enumeration>
</restriction>
</simpleType>
<simpleType name="FrequencyCapError.Reason">
<restriction base="xsd:string">
<enumeration value="IMPRESSION_LIMIT_EXCEEDED"/>
<enumeration value="IMPRESSIONS_TOO_LOW"/>
<enumeration value="RANGE_LIMIT_EXCEEDED"/>
<enumeration value="RANGE_TOO_LOW"/>
<enumeration value="DUPLICATE_TIME_RANGE"/>
<enumeration value="TOO_MANY_FREQUENCY_CAPS"/>
<enumeration value="UNKNOWN">
<annotation>
<documentation> The value returned if the actual value is not exposed by the requested API version. </documentation>
</annotation>
</enumeration>
</restriction>
</simpleType>
<simpleType name="GenericTargetingError.Reason">
<annotation>
<documentation> The reasons for the target error. </documentation>
</annotation>
<restriction base="xsd:string">
<enumeration value="CONFLICTING_INCLUSION_OR_EXCLUSION_OF_SIBLINGS">
<annotation>
<documentation> Both including and excluding sibling criteria is disallowed. </documentation>
</annotation>
</enumeration>
<enumeration value="INCLUDING_DESCENDANTS_OF_EXCLUDED_CRITERIA">
<annotation>
<documentation> Including descendants of excluded criteria is disallowed. </documentation>
</annotation>
</enumeration>
<enumeration value="UNKNOWN">
<annotation>
<documentation> The value returned if the actual value is not exposed by the requested API version. </documentation>
</annotation>
</enumeration>
</restriction>
</simpleType>
<simpleType name="GeoTargetingError.Reason">
<annotation>
<documentation> The reasons for the target error. </documentation>
</annotation>
<restriction base="xsd:string">
<enumeration value="TARGETED_LOCATIONS_NOT_EXCLUDABLE">
<annotation>
<documentation> A location that is targeted cannot also be excluded. </documentation>
</annotation>
</enumeration>
<enumeration value="EXCLUDED_LOCATIONS_CANNOT_HAVE_CHILDREN_TARGETED">
<annotation>
<documentation> Excluded locations cannot have any of their children targeted. </documentation>
</annotation>
</enumeration>
<enumeration value="POSTAL_CODES_CANNOT_BE_EXCLUDED">
<annotation>
<documentation> Postal codes cannot be excluded. </documentation>
</annotation>
</enumeration>
<enumeration value="UNTARGETABLE_LOCATION">
<annotation>
<documentation> Indicates that location targeting is not allowed. </documentation>
</annotation>
</enumeration>
<enumeration value="UNKNOWN">
<annotation>
<documentation> The value returned if the actual value is not exposed by the requested API version. </documentation>
</annotation>
</enumeration>
</restriction>
</simpleType>
<simpleType name="GrpSettingsError.Reason">
<annotation>
<documentation> Reason for GRP settings error. </documentation>
</annotation>
<restriction base="xsd:string">
<enumeration value="INVALID_AGE_RANGE">
<annotation>
<documentation> Age range for GRP audience is not valid. Please see the <a href="https://support.google.com/admanager/answer/6135438">Ad Manager Help Center</a> for more information. </documentation>
</annotation>
</enumeration>
<enumeration value="UNDER_18_MIN_AGE_REQUIRES_ALL_AGES">
<annotation>
<documentation> Age range for GRP audience is not allowed to include ages under 18 unless designating all ages in target(2-65+). </documentation>
</annotation>
</enumeration>
<enumeration value="LINE_ITEM_ENVIRONMENT_TYPE_NOT_SUPPORTED">
<annotation>
<documentation> GRP settings are only supported for video line items. </documentation>
</annotation>
</enumeration>
<enumeration value="NIELSEN_DAR_REQUIRES_INSTREAM_VIDEO">
<annotation>
<documentation> For deals with Nielsen DAR enabled, there must be an instream video environment. </documentation>
</annotation>
</enumeration>
<enumeration value="LINE_ITEM_TYPE_NOT_SUPPORTED">
<annotation>
<documentation> GRP settings are not supported for the given line item type. </documentation>
</annotation>
</enumeration>
<enumeration value="CANNOT_SPECIFY_GENDER_FOR_GIVEN_AGE_RANGE">
<annotation>
<documentation> GRP audience gender cannot be specified for the selected age range. </documentation>
</annotation>
</enumeration>
<enumeration value="INVALID_MIN_AGE">
<annotation>
<documentation> Minimum age for GRP audience is not valid. </documentation>
</annotation>
</enumeration>
<enumeration value="INVALID_MAX_AGE">
<annotation>
<documentation> Maximum age for GRP audience is not valid. </documentation>
</annotation>
</enumeration>
<enumeration value="CANNOT_DISABLE_GRP_AFTER_ENABLING">
<annotation>
<documentation> GRP settings cannot be disabled. </documentation>
</annotation>
</enumeration>
<enumeration value="CANNOT_CHANGE_GRP_PROVIDERS">
<annotation>
<documentation> GRP provider cannot be updated. </documentation>
</annotation>
</enumeration>
<enumeration value="CANNOT_CHANGE_GRP_SETTINGS">
<annotation>
<documentation> GRP settings cannot be updated once the line item has started serving. </documentation>
</annotation>
</enumeration>
<enumeration value="GRP_AUDIENCE_GOAL_NOT_SUPPORTED">
<annotation>
<documentation> Impression goal based on GRP audience is not supported. </documentation>
</annotation>
</enumeration>
<enumeration value="DEMOG_GOAL_EXPECTED">
<annotation>
<documentation> Impression goal based on GRP audience expected. </documentation>
</annotation>
</enumeration>
<enumeration value="CANNOT_SET_GRP_AUDIENCE_GOAL">
<annotation>
<documentation> Impression goal based on GRP audience cannot be set once the line item has started serving. </documentation>
</annotation>
</enumeration>
<enumeration value="CANNOT_REMOVE_GRP_AUDIENCE_GOAL">
<annotation>
<documentation> Impression goal based on GRP audience cannot be removed once the line item has started serving. </documentation>
</annotation>
</enumeration>
<enumeration value="UNSUPPORTED_GEO_TARGETING">
<annotation>
<documentation> Unsupported geographic location targeted for line item with GRP audience goal. </documentation>
</annotation>
</enumeration>
<enumeration value="UNSUPPORTED_GRP_SETTING">
<annotation>
<documentation> GRP Settings specified are unsupported. </documentation>
</annotation>
</enumeration>
<enumeration value="SHOULD_SET_IN_TARGET_GOAL_THROUGH_GRP_SETTINGS">
<annotation>
<documentation> In-target line items should be set through the grpSettings target impression goal. </documentation>
</annotation>
</enumeration>
<enumeration value="SHOULD_SET_IN_TARGET_GOAL_THROUGH_PRIMARY_GOAL">
<annotation>
<documentation> In-target line items should be set through the primaryReservationUnit's in-target Impressions unit type. </documentation>
</annotation>
</enumeration>
<enumeration value="NIELSEN_REGISTRATION_FAILED">
<annotation>
<documentation> Attempt to register with Nielsen failed. </documentation>
</annotation>
</enumeration>
<enumeration value="LEGACY_NIELSEN_CAMPAIGN_REGISTRATION_ATTEMPT">
<annotation>
<documentation> Attempted to register a placement on a legacy Nielsen campaign. </documentation>
</annotation>
</enumeration>
<enumeration value="UNKNOWN">
<annotation>
<documentation> The value returned if the actual value is not exposed by the requested API version. </documentation>
</annotation>
</enumeration>
</restriction>
</simpleType>
<simpleType name="ImageError.Reason">
<annotation>
<documentation> The reasons for the target error. </documentation>
</annotation>
<restriction base="xsd:string">
<enumeration value="INVALID_IMAGE">
<annotation>
<documentation> The file's format is invalid. </documentation>
</annotation>
</enumeration>
<enumeration value="INVALID_SIZE">
<annotation>
<documentation> {@link Size#width} and {@link Size#height} cannot be negative. </documentation>
</annotation>
</enumeration>
<enumeration value="UNEXPECTED_SIZE">
<annotation>
<documentation> The actual image size does not match the expected image size. </documentation>
</annotation>
</enumeration>
<enumeration value="OVERLAY_SIZE_TOO_LARGE">
<annotation>
<documentation> The size of the asset is larger than that of the overlay creative. </documentation>
</annotation>
</enumeration>
<enumeration value="ANIMATED_NOT_ALLOWED">
<annotation>
<documentation> Animated images are not allowed. </documentation>
</annotation>
</enumeration>
<enumeration value="ANIMATION_TOO_LONG">
<annotation>
<documentation> Animation length exceeded the allowed policy limit. </documentation>
</annotation>
</enumeration>
<enumeration value="CMYK_JPEG_NOT_ALLOWED">
<annotation>
<documentation> Images in CMYK color formats are not allowed. </documentation>
</annotation>
</enumeration>
<enumeration value="FLASH_NOT_ALLOWED">
<annotation>
<documentation> Flash files are not allowed. </documentation>
</annotation>
</enumeration>
<enumeration value="FLASH_WITHOUT_CLICKTAG">
<annotation>
<documentation> If {@link FlashCreative#clickTagRequired} is {@code true}, then the flash file is required to have a click tag embedded in it. </documentation>
</annotation>
</enumeration>
<enumeration value="ANIMATED_VISUAL_EFFECT">
<annotation>
<documentation> Animated visual effect is not allowed. </documentation>
</annotation>
</enumeration>
<enumeration value="FLASH_ERROR">
<annotation>
<documentation> An error was encountered in the flash file. </documentation>
</annotation>
</enumeration>
<enumeration value="LAYOUT_PROBLEM">
<annotation>
<documentation> Incorrect image layout. </documentation>
</annotation>
</enumeration>
<enumeration value="FLASH_HAS_NETWORK_OBJECTS">
<annotation>
<documentation> Flash files with network objects are not allowed. </documentation>
</annotation>
</enumeration>
<enumeration value="FLASH_HAS_NETWORK_METHODS">
<annotation>
<documentation> Flash files with network methods are not allowed. </documentation>
</annotation>
</enumeration>
<enumeration value="FLASH_HAS_URL">
<annotation>
<documentation> Flash files with hard-coded click thru URLs are not allowed. </documentation>
</annotation>
</enumeration>
<enumeration value="FLASH_HAS_MOUSE_TRACKING">
<annotation>
<documentation> Flash files with mouse tracking are not allowed. </documentation>
</annotation>
</enumeration>
<enumeration value="FLASH_HAS_RANDOM_NUM">
<annotation>
<documentation> Flash files that generate or use random numbers are not allowed. </documentation>
</annotation>
</enumeration>
<enumeration value="FLASH_SELF_TARGETS">
<annotation>
<documentation> Flash files with self targets are not allowed. </documentation>
</annotation>
</enumeration>
<enumeration value="FLASH_BAD_GETURL_TARGET">
<annotation>
<documentation> Flash file contains a bad geturl target. </documentation>
</annotation>
</enumeration>
<enumeration value="FLASH_VERSION_NOT_SUPPORTED">
<annotation>
<documentation> Flash or ActionScript version in the submitted file is not supported. </documentation>
</annotation>
</enumeration>
<enumeration value="FILE_TOO_LARGE">
<annotation>
<documentation> The uploaded file is too large. </documentation>
</annotation>
</enumeration>
<enumeration value="SYSTEM_ERROR_IRS">
<annotation>
<documentation> A system error occurred, please try again. </documentation>
</annotation>
</enumeration>
<enumeration value="SYSTEM_ERROR_SCS">
<annotation>
<documentation> A system error occurred, please try again. </documentation>
</annotation>
</enumeration>
<enumeration value="UNEXPECTED_PRIMARY_ASSET_DENSITY">
<annotation>
<documentation> The image density for a primary asset was not one of the expected image densities. </documentation>
</annotation>
</enumeration>
<enumeration value="DUPLICATE_ASSET_DENSITY">
<annotation>
<documentation> Two or more assets have the same image density. </documentation>
</annotation>
</enumeration>
<enumeration value="MISSING_DEFAULT_ASSET">
<annotation>
<documentation> The creative does not contain a primary asset. (For high-density creatives, the primary asset must be a standard image file with 1x density.) </documentation>
</annotation>
</enumeration>
<enumeration value="PREVERIFIED_MIMETYPE_NOT_ALLOWED">
<annotation>
<documentation> preverified_mime_type is not in the client spec's allowlist. </documentation>
</annotation>
</enumeration>
<enumeration value="UNKNOWN">
<annotation>
<documentation> The value returned if the actual value is not exposed by the requested API version. </documentation>
</annotation>
</enumeration>
</restriction>
</simpleType>
<simpleType name="InternalApiError.Reason">
<annotation>
<documentation> The single reason for the internal API error. </documentation>
</annotation>
<restriction base="xsd:string">
<enumeration value="UNEXPECTED_INTERNAL_API_ERROR">
<annotation>
<documentation> API encountered an unexpected internal error. </documentation>
</annotation>
</enumeration>
<enumeration value="TRANSIENT_ERROR">
<annotation>
<documentation> A temporary error occurred during the request. Please retry. </documentation>
</annotation>
</enumeration>
<enumeration value="UNKNOWN">
<annotation>
<documentation> The cause of the error is not known or only defined in newer versions. </documentation>
</annotation>
</enumeration>
<enumeration value="DOWNTIME">
<annotation>
<documentation> The API is currently unavailable for a planned downtime. </documentation>
</annotation>
</enumeration>
<enumeration value="ERROR_GENERATING_RESPONSE">
<annotation>
<documentation> Mutate succeeded but server was unable to build response. Client should not retry mutate. </documentation>
</annotation>
</enumeration>
</restriction>
</simpleType>
<simpleType name="InvalidEmailError.Reason">
<annotation>
<documentation> Describes reasons for an email to be invalid. </documentation>
</annotation>
<restriction base="xsd:string">
<enumeration value="INVALID_FORMAT">
<annotation>
<documentation> The value is not a valid email address. </documentation>
</annotation>
</enumeration>
<enumeration value="UNKNOWN">
<annotation>
<documentation> The value returned if the actual value is not exposed by the requested API version. </documentation>
</annotation>
</enumeration>
</restriction>
</simpleType>
<simpleType name="InvalidUrlError.Reason">
<restriction base="xsd:string">
<enumeration value="ILLEGAL_CHARACTERS">
<annotation>
<documentation> The URL contains invalid characters. </documentation>
</annotation>
</enumeration>
<enumeration value="INVALID_FORMAT">
<annotation>
<documentation> The format of the URL is not allowed. This could occur for a number of reasons. For example, if an invalid scheme is specified (like "ftp://") or if a port is specified when not required, or if a query was specified when not required. </documentation>
</annotation>
</enumeration>
<enumeration value="INSECURE_SCHEME">
<annotation>
<documentation> URL contains insecure scheme. </documentation>
</annotation>
</enumeration>
<enumeration value="NO_SCHEME">
<annotation>
<documentation> The URL does not contain a scheme. </documentation>
</annotation>
</enumeration>
<enumeration value="UNKNOWN">
<annotation>
<documentation> The value returned if the actual value is not exposed by the requested API version. </documentation>
</annotation>
</enumeration>
</restriction>
</simpleType>
<simpleType name="InventoryTargetingError.Reason">
<annotation>
<documentation> The reasons for the target error. </documentation>
</annotation>
<restriction base="xsd:string">
<enumeration value="AT_LEAST_ONE_PLACEMENT_OR_INVENTORY_UNIT_REQUIRED">
<annotation>
<documentation> At least one placement or inventory unit is required </documentation>
</annotation>
</enumeration>
<enumeration value="INVENTORY_CANNOT_BE_TARGETED_AND_EXCLUDED">
<annotation>
<documentation> The same inventory unit or placement cannot be targeted and excluded at the same time </documentation>
</annotation>
</enumeration>
<enumeration value="INVENTORY_UNIT_CANNOT_BE_TARGETED_IF_ANCESTOR_IS_TARGETED">
<annotation>
<documentation> A child inventory unit cannot be targeted if its ancestor inventory unit is also targeted. </documentation>
</annotation>
</enumeration>
<enumeration value="INVENTORY_UNIT_CANNOT_BE_TARGETED_IF_ANCESTOR_IS_EXCLUDED">
<annotation>
<documentation> A child inventory unit cannot be targeted if its ancestor inventory unit is excluded. </documentation>
</annotation>
</enumeration>
<enumeration value="INVENTORY_UNIT_CANNOT_BE_EXCLUDED_IF_ANCESTOR_IS_EXCLUDED">
<annotation>
<documentation> A child inventory unit cannot be excluded if its ancestor inventory unit is also excluded. </documentation>
</annotation>
</enumeration>
<enumeration value="EXPLICITLY_TARGETED_INVENTORY_UNIT_CANNOT_BE_TARGETED">
<annotation>
<documentation> An explicitly targeted inventory unit cannot be targeted. </documentation>
</annotation>
</enumeration>
<enumeration value="EXPLICITLY_TARGETED_INVENTORY_UNIT_CANNOT_BE_EXCLUDED">
<annotation>
<documentation> An explicitly targeted inventory unit cannot be excluded. </documentation>
</annotation>
</enumeration>
<enumeration value="SELF_ONLY_INVENTORY_UNIT_NOT_ALLOWED">
<annotation>
<documentation> A landing page-only ad unit cannot be targeted. </documentation>
</annotation>
</enumeration>
<enumeration value="SELF_ONLY_INVENTORY_UNIT_WITHOUT_DESCENDANTS">
<annotation>
<documentation> A landing page-only ad unit cannot be targeted if it doesn't have any children. </documentation>
</annotation>
</enumeration>
<enumeration value="YOUTUBE_AUDIENCE_SEGMENTS_CAN_ONLY_BE_TARGETED_WITH_YOUTUBE_SHARED_INVENTORY">
<annotation>
<documentation> Audience segments shared from YouTube can only be targeted with inventory shared from YouTube for cross selling. </documentation>
</annotation>
</enumeration>
<enumeration value="UNKNOWN">
<annotation>
<documentation> The value returned if the actual value is not exposed by the requested API version. </documentation>
</annotation>
</enumeration>
</restriction>
</simpleType>
<simpleType name="LabelEntityAssociationError.Reason">
<annotation>
<documentation> The reasons for the target error. </documentation>
</annotation>
<restriction base="xsd:string">
<enumeration value="DUPLICATE_ASSOCIATION">
<annotation>
<documentation> The label has already been attached to the entity. </documentation>
</annotation>
</enumeration>
<enumeration value="INVALID_ASSOCIATION">
<annotation>
<documentation> A label is being applied to an entity that does not support that entity type. </documentation>
</annotation>
</enumeration>
<enumeration value="NEGATION_NOT_ALLOWED">
<annotation>
<documentation> Label negation cannot be applied to the entity type. </documentation>
</annotation>
</enumeration>
<enumeration value="DUPLICATE_ASSOCIATION_WITH_NEGATION">
<annotation>
<documentation> The same label is being applied and negated to the same entity. </documentation>
</annotation>
</enumeration>
<enumeration value="UNKNOWN">
<annotation>
<documentation> The value returned if the actual value is not exposed by the requested API version. </documentation>
</annotation>
</enumeration>
</restriction>
</simpleType>
<simpleType name="LineItemActivityAssociationError.Reason">
<annotation>
<documentation> The reasons for the target error. </documentation>
</annotation>
<restriction base="xsd:string">
<enumeration value="INVALID_ACTIVITY_FOR_ADVERTISER">
<annotation>
<documentation> When associating an activity to a line item the activity must belong to the same advertiser as the line item. </documentation>
</annotation>
</enumeration>
<enumeration value="INVALID_COST_TYPE_FOR_ASSOCIATION">
<annotation>
<documentation> Activities can only be associated with line items of {@link CostType.CPA}. </documentation>
</annotation>
</enumeration>
<enumeration value="UNKNOWN">
<annotation>
<documentation> The value returned if the actual value is not exposed by the requested API version. </documentation>
</annotation>
</enumeration>
</restriction>
</simpleType>
<simpleType name="LineItemCreativeAssociationError.Reason">
<annotation>
<documentation> The reasons for the target error. </documentation>
</annotation>
<restriction base="xsd:string">
<enumeration value="CREATIVE_IN_WRONG_ADVERTISERS_LIBRARY">
<annotation>
<documentation> Cannot associate a creative to the wrong advertiser </documentation>
</annotation>
</enumeration>
<enumeration value="INVALID_LINEITEM_CREATIVE_PAIRING">
<annotation>
<documentation> The creative type being associated is a invalid for the line item type. </documentation>
</annotation>
</enumeration>
<enumeration value="STARTDATE_BEFORE_LINEITEM_STARTDATE">
<annotation>
<documentation> Association start date cannot be before line item start date </documentation>
</annotation>
</enumeration>
<enumeration value="STARTDATE_NOT_BEFORE_LINEITEM_ENDDATE">
<annotation>
<documentation> Association start date cannot be same as or after line item end date </documentation>
</annotation>
</enumeration>
<enumeration value="ENDDATE_AFTER_LINEITEM_ENDDATE">
<annotation>
<documentation> Association end date cannot be after line item end date </documentation>
</annotation>
</enumeration>
<enumeration value="ENDDATE_NOT_AFTER_LINEITEM_STARTDATE">
<annotation>
<documentation> Association end date cannot be same as or before line item start date </documentation>
</annotation>
</enumeration>
<enumeration value="ENDDATE_NOT_AFTER_STARTDATE">
<annotation>
<documentation> Association end date cannot be same as or before its start date </documentation>
</annotation>
</enumeration>
<enumeration value="ENDDATE_IN_THE_PAST">
<annotation>
<documentation> Association end date cannot be in the past. </documentation>
</annotation>
</enumeration>
<enumeration value="CANNOT_COPY_WITHIN_SAME_LINE_ITEM">
<annotation>
<documentation> Cannot copy an association to the same line item without creating new creative </documentation>
</annotation>
</enumeration>
<enumeration value="UNSUPPORTED_CREATIVE_VAST_REDIRECT_TYPE">
<annotation>
<documentation> Programmatic only supports the "Video" redirect type. </documentation>
</annotation>
</enumeration>
<enumeration value="UNSUPPORTED_YOUTUBE_HOSTED_CREATIVE">
<annotation>
<documentation> Programmatic does not support YouTube hosted creatives. </documentation>
</annotation>
</enumeration>
<enumeration value="PROGRAMMATIC_CREATIVES_CAN_ONLY_BE_ASSIGNED_TO_ONE_LINE_ITEM">
<annotation>
<documentation> Programmatic creatives can only be assigned to one line item. </documentation>
</annotation>
</enumeration>
<enumeration value="CANNOT_ACTIVATE_ASSOCIATION_WITH_INACTIVE_CREATIVE">
<annotation>
<documentation> Cannot activate a line item creative association if the associated creative is inactive. </documentation>
</annotation>
</enumeration>
<enumeration value="CANNOT_CREATE_PROGRAMMATIC_CREATIVES">
<annotation>
<documentation> Cannot create programmatic creatives. </documentation>
</annotation>
</enumeration>
<enumeration value="CANNOT_UPDATE_PROGRAMMATIC_CREATIVES">
<annotation>
<documentation> Cannot update programmatic creatives. </documentation>
</annotation>
</enumeration>
<enumeration value="CREATIVE_AND_LINE_ITEM_MUST_BOTH_BE_SET_TOP_BOX_ENABLED">
<annotation>
<documentation> Cannot associate a creative with a line item if only one of them is set-top box enabled. </documentation>
</annotation>
</enumeration>
<enumeration value="CANNOT_DELETE_SET_TOP_BOX_ENABLED_ASSOCIATIONS">
<annotation>
<documentation> Cannot delete associations between set-top box enabled line items and set-top box enabled creatives. </documentation>
</annotation>
</enumeration>
<enumeration value="SET_TOP_BOX_CREATIVE_ROTATION_WEIGHT_MUST_BE_INTEGER">
<annotation>
<documentation> Creative rotation weights must be integers. </documentation>
</annotation>
</enumeration>
<enumeration value="INVALID_CREATIVE_ROTATION_TYPE_FOR_MANUAL_WEIGHT">
<annotation>
<documentation> Creative rotation weights are only valid when creative rotation type is set to {@link CreativeRotationType#MANUAL}. </documentation>
</annotation>
</enumeration>
<enumeration value="CLICK_MACROS_REQUIRED">
<annotation>
<documentation> The code snippet of a creative must contain a click macro (%%CLICK_URL_ESC%% or %%CLICK_URL_UNESC%%). </documentation>
</annotation>
</enumeration>
<enumeration value="VIEW_MACROS_NOT_ALLOWED">
<annotation>
<documentation> The code snippet of a creative must not contain a view macro (%%VIEW_URL_ESC%% or %%VIEW_URL_UNESC%%). </documentation>
</annotation>
</enumeration>
<enumeration value="UNKNOWN">
<annotation>
<documentation> The value returned if the actual value is not exposed by the requested API version. </documentation>
</annotation>
</enumeration>
</restriction>
</simpleType>
<simpleType name="LineItemError.Reason">
<annotation>
<documentation> The reasons for the target error. </documentation>
</annotation>
<restriction base="xsd:string">
<enumeration value="ALREADY_STARTED">
<annotation>
<documentation> Some changes may not be allowed because a line item has already started. </documentation>
</annotation>
</enumeration>
<enumeration value="UPDATE_RESERVATION_NOT_ALLOWED">
<annotation>
<documentation> Update reservation is not allowed because a line item has already started, users must pause the line item first. </documentation>
</annotation>
</enumeration>
<enumeration value="ALL_ROADBLOCK_NOT_ALLOWED">
<annotation>
<documentation> Roadblocking to display all creatives is not allowed. </documentation>
</annotation>
</enumeration>
<enumeration value="ALL_COMPANION_DELIVERY_NOT_ALLOWED">
<annotation>
<documentation> Companion delivery to display all creatives is not allowed. </documentation>
</annotation>
</enumeration>
<enumeration value="CREATIVE_SET_ROADBLOCK_NOT_ALLOWED">
<annotation>
<documentation> Roadblocking to display all master and companion creative set is not allowed. </documentation>
</annotation>
</enumeration>
<enumeration value="FRACTIONAL_PERCENTAGE_NOT_ALLOWED">
<annotation>
<documentation> Fractional percentage is not allowed. </documentation>
</annotation>
</enumeration>
<enumeration value="DISCOUNT_NOT_ALLOWED">
<annotation>
<documentation> For certain LineItem configurations discounts are not allowed. </documentation>
</annotation>
</enumeration>
<enumeration value="UPDATE_CANCELED_LINE_ITEM_NOT_ALLOWED">
<annotation>
<documentation> Updating a canceled line item is not allowed. </documentation>
</annotation>
</enumeration>
<enumeration value="UPDATE_PENDING_APPROVAL_LINE_ITEM_NOT_ALLOWED">
<annotation>
<documentation> Updating a pending approval line item is not allowed. </documentation>
</annotation>
</enumeration>
<enumeration value="UPDATE_ARCHIVED_LINE_ITEM_NOT_ALLOWED">
<annotation>
<documentation> Updating an archived line item is not allowed. </documentation>
</annotation>
</enumeration>
<enumeration value="CREATE_OR_UPDATE_LEGACY_DFP_LINE_ITEM_TYPE_NOT_ALLOWED">
<annotation>
<documentation> Create or update legacy dfp line item type is not allowed. </documentation>
</annotation>
</enumeration>
<enumeration value="COPY_LINE_ITEM_FROM_DIFFERENT_COMPANY_NOT_ALLOWED">
<annotation>
<documentation> Copying line item from different company (advertiser) to the same order is not allowed. </documentation>
</annotation>
</enumeration>
<enumeration value="INVALID_SIZE_FOR_PLATFORM">
<annotation>
<documentation> The size is invalid for the specified platform. </documentation>
</annotation>
</enumeration>
<enumeration value="INVALID_LINE_ITEM_TYPE_FOR_PLATFORM">
<annotation>
<documentation> The line item type is invalid for the specified platform. </documentation>
</annotation>
</enumeration>
<enumeration value="INVALID_WEB_PROPERTY_FOR_PLATFORM">
<annotation>
<documentation> The web property cannot be served on the specified platform. </documentation>
</annotation>
</enumeration>
<enumeration value="INVALID_WEB_PROPERTY_FOR_ENVIRONMENT">
<annotation>
<documentation> The web property cannot be served on the specified environment. </documentation>
</annotation>
</enumeration>
<enumeration value="AFMA_BACKFILL_NOT_ALLOWED">
<annotation>
<documentation> AFMA backfill not supported. </documentation>
</annotation>
</enumeration>
<enumeration value="UPDATE_ENVIRONMENT_TYPE_NOT_ALLOWED">
<annotation>
<documentation> Environment type cannot change once saved. </documentation>
</annotation>
</enumeration>
<enumeration value="COMPANIONS_NOT_ALLOWED">
<annotation>
<documentation> The placeholders are invalid because they contain companions, but the line item does not support companions. </documentation>
</annotation>
</enumeration>
<enumeration value="ROADBLOCKS_WITH_NONROADBLOCKS_NOT_ALLOWED">
<annotation>
<documentation> The placeholders are invalid because some of them are roadblocks, and some are not. Either all roadblock placeholders must contain companions, or no placeholders may contain companions. This does not apply to video creative sets. </documentation>
</annotation>
</enumeration>
<enumeration value="CANNOT_UPDATE_TO_OR_FROM_CREATIVE_SET_ROADBLOCK">
<annotation>
<documentation> A line item cannot be updated from having {@link RoadblockingType#CREATIVE_SET} to having a different RoadblockingType, or vice versa. </documentation>
</annotation>
</enumeration>
<enumeration value="UPDATE_FROM_BACKFILL_LINE_ITEM_TYPE_NOT_ALLOWED">
<annotation>
<documentation> Can not change from a backfill line item type once creatives have been assigned. </documentation>
</annotation>
</enumeration>
<enumeration value="UPDATE_TO_BACKFILL_LINE_ITEM_TYPE_NOT_ALLOWED">
<annotation>
<documentation> Can not change to a backfill line item type once creatives have been assigned. </documentation>
</annotation>
</enumeration>
<enumeration value="UPDATE_BACKFILL_WEB_PROPERTY_NOT_ALLOWED">
<annotation>
<documentation> Can not change to backfill web property once creatives have been assigned. </documentation>
</annotation>
</enumeration>
<enumeration value="INVALID_COMPANION_DELIVERY_OPTION_FOR_ENVIRONMENT_TYPE">
<annotation>
<documentation> The companion delivery option is not valid for your environment type. </documentation>
</annotation>
</enumeration>
<enumeration value="COMPANION_BACKFILL_REQUIRES_VIDEO">
<annotation>
<documentation> Companion backfill is enabled but environment type not video. </documentation>
</annotation>
</enumeration>
<enumeration value="COMPANION_DELIVERY_OPTION_REQUIRE_PREMIUM">
<annotation>
<documentation> Companion delivery options require Ad Manager 360 networks. </documentation>
</annotation>
</enumeration>
<enumeration value="DUPLICATE_MASTER_SIZES">
<annotation>
<documentation> The master size of placeholders have duplicates. </documentation>
</annotation>
</enumeration>
<enumeration value="INVALID_PRIORITY_FOR_LINE_ITEM_TYPE">
<annotation>
<documentation> The line item priority is invalid if for dynamic allocation line items it is different than the default for free publishers. When allowed, Ad Manager 360 users can change the priority to any value. </documentation>
</annotation>
</enumeration>
<enumeration value="INVALID_ENVIRONMENT_TYPE">
<annotation>
<documentation> The environment type is not valid. </documentation>
</annotation>
</enumeration>
<enumeration value="INVALID_ENVIRONMENT_TYPE_FOR_PLATFORM">
<annotation>
<documentation> The environment type is not valid for the target platform. </documentation>
</annotation>
</enumeration>
<enumeration value="INVALID_TYPE_FOR_AUTO_EXTENSION">
<annotation>
<documentation> Only {@link LineItemType#STANDARD} line items can be auto extended. </documentation>
</annotation>
</enumeration>
<enumeration value="VIDEO_INVALID_ROADBLOCKING">
<annotation>
<documentation> Video line items cannot change the roadblocking type. </documentation>
</annotation>
</enumeration>
<enumeration value="BACKFILL_TYPE_NOT_ALLOWED">
<annotation>
<documentation> The backfill feature is not enabled according to your features. </documentation>
</annotation>
</enumeration>
<enumeration value="INVALID_BACKFILL_LINK_TYPE">
<annotation>
<documentation> The web property is invalid. A line item must have an appropriate web property selected. </documentation>
</annotation>
</enumeration>
<enumeration value="DIFFERENT_BACKFILL_ACCOUNT">
<annotation>
<documentation> All line items in a programmatic order must have web property codes from the same account. </documentation>
</annotation>
</enumeration>
<enumeration value="COMPANION_DELIVERY_OPTIONS_NOT_ALLOWED_WITH_BACKFILL">
<annotation>
<documentation> Companion delivery options are not allowed with dynamic allocation line items. </documentation>
</annotation>
</enumeration>
<enumeration value="INVALID_WEB_PROPERTY_FOR_ADX_BACKFILL">
<annotation>
<documentation> Dynamic allocation using the AdExchange should always use an AFC web property. </documentation>
</annotation>
</enumeration>
<enumeration value="INVALID_COST_PER_UNIT_FOR_BACKFILL">
<annotation>
<documentation> CPM for backfill inventory must be 0. </documentation>
</annotation>
</enumeration>
<enumeration value="INVALID_SIZE_FOR_ENVIRONMENT">
<annotation>
<documentation> Aspect ratio sizes cannot be used with video line items. </documentation>
</annotation>
</enumeration>
<enumeration value="TARGET_PLATOFRM_NOT_ALLOWED">
<annotation>
<documentation> The specified target platform is not allowed. </documentation>
</annotation>
</enumeration>
<enumeration value="INVALID_LINE_ITEM_CURRENCY">
<annotation>
<documentation> Currency on a line item must be one of the specified network currencies. </documentation>
</annotation>
</enumeration>
<enumeration value="LINE_ITEM_CANNOT_HAVE_MULTIPLE_CURRENCIES">
<annotation>
<documentation> All money fields on a line item must specify the same currency. </documentation>
</annotation>
</enumeration>
<enumeration value="CANNOT_CHANGE_CURRENCY">
<annotation>
<documentation> Once a line item has moved into a a delivering state the currency cannot be changed. </documentation>
</annotation>
</enumeration>
<enumeration value="INVALID_LINE_ITEM_DATE_TIME">
<annotation>
<documentation> A DateTime associated with the line item is not valid. </documentation>
</annotation>
</enumeration>
<enumeration value="INVALID_COST_PER_UNIT_FOR_CPA">
<annotation>
<documentation> CPA {@link LineItem line items} must specify a zero cost for the {@link LineItem#costPerUnit}. </documentation>
</annotation>
</enumeration>
<enumeration value="UPDATE_CPA_COST_TYPE_NOT_ALLOWED">
<annotation>
<documentation> Once a {@link LineItem} is activated its {@link LineItem#costPerUnit} cannot be updated to/from CPA. </documentation>
</annotation>
</enumeration>
<enumeration value="UPDATE_VCPM_COST_TYPE_NOT_ALLOWED">
<annotation>
<documentation> Once a {@link LineItem} is activated its {@link LineItem#costPerUnit} cannot be updated to/from Viewable CPM. </documentation>
</annotation>
</enumeration>
<enumeration value="MASTER_COMPANION_LINE_ITEM_CANNOT_HAVE_VCPM_COST_TYPE">
<annotation>
<documentation> A {@link LineItem} with master/companion creative placeholders cannot have Viewable CPM as its {@link LineItem#costPerUnit}. </documentation>
</annotation>
</enumeration>
<enumeration value="DUPLICATED_UNIT_TYPE">
<annotation>
<documentation> There cannot be goals with duplicated unit type among the secondary goals for a {@link LineItem line items}. </documentation>
</annotation>
</enumeration>
<enumeration value="MULTIPLE_GOAL_TYPE_NOT_ALLOWED">
<annotation>
<documentation> The secondary goals of a {@link LineItem line items} must have the same goal type. </documentation>
</annotation>
</enumeration>
<enumeration value="INVALID_UNIT_TYPE_COMBINATION_FOR_SECONDARY_GOALS">
<annotation>
<documentation> For a CPA {@link LineItem line item}, the possible combinations for secondary goals must be either click-through conversion only, click-through conversion with view-through conversion or total conversion only. For a Viewable CPM {@link LineItem line item} or a CPM based Sponsorship {@link LineItem line item}, its secondary goal has to be impression-based. </documentation>
</annotation>
</enumeration>
<enumeration value="INVALID_CREATIVE_TARGETING_NAME">
<annotation>
<documentation> One or more of the targeting names specified by a creative placeholder or line item creative association were not found on the line item. </documentation>
</annotation>
</enumeration>
<enumeration value="INVALID_CREATIVE_CUSTOM_TARGETING_MATCH_TYPE">
<annotation>
<documentation> Creative targeting expressions on the line item can only have custom criteria targeting with {@link CustomTargetingValue.MatchType#EXACT}. </documentation>
</annotation>
</enumeration>
<enumeration value="INVALID_CREATIVE_ROTATION_TYPE_WITH_CREATIVE_TARGETING">
<annotation>
<documentation> Line item with creative targeting expressions cannot have creative rotation type set to {@link CreativeRotationType#SEQUENTIAL}. </documentation>
</annotation>
</enumeration>
<enumeration value="CANNOT_OVERBOOK_WITH_CREATIVE_TARGETING">
<annotation>
<documentation> Line items cannot overbook inventory when applying creative-level targeting if the originating proposal line item did not overbook inventory. Remove creative-level targeting and try again. </documentation>
</annotation>
</enumeration>
<enumeration value="PLACEHOLDERS_DO_NOT_MATCH_PROPOSAL">
<annotation>
<documentation> For a managed line item, inventory sizes must match sizes that are set on the originating proposal line item. In the case that a size is broken out by creative-level targeting, the sum of the creative counts for each size must equal the expected creative count that is set for that size on the originating proposal line item. </documentation>
</annotation>
</enumeration>
<enumeration value="UNSUPPORTED_LINE_ITEM_TYPE_FOR_THIS_API_VERSION">
<annotation>
<documentation> The line item type is not supported for this API version. </documentation>
</annotation>
</enumeration>
<enumeration value="NATIVE_CREATIVE_TEMPLATE_REQUIRED">
<annotation>
<documentation> Placeholders can only have native creative templates. </documentation>
</annotation>
</enumeration>
<enumeration value="CANNOT_HAVE_CREATIVE_TEMPLATE">
<annotation>
<documentation> Non-native placeholders cannot have creative templates. </documentation>
</annotation>
</enumeration>
<enumeration value="CANNOT_INCLUDE_NATIVE_CREATIVE_TEMPLATE">
<annotation>
<documentation> Cannot include native creative templates in the placeholders for Ad Exchange line items. </documentation>
</annotation>
</enumeration>
<enumeration value="CANNOT_INCLUDE_NATIVE_PLACEHOLDER_WITHOUT_TEMPLATE_ID">
<annotation>
<documentation> Cannot include native placeholders without native creative templates for direct-sold line items. </documentation>
</annotation>
</enumeration>
<enumeration value="NO_SIZE_WITH_DURATION">
<annotation>
<documentation> For forecasting only, error when line item has duration, but no creative sizes specified. </documentation>
</annotation>
</enumeration>
<enumeration value="INVALID_VIEWABILITY_PROVIDER_COMPANY">
<annotation>
<documentation> Used when the company pointed to by the viewabilityProviderCompanyId is not of type VIEWABILITY_PROVIDER. </documentation>
</annotation>
</enumeration>
<enumeration value="CANNOT_ACCESS_CUSTOM_PACING_CURVE_CLOUD_STORAGE_BUCKET">
<annotation>
<documentation> An error occurred while accessing the custom pacing curve Google Cloud Storage bucket. </documentation>
</annotation>
</enumeration>
<enumeration value="CMS_METADATA_LINE_ITEM_ENVIRONMENT_TYPE_NOT_SUPPORTED">
<annotation>
<documentation> CMS Metadata targeting is only supported for video line items. </documentation>
</annotation>
</enumeration>
<enumeration value="SKIPPABLE_AD_TYPE_NOT_ALLOWED">
<annotation>
<documentation> The {@code SkippableAdType} is not allowed. </documentation>
</annotation>
</enumeration>
<enumeration value="CUSTOM_PACING_CURVE_START_TIME_MUST_MATCH_LINE_ITEM_START_TIME">
<annotation>
<documentation> Custom pacing curve start time must match the line item's start time. </documentation>
</annotation>
</enumeration>
<enumeration value="CUSTOM_PACING_CURVE_START_TIME_PAST_LINE_ITEM_END_TIME">
<annotation>
<documentation> Custom pacing curve goal start time must be before line item end time. </documentation>
</annotation>
</enumeration>
<enumeration value="INVALID_LINE_ITEM_TYPE_FOR_DELIVERY_FORECAST_SOURCE">
<annotation>
<documentation> The line item type is invalid for the specified delivery forecast source. </documentation>
</annotation>
</enumeration>
<enumeration value="INVALID_TOTAL_CUSTOM_PACING_GOAL_AMOUNTS">
<annotation>
<documentation> The sum of the custom pacing goal amounts is invalid. </documentation>
</annotation>
</enumeration>
<enumeration value="COPY_LINE_ITEM_WITH_CUSTOM_PACING_CURVE_FULLY_IN_PAST_NOT_ALLOWED">
<annotation>
<documentation> Copying line items with custom pacing curves that are totally in the past is not allowed. </documentation>
</annotation>
</enumeration>
<enumeration value="LAST_CUSTOM_PACING_GOAL_AMOUNT_CANNOT_BE_ZERO">
<annotation>
<documentation> The last custom pacing goal cannot be zero. </documentation>
</annotation>
</enumeration>
<enumeration value="GRP_PACED_LINE_ITEM_CANNOT_HAVE_ABSOLUTE_CUSTOM_PACING_CURVE_GOALS">
<annotation>
<documentation> GRP paced line items cannot have absolute custom pacing curve goals. </documentation>
</annotation>
</enumeration>
<enumeration value="INVALID_MAX_VIDEO_CREATIVE_DURATION">
<annotation>
<documentation> {@link LineItem line item} has invalid video creative duration. </documentation>
</annotation>
</enumeration>
<enumeration value="INVALID_NATIVE_SIZE">
<annotation>
<documentation> Native size types must by 1x1. </documentation>
</annotation>
</enumeration>
<enumeration value="INVALID_TARGETED_REQUEST_PLATFORM_FOR_WEB_PROPERTY_CODE">
<annotation>
<documentation> For AdExchange Line Items, the targeted request platform must match the syndication type of the web property code. </documentation>
</annotation>
</enumeration>
<enumeration value="UNKNOWN">
<annotation>
<documentation> The value returned if the actual value is not exposed by the requested API version. </documentation>
</annotation>
</enumeration>
</restriction>
</simpleType>
<simpleType name="LineItemFlightDateError.Reason">
<annotation>
<documentation> The reasons for the target error. </documentation>
</annotation>
<restriction base="xsd:string">
<enumeration value="START_DATE_TIME_IS_IN_PAST"/>
<enumeration value="END_DATE_TIME_IS_IN_PAST"/>
<enumeration value="END_DATE_TIME_NOT_AFTER_START_TIME"/>
<enumeration value="END_DATE_TIME_TOO_LATE"/>
<enumeration value="UNKNOWN">
<annotation>
<documentation> The value returned if the actual value is not exposed by the requested API version. </documentation>
</annotation>
</enumeration>
</restriction>
</simpleType>
<simpleType name="LineItemOperationError.Reason">
<annotation>
<documentation> The reasons for the target error. </documentation>
</annotation>
<restriction base="xsd:string">
<enumeration value="NOT_ALLOWED">
<annotation>
<documentation> The operation is not allowed due to lack of permissions. </documentation>
</annotation>
</enumeration>
<enumeration value="NOT_APPLICABLE">
<annotation>
<documentation> The operation is not applicable for the current state of the {@link LineItem}. </documentation>
</annotation>
</enumeration>
<enumeration value="HAS_COMPLETED">
<annotation>
<documentation> The {@link LineItem} is completed. A {@link LineItemAction} cannot be applied to a line item that is completed. </documentation>
</annotation>
</enumeration>
<enumeration value="HAS_NO_ACTIVE_CREATIVES">
<annotation>
<documentation> The {@link LineItem} has no active creatives. A line item cannot be activated with no active creatives. </documentation>
</annotation>
</enumeration>
<enumeration value="CANNOT_ACTIVATE_LEGACY_DFP_LINE_ITEM">
<annotation>
<documentation> A {@link LineItem} of type {@link LineItemType#LEGACY_DFP} cannot be Activated. </documentation>
</annotation>
</enumeration>
<enumeration value="CANNOT_ACTIVATE_UNCONFIGURED_LINE_ITEM">
<annotation>
<documentation> A {@link LineItem} with publisher creative source cannot be activated if the corresponding deal is not yet configured by the buyer. </documentation>
</annotation>
</enumeration>
<enumeration value="CANNOT_DELETE_DELIVERED_LINE_ITEM">
<annotation>
<documentation> Deleting an {@link LineItem} that has delivered is not allowed </documentation>
</annotation>
</enumeration>
<enumeration value="CANNOT_RESERVE_COMPANY_CREDIT_STATUS_NOT_ACTIVE">
<annotation>
<documentation> Reservation cannot be made for line item because the {@link LineItem#advertiserId} it is associated with has {@link Company#creditStatus} that is not {@code ACTIVE} or {@code ON_HOLD}. </documentation>
</annotation>
</enumeration>
<enumeration value="CANNOT_ACTIVATE_INVALID_COMPANY_CREDIT_STATUS">
<annotation>
<documentation> Cannot activate line item because the {@link LineItem#advertiserId} it is associated with has {@link Company#creditStatus} that is not {@code ACTIVE}, {@code INACTIVE}, or {@code ON_HOLD}. </documentation>
</annotation>
</enumeration>
<enumeration value="UNKNOWN">
<annotation>
<documentation> The value returned if the actual value is not exposed by the requested API version. </documentation>
</annotation>
</enumeration>
</restriction>
</simpleType>
<simpleType name="MobileApplicationTargetingError.Reason">
<annotation>
<documentation> {@link ApiErrorReason} enum for user domain targeting error. </documentation>
</annotation>
<restriction base="xsd:string">
<enumeration value="CANNOT_TARGET_UNLINKED_APPLICATION">
<annotation>
<documentation> Only applications that are linked to a store entry may be targeted. </documentation>
</annotation>
</enumeration>
<enumeration value="UNKNOWN">
<annotation>
<documentation> The value returned if the actual value is not exposed by the requested API version. </documentation>
</annotation>
</enumeration>
</restriction>
</simpleType>
<simpleType name="NotNullError.Reason">
<annotation>
<documentation> The reasons for the target error. </documentation>
</annotation>
<restriction base="xsd:string">
<enumeration value="ARG1_NULL">
<annotation>
<documentation> Assuming that a method will not have more than 3 arguments, if it does, return NULL </documentation>
</annotation>
</enumeration>
<enumeration value="ARG2_NULL"/>
<enumeration value="ARG3_NULL"/>
<enumeration value="NULL"/>
<enumeration value="UNKNOWN">
<annotation>
<documentation> The value returned if the actual value is not exposed by the requested API version. </documentation>
</annotation>
</enumeration>
</restriction>
</simpleType>
<simpleType name="NullError.Reason">
<annotation>
<documentation> The reasons for the validation error. </documentation>
</annotation>
<restriction base="xsd:string">
<enumeration value="NULL_CONTENT">
<annotation>
<documentation> Specified list/container must not contain any null elements </documentation>
</annotation>
</enumeration>
</restriction>
</simpleType>
<simpleType name="OrderActionError.Reason">
<annotation>
<documentation> The reasons for the target error. </documentation>
</annotation>
<restriction base="xsd:string">
<enumeration value="PERMISSION_DENIED">
<annotation>
<documentation> The operation is not allowed due to lack of permissions. </documentation>
</annotation>
</enumeration>
<enumeration value="NOT_APPLICABLE">
<annotation>
<documentation> The operation is not applicable for the current state of the {@link Order}. </documentation>
</annotation>
</enumeration>
<enumeration value="IS_ARCHIVED">
<annotation>
<documentation> The {@link Order} is archived, an {@link OrderAction} cannot be applied to an archived order. </documentation>
</annotation>
</enumeration>
<enumeration value="HAS_ENDED">
<annotation>
<documentation> The {@link Order} is past its end date, An {@link OrderAction} cannot be applied to a order that has ended. </documentation>
</annotation>
</enumeration>
<enumeration value="CANNOT_APPROVE_WITH_UNRESERVED_LINE_ITEMS">
<annotation>
<documentation> A {@link Order} cannot be approved if it contains reservable {@link LineItem}s that are unreserved. </documentation>
</annotation>
</enumeration>
<enumeration value="CANNOT_DELETE_ORDER_WITH_DELIVERED_LINEITEMS">
<annotation>
<documentation> Deleting an {@link Order} with delivered line items is not allowed </documentation>
</annotation>
</enumeration>
<enumeration value="CANNOT_APPROVE_COMPANY_CREDIT_STATUS_NOT_ACTIVE">
<annotation>
<documentation> Cannot approve because company credit status is not active. </documentation>
</annotation>
</enumeration>
<enumeration value="UNKNOWN">
<annotation>
<documentation> The value returned if the actual value is not exposed by the requested API version. </documentation>
</annotation>
</enumeration>
</restriction>
</simpleType>
<simpleType name="OrderError.Reason">
<annotation>
<documentation> The reasons for the target error. </documentation>
</annotation>
<restriction base="xsd:string">
<enumeration value="UPDATE_CANCELED_ORDER_NOT_ALLOWED">
<annotation>
<documentation> Updating a canceled order is not allowed. </documentation>
</annotation>
</enumeration>
<enumeration value="UPDATE_PENDING_APPROVAL_ORDER_NOT_ALLOWED">
<annotation>
<documentation> Updating an order that has its approval pending is not allowed. </documentation>
</annotation>
</enumeration>
<enumeration value="UPDATE_ARCHIVED_ORDER_NOT_ALLOWED">
<annotation>
<documentation> Updating an archived order is not allowed. </documentation>
</annotation>
</enumeration>
<enumeration value="CANNOT_MODIFY_PROPOSAL_ID">
<annotation>
<documentation> DSM can set the proposal ID only at the time of creation of order. Setting or changing proposal ID at the time of order update is not allowed. </documentation>
</annotation>
</enumeration>
<enumeration value="PRIMARY_USER_REQUIRED">
<annotation>
<documentation> Cannot have secondary user without a primary user. </documentation>
</annotation>
</enumeration>
<enumeration value="PRIMARY_USER_CANNOT_BE_SECONDARY">
<annotation>
<documentation> Primary user cannot be added as a secondary user too. </documentation>
</annotation>
</enumeration>
<enumeration value="ORDER_TEAM_NOT_ASSOCIATED_WITH_ADVERTISER">
<annotation>
<documentation> A team associated with the order must also be associated with the advertiser. </documentation>
</annotation>
</enumeration>
<enumeration value="USER_NOT_ON_ORDERS_TEAMS">
<annotation>
<documentation> The user assigned to the order, like salesperson or trafficker, must be on one of the order's teams. </documentation>
</annotation>
</enumeration>
<enumeration value="AGENCY_NOT_ON_ORDERS_TEAMS">
<annotation>
<documentation> The agency assigned to the order must belong to one of the order's teams. </documentation>
</annotation>
</enumeration>
<enumeration value="INVALID_FIELDS_SET_FOR_NON_PROGRAMMATIC_ORDER">
<annotation>
<documentation> Programmatic info fields should not be set for a non-programmatic order. </documentation>
</annotation>
</enumeration>
<enumeration value="UNKNOWN">
<annotation>
<documentation> The value returned if the actual value is not exposed by the requested API version. </documentation>
</annotation>
</enumeration>
</restriction>
</simpleType>
<simpleType name="OrderStatus">
<annotation>
<documentation> Describes the order statuses. </documentation>
</annotation>
<restriction base="xsd:string">
<enumeration value="DRAFT">
<annotation>
<documentation> Indicates that the {@link Order} has just been created but no approval has been requested yet. </documentation>
</annotation>
</enumeration>
<enumeration value="PENDING_APPROVAL">
<annotation>
<documentation> Indicates that a request for approval for the {@link Order} has been made. </documentation>
</annotation>
</enumeration>
<enumeration value="APPROVED">
<annotation>
<documentation> Indicates that the {@link Order} has been approved and is ready to serve. </documentation>
</annotation>
</enumeration>
<enumeration value="DISAPPROVED">
<annotation>
<documentation> Indicates that the {@link Order} has been disapproved and is not eligible to serve. </documentation>
</annotation>
</enumeration>
<enumeration value="PAUSED">
<annotation>
<documentation> This is a legacy state. Paused status should be checked on {@link LineItems}s within the order. </documentation>
</annotation>
</enumeration>
<enumeration value="CANCELED">
<annotation>
<documentation> Indicates that the {@link Order} has been canceled and cannot serve. </documentation>
</annotation>
</enumeration>
<enumeration value="DELETED">
<annotation>
<documentation> Indicates that the {@link Order} has been deleted by DSM. </documentation>
</annotation>
</enumeration>
<enumeration value="UNKNOWN">
<annotation>
<documentation> The value returned if the actual value is not exposed by the requested API version. </documentation>
</annotation>
</enumeration>
</restriction>
</simpleType>
<simpleType name="ParseError.Reason">
<annotation>
<documentation> The reasons for the target error. </documentation>
</annotation>
<restriction base="xsd:string">
<enumeration value="UNPARSABLE">
<annotation>
<documentation> Indicates an error in parsing an attribute. </documentation>
</annotation>
</enumeration>
<enumeration value="UNKNOWN">
<annotation>
<documentation> The value returned if the actual value is not exposed by the requested API version. </documentation>
</annotation>
</enumeration>
</restriction>
</simpleType>
<simpleType name="PermissionError.Reason">
<annotation>
<documentation> Describes reasons for permission errors. </documentation>
</annotation>
<restriction base="xsd:string">
<enumeration value="PERMISSION_DENIED">
<annotation>
<documentation> User does not have the required permission for the request. </documentation>
</annotation>
</enumeration>
<enumeration value="UNKNOWN">
<annotation>
<documentation> The value returned if the actual value is not exposed by the requested API version. </documentation>
</annotation>
</enumeration>
</restriction>
</simpleType>
<simpleType name="ProgrammaticError.Reason">
<annotation>
<documentation> Possible error reasons for a programmatic error. </documentation>
</annotation>
<restriction base="xsd:string">
<enumeration value="AUDIENCE_EXTENSION_NOT_SUPPORTED">
<annotation>
<documentation> Audience extension is not supported by programmatic line items. </documentation>
</annotation>
</enumeration>
<enumeration value="AUTO_EXTENSION_DAYS_NOT_SUPPORTED">
<annotation>
<documentation> Auto extension days is not supported by programmatic line items. </documentation>
</annotation>
</enumeration>
<enumeration value="VIDEO_NOT_SUPPORTED">
<annotation>
<documentation> Video is currently not supported. </documentation>
</annotation>
</enumeration>
<enumeration value="ROADBLOCKING_NOT_SUPPORTED">
<annotation>
<documentation> Roadblocking is not supported by programmatic line items. </documentation>
</annotation>
</enumeration>
<enumeration value="INVALID_CREATIVE_ROTATION">
<annotation>
<documentation> Programmatic line items do not support {@link CreativeRotationType#SEQUENTIAL}. </documentation>
</annotation>
</enumeration>
<enumeration value="INVALID_LINE_ITEM_TYPE">
<annotation>
<documentation> Programmatic line items only support {@link LineItemType#STANDARD} and {@link LineItemType#SPONSORSHIP} if the relevant feature is on. </documentation>
</annotation>
</enumeration>
<enumeration value="INVALID_COST_TYPE">
<annotation>
<documentation> Programmatic line items only support {@link CostType#CPM}. </documentation>
</annotation>
</enumeration>
<enumeration value="SIZE_NOT_SUPPORTED">
<annotation>
<documentation> Programmatic line items only support a creative size that is supported by AdX. The list of supported sizes is maintained based on the list published in the help docs: <a href="https://support.google.com/adxseller/answer/1100453"> https://support.google.com/adxseller/answer/1100453</a> </documentation>
</annotation>
</enumeration>
<enumeration value="ZERO_COST_PER_UNIT_NOT_SUPPORTED">
<annotation>
<documentation> Zero cost per unit is not supported by programmatic line items. </documentation>
</annotation>
</enumeration>
<enumeration value="CANNOT_UPDATE_FIELD_FOR_APPROVED_LINE_ITEMS">
<annotation>
<documentation> Some fields cannot be updated on approved line items. </documentation>
</annotation>
</enumeration>
<enumeration value="CANNOT_CREATE_LINE_ITEM_FOR_APPROVED_ORDER">
<annotation>
<documentation> Creating a new line item in an approved order is not allowed. </documentation>
</annotation>
</enumeration>
<enumeration value="CANNOT_UPDATE_BACKFILL_WEB_PROPERTY_FOR_APPROVED_LINE_ITEMS">
<annotation>
<documentation> Cannot change backfill web property for a programmatic line item whose order has been approved. </documentation>
</annotation>
</enumeration>
<enumeration value="COST_PER_UNIT_TOO_LOW">
<annotation>
<documentation> Cost per unit is too low. It has to be at least 0.005 USD. </documentation>
</annotation>
</enumeration>
<enumeration value="UNKNOWN">
<annotation>
<documentation> The value returned if the actual value is not exposed by the requested API version. </documentation>
</annotation>
</enumeration>
</restriction>
</simpleType>
<simpleType name="PublisherQueryLanguageContextError.Reason">
<annotation>
<documentation> The reasons for the target error. </documentation>
</annotation>
<restriction base="xsd:string">
<enumeration value="UNEXECUTABLE">
<annotation>
<documentation> Indicates that there was an error executing the PQL. </documentation>
</annotation>
</enumeration>
<enumeration value="UNKNOWN">
<annotation>
<documentation> The value returned if the actual value is not exposed by the requested API version. </documentation>
</annotation>
</enumeration>
</restriction>
</simpleType>
<simpleType name="PublisherQueryLanguageSyntaxError.Reason">
<annotation>
<documentation> The reasons for the target error. </documentation>
</annotation>
<restriction base="xsd:string">
<enumeration value="UNPARSABLE">
<annotation>
<documentation> Indicates that there was a PQL syntax error. </documentation>
</annotation>
</enumeration>
<enumeration value="UNKNOWN">
<annotation>
<documentation> The value returned if the actual value is not exposed by the requested API version. </documentation>
</annotation>
</enumeration>
</restriction>
</simpleType>
<simpleType name="QuotaError.Reason">
<restriction base="xsd:string">
<enumeration value="EXCEEDED_QUOTA">
<annotation>
<documentation> The number of requests made per second is too high and has exceeded the allowable limit. The recommended approach to handle this error is to wait about 5 seconds and then retry the request. Note that this does not guarantee the request will succeed. If it fails again, try increasing the wait time. <p>Another way to mitigate this error is to limit requests to 8 per second for Ad Manager 360 accounts, or 2 per second for Ad Manager accounts. Once again this does not guarantee that every request will succeed, but may help reduce the number of times you receive this error. </documentation>
</annotation>
</enumeration>
<enumeration value="UNKNOWN">
<annotation>
<documentation> The value returned if the actual value is not exposed by the requested API version. </documentation>
</annotation>
</enumeration>
<enumeration value="REPORT_JOB_LIMIT">
<annotation>
<documentation> This user has exceeded the allowed number of new report requests per hour (this includes both reports run via the UI and reports run via {@link ReportService#runReportJob}). The recommended approach to handle this error is to wait about 10 minutes and then retry the request. Note that this does not guarantee the request will succeed. If it fails again, try increasing the wait time. <p>Another way to mitigate this error is to limit the number of new report requests to 250 per hour per user. Once again, this does not guarantee that every request will succeed, but may help reduce the number of times you receive this error. </documentation>
</annotation>
</enumeration>
</restriction>
</simpleType>
<simpleType name="RangeError.Reason">
<restriction base="xsd:string">
<enumeration value="TOO_HIGH"/>
<enumeration value="TOO_LOW"/>
<enumeration value="UNKNOWN">
<annotation>
<documentation> The value returned if the actual value is not exposed by the requested API version. </documentation>
</annotation>
</enumeration>
</restriction>
</simpleType>
<simpleType name="RegExError.Reason">
<annotation>
<documentation> The reasons for the target error. </documentation>
</annotation>
<restriction base="xsd:string">
<enumeration value="INVALID">
<annotation>
<documentation> Invalid value found. </documentation>
</annotation>
</enumeration>
<enumeration value="NULL">
<annotation>
<documentation> Null value found. </documentation>
</annotation>
</enumeration>
<enumeration value="UNKNOWN">
<annotation>
<documentation> The value returned if the actual value is not exposed by the requested API version. </documentation>
</annotation>
</enumeration>
</restriction>
</simpleType>
<simpleType name="RequestPlatformTargetingError.Reason">
<annotation>
<documentation> {@link ApiErrorReason} enum for the request platform targeting error. </documentation>
</annotation>
<restriction base="xsd:string">
<enumeration value="REQUEST_PLATFORM_TYPE_NOT_SUPPORTED_BY_LINE_ITEM_TYPE">
<annotation>
<documentation> The line item type does not support the targeted request platform type. </documentation>
</annotation>
</enumeration>
<enumeration value="UNKNOWN">
<annotation>
<documentation> The value returned if the actual value is not exposed by the requested API version. </documentation>
</annotation>
</enumeration>
</restriction>
</simpleType>
<simpleType name="RequiredCollectionError.Reason">
<restriction base="xsd:string">
<enumeration value="REQUIRED">
<annotation>
<documentation> A required collection is missing. </documentation>
</annotation>
</enumeration>
<enumeration value="TOO_LARGE">
<annotation>
<documentation> Collection size is too large. </documentation>
</annotation>
</enumeration>
<enumeration value="TOO_SMALL">
<annotation>
<documentation> Collection size is too small. </documentation>
</annotation>
</enumeration>
<enumeration value="UNKNOWN">
<annotation>
<documentation> The value returned if the actual value is not exposed by the requested API version. </documentation>
</annotation>
</enumeration>
</restriction>
</simpleType>
<simpleType name="RequiredError.Reason">
<annotation>
<documentation> The reasons for the target error. </documentation>
</annotation>
<restriction base="xsd:string">
<enumeration value="REQUIRED">
<annotation>
<documentation> Missing required field. </documentation>
</annotation>
</enumeration>
</restriction>
</simpleType>
<simpleType name="RequiredNumberError.Reason">
<annotation>
<documentation> Describes reasons for a number to be invalid. </documentation>
</annotation>
<restriction base="xsd:string">
<enumeration value="REQUIRED"/>
<enumeration value="TOO_LARGE"/>
<enumeration value="TOO_SMALL"/>
<enumeration value="TOO_LARGE_WITH_DETAILS"/>
<enumeration value="TOO_SMALL_WITH_DETAILS"/>
<enumeration value="UNKNOWN">
<annotation>
<documentation> The value returned if the actual value is not exposed by the requested API version. </documentation>
</annotation>
</enumeration>
</restriction>
</simpleType>
<simpleType name="RequiredSizeError.Reason">
<restriction base="xsd:string">
<enumeration value="REQUIRED">
<annotation>
<documentation> {@link Creative#size} or {@link LineItem#creativePlaceholders} size is missing. </documentation>
</annotation>
</enumeration>
<enumeration value="NOT_ALLOWED">
<annotation>
<documentation> {@link LineItemCreativeAssociation#sizes} must be a subset of {@link LineItem#creativePlaceholders} sizes. </documentation>
</annotation>
</enumeration>
<enumeration value="UNKNOWN">
<annotation>
<documentation> The value returned if the actual value is not exposed by the requested API version. </documentation>
</annotation>
</enumeration>
</restriction>
</simpleType>
<simpleType name="ReservationDetailsError.Reason">
<annotation>
<documentation> The reasons for the target error. </documentation>
</annotation>
<restriction base="xsd:string">
<enumeration value="UNLIMITED_UNITS_BOUGHT_NOT_ALLOWED">
<annotation>
<documentation> There is no limit on the number of ads delivered for a line item when you set {@link LineItem#duration} to be {@link LineItemSummary.Duration#NONE}. This can only be set for line items of type {@link LineItemType#PRICE_PRIORITY}. </documentation>
</annotation>
</enumeration>
<enumeration value="UNLIMITED_END_DATE_TIME_NOT_ALLOWED">
<annotation>
<documentation> {@link LineItem#unlimitedEndDateTime} can be set to true for only line items of type {@link LineItemType#SPONSORSHIP}, {@link LineItemType#NETWORK}, {@link LineItemType#PRICE_PRIORITY} and {@link LineItemType#HOUSE}. </documentation>
</annotation>
</enumeration>
<enumeration value="PERCENTAGE_UNITS_BOUGHT_TOO_HIGH">
<annotation>
<documentation> When {@link LineItem#lineItemType} is {@link LineItemType#SPONSORSHIP}, then {@link LineItem#unitsBought} represents the percentage of available impressions reserved. That value cannot exceed 100. </documentation>
</annotation>
</enumeration>
<enumeration value="DURATION_NOT_ALLOWED">
<annotation>
<documentation> The line item type does not support the specified duration. See {@link LineItemSummary.Duration} for allowed values. </documentation>
</annotation>
</enumeration>
<enumeration value="UNIT_TYPE_NOT_ALLOWED">
<annotation>
<documentation> The {@link LineItem#unitType} is not allowed for the given {@link LineItem#lineItemType}. See {@link UnitType} for allowed values. </documentation>
</annotation>
</enumeration>
<enumeration value="COST_TYPE_NOT_ALLOWED">
<annotation>
<documentation> The {@link LineItem#costType} is not allowed for the {@link LineItem#lineItemType}. See {@link CostType} for allowed values. </documentation>
</annotation>
</enumeration>
<enumeration value="COST_TYPE_UNIT_TYPE_MISMATCH_NOT_ALLOWED">
<annotation>
<documentation> When {@link LineItem#costType} is {@link CostType#CPM}, {@link LineItem#unitType} must be {@link UnitType#IMPRESSIONS} and when {@link LineItem#costType} is {@link CostType#CPC}, {@link LineItem#unitType} must be {@link UnitType#CLICKS}. </documentation>
</annotation>
</enumeration>
<enumeration value="LINE_ITEM_TYPE_NOT_ALLOWED">
<annotation>
<documentation> Inventory cannot be reserved for line items which are not of type {@link LineItemType#SPONSORSHIP} or {@link LineItemType#STANDARD}. </documentation>
</annotation>
</enumeration>
<enumeration value="NETWORK_REMNANT_ORDER_CANNOT_UPDATE_LINEITEM_TYPE">
<annotation>
<documentation> Network remnant line items cannot be changed to other line item types once delivery begins. This restriction does not apply to any new line items created in Ad Manager. </documentation>
</annotation>
</enumeration>
<enumeration value="BACKFILL_WEBPROPERTY_CODE_NOT_ALLOWED">
<annotation>
<documentation> A dynamic allocation web property can only be set on a line item of type AdSense or Ad Exchange. </documentation>
</annotation>
</enumeration>
<enumeration value="UNKNOWN">
<annotation>
<documentation> The value returned if the actual value is not exposed by the requested API version. </documentation>
</annotation>
</enumeration>
</restriction>
</simpleType>
<simpleType name="AudienceSegmentError.Reason">
<annotation>
<documentation> Reason of the given {@link AudienceSegmentError}. </documentation>
</annotation>
<restriction base="xsd:string">
<enumeration value="FIRST_PARTY_AUDIENCE_SEGMENT_NOT_SUPPORTED">
<annotation>
<documentation> First party audience segment is not supported. </documentation>
</annotation>
</enumeration>
<enumeration value="ONLY_RULE_BASED_FIRST_PARTY_AUDIENCE_SEGMENTS_CAN_BE_CREATED">
<annotation>
<documentation> Only rule-based first-party audience segments can be created. </documentation>
</annotation>
</enumeration>
<enumeration value="AUDIENCE_SEGMENT_ID_NOT_FOUND">
<annotation>
<documentation> Audience segment for the given id is not found. </documentation>
</annotation>
</enumeration>
<enumeration value="INVALID_AUDIENCE_SEGMENT_RULE">
<annotation>
<documentation> Audience segment rule is invalid. </documentation>
</annotation>
</enumeration>
<enumeration value="AUDIENCE_SEGMENT_RULE_TOO_LONG">
<annotation>
<documentation> Audience segment rule contains too many ad units and/or custom criteria. </documentation>
</annotation>
</enumeration>
<enumeration value="INVALID_AUDIENCE_SEGMENT_NAME">
<annotation>
<documentation> Audience segment name is invalid. </documentation>
</annotation>
</enumeration>
<enumeration value="DUPLICATE_AUDIENCE_SEGMENT_NAME">
<annotation>
<documentation> Audience segment with this name already exists. </documentation>
</annotation>
</enumeration>
<enumeration value="INVALID_AUDIENCE_SEGMENT_DESCRIPTION">
<annotation>
<documentation> Audience segment description is invalid. </documentation>
</annotation>
</enumeration>
<enumeration value="INVALID_AUDIENCE_SEGMENT_PAGEVIEWS">
<annotation>
<documentation> Audience segment pageviews value is invalid. It must be between 1 and 12. </documentation>
</annotation>
</enumeration>
<enumeration value="INVALID_AUDIENCE_SEGMENT_RECENCY">
<annotation>
<documentation> Audience segment recency value is invalid. It must be between 1 and 90 if pageviews > 1. </documentation>
</annotation>
</enumeration>
<enumeration value="INVALID_AUDIENCE_SEGMENT_MEMBERSHIP_EXPIRATION">
<annotation>
<documentation> Audience segment membership expiration value is invalid. It must be between 1 and 180. </documentation>
</annotation>
</enumeration>
<enumeration value="INVALID_AUDIENCE_SEGMENT_CUSTOM_KEY_NAME">
<annotation>
<documentation> The given custom key cannot be part of audience segment rule due to unsupported characters. </documentation>
</annotation>
</enumeration>
<enumeration value="INVALID_AUDIENCE_SEGMENT_CUSTOM_VALUE_NAME">
<annotation>
<documentation> The given custom value cannot be part of audience segment rule due to unsupported characters. </documentation>
</annotation>
</enumeration>
<enumeration value="INVALID_AUDIENCE_SEGMENT_CUSTOM_VALUE_MATCH_TYPE">
<annotation>
<documentation> Broad-match custom value cannot be part of audience segment rule. </documentation>
</annotation>
</enumeration>
<enumeration value="INVALID_NESTED_FIRST_PARTY_AUDIENCE_SEGMENT">
<annotation>
<documentation> Audience segment rule cannot contain itself. </documentation>
</annotation>
</enumeration>
<enumeration value="SHARED_SELLING_PARTNER_ROOT_CANNOT_BE_INCLUDED">
<annotation>
<documentation> Audience segment rule cannot contain shared selling inventory unit. </documentation>
</annotation>
</enumeration>
<enumeration value="INVALID_NESTED_THIRD_PARTY_AUDIENCE_SEGMENT">
<annotation>
<documentation> Audience segment rule cannot contain a nested third-party segment. </documentation>
</annotation>
</enumeration>
<enumeration value="INACTIVE_NESTED_AUDIENCE_SEGMENT">
<annotation>
<documentation> Audience segment rule cannot contain a nested inactive segment. </documentation>
</annotation>
</enumeration>
<enumeration value="AUDIENCE_SEGMENT_GLOBAL_LICENSE_ERROR">
<annotation>
<documentation> An error occurred when purchasing global licenses. </documentation>
</annotation>
</enumeration>
<enumeration value="SEGMENT_VIOLATED_POLICY">
<annotation>
<documentation> Segment cannot be activated as it violates Google's Platform Policy. </documentation>
</annotation>
</enumeration>
<enumeration value="UNKNOWN">
<annotation>
<documentation> The value returned if the actual value is not exposed by the requested API version. </documentation>
</annotation>
</enumeration>
</restriction>
</simpleType>
<simpleType name="ServerError.Reason">
<annotation>
<documentation> Describes reasons for server errors </documentation>
</annotation>
<restriction base="xsd:string">
<enumeration value="SERVER_ERROR">
<annotation>
<documentation> Indicates that an unexpected error occured. </documentation>
</annotation>
</enumeration>
<enumeration value="SERVER_BUSY">
<annotation>
<documentation> Indicates that the server is currently experiencing a high load. Please wait and try your request again. </documentation>
</annotation>
</enumeration>
<enumeration value="UNKNOWN">
<annotation>
<documentation> The value returned if the actual value is not exposed by the requested API version. </documentation>
</annotation>
</enumeration>
</restriction>
</simpleType>
<simpleType name="SetTopBoxLineItemError.Reason">
<annotation>
<documentation> Reason for set-top box error. </documentation>
</annotation>
<restriction base="xsd:string">
<enumeration value="NON_SET_TOP_BOX_AD_UNIT_TARGETED">
<annotation>
<documentation> The set-top box line item cannot target an ad unit that doesn't have an external set-top box channel ID. </documentation>
</annotation>
</enumeration>
<enumeration value="AT_LEAST_ONE_AD_UNIT_MUST_BE_TARGETED">
<annotation>
<documentation> The set-top box line item must target at least one ad unit. </documentation>
</annotation>
</enumeration>
<enumeration value="CANNOT_EXCLUDE_AD_UNITS">
<annotation>
<documentation> The set-top box line item cannot exclude ad units. </documentation>
</annotation>
</enumeration>
<enumeration value="POD_POSITION_OUT_OF_RANGE">
<annotation>
<documentation> The set-top box line item can only target pod positions 1 - 15. </documentation>
</annotation>
</enumeration>
<enumeration value="MIDROLL_POSITION_OUT_OF_RANGE">
<annotation>
<documentation> The set-top box line item can only target midroll positions 4 - 100. </documentation>
</annotation>
</enumeration>
<enumeration value="FEATURE_NOT_ENABLED">
<annotation>
<documentation> The set-top box feature is not enabled. </documentation>
</annotation>
</enumeration>
<enumeration value="INVALID_ENVIRONMENT_TYPE">
<annotation>
<documentation> Only {@link EnvironmentType#VIDEO_PLAYER} is supported for set-top box line items. </documentation>
</annotation>
</enumeration>
<enumeration value="COMPANIONS_NOT_SUPPORTED">
<annotation>
<documentation> Companions are not supported for set-top box line items. </documentation>
</annotation>
</enumeration>
<enumeration value="INVALID_CREATIVE_SIZE">
<annotation>
<documentation> Set-top box line items only support sizes supported by Canoe. </documentation>
</annotation>
</enumeration>
<enumeration value="INVALID_LINE_ITEM_TYPE">
<annotation>
<documentation> Set-top box line items only support {@link LineItemType#STANDARD}, {@link LineItemType#HOUSE}, and {@link LineItemType#SPONSORSHIP} line item types. </documentation>
</annotation>
</enumeration>
<enumeration value="ORDERS_WITH_STANDARD_LINE_ITEMS_CANNOT_CONTAIN_HOUSE_OR_SPONSORSHIP_LINE_ITEMS">
<annotation>
<documentation> {@link Order orders} containing {@link LineItemType#STANDARD} set-top box line items cannot contain set-top box line items of type {@link LineItemType#HOUSE} or {@link LineItemType#SPONSORSHIP}. </documentation>
</annotation>
</enumeration>
<enumeration value="INVALID_COST_TYPE">
<annotation>
<documentation> Set-top box line items only support {@link CostType#CPM}. </documentation>
</annotation>
</enumeration>
<enumeration value="COST_PER_UNIT_NOT_ALLOWED">
<annotation>
<documentation> Set-top box line items do not support a cost per unit. </documentation>
</annotation>
</enumeration>
<enumeration value="DISCOUNT_NOT_ALLOWED">
<annotation>
<documentation> Set-top box line items do not support discounts. </documentation>
</annotation>
</enumeration>
<enumeration value="FRONTLOADED_DELIVERY_RATE_NOT_SUPPORTED">
<annotation>
<documentation> Set-top box line items do not support {@link DeliveryRateType#FRONTLOADED}. </documentation>
</annotation>
</enumeration>
<enumeration value="INVALID_LINE_ITEM_STATUS_CHANGE">
<annotation>
<documentation> Set-top box line items cannot go from a state that is ready to be synced to a state that is not ready to be synced. </documentation>
</annotation>
</enumeration>
<enumeration value="INVALID_LINE_ITEM_PRIORITY">
<annotation>
<documentation> Set-top box line items can only have certain priorities for different {@link ReservationType reservation types}: <ul> <li>{@link ReservationType#SPONSORSHIP} => 1</li> <li>{@link ReservationType#HOUSE} => 16</li> <li>{@link ReservationType#STANDARD} => Between 1 and 16 inclusive.</li> </ul> </documentation>
</annotation>
</enumeration>
<enumeration value="SYNC_REVISION_NOT_INCREASING">
<annotation>
<documentation> When a set-top box line item is pushed to Canoe, a revision number is used to keep track of the last version of the line item that Ad Manager synced with Canoe. The only change allowed on revisions within Ad Manager is increasing the revision number. </documentation>
</annotation>
</enumeration>
<enumeration value="SYNC_REVISION_MUST_BE_GREATER_THAN_ZERO">
<annotation>
<documentation> When a set-top box line item is pushed to Canoe, a revision number is used to keep track of the last version of the line item that Ad Manager synced with Canoe. Sync revisions begin at one and can only increase in value. </documentation>
</annotation>
</enumeration>
<enumeration value="CANNOT_UNARCHIVE_SET_TOP_BOX_LINE_ITEMS">
<annotation>
<documentation> Set Top box line items cannot be unarchived. </documentation>
</annotation>
</enumeration>
<enumeration value="COPY_SET_TOP_BOX_ENABLED_LINE_ITEM_NOT_ALLOWED">
<annotation>
<documentation> Set-top box enabled line items cannot be copied for V0 of the video Canoe campaign push. </documentation>
</annotation>
</enumeration>
<enumeration value="INVALID_LINE_ITEM_TYPE_CHANGE">
<annotation>
<documentation> Standard set-top box line items cannot be updated to be {@link LineItemType#House} or {@link LineItemType#Sponsorship} line items and vice versa. </documentation>
</annotation>
</enumeration>
<enumeration value="CREATIVE_ROTATION_TYPE_MUST_BE_EVENLY_OR_WEIGHTED">
<annotation>
<documentation> Set-top box line items can only have a creative rotation type of {@link CreativeRotationType.EVEN} or {@link CreativeRotationType#MANUAL}. </documentation>
</annotation>
</enumeration>
<enumeration value="INVALID_FREQUENCY_CAP_TIME_UNIT">
<annotation>
<documentation> Set-top box line items can only have frequency capping with time units of {@link TimeUnit#DAY}, {@link TimeUnit#HOUR}, {@link TimeUnit#POD}, or {@link TimeUnit#STREAM}. </documentation>
</annotation>
</enumeration>
<enumeration value="INVALID_FREQUENCY_CAP_TIME_RANGE">
<annotation>
<documentation> Set-top box line items can only have specific time ranges for certain time units: <ul> <li>{@link TimeUnit#HOUR} => 1, 2, 6</li> <li>{@link TimeUnit#DAY} => 1, 3</li> </ul> </documentation>
</annotation>
</enumeration>
<enumeration value="INVALID_PRIMARY_GOAL_UNIT_TYPE">
<annotation>
<documentation> Set-top box line items can only have a unit type of {@link UnitType#IMPRESSIONS}. </documentation>
</annotation>
</enumeration>
<enumeration value="UNKNOWN">
<annotation>
<documentation> The value returned if the actual value is not exposed by the requested API version. </documentation>
</annotation>
</enumeration>
</restriction>
</simpleType>
<simpleType name="StatementError.Reason">
<restriction base="xsd:string">
<enumeration value="VARIABLE_NOT_BOUND_TO_VALUE">
<annotation>
<documentation> A bind variable has not been bound to a value. </documentation>
</annotation>
</enumeration>
<enumeration value="UNKNOWN">
<annotation>
<documentation> The value returned if the actual value is not exposed by the requested API version. </documentation>
</annotation>
</enumeration>
</restriction>
</simpleType>
<simpleType name="StringFormatError.Reason">
<annotation>
<documentation> The reasons for the target error. </documentation>
</annotation>
<restriction base="xsd:string">
<enumeration value="UNKNOWN"/>
<enumeration value="ILLEGAL_CHARS">
<annotation>
<documentation> The input string value contains disallowed characters. </documentation>
</annotation>
</enumeration>
<enumeration value="INVALID_FORMAT">
<annotation>
<documentation> The input string value is invalid for the associated field. </documentation>
</annotation>
</enumeration>
</restriction>
</simpleType>
<simpleType name="StringLengthError.Reason">
<restriction base="xsd:string">
<enumeration value="TOO_LONG"/>
<enumeration value="TOO_SHORT"/>
<enumeration value="UNKNOWN">
<annotation>
<documentation> The value returned if the actual value is not exposed by the requested API version. </documentation>
</annotation>
</enumeration>
</restriction>
</simpleType>
<simpleType name="TeamError.Reason">
<annotation>
<documentation> The reasons for the target error. </documentation>
</annotation>
<restriction base="xsd:string">
<enumeration value="ENTITY_NOT_ON_USERS_TEAMS">
<annotation>
<documentation> User cannot use this entity because it is not on any of the user's teams. </documentation>
</annotation>
</enumeration>
<enumeration value="AD_UNITS_NOT_ON_ORDER_TEAMS">
<annotation>
<documentation> The targeted or excluded ad unit must be on the order's teams. </documentation>
</annotation>
</enumeration>
<enumeration value="PLACEMENTS_NOT_ON_ORDER_TEAMS">
<annotation>
<documentation> The targeted placement must be on the order's teams. </documentation>
</annotation>
</enumeration>
<enumeration value="MISSING_USERS_TEAM">
<annotation>
<documentation> Entity cannot be created because it is not on any of the user's teams. </documentation>
</annotation>
</enumeration>
<enumeration value="ALL_TEAM_ASSOCIATION_NOT_ALLOWED">
<annotation>
<documentation> A team that gives access to all entities of a given type cannot be associated with an entity of that type. </documentation>
</annotation>
</enumeration>
<enumeration value="INVALID_TEAM_ASSIGNMENT">
<annotation>
<documentation> The assignment of team to entities is invalid. </documentation>
</annotation>
</enumeration>
<enumeration value="ALL_TEAM_ACCESS_OVERRIDE_NOT_ALLOWED">
<annotation>
<documentation> The all entities team access type cannot be overridden. </documentation>
</annotation>
</enumeration>
<enumeration value="CANNOT_UPDATE_INACTIVE_TEAM">
<annotation>
<documentation> Cannot modify or create a team with an inactive status. </documentation>
</annotation>
</enumeration>
<enumeration value="UNKNOWN">
<annotation>
<documentation> The value returned if the actual value is not exposed by the requested API version. </documentation>
</annotation>
</enumeration>
</restriction>
</simpleType>
<simpleType name="TechnologyTargetingError.Reason">
<annotation>
<documentation> The reasons for the target error. </documentation>
</annotation>
<restriction base="xsd:string">
<enumeration value="MOBILE_LINE_ITEM_CONTAINS_WEB_TECH_CRITERIA">
<annotation>
<documentation> Mobile line item cannot target web-only targeting criteria. </documentation>
</annotation>
</enumeration>
<enumeration value="WEB_LINE_ITEM_CONTAINS_MOBILE_TECH_CRITERIA">
<annotation>
<documentation> Web line item cannot target mobile-only targeting criteria. </documentation>
</annotation>
</enumeration>
<enumeration value="MOBILE_CARRIER_TARGETING_FEATURE_NOT_ENABLED">
<annotation>
<documentation> The mobile carrier targeting feature is not enabled. </documentation>
</annotation>
</enumeration>
<enumeration value="DEVICE_CAPABILITY_TARGETING_FEATURE_NOT_ENABLED">
<annotation>
<documentation> The device capability targeting feature is not enabled. </documentation>
</annotation>
</enumeration>
<enumeration value="UNKNOWN">
<annotation>
<documentation> The value returned if the actual value is not exposed by the requested API version. </documentation>
</annotation>
</enumeration>
</restriction>
</simpleType>
<simpleType name="TemplateInstantiatedCreativeError.Reason">
<annotation>
<documentation> The reason for the error </documentation>
</annotation>
<restriction base="xsd:string">
<enumeration value="INACTIVE_CREATIVE_TEMPLATE">
<annotation>
<documentation> A new creative cannot be created from an inactive creative template. </documentation>
</annotation>
</enumeration>
<enumeration value="FILE_TYPE_NOT_ALLOWED">
<annotation>
<documentation> An uploaded file type is not allowed </documentation>
</annotation>
</enumeration>
<enumeration value="UNKNOWN">
<annotation>
<documentation> The value returned if the actual value is not exposed by the requested API version. </documentation>
</annotation>
</enumeration>
</restriction>
</simpleType>
<simpleType name="TimeZoneError.Reason">
<annotation>
<documentation> Describes reasons for invalid timezone. </documentation>
</annotation>
<restriction base="xsd:string">
<enumeration value="INVALID_TIMEZONE_ID">
<annotation>
<documentation> Indicates that the timezone ID provided is not supported. </documentation>
</annotation>
</enumeration>
<enumeration value="TIMEZONE_ID_IN_WRONG_FORMAT">
<annotation>
<documentation> Indicates that the timezone ID provided is in the wrong format. The timezone ID must be in tz database format (e.g. "America/Los_Angeles"). </documentation>
</annotation>
</enumeration>
<enumeration value="UNKNOWN">
<annotation>
<documentation> The value returned if the actual value is not exposed by the requested API version. </documentation>
</annotation>
</enumeration>
</restriction>
</simpleType>
<simpleType name="TranscodingError.Reason">
<annotation>
<documentation> The type of transcode request rejection. </documentation>
</annotation>
<restriction base="xsd:string">
<enumeration value="CANNOT_COPY_CREATIVE_PENDING_TRANSCODE">
<annotation>
<documentation> The request to copy the creative(s) was rejected because the source is not transcoded. </documentation>
</annotation>
</enumeration>
<enumeration value="CANNOT_COPY_INVALID_CREATIVE">
<annotation>
<documentation> The request to copy the creative(s) was rejected because the source is invalid. </documentation>
</annotation>
</enumeration>
<enumeration value="TRANSCODING_IS_IN_PROGRESS">
<annotation>
<documentation> The creative is still being transcoded or processed. Please try again later. </documentation>
</annotation>
</enumeration>
<enumeration value="UNKNOWN">
<annotation>
<documentation> The value returned if the actual value is not exposed by the requested API version. </documentation>
</annotation>
</enumeration>
</restriction>
</simpleType>
<simpleType name="UserDomainTargetingError.Reason">
<annotation>
<documentation> {@link ApiErrorReason} enum for user domain targeting error. </documentation>
</annotation>
<restriction base="xsd:string">
<enumeration value="INVALID_DOMAIN_NAMES">
<annotation>
<documentation> Invalid domain names. Domain names must be at most 67 characters long. And must contain only alphanumeric characters and hyphens. </documentation>
</annotation>
</enumeration>
<enumeration value="UNKNOWN">
<annotation>
<documentation> The value returned if the actual value is not exposed by the requested API version. </documentation>
</annotation>
</enumeration>
</restriction>
</simpleType>
<simpleType name="VideoPositionTargetingError.Reason">
<annotation>
<documentation> The reasons for the video position targeting error. </documentation>
</annotation>
<restriction base="xsd:string">
<enumeration value="CANNOT_MIX_BUMPER_AND_NON_BUMPER_TARGETING">
<annotation>
<documentation> Video position targeting cannot contain both bumper and non-bumper targeting values. </documentation>
</annotation>
</enumeration>
<enumeration value="INVALID_BUMPER_TARGETING">
<annotation>
<documentation> The bumper video position targeting is invalid. </documentation>
</annotation>
</enumeration>
<enumeration value="CAN_ONLY_TARGET_CUSTOM_AD_SPOTS">
<annotation>
<documentation> Only custom spot {@link AdSpot} objects can be targeted. </documentation>
</annotation>
</enumeration>
<enumeration value="UNKNOWN">
<annotation>
<documentation> The value returned if the actual value is not exposed by the requested API version. </documentation>
</annotation>
</enumeration>
</restriction>
</simpleType>
<element name="createOrders">
<annotation>
<documentation> Creates new {@link Order} objects. </documentation>
</annotation>
<complexType>
<sequence>
<element maxOccurs="unbounded" minOccurs="0" name="orders" type="tns:Order"/>
</sequence>
</complexType>
</element>
<element name="createOrdersResponse">
<complexType>
<sequence>
<element maxOccurs="unbounded" minOccurs="0" name="rval" type="tns:Order"/>
</sequence>
</complexType>
</element>
<element name="ApiExceptionFault" type="tns:ApiException">
<annotation>
<documentation> A fault element of type ApiException. </documentation>
</annotation>
</element>
<element name="getOrdersByStatement">
<annotation>
<documentation> Gets an {@link OrderPage} of {@link Order} objects that satisfy the given {@link Statement#query}. The following fields are supported for filtering: <table> <tr> <th scope="col">PQL Property</th> <th scope="col">Object Property</th> </tr> <tr> <td>{@code advertiserId}</td> <td>{@link Order#advertiserId}</td> </tr> <tr> <td>{@code endDateTime}</td> <td>{@link Order#endDateTime}</td> </tr> <tr> <td>{@code id}</td> <td>{@link Order#id}</td> </tr> <tr> <td>{@code name}</td> <td>{@link Order#name}</td> </tr> <tr> <td>{@code salespersonId}</td> <td>{@link Order#salespersonId}</td> </tr> <tr> <td>{@code startDateTime}</td> <td>{@link Order#startDateTime}</td> </tr> <tr> <td>{@code status}</td> <td>{@link Order#status}</td> </tr> <tr> <td>{@code traffickerId}</td> <td>{@link Order#traffickerId}</td> </tr> <tr> <td>{@code lastModifiedDateTime}</td> <td>{@link Order#lastModifiedDateTime}</td> </tr> </table> </documentation>
</annotation>
<complexType>
<sequence>
<element maxOccurs="1" minOccurs="0" name="filterStatement" type="tns:Statement"/>
</sequence>
</complexType>
</element>
<element name="getOrdersByStatementResponse">
<complexType>
<sequence>
<element maxOccurs="1" minOccurs="0" name="rval" type="tns:OrderPage"/>
</sequence>
</complexType>
</element>
<element name="performOrderAction">
<annotation>
<documentation> Performs actions on {@link Order} objects that match the given {@link Statement#query}. </documentation>
</annotation>
<complexType>
<sequence>
<element maxOccurs="1" minOccurs="0" name="orderAction" type="tns:OrderAction"/>
<element maxOccurs="1" minOccurs="0" name="filterStatement" type="tns:Statement"/>
</sequence>
</complexType>
</element>
<element name="performOrderActionResponse">
<complexType>
<sequence>
<element maxOccurs="1" minOccurs="0" name="rval" type="tns:UpdateResult"/>
</sequence>
</complexType>
</element>
<element name="updateOrders">
<annotation>
<documentation> Updates the specified {@link Order} objects. </documentation>
</annotation>
<complexType>
<sequence>
<element maxOccurs="unbounded" minOccurs="0" name="orders" type="tns:Order"/>
</sequence>
</complexType>
</element>
<element name="updateOrdersResponse">
<complexType>
<sequence>
<element maxOccurs="unbounded" minOccurs="0" name="rval" type="tns:Order"/>
</sequence>
</complexType>
</element>
<element name="RequestHeader" type="tns:SoapRequestHeader"/>
<element name="ResponseHeader" type="tns:SoapResponseHeader"/>
</schema>
</wsdl:types>
<wsdl:message name="RequestHeader">
<wsdl:part element="tns:RequestHeader" name="RequestHeader"/>
</wsdl:message>
<wsdl:message name="ResponseHeader">
<wsdl:part element="tns:ResponseHeader" name="ResponseHeader"/>
</wsdl:message>
<wsdl:message name="createOrdersRequest">
<wsdl:part element="tns:createOrders" name="parameters"/>
</wsdl:message>
<wsdl:message name="createOrdersResponse">
<wsdl:part element="tns:createOrdersResponse" name="parameters"/>
</wsdl:message>
<wsdl:message name="ApiException">
<wsdl:part element="tns:ApiExceptionFault" name="ApiException"/>
</wsdl:message>
<wsdl:message name="getOrdersByStatementRequest">
<wsdl:part element="tns:getOrdersByStatement" name="parameters"/>
</wsdl:message>
<wsdl:message name="getOrdersByStatementResponse">
<wsdl:part element="tns:getOrdersByStatementResponse" name="parameters"/>
</wsdl:message>
<wsdl:message name="performOrderActionRequest">
<wsdl:part element="tns:performOrderAction" name="parameters"/>
</wsdl:message>
<wsdl:message name="performOrderActionResponse">
<wsdl:part element="tns:performOrderActionResponse" name="parameters"/>
</wsdl:message>
<wsdl:message name="updateOrdersRequest">
<wsdl:part element="tns:updateOrders" name="parameters"/>
</wsdl:message>
<wsdl:message name="updateOrdersResponse">
<wsdl:part element="tns:updateOrdersResponse" name="parameters"/>
</wsdl:message>
<wsdl:portType name="OrderServiceInterface">
<wsdl:documentation> Provides methods for creating, updating and retrieving {@link Order} objects. <p>An order is a grouping of {@link LineItem} objects. Line items have a many-to-one relationship with orders, meaning each line item can belong to only one order, but orders can have multiple line items. An order can be used to manage the line items it contains. </wsdl:documentation>
<wsdl:operation name="createOrders">
<wsdl:documentation> Creates new {@link Order} objects. </wsdl:documentation>
<wsdl:input message="tns:createOrdersRequest" name="createOrdersRequest"/>
<wsdl:output message="tns:createOrdersResponse" name="createOrdersResponse"/>
<wsdl:fault message="tns:ApiException" name="ApiException"/>
</wsdl:operation>
<wsdl:operation name="getOrdersByStatement">
<wsdl:documentation> Gets an {@link OrderPage} of {@link Order} objects that satisfy the given {@link Statement#query}. The following fields are supported for filtering: <table> <tr> <th scope="col">PQL Property</th> <th scope="col">Object Property</th> </tr> <tr> <td>{@code advertiserId}</td> <td>{@link Order#advertiserId}</td> </tr> <tr> <td>{@code endDateTime}</td> <td>{@link Order#endDateTime}</td> </tr> <tr> <td>{@code id}</td> <td>{@link Order#id}</td> </tr> <tr> <td>{@code name}</td> <td>{@link Order#name}</td> </tr> <tr> <td>{@code salespersonId}</td> <td>{@link Order#salespersonId}</td> </tr> <tr> <td>{@code startDateTime}</td> <td>{@link Order#startDateTime}</td> </tr> <tr> <td>{@code status}</td> <td>{@link Order#status}</td> </tr> <tr> <td>{@code traffickerId}</td> <td>{@link Order#traffickerId}</td> </tr> <tr> <td>{@code lastModifiedDateTime}</td> <td>{@link Order#lastModifiedDateTime}</td> </tr> </table> </wsdl:documentation>
<wsdl:input message="tns:getOrdersByStatementRequest" name="getOrdersByStatementRequest"/>
<wsdl:output message="tns:getOrdersByStatementResponse" name="getOrdersByStatementResponse"/>
<wsdl:fault message="tns:ApiException" name="ApiException"/>
</wsdl:operation>
<wsdl:operation name="performOrderAction">
<wsdl:documentation> Performs actions on {@link Order} objects that match the given {@link Statement#query}. </wsdl:documentation>
<wsdl:input message="tns:performOrderActionRequest" name="performOrderActionRequest"/>
<wsdl:output message="tns:performOrderActionResponse" name="performOrderActionResponse"/>
<wsdl:fault message="tns:ApiException" name="ApiException"/>
</wsdl:operation>
<wsdl:operation name="updateOrders">
<wsdl:documentation> Updates the specified {@link Order} objects. </wsdl:documentation>
<wsdl:input message="tns:updateOrdersRequest" name="updateOrdersRequest"/>
<wsdl:output message="tns:updateOrdersResponse" name="updateOrdersResponse"/>
<wsdl:fault message="tns:ApiException" name="ApiException"/>
</wsdl:operation>
</wsdl:portType>
<wsdl:binding name="OrderServiceSoapBinding" type="tns:OrderServiceInterface">
<wsdlsoap:binding style="document" transport="http://schemas.xmlsoap.org/soap/http"/>
<wsdl:operation name="createOrders">
<wsdlsoap:operation soapAction=""/>
<wsdl:input name="createOrdersRequest">
<wsdlsoap:header message="tns:RequestHeader" part="RequestHeader" use="literal"/>
<wsdlsoap:body use="literal"/>
</wsdl:input>
<wsdl:output name="createOrdersResponse">
<wsdlsoap:header message="tns:ResponseHeader" part="ResponseHeader" use="literal"/>
<wsdlsoap:body use="literal"/>
</wsdl:output>
<wsdl:fault name="ApiException">
<wsdlsoap:fault name="ApiException" use="literal"/>
</wsdl:fault>
</wsdl:operation>
<wsdl:operation name="getOrdersByStatement">
<wsdlsoap:operation soapAction=""/>
<wsdl:input name="getOrdersByStatementRequest">
<wsdlsoap:header message="tns:RequestHeader" part="RequestHeader" use="literal"/>
<wsdlsoap:body use="literal"/>
</wsdl:input>
<wsdl:output name="getOrdersByStatementResponse">
<wsdlsoap:header message="tns:ResponseHeader" part="ResponseHeader" use="literal"/>
<wsdlsoap:body use="literal"/>
</wsdl:output>
<wsdl:fault name="ApiException">
<wsdlsoap:fault name="ApiException" use="literal"/>
</wsdl:fault>
</wsdl:operation>
<wsdl:operation name="performOrderAction">
<wsdlsoap:operation soapAction=""/>
<wsdl:input name="performOrderActionRequest">
<wsdlsoap:header message="tns:RequestHeader" part="RequestHeader" use="literal"/>
<wsdlsoap:body use="literal"/>
</wsdl:input>
<wsdl:output name="performOrderActionResponse">
<wsdlsoap:header message="tns:ResponseHeader" part="ResponseHeader" use="literal"/>
<wsdlsoap:body use="literal"/>
</wsdl:output>
<wsdl:fault name="ApiException">
<wsdlsoap:fault name="ApiException" use="literal"/>
</wsdl:fault>
</wsdl:operation>
<wsdl:operation name="updateOrders">
<wsdlsoap:operation soapAction=""/>
<wsdl:input name="updateOrdersRequest">
<wsdlsoap:header message="tns:RequestHeader" part="RequestHeader" use="literal"/>
<wsdlsoap:body use="literal"/>
</wsdl:input>
<wsdl:output name="updateOrdersResponse">
<wsdlsoap:header message="tns:ResponseHeader" part="ResponseHeader" use="literal"/>
<wsdlsoap:body use="literal"/>
</wsdl:output>
<wsdl:fault name="ApiException">
<wsdlsoap:fault name="ApiException" use="literal"/>
</wsdl:fault>
</wsdl:operation>
</wsdl:binding>
<wsdl:service name="OrderService">
<wsdl:port binding="tns:OrderServiceSoapBinding" name="OrderServiceInterfacePort">
<wsdlsoap:address location="https://ads.google.com/apis/ads/publisher/v202305/OrderService"/>
</wsdl:port>
</wsdl:service>
</wsdl:definitions>
"""

from __future__ import annotations
from typing import Optional, Literal, List
from pydantic import Field

from .common import GAMSOAPBaseModel, DateTime, Money, AppliedLabel, BaseCustomFieldValue


OrderStatus = Literal[
    "DRAFT", "PENDING_APPROVAL", "APPROVED", "DISAPPROVED", "PAUSED", "CANCELED", "DELETED", "UNKNOWN"
]


class Order(GAMSOAPBaseModel):
    """
    <complexType name="Order">
    <annotation>
    <documentation> An {@code Order} represents a grouping of individual {@link LineItem} objects, each of which fulfill an ad request from a particular advertiser. </documentation>
    </annotation>
    <sequence>
    <element maxOccurs="1" minOccurs="0" name="id" type="xsd:long">
    <annotation>
    <documentation> The unique ID of the {@code Order}. This value is readonly and is assigned by Google. </documentation>
    </annotation>
    </element>
    <element maxOccurs="1" minOccurs="0" name="name" type="xsd:string">
    <annotation>
    <documentation> The name of the {@code Order}. This value is required to create an order and has a maximum length of 255 characters. </documentation>
    </annotation>
    </element>
    <element maxOccurs="1" minOccurs="0" name="startDateTime" type="tns:DateTime">
    <annotation>
    <documentation> The date and time at which the {@code Order} and its associated line items are eligible to begin serving. This attribute is readonly and is derived from the line item of the order which has the earliest {@link LineItem#startDateTime}. </documentation>
    </annotation>
    </element>
    <element maxOccurs="1" minOccurs="0" name="endDateTime" type="tns:DateTime">
    <annotation>
    <documentation> The date and time at which the {@code Order} and its associated line items stop being served. This attribute is readonly and is derived from the line item of the order which has the latest {@link LineItem#endDateTime}. </documentation>
    </annotation>
    </element>
    <element maxOccurs="1" minOccurs="0" name="unlimitedEndDateTime" type="xsd:boolean">
    <annotation>
    <documentation> Specifies whether or not the {@code Order} has an unlimited end date. This attribute is readonly and is {@code true} if any of the order's line items has {@link LineItem#unlimitedEndDateTime} set to {@code true}. </documentation>
    </annotation>
    </element>
    <element maxOccurs="1" minOccurs="0" name="status" type="tns:OrderStatus">
    <annotation>
    <documentation> The status of the {@code Order}. This attribute is read-only. </documentation>
    </annotation>
    </element>
    <element maxOccurs="1" minOccurs="0" name="isArchived" type="xsd:boolean">
    <annotation>
    <documentation> The archival status of the {@code Order}. This attribute is readonly. </documentation>
    </annotation>
    </element>
    <element maxOccurs="1" minOccurs="0" name="notes" type="xsd:string">
    <annotation>
    <documentation> Provides any additional notes that may annotate the {@code Order}. This attribute is optional and has a maximum length of 65,535 characters. </documentation>
    </annotation>
    </element>
    <element maxOccurs="1" minOccurs="0" name="externalOrderId" type="xsd:int">
    <annotation>
    <documentation> An arbitrary ID to associate to the {@code Order}, which can be used as a key to an external system. This value is optional. </documentation>
    </annotation>
    </element>
    <element maxOccurs="1" minOccurs="0" name="poNumber" type="xsd:string">
    <annotation>
    <documentation> The purchase order number for the {@code Order}. This value is optional and has a maximum length of 63 characters. </documentation>
    </annotation>
    </element>
    <element maxOccurs="1" minOccurs="0" name="currencyCode" type="xsd:string">
    <annotation>
    <documentation> The ISO currency code for the currency used by the {@code Order}. This value is read-only and is the network's currency code. </documentation>
    </annotation>
    </element>
    <element maxOccurs="1" minOccurs="0" name="advertiserId" type="xsd:long">
    <annotation>
    <documentation> The unique ID of the {@link Company}, which is of type {@link Company.Type#ADVERTISER}, to which this order belongs. This attribute is required. </documentation>
    </annotation>
    </element>
    <element maxOccurs="unbounded" minOccurs="0" name="advertiserContactIds" type="xsd:long">
    <annotation>
    <documentation> List of IDs for advertiser contacts of the order. </documentation>
    </annotation>
    </element>
    <element maxOccurs="1" minOccurs="0" name="agencyId" type="xsd:long">
    <annotation>
    <documentation> The unique ID of the {@link Company}, which is of type {@link Company.Type#AGENCY}, with which this order is associated. This attribute is optional. </documentation>
    </annotation>
    </element>
    <element maxOccurs="unbounded" minOccurs="0" name="agencyContactIds" type="xsd:long">
    <annotation>
    <documentation> List of IDs for agency contacts of the order. </documentation>
    </annotation>
    </element>
    <element maxOccurs="1" minOccurs="0" name="creatorId" type="xsd:long">
    <annotation>
    <documentation> The unique ID of the {@link User} who created the {@code Order} on behalf of the advertiser. This value is readonly and is assigned by Google. </documentation>
    </annotation>
    </element>
    <element maxOccurs="1" minOccurs="0" name="traffickerId" type="xsd:long">
    <annotation>
    <documentation> The unique ID of the {@link User} responsible for trafficking the {@code Order}. This value is required for creating an order. </documentation>
    </annotation>
    </element>
    <element maxOccurs="unbounded" minOccurs="0" name="secondaryTraffickerIds" type="xsd:long">
    <annotation>
    <documentation> The IDs of the secondary traffickers associated with the order. This value is optional. </documentation>
    </annotation>
    </element>
    <element maxOccurs="1" minOccurs="0" name="salespersonId" type="xsd:long">
    <annotation>
    <documentation> The unique ID of the {@link User} responsible for the sales of the {@code Order}. This value is optional. </documentation>
    </annotation>
    </element>
    <element maxOccurs="unbounded" minOccurs="0" name="secondarySalespersonIds" type="xsd:long">
    <annotation>
    <documentation> The IDs of the secondary salespeople associated with the order. This value is optional. </documentation>
    </annotation>
    </element>
    <element maxOccurs="1" minOccurs="0" name="totalImpressionsDelivered" type="xsd:long">
    <annotation>
    <documentation> Total impressions delivered for all line items of this {@code Order}. This value is read-only and is assigned by Google. </documentation>
    </annotation>
    </element>
    <element maxOccurs="1" minOccurs="0" name="totalClicksDelivered" type="xsd:long">
    <annotation>
    <documentation> Total clicks delivered for all line items of this {@code Order}. This value is read-only and is assigned by Google. </documentation>
    </annotation>
    </element>
    <element maxOccurs="1" minOccurs="0" name="totalViewableImpressionsDelivered" type="xsd:long">
    <annotation>
    <documentation> Total viewable impressions delivered for all line items of this {@code Order}. This value is read-only and is assigned by Google. Starting in v201705, this will be {@code null} when the order does not have line items trafficked against a viewable impressions goal. </documentation>
    </annotation>
    </element>
    <element maxOccurs="1" minOccurs="0" name="totalBudget" type="tns:Money">
    <annotation>
    <documentation> Total budget for all line items of this {@code Order}. This value is a readonly field assigned by Google and is calculated from the associated {@link LineItem#costPerUnit} values. </documentation>
    </annotation>
    </element>
    <element maxOccurs="unbounded" minOccurs="0" name="appliedLabels" type="tns:AppliedLabel">
    <annotation>
    <documentation> The set of labels applied directly to this order. </documentation>
    </annotation>
    </element>
    <element maxOccurs="unbounded" minOccurs="0" name="effectiveAppliedLabels" type="tns:AppliedLabel">
    <annotation>
    <documentation> Contains the set of labels applied directly to the order as well as those inherited from the company that owns the order. If a label has been negated, only the negated label is returned. This field is readonly and is assigned by Google. </documentation>
    </annotation>
    </element>
    <element maxOccurs="1" minOccurs="0" name="lastModifiedByApp" type="xsd:string">
    <annotation>
    <documentation> The application which modified this order. This attribute is read only and is assigned by Google. </documentation>
    </annotation>
    </element>
    <element maxOccurs="1" minOccurs="0" name="isProgrammatic" type="xsd:boolean">
    <annotation>
    <documentation> Specifies whether or not the {@code Order} is a programmatic order. This value is optional and defaults to false. </documentation>
    </annotation>
    </element>
    <element maxOccurs="unbounded" minOccurs="0" name="appliedTeamIds" type="xsd:long">
    <annotation>
    <documentation> The IDs of all teams that this order is on directly. </documentation>
    </annotation>
    </element>
    <element maxOccurs="1" minOccurs="0" name="lastModifiedDateTime" type="tns:DateTime">
    <annotation>
    <documentation> The date and time this order was last modified. </documentation>
    </annotation>
    </element>
    <element maxOccurs="unbounded" minOccurs="0" name="customFieldValues" type="tns:BaseCustomFieldValue">
    <annotation>
    <documentation> The values of the custom fields associated with this order. </documentation>
    </annotation>
    </element>
    </sequence>
    </complexType>
    """

    id: Optional[int] = Field(
        default=None,
        description="The unique ID of the {@code Order}. This value is readonly and is assigned by Google.",
    )
    name: str = Field(
        max_length=255,
        description=(
            "The name of the {@code Order}."
            "This value is required to create an order and has a maximum length of 255 characters."
        )
    )
    startDateTime: Optional[DateTime] = Field(
        default=None,
        description=(
            "The date and time at which the {@code Order} and its associated line items are eligible to begin serving. "
            "This attribute is readonly and is derived from the line item of the order which has the earliest "
            "{@link LineItem#startDateTime}."
        ),
    )
    endDateTime: Optional[DateTime] = Field(
        default=None,
        description=(
            "The date and time at which the {@code Order} and its associated line items stop being served. "
            "This attribute is readonly and is derived from the line item of the order which has the latest "
            "{@link LineItem#endDateTime}."
        ),
    )
    unlimitedEndDateTime: Optional[bool] = Field(
        default=None,
        description=(
            "Specifies whether or not the {@code Order} has an unlimited end date. "
            "This attribute is readonly and is {@code true} if any of the order's line items has "
            "{@link LineItem#unlimitedEndDateTime} set to {@code true}."
        )
    )
    status: Optional[OrderStatus] = Field(
        default=None, description="The status of the {@code Order}. This attribute is read-only."
    )
    isArchived: Optional[bool] = Field(
        default=None, description="The archival status of the {@code Order}. This attribute is readonly."
    )
    notes: Optional[str] = Field(
        default=None,
        max_length=65535,
        description=(
            "Provides any additional notes that may annotate the {@code Order}. "
            "This attribute is optional and has a maximum length of 65,535 characters."
        ),
    )
    externalOrderId: Optional[int] = Field(
        default=None,
        description=(
            "An arbitrary ID to associate to the {@code Order}, which can be used as a key to an external system. "
            "This value is optional."
        ),
    )
    poNumber: Optional[str] = Field(
        default=None,
        max_length=63,
        description=(
            "The purchase order number for the {@code Order}. "
            "This value is optional and has a maximum length of 63 characters."
        ),
    )
    currencyCode: Optional[str] = Field(
        default=None,
        description=(
            "The ISO currency code for the currency used by the {@code Order}. "
            "This value is read-only and is the network's currency code."
        ),
    )
    advertiserId: int = Field(
        description=(
            "The unique ID of the {@link Company}, which is of type {@link Company.Type#ADVERTISER}, "
            "to which this order belongs. This attribute is required."
        )
    )
    advertiserContactIds: Optional[List[int]] = Field(
        default=None, description="List of IDs for advertiser contacts of the order."
    )
    agencyId: Optional[int] = Field(
        default=None,
        description=(
            "The unique ID of the {@link Company}, which is of type {@link Company.Type#AGENCY}, "
            "with which this order is associated. This attribute is optional."
        ),
    )
    agencyContactIds: Optional[List[int]] = Field(
        default=None, description="List of IDs for agency contacts of the order."
    )
    creatorId: Optional[int] = Field(
        default=None,
        description=(
            "The unique ID of the {@link User} who created the {@code Order} on behalf of the advertiser. "
            "This value is readonly and is assigned by Google."
        ),
    )
    traffickerId: int = Field(
        description=(
            "The unique ID of the {@link User} responsible for trafficking the {@code Order}."
            "This value is required for creating an order."
        ),
    )
    secondaryTraffickerIds: Optional[List[int]] = Field(
        default=None,
        description="The IDs of the secondary traffickers associated with the order. This value is optional.",
    )
    salespersonId: Optional[int] = Field(
        default=None,
        description=(
            "The unique ID of the {@link User} responsible for the sales of the {@code Order}. This value is optional."
        ),
    )
    secondarySalespersonIds: Optional[List[int]] = Field(
        default=None,
        description="The IDs of the secondary salespeople associated with the order. This value is optional.",
    )
    totalImpressionsDelivered: Optional[int] = Field(
        default=None,
        description=(
            "Total impressions delivered for all line items of this {@code Order}. "
            "This value is read-only and is assigned by Google."
        ),
    )
    totalClicksDelivered: Optional[int] = Field(
        default=None,
        description=(
            "Total clicks delivered for all line items of this {@code Order}. "
            "This value is read-only and is assigned by Google."
        ),
    )
    totalViewableImpressionsDelivered: Optional[int] = Field(
        default=None,
        description=(
            "Total viewable impressions delivered for all line items of this {@code Order}. "
            "This value is read-only and is assigned by Google. Starting in v201705, "
            "this will be {@code null} when the order does not have line items trafficked against a "
            "viewable impressions goal."
        ),
    )
    totalBudget: Optional[Money] = Field(
        default=None,
        description=(
            "Total budget for all line items of this {@code Order}. This value is a readonly field assigned by "
            "Google and is calculated from the associated {@link LineItem#costPerUnit} values."
        )
    )
    appliedLabels: Optional[List[AppliedLabel]] = Field(
        default=None, description="The set of labels applied directly to this order."
    )
    effectiveAppliedLabels: Optional[List[AppliedLabel]] = Field(
        default=None,
        description=(
            "Contains the set of labels applied directly to the order as well as those inherited from the company "
            "that owns the order. If a label has been negated, only the negated label is returned. "
            "This field is readonly and is assigned by Google."
        ),
    )
    lastModifiedByApp: Optional[str] = Field(
        default=None,
        description="The application which modified this order. This attribute is read only and is assigned by Google.",
    )
    isProgrammatic: Optional[bool] = Field(
        default=False,
        description=(
            "Specifies whether or not the {@code Order} is a programmatic order. "
            "This value is optional and defaults to false."
        ),
    )
    appliedTeamIds: Optional[List[int]] = Field(
        default=None,
        description="The IDs of all teams that this order is on directly."
    )
    lastModifiedDateTime: Optional[DateTime] = Field(
        default=None,
        description="The date and time this order was last modified."
    )
    customFieldValues: Optional[List[BaseCustomFieldValue]] = Field(
        default=None,
        description="The values of the custom fields associated with this order."
    )
