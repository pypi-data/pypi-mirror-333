# ruff: noqa: E501
"""
<!--  Generated file, do not edit  -->
<!--  Copyright 2024 Google Inc. All Rights Reserved  -->
<wsdl:definitions xmlns:tns="https://www.google.com/apis/ads/publisher/v202408" xmlns:wsdl="http://schemas.xmlsoap.org/wsdl/" xmlns:wsdlsoap="http://schemas.xmlsoap.org/wsdl/soap/" xmlns:xsd="http://www.w3.org/2001/XMLSchema" targetNamespace="https://www.google.com/apis/ads/publisher/v202408">
<script/>
<wsdl:types>
<schema xmlns="http://www.w3.org/2001/XMLSchema" xmlns:jaxb="http://java.sun.com/xml/ns/jaxb" xmlns:tns="https://www.google.com/apis/ads/publisher/v202408" elementFormDefault="qualified" jaxb:version="1.0" targetNamespace="https://www.google.com/apis/ads/publisher/v202408">
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
<complexType name="AdUnitCodeError">
<annotation>
<documentation> Lists the generic errors associated with {@link AdUnit#adUnitCode}. </documentation>
</annotation>
<complexContent>
<extension base="tns:ApiError">
<sequence>
<element maxOccurs="1" minOccurs="0" name="reason" type="tns:AdUnitCodeError.Reason"/>
</sequence>
</extension>
</complexContent>
</complexType>
<complexType name="AdUnitTargeting">
<annotation>
<documentation> Represents targeted or excluded ad units. </documentation>
</annotation>
<sequence>
<element maxOccurs="1" minOccurs="0" name="adUnitId" type="xsd:string">
<annotation>
<documentation> Included or excluded ad unit id. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="includeDescendants" type="xsd:boolean">
<annotation>
<documentation> Whether or not all descendants are included (or excluded) as part of including (or excluding) this ad unit. By default, the value is {@code true} which means targeting this ad unit will target all of its descendants. </documentation>
</annotation>
</element>
</sequence>
</complexType>
<complexType name="AlternativeUnitTypeForecast">
<annotation>
<documentation> A view of the forecast in terms of an alternative unit type. <p>For example, a forecast for an impressions goal may include this to express the matched, available, and possible viewable impressions. </documentation>
</annotation>
<sequence>
<element maxOccurs="1" minOccurs="0" name="unitType" type="tns:UnitType">
<annotation>
<documentation> The alternative unit type being presented. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="matchedUnits" type="xsd:long">
<annotation>
<documentation> The number of units, defined by {@link #unitType}, that match the specified targeting and delivery settings. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="availableUnits" type="xsd:long">
<annotation>
<documentation> The number of units, defined by {@link #unitType}, that can be booked without affecting the delivery of any reserved line items. Exceeding this value will not cause an overbook, but lower-priority line items may not run. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="possibleUnits" type="xsd:long">
<annotation>
<documentation> The maximum number of units, defined by {@link #unitType}, that could be booked by taking inventory away from lower-priority line items. </documentation>
</annotation>
</element>
</sequence>
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
<complexType name="TechnologyTargeting">
<annotation>
<documentation> Provides {@link LineItem} objects the ability to target or exclude technologies. </documentation>
</annotation>
<sequence>
<element maxOccurs="1" minOccurs="0" name="bandwidthGroupTargeting" type="tns:BandwidthGroupTargeting">
<annotation>
<documentation> The bandwidth groups being targeted by the {@link LineItem}. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="browserTargeting" type="tns:BrowserTargeting">
<annotation>
<documentation> The browsers being targeted by the {@link LineItem}. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="browserLanguageTargeting" type="tns:BrowserLanguageTargeting">
<annotation>
<documentation> The languages of browsers being targeted by the {@link LineItem}. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="deviceCapabilityTargeting" type="tns:DeviceCapabilityTargeting">
<annotation>
<documentation> The device capabilities being targeted by the {@link LineItem}. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="deviceCategoryTargeting" type="tns:DeviceCategoryTargeting">
<annotation>
<documentation> The device categories being targeted by the {@link LineItem}. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="deviceManufacturerTargeting" type="tns:DeviceManufacturerTargeting">
<annotation>
<documentation> The device manufacturers being targeted by the {@link LineItem}. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="mobileCarrierTargeting" type="tns:MobileCarrierTargeting">
<annotation>
<documentation> The mobile carriers being targeted by the {@link LineItem}. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="mobileDeviceTargeting" type="tns:MobileDeviceTargeting">
<annotation>
<documentation> The mobile devices being targeted by the {@link LineItem}. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="mobileDeviceSubmodelTargeting" type="tns:MobileDeviceSubmodelTargeting">
<annotation>
<documentation> The mobile device submodels being targeted by the {@link LineItem}. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="operatingSystemTargeting" type="tns:OperatingSystemTargeting">
<annotation>
<documentation> The operating systems being targeted by the {@link LineItem}. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="operatingSystemVersionTargeting" type="tns:OperatingSystemVersionTargeting">
<annotation>
<documentation> The operating system versions being targeted by the {@link LineItem}. </documentation>
</annotation>
</element>
</sequence>
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
<complexType name="AvailabilityForecast">
<annotation>
<documentation> Describes predicted inventory availability for a {@link ProspectiveLineItem}. <p>Inventory has three threshold values along a line of possible inventory. From least to most, these are: <ul> <li>Available units -- How many units can be booked without affecting any other line items. Booking more than this number can cause lower and same priority line items to underdeliver. <li>Possible units -- How many units can be booked without affecting any higher priority line items. Booking more than this number can cause the line item to underdeliver. <li>Matched (forecast) units -- How many units satisfy all specified criteria. </ul> <p>Underdelivery is caused by overbooking. However, if more impressions are served than are predicted, the extra available inventory might enable all inventory guarantees to be met without overbooking. </documentation>
</annotation>
<sequence>
<element maxOccurs="1" minOccurs="0" name="lineItemId" type="xsd:long">
<annotation>
<documentation> Uniquely identifies this availability forecast. This value is read-only and is assigned by Google when the forecast is created. The attribute will be either the ID of the {@link LineItem} object it represents, or {@code null} if the forecast represents a prospective line item. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="orderId" type="xsd:long">
<annotation>
<documentation> The unique ID for the {@link Order} object that this line item belongs to, or {@code null} if the forecast represents a prospective line item without an {@link LineItem#orderId} set. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="unitType" type="tns:UnitType">
<annotation>
<documentation> The unit with which the goal or cap of the {@link LineItem} is defined. Will be the same value as {@link Goal#unitType} for both a set line item or a prospective one. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="availableUnits" type="xsd:long">
<annotation>
<documentation> The number of units, defined by {@link Goal#unitType}, that can be booked without affecting the delivery of any reserved line items. Exceeding this value will not cause an overbook, but lower priority line items may not run. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="deliveredUnits" type="xsd:long">
<annotation>
<documentation> The number of units, defined by {@link Goal#unitType}, that have already been served if the reservation is already running. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="matchedUnits" type="xsd:long">
<annotation>
<documentation> The number of units, defined by {@link Goal#unitType}, that match the specified targeting and delivery settings. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="possibleUnits" type="xsd:long">
<annotation>
<documentation> The maximum number of units, defined by {@link Goal#unitType}, that could be booked by taking inventory away from lower priority line items and some same priority line items. <p>Please note: booking this number may cause lower priority line items and some same priority line items to underdeliver. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="reservedUnits" type="xsd:long">
<annotation>
<documentation> The number of reserved units, defined by {@link Goal#unitType}, requested. This can be an absolute or percentage value. </documentation>
</annotation>
</element>
<element maxOccurs="unbounded" minOccurs="0" name="breakdowns" type="tns:ForecastBreakdown">
<annotation>
<documentation> The breakdowns for each time window defined in {@link ForecastBreakdownOptions#timeWindows}. <p>If no breakdown was requested through {@link AvailabilityForecastOptions#breakdown}, this field will be empty. If targeting breakdown was requested by {@link ForecastBreakdownOptions#targets} with no time breakdown, this list will contain a single {@link ForecastBreakdown} corresponding to the time window of the forecasted {@link LineItem}. Otherwise, each time window defined by {@link ForecastBreakdownOptions#timeWindows} will correspond to one {@link ForecastBreakdown} in the same order. Targeting breakdowns for every time window are returned in {@link ForecastBreakdown#breakdownEntries}. Some examples: For a targeting breakdown in the form of {@code ForecastBreakdownOptions{targets=[IU=A, {IU=B, creative=1x1}]}}, the {@link #breakdowns} field may look like: {@code [ForecastBreakdown{breakdownEntries=[availableUnits=10, availableUnits=20]}]} where the entries correspond to {@code {IU=A}} and {@code {IU=B, creative=1x1}} respectively. For a time breakdown in the form of {@code ForecastBreakdownOptions{timeWindows=[1am, 2am, 3am]}}, the {@code breakdowns} field may look like: <pre>{@code [ ForecastBreakdown{startTime=1am, endTime=2am, breakdownEntries=[availableUnits=10]}, ForecastBreakdown{startTime=2am, endTime=3am, breakdownEntries=[availableUnits=20]} ] }</pre> where the two {@link #ForecastBreakdown} correspond to the [1am, 2am) and [2am, 3am) time windows respecively. For a two-dimensional breakdown in the form of {@code ForecastBreakdownOptions{timeWindows=[1am, 2am, 3am], targets=[IU=A, IU=B]}, the {@code breakdowns} field may look like: <pre>{@code [ ForecastBreakdown{startTime=1am, endTime=2am, breakdownEntries=[availableUnits=10, availableUnits=100]}, ForecastBreakdown{startTime=2am, endTime=3am, breakdownEntries=[availableUnits=20, availableUnits=200]} ] }</pre> where the first ForecastBreakdown respresents the [1am, 2am) time window with two entries for the IU A and IU B respectively; and the second ForecastBreakdown represents the [2am, 3am) time window also with two entries corresponding to the two IUs. </documentation>
</annotation>
</element>
<element maxOccurs="unbounded" minOccurs="0" name="targetingCriteriaBreakdowns" type="tns:TargetingCriteriaBreakdown">
<annotation>
<documentation> The forecast result broken down by the targeting of the forecasted line item. </documentation>
</annotation>
</element>
<element maxOccurs="unbounded" minOccurs="0" name="contendingLineItems" type="tns:ContendingLineItem">
<annotation>
<documentation> List of {@link ContendingLineItem contending line items} for this forecast. </documentation>
</annotation>
</element>
<element maxOccurs="unbounded" minOccurs="0" name="alternativeUnitTypeForecasts" type="tns:AlternativeUnitTypeForecast">
<annotation>
<documentation> Views of this forecast, with alternative unit types. </documentation>
</annotation>
</element>
</sequence>
</complexType>
<complexType name="AvailabilityForecastOptions">
<annotation>
<documentation> Forecasting options for line item availability forecasts. </documentation>
</annotation>
<sequence>
<element maxOccurs="1" minOccurs="0" name="includeTargetingCriteriaBreakdown" type="xsd:boolean">
<annotation>
<documentation> When specified, forecast result for the availability line item will also include breakdowns by its targeting in {@link AvailabilityForecast#targetingCriteriaBreakdowns}. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="includeContendingLineItems" type="xsd:boolean">
<annotation>
<documentation> When specified, the forecast result for the availability line item will also include contending line items in {@link AvailabilityForecast#contendingLineItems}. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="breakdown" type="tns:ForecastBreakdownOptions"/>
</sequence>
</complexType>
<complexType name="BandwidthGroup">
<annotation>
<documentation> Represents a group of bandwidths that are logically organized by some well known generic names such as 'Cable' or 'DSL'. </documentation>
</annotation>
<complexContent>
<extension base="tns:Technology">
<sequence/>
</extension>
</complexContent>
</complexType>
<complexType name="BandwidthGroupTargeting">
<annotation>
<documentation> Represents bandwidth groups that are being targeted or excluded by the {@link LineItem}. </documentation>
</annotation>
<sequence>
<element maxOccurs="1" minOccurs="0" name="isTargeted" type="xsd:boolean">
<annotation>
<documentation> Indicates whether bandwidth groups should be targeted or excluded. This attribute is optional and defaults to {@code true}. </documentation>
</annotation>
</element>
<element maxOccurs="unbounded" minOccurs="0" name="bandwidthGroups" type="tns:Technology">
<annotation>
<documentation> The bandwidth groups that are being targeted or excluded by the {@link LineItem}. </documentation>
</annotation>
</element>
</sequence>
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
<complexType name="Browser">
<annotation>
<documentation> Represents an internet browser. </documentation>
</annotation>
<complexContent>
<extension base="tns:Technology">
<sequence>
<element maxOccurs="1" minOccurs="0" name="majorVersion" type="xsd:string">
<annotation>
<documentation> Browser major version. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="minorVersion" type="xsd:string">
<annotation>
<documentation> Browser minor version. </documentation>
</annotation>
</element>
</sequence>
</extension>
</complexContent>
</complexType>
<complexType name="BrowserLanguage">
<annotation>
<documentation> Represents a Browser's language. </documentation>
</annotation>
<complexContent>
<extension base="tns:Technology">
<sequence/>
</extension>
</complexContent>
</complexType>
<complexType name="BrowserLanguageTargeting">
<annotation>
<documentation> Represents browser languages that are being targeted or excluded by the {@link LineItem}. </documentation>
</annotation>
<sequence>
<element maxOccurs="1" minOccurs="0" name="isTargeted" type="xsd:boolean">
<annotation>
<documentation> Indicates whether browsers languages should be targeted or excluded. This attribute is optional and defaults to {@code true}. </documentation>
</annotation>
</element>
<element maxOccurs="unbounded" minOccurs="0" name="browserLanguages" type="tns:Technology">
<annotation>
<documentation> Browser languages that are being targeted or excluded by the {@link LineItem}. </documentation>
</annotation>
</element>
</sequence>
</complexType>
<complexType name="BrowserTargeting">
<annotation>
<documentation> Represents browsers that are being targeted or excluded by the {@link LineItem}. </documentation>
</annotation>
<sequence>
<element maxOccurs="1" minOccurs="0" name="isTargeted" type="xsd:boolean">
<annotation>
<documentation> Indicates whether browsers should be targeted or excluded. This attribute is optional and defaults to {@code true}. </documentation>
</annotation>
</element>
<element maxOccurs="unbounded" minOccurs="0" name="browsers" type="tns:Technology">
<annotation>
<documentation> Browsers that are being targeted or excluded by the {@link LineItem}. </documentation>
</annotation>
</element>
</sequence>
</complexType>
<complexType name="BuyerUserListTargeting">
<annotation>
<documentation> The {@code BuyerUserListTargeting} associated with a programmatic {@link LineItem} or {@link ProposalLineItem} object. </documentation>
</annotation>
<sequence>
<element maxOccurs="1" minOccurs="0" name="hasBuyerUserListTargeting" type="xsd:boolean">
<annotation>
<documentation> Whether the programmatic {@code LineItem} or {@code ProposalLineItem} object has buyer user list targeting. </documentation>
</annotation>
</element>
</sequence>
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
<complexType name="ContendingLineItem">
<annotation>
<documentation> Describes contending line items for a {@link Forecast}. </documentation>
</annotation>
<sequence>
<element maxOccurs="1" minOccurs="0" name="lineItemId" type="xsd:long">
<annotation>
<documentation> The {@link LineItem#id Id} of the contending line item. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="contendingImpressions" type="xsd:long">
<annotation>
<documentation> Number of impressions contended for by both the forecasted line item and this line item, but served to this line item in the forecast simulation. </documentation>
</annotation>
</element>
</sequence>
</complexType>
<complexType name="ContentLabelTargeting">
<annotation>
<documentation> Content label targeting information. </documentation>
</annotation>
<sequence>
<element maxOccurs="unbounded" minOccurs="0" name="excludedContentLabelIds" type="xsd:long"/>
</sequence>
</complexType>
<complexType name="ContentTargeting">
<annotation>
<documentation> Used to target {@link LineItem}s to specific videos on a publisher's site. </documentation>
</annotation>
<sequence>
<element maxOccurs="unbounded" minOccurs="0" name="targetedContentIds" type="xsd:long">
<annotation>
<documentation> The IDs of content being targeted by the {@code LineItem}. </documentation>
</annotation>
</element>
<element maxOccurs="unbounded" minOccurs="0" name="excludedContentIds" type="xsd:long">
<annotation>
<documentation> The IDs of content being excluded by the {@code LineItem}. </documentation>
</annotation>
</element>
<element maxOccurs="unbounded" minOccurs="0" name="targetedVideoContentBundleIds" type="xsd:long">
<annotation>
<documentation> A list of video content bundles, represented by {@link ContentBundle} IDs, that are being targeted by the {@code LineItem}. </documentation>
</annotation>
</element>
<element maxOccurs="unbounded" minOccurs="0" name="excludedVideoContentBundleIds" type="xsd:long">
<annotation>
<documentation> A list of video content bundles, represented by {@link ContentBundle} IDs, that are being excluded by the {@code LineItem}. </documentation>
</annotation>
</element>
</sequence>
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
<complexType name="CreativePlaceholder">
<annotation>
<documentation> A {@code CreativePlaceholder} describes a slot that a creative is expected to fill. This is used primarily to help in forecasting, and also to validate that the correct creatives are associated with the line item. A {@code CreativePlaceholder} must contain a size, and it can optionally contain companions. Companions are only valid if the line item's environment type is {@link EnvironmentType#VIDEO_PLAYER}. </documentation>
</annotation>
<sequence>
<element maxOccurs="1" minOccurs="0" name="size" type="tns:Size">
<annotation>
<documentation> The dimensions that the creative is expected to have. This attribute is required. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="creativeTemplateId" type="xsd:long">
<annotation>
<documentation> The native creative template ID. <p>This value is only required if {@link #creativeSizeType} is {@link CreativeSizeType#NATIVE}. </documentation>
</annotation>
</element>
<element maxOccurs="unbounded" minOccurs="0" name="companions" type="tns:CreativePlaceholder">
<annotation>
<documentation> The companions that the creative is expected to have. This attribute can only be set if the line item it belongs to has a {@link LineItem#environmentType} of {@link EnvironmentType#VIDEO_PLAYER} or {@link LineItem#roadblockingType} of {@link RoadblockingType#CREATIVE_SET}. </documentation>
</annotation>
</element>
<element maxOccurs="unbounded" minOccurs="0" name="appliedLabels" type="tns:AppliedLabel">
<annotation>
<documentation> The set of label frequency caps applied directly to this creative placeholder. </documentation>
</annotation>
</element>
<element maxOccurs="unbounded" minOccurs="0" name="effectiveAppliedLabels" type="tns:AppliedLabel">
<annotation>
<documentation> Contains the set of labels applied directly to this creative placeholder as well as those inherited from the creative template from which this creative placeholder was instantiated. This field is readonly and is assigned by Google. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="expectedCreativeCount" type="xsd:int">
<annotation>
<documentation> Expected number of creatives that will be uploaded corresponding to this creative placeholder. This estimate is used to improve the accuracy of forecasting; for example, if label frequency capping limits the number of times a creative may be served. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="creativeSizeType" type="tns:CreativeSizeType">
<annotation>
<documentation> Describes the types of sizes a creative can be. By default, the creative's size is {@link CreativeSizeType#PIXEL}, which is a dimension based size (width-height pair). </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="targetingName" type="xsd:string">
<annotation>
<documentation> The name of the {@link CreativeTargeting} for creatives this placeholder represents. <p>This attribute is optional. Specifying creative targeting here is for forecasting purposes only and has no effect on serving. The same creative targeting should be specified on a {@link LineItemCreativeAssociation} when associating a {@link Creative} with the {@link LineItem}. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="isAmpOnly" type="xsd:boolean">
<annotation>
<documentation> Indicate if the expected creative of this placeholder has an AMP only variant. <p>This attribute is optional. It is for forecasting purposes only and has no effect on serving. </documentation>
</annotation>
</element>
</sequence>
</complexType>
<complexType name="CreativeTargeting">
<annotation>
<documentation> Represents the creative targeting criteria for a {@link LineItem}. </documentation>
</annotation>
<sequence>
<element maxOccurs="1" minOccurs="0" name="name" type="xsd:string">
<annotation>
<documentation> The name of this creative targeting. This attribute is required. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="targeting" type="tns:Targeting">
<annotation>
<documentation> The {@link Targeting} criteria of this creative targeting. This attribute is required. </documentation>
</annotation>
</element>
</sequence>
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
<complexType name="CustomCriteria">
<annotation>
<documentation> A {@link CustomCriteria} object is used to perform custom criteria targeting on custom targeting keys of type {@link CustomTargetingKey.Type#PREDEFINED} or {@link CustomTargetingKey.Type#FREEFORM}. </documentation>
</annotation>
<complexContent>
<extension base="tns:CustomCriteriaLeaf">
<sequence>
<element maxOccurs="1" minOccurs="0" name="keyId" type="xsd:long">
<annotation>
<documentation> The {@link CustomTargetingKey#id} of the {@link CustomTargetingKey} object that was created using {@link CustomTargetingService}. This attribute is required. </documentation>
</annotation>
</element>
<element maxOccurs="unbounded" minOccurs="0" name="valueIds" type="xsd:long">
<annotation>
<documentation> The ids of {@link CustomTargetingValue} objects to target the custom targeting key with id {@link CustomCriteria#keyId}. This attribute is required. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="operator" type="tns:CustomCriteria.ComparisonOperator">
<annotation>
<documentation> The comparison operator. This attribute is required. </documentation>
</annotation>
</element>
</sequence>
</extension>
</complexContent>
</complexType>
<complexType name="CustomCriteriaSet">
<annotation>
<documentation> A {@link CustomCriteriaSet} comprises of a set of {@link CustomCriteriaNode} objects combined by the {@link CustomCriteriaSet.LogicalOperator#logicalOperator}. The custom criteria targeting tree is subject to the rules defined on {@link Targeting#customTargeting}. </documentation>
</annotation>
<complexContent>
<extension base="tns:CustomCriteriaNode">
<sequence>
<element maxOccurs="1" minOccurs="0" name="logicalOperator" type="tns:CustomCriteriaSet.LogicalOperator">
<annotation>
<documentation> The logical operator to be applied to {@link CustomCriteriaSet#children}. This attribute is required. <span class="constraint Required">This attribute is required.</span> </documentation>
</annotation>
</element>
<element maxOccurs="unbounded" minOccurs="0" name="children" type="tns:CustomCriteriaNode">
<annotation>
<documentation> The custom criteria. This attribute is required. </documentation>
</annotation>
</element>
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
<complexType name="CustomPacingCurve">
<annotation>
<documentation> A curve consisting of {@link CustomPacingGoal} objects that is used to pace line item delivery. </documentation>
</annotation>
<sequence>
<element maxOccurs="1" minOccurs="0" name="customPacingGoalUnit" type="tns:CustomPacingGoalUnit">
<annotation>
<documentation> The unit of the {@link CustomPacingGoalDto#amount} values. </documentation>
</annotation>
</element>
<element maxOccurs="unbounded" minOccurs="0" name="customPacingGoals" type="tns:CustomPacingGoal">
<annotation>
<documentation> The list of goals that make up the custom pacing curve. </documentation>
</annotation>
</element>
</sequence>
</complexType>
<complexType name="CustomPacingGoal">
<annotation>
<documentation> An interval of a {@link CustomPacingCurve}. A custom pacing goal contains a start time and an amount. The goal will apply until either the next custom pacing goal's {@code getStartTime} or the line item's end time if it is the last goal. </documentation>
</annotation>
<sequence>
<element maxOccurs="1" minOccurs="0" name="startDateTime" type="tns:DateTime">
<annotation>
<documentation> The start date and time of the goal. This field is required unless {@code useLineItemStartDateTime} is true. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="useLineItemStartDateTime" type="xsd:boolean">
<annotation>
<documentation> Whether the {@link LineItem#startDateTime} should be used for the start date and time of this goal. This field is not persisted and if it is set to true, the {@code startDateTime} field will be populated by the line item's start time. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="amount" type="xsd:long"/>
</sequence>
</complexType>
<complexType name="CmsMetadataCriteria">
<annotation>
<documentation> A {@code CmsMetadataCriteria} object is used to target {@code CmsMetadataValue} objects. </documentation>
</annotation>
<complexContent>
<extension base="tns:CustomCriteriaLeaf">
<sequence>
<element maxOccurs="1" minOccurs="0" name="operator" type="tns:CmsMetadataCriteria.ComparisonOperator">
<annotation>
<documentation> The comparison operator. This attribute is required. </documentation>
</annotation>
</element>
<element maxOccurs="unbounded" minOccurs="0" name="cmsMetadataValueIds" type="xsd:long">
<annotation>
<documentation> The ids of {@link CmsMetadataValue} objects used to target CMS metadata. This attribute is required. </documentation>
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
<complexType abstract="true" name="CustomCriteriaLeaf">
<annotation>
<documentation> A {@link CustomCriteriaLeaf} object represents a generic leaf of {@link CustomCriteria} tree structure. </documentation>
</annotation>
<complexContent>
<extension base="tns:CustomCriteriaNode">
<sequence/>
</extension>
</complexContent>
</complexType>
<complexType abstract="true" name="CustomCriteriaNode">
<annotation>
<documentation> A {@link CustomCriteriaNode} is a node in the custom targeting tree. A custom criteria node can either be a {@link CustomCriteriaSet} (a non-leaf node) or a {@link CustomCriteria} (a leaf node). The custom criteria targeting tree is subject to the rules defined on {@link Targeting#customTargeting}. </documentation>
</annotation>
<sequence/>
</complexType>
<complexType name="AudienceSegmentCriteria">
<annotation>
<documentation> An {@link AudienceSegmentCriteria} object is used to target {@link AudienceSegment} objects. </documentation>
</annotation>
<complexContent>
<extension base="tns:CustomCriteriaLeaf">
<sequence>
<element maxOccurs="1" minOccurs="0" name="operator" type="tns:AudienceSegmentCriteria.ComparisonOperator">
<annotation>
<documentation> The comparison operator. This attribute is required. </documentation>
</annotation>
</element>
<element maxOccurs="unbounded" minOccurs="0" name="audienceSegmentIds" type="xsd:long">
<annotation>
<documentation> The ids of {@link AudienceSegment} objects used to target audience segments. This attribute is required. </documentation>
</annotation>
</element>
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
<complexType name="DateError">
<annotation>
<documentation> A list of all errors associated with the dates. </documentation>
</annotation>
<complexContent>
<extension base="tns:ApiError">
<sequence>
<element maxOccurs="1" minOccurs="0" name="reason" type="tns:DateError.Reason"/>
</sequence>
</extension>
</complexContent>
</complexType>
<complexType name="DateRange">
<annotation>
<documentation> Represents a range of dates that has an upper and a lower bound. <p>An open ended date range can be described by only setting either one of the bounds, the upper bound or the lower bound. </documentation>
</annotation>
<sequence>
<element maxOccurs="1" minOccurs="0" name="startDate" type="tns:Date">
<annotation>
<documentation> The start date of this range. This field is optional and if it is not set then there is no lower bound on the date range. If this field is not set then {@code endDate} must be specified. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="endDate" type="tns:Date">
<annotation>
<documentation> The end date of this range. This field is optional and if it is not set then there is no upper bound on the date range. If this field is not set then {@code startDate} must be specified. </documentation>
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
<complexType name="DateTimeRange">
<annotation>
<documentation> Represents a range of dates (combined with time of day) that has an upper and/or lower bound. </documentation>
</annotation>
<sequence>
<element maxOccurs="1" minOccurs="0" name="startDateTime" type="tns:DateTime">
<annotation>
<documentation> The start date time of this range. This field is optional and if it is not set then there is no lower bound on the date time range. If this field is not set then {@code endDateTime} must be specified. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="endDateTime" type="tns:DateTime">
<annotation>
<documentation> The end date time of this range. This field is optional and if it is not set then there is no upper bound on the date time range. If this field is not set then {@code startDateTime} must be specified. </documentation>
</annotation>
</element>
</sequence>
</complexType>
<complexType name="DateTimeRangeTargeting">
<annotation>
<documentation> The date time ranges that the line item is eligible to serve. </documentation>
</annotation>
<sequence>
<element maxOccurs="unbounded" minOccurs="0" name="targetedDateTimeRanges" type="tns:DateTimeRange"/>
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
<complexType name="DayPart">
<annotation>
<documentation> {@code DayPart} represents a time-period within a day of the week which is targeted by a {@link LineItem}. </documentation>
</annotation>
<sequence>
<element maxOccurs="1" minOccurs="0" name="dayOfWeek" type="tns:DayOfWeek">
<annotation>
<documentation> Day of the week the target applies to. This field is required. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="startTime" type="tns:TimeOfDay">
<annotation>
<documentation> Represents the start time of the targeted period (inclusive). </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="endTime" type="tns:TimeOfDay">
<annotation>
<documentation> Represents the end time of the targeted period (exclusive). </documentation>
</annotation>
</element>
</sequence>
</complexType>
<complexType name="DayPartTargeting">
<annotation>
<documentation> Modify the delivery times of line items for particular days of the week. By default, line items are served at all days and times. </documentation>
</annotation>
<sequence>
<element maxOccurs="unbounded" minOccurs="0" name="dayParts" type="tns:DayPart">
<annotation>
<documentation> Specifies days of the week and times at which a {@code LineItem} will be delivered. <p>If targeting all days and times, this value will be ignored. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="timeZone" type="tns:DeliveryTimeZone">
<annotation>
<documentation> Specifies the time zone to be used for delivering {@link LineItem} objects. This attribute is optional and defaults to {@link DeliveryTimeZone#BROWSER}. <p>Setting this has no effect if targeting all days and times. </documentation>
</annotation>
</element>
</sequence>
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
<complexType name="DeliveryData">
<annotation>
<documentation> Holds the number of clicks or impressions, determined by {@link LineItem#costType}, delivered for a single line item for the last 7 days </documentation>
</annotation>
<sequence>
<element maxOccurs="unbounded" minOccurs="0" name="units" type="xsd:long">
<annotation>
<documentation> Clicks or impressions delivered for the last 7 days. </documentation>
</annotation>
</element>
</sequence>
</complexType>
<complexType name="BreakdownForecast">
<annotation>
<documentation> Represents a single delivery data point, with both available and forecast number. </documentation>
</annotation>
<sequence>
<element maxOccurs="1" minOccurs="0" name="matched" type="xsd:long"/>
<element maxOccurs="1" minOccurs="0" name="available" type="xsd:long"/>
<element maxOccurs="1" minOccurs="0" name="possible" type="xsd:long"/>
</sequence>
</complexType>
<complexType name="DeliveryForecastOptions">
<annotation>
<documentation> Forecasting options for line item delivery forecasts. </documentation>
</annotation>
<sequence>
<element maxOccurs="unbounded" minOccurs="0" name="ignoredLineItemIds" type="xsd:long">
<annotation>
<documentation> Line item IDs to be ignored while performing the delivery simulation. </documentation>
</annotation>
</element>
</sequence>
</complexType>
<complexType name="DeliveryForecast">
<annotation>
<documentation> The forecast of delivery for a list of {@link ProspectiveLineItem} objects to be reserved at the same time. </documentation>
</annotation>
<sequence>
<element maxOccurs="unbounded" minOccurs="0" name="lineItemDeliveryForecasts" type="tns:LineItemDeliveryForecast">
<annotation>
<documentation> The delivery forecasts of the forecasted line items. </documentation>
</annotation>
</element>
</sequence>
</complexType>
<complexType name="DeliveryIndicator">
<annotation>
<documentation> Indicates the delivery performance of the {@link LineItem}. </documentation>
</annotation>
<sequence>
<element maxOccurs="1" minOccurs="0" name="expectedDeliveryPercentage" type="xsd:double">
<annotation>
<documentation> How much the {@code LineItem} was expected to deliver as a percentage of {@link LineItem#primaryGoal}. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="actualDeliveryPercentage" type="xsd:double">
<annotation>
<documentation> How much the line item actually delivered as a percentage of {@link LineItem#primaryGoal}. </documentation>
</annotation>
</element>
</sequence>
</complexType>
<complexType name="DeviceCapability">
<annotation>
<documentation> Represents a capability of a physical device. </documentation>
</annotation>
<complexContent>
<extension base="tns:Technology">
<sequence/>
</extension>
</complexContent>
</complexType>
<complexType name="DeviceCapabilityTargeting">
<annotation>
<documentation> Represents device capabilities that are being targeted or excluded by the {@link LineItem}. </documentation>
</annotation>
<sequence>
<element maxOccurs="unbounded" minOccurs="0" name="targetedDeviceCapabilities" type="tns:Technology">
<annotation>
<documentation> Device capabilities that are being targeted by the {@link LineItem}. </documentation>
</annotation>
</element>
<element maxOccurs="unbounded" minOccurs="0" name="excludedDeviceCapabilities" type="tns:Technology">
<annotation>
<documentation> Device capabilities that are being excluded by the {@link LineItem}. </documentation>
</annotation>
</element>
</sequence>
</complexType>
<complexType name="DeviceCategory">
<annotation>
<documentation> Represents the category of a device. </documentation>
</annotation>
<complexContent>
<extension base="tns:Technology">
<sequence/>
</extension>
</complexContent>
</complexType>
<complexType name="DeviceCategoryTargeting">
<annotation>
<documentation> Represents device categories that are being targeted or excluded by the {@link LineItem}. </documentation>
</annotation>
<sequence>
<element maxOccurs="unbounded" minOccurs="0" name="targetedDeviceCategories" type="tns:Technology">
<annotation>
<documentation> Device categories that are being targeted by the {@link LineItem}. </documentation>
</annotation>
</element>
<element maxOccurs="unbounded" minOccurs="0" name="excludedDeviceCategories" type="tns:Technology">
<annotation>
<documentation> Device categories that are being excluded by the {@link LineItem}. </documentation>
</annotation>
</element>
</sequence>
</complexType>
<complexType name="DeviceManufacturer">
<annotation>
<documentation> Represents a mobile device's manufacturer. </documentation>
</annotation>
<complexContent>
<extension base="tns:Technology">
<sequence/>
</extension>
</complexContent>
</complexType>
<complexType name="DeviceManufacturerTargeting">
<annotation>
<documentation> Represents device manufacturer that are being targeted or excluded by the {@link LineItem}. </documentation>
</annotation>
<sequence>
<element maxOccurs="1" minOccurs="0" name="isTargeted" type="xsd:boolean">
<annotation>
<documentation> Indicates whether device manufacturers should be targeted or excluded. This attribute is optional and defaults to {@code true}. </documentation>
</annotation>
</element>
<element maxOccurs="unbounded" minOccurs="0" name="deviceManufacturers" type="tns:Technology">
<annotation>
<documentation> Device manufacturers that are being targeted or excluded by the {@link LineItem}. </documentation>
</annotation>
</element>
</sequence>
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
<complexType name="ForecastBreakdown">
<annotation>
<documentation> Represents the breakdown entries for a list of targetings and/or creatives. </documentation>
</annotation>
<sequence>
<element maxOccurs="1" minOccurs="0" name="startTime" type="tns:DateTime">
<annotation>
<documentation> The starting time of the represented breakdown. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="endTime" type="tns:DateTime">
<annotation>
<documentation> The end time of the represented breakdown. </documentation>
</annotation>
</element>
<element maxOccurs="unbounded" minOccurs="0" name="breakdownEntries" type="tns:ForecastBreakdownEntry">
<annotation>
<documentation> The forecast breakdown entries in the same order as in the {@link ForecastBreakdownOptions#targets} field. </documentation>
</annotation>
</element>
</sequence>
</complexType>
<complexType name="ForecastBreakdownEntry">
<annotation>
<documentation> A single forecast breakdown entry. </documentation>
</annotation>
<sequence>
<element maxOccurs="1" minOccurs="0" name="name" type="xsd:string">
<annotation>
<documentation> The optional name of this entry, as specified in the corresponding {@link ForecastBreakdownTarget#name} field. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="forecast" type="tns:BreakdownForecast">
<annotation>
<documentation> The forecast of this entry. </documentation>
</annotation>
</element>
</sequence>
</complexType>
<complexType name="ForecastBreakdownOptions">
<annotation>
<documentation> Configuration of forecast breakdown. </documentation>
</annotation>
<sequence>
<element maxOccurs="unbounded" minOccurs="0" name="timeWindows" type="tns:DateTime">
<annotation>
<documentation> The boundaries of time windows to configure time breakdown. <p>By default, the time window of the forecasted {@link LineItem} is assumed if none are explicitly specified in this field. But if set, at least two {@link DateTime}s are needed to define the boundaries of minimally one time window. <p>Also, the time boundaries are required to be in the same time zone, in strictly ascending order. </documentation>
</annotation>
</element>
<element maxOccurs="unbounded" minOccurs="0" name="targets" type="tns:ForecastBreakdownTarget">
<annotation>
<documentation> For each time window, these are the breakdown targets. If none specified, the targeting of the forecasted {@link LineItem} is assumed. </documentation>
</annotation>
</element>
</sequence>
</complexType>
<complexType name="ForecastBreakdownTarget">
<annotation>
<documentation> Specifies inventory targeted by a breakdown entry. </documentation>
</annotation>
<sequence>
<element maxOccurs="1" minOccurs="0" name="name" type="xsd:string">
<annotation>
<documentation> An optional name for this breakdown target, to be populated in the corresponding {@link ForecastBreakdownEntry#name} field. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="targeting" type="tns:Targeting">
<annotation>
<documentation> If specified, the targeting for this breakdown. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="creative" type="tns:CreativePlaceholder">
<annotation>
<documentation> If specified, restrict the breakdown to only inventory matching this creative. </documentation>
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
<complexType name="FrequencyCap">
<annotation>
<documentation> Represents a limit on the number of times a single viewer can be exposed to the same {@link LineItem} in a specified time period. </documentation>
</annotation>
<sequence>
<element maxOccurs="1" minOccurs="0" name="maxImpressions" type="xsd:int">
<annotation>
<documentation> The maximum number of impressions than can be served to a user within a specified time period. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="numTimeUnits" type="xsd:int">
<annotation>
<documentation> The number of {@code FrequencyCap#timeUnit} to represent the total time period. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="timeUnit" type="tns:TimeUnit">
<annotation>
<documentation> The unit of time for specifying the time period. </documentation>
</annotation>
</element>
</sequence>
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
<complexType name="GeoTargeting">
<annotation>
<documentation> Provides line items the ability to target geographical locations. By default, line items target all countries and their subdivisions. With geographical targeting, you can target line items to specific countries, regions, metro areas, and cities. You can also exclude the same. <p>The following rules apply for geographical targeting: <ul> <li>You cannot target and exclude the same location. <li>You cannot target a child whose parent has been excluded. For example, if the state of Illinois has been excluded, then you cannot target Chicago. <li>You must not target a location if you are also targeting its parent. For example, if you are targeting New York City, you must not have the state of New York as one of the targeted locations. <li>You cannot explicitly define inclusions or exclusions that are already implicit. For example, if you explicitly include California, you implicitly exclude all other states. You therefore cannot explicitly exclude Florida, because it is already implicitly excluded. Conversely if you explicitly exclude Florida, you cannot explicitly include California. </ul> </documentation>
</annotation>
<sequence>
<element maxOccurs="unbounded" minOccurs="0" name="targetedLocations" type="tns:Location">
<annotation>
<documentation> The geographical locations being targeted by the {@link LineItem}. </documentation>
</annotation>
</element>
<element maxOccurs="unbounded" minOccurs="0" name="excludedLocations" type="tns:Location">
<annotation>
<documentation> The geographical locations being excluded by the {@link LineItem}. </documentation>
</annotation>
</element>
</sequence>
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
<complexType name="Goal">
<annotation>
<documentation> Defines the criteria a {@link LineItem} needs to satisfy to meet its delivery goal. </documentation>
</annotation>
<sequence>
<element maxOccurs="1" minOccurs="0" name="goalType" type="tns:GoalType">
<annotation>
<documentation> The type of the goal for the {@code LineItem}. It defines the period over which the goal for {@code LineItem} should be reached. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="unitType" type="tns:UnitType">
<annotation>
<documentation> The type of the goal unit for the {@code LineItem}. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="units" type="xsd:long">
<annotation>
<documentation> If this is a primary goal, it represents the number or percentage of impressions or clicks that will be reserved for the {@code LineItem}. If the line item is of type {@link LineItemType#SPONSORSHIP}, it represents the percentage of available impressions reserved. If the line item is of type {@link LineItemType#BULK} or {@link LineItemType#PRICE_PRIORITY}, it represents the number of remaining impressions reserved. If the line item is of type {@link LineItemType#NETWORK} or {@link LineItemType#HOUSE}, it represents the percentage of remaining impressions reserved. <p>If this is a secondary goal, it represents the number of impressions or conversions that the line item will stop serving at if reached. For valid line item types, see {@link LineItem#secondaryGoals}. </documentation>
</annotation>
</element>
</sequence>
</complexType>
<complexType name="GrpSettings">
<annotation>
<documentation> {@code GrpSettings} contains information for a line item that will have a target demographic when serving. This information will be used to set up tracking and enable reporting on the demographic information. </documentation>
</annotation>
<sequence>
<element maxOccurs="1" minOccurs="0" name="minTargetAge" type="xsd:long">
<annotation>
<documentation> Specifies the minimum target age (in years) of the {@link LineItem}. This field is only applicable if {@link #provider} is not null. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="maxTargetAge" type="xsd:long">
<annotation>
<documentation> Specifies the maximum target age (in years) of the {@link LineItem}. This field is only applicable if {@link #provider} is not null. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="targetGender" type="tns:GrpTargetGender">
<annotation>
<documentation> Specifies the target gender of the {@link LineItem}. This field is only applicable if {@link #provider} is not null. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="provider" type="tns:GrpProvider">
<annotation>
<documentation> Specifies the GRP provider of the {@link LineItem}. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="inTargetRatioEstimateMilliPercent" type="xsd:long">
<annotation>
<documentation> Estimate for the in-target ratio given the line item's audience targeting. This field is only applicable if {@link #provider} is Nielsen, {@link LineItem#primaryGoal#unitType} is in-target impressions, and {@link LineItem#CostType} is in-target CPM. This field determines the in-target ratio to use for pacing Nielsen line items before Nielsen reporting data is available. Represented as a milli percent, so 55.7% becomes 55700. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="nielsenCtvPacingType" type="tns:NielsenCtvPacingType">
<annotation>
<documentation> Specifies which pacing computation to apply in pacing to impressions from connected devices. This field is required if {@code enableNielsenCoViewingSupport} is true. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="pacingDeviceCategorizationType" type="tns:PacingDeviceCategorizationType">
<annotation>
<documentation> Specifies whether to use Google or Nielsen device breakdown in Nielsen Line Item auto pacing. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="applyTrueCoview" type="xsd:boolean"/>
</sequence>
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
<complexType name="InventorySizeTargeting">
<annotation>
<documentation> Represents a collection of targeted and excluded inventory sizes. This is currently only available on {@link YieldGroup} and {@link TrafficDataRequest}. </documentation>
</annotation>
<sequence>
<element maxOccurs="1" minOccurs="0" name="isTargeted" type="xsd:boolean">
<annotation>
<documentation> Whether the inventory sizes should be targeted or excluded. </documentation>
</annotation>
</element>
<element maxOccurs="unbounded" minOccurs="0" name="targetedSizes" type="tns:TargetedSize">
<annotation>
<documentation> A list of {@link TargetedSizeDto}s. </documentation>
</annotation>
</element>
</sequence>
</complexType>
<complexType name="InventoryTargeting">
<annotation>
<documentation> A collection of targeted and excluded ad units and placements. </documentation>
</annotation>
<sequence>
<element maxOccurs="unbounded" minOccurs="0" name="targetedAdUnits" type="tns:AdUnitTargeting">
<annotation>
<documentation> A list of targeted {@link AdUnitTargeting}. </documentation>
</annotation>
</element>
<element maxOccurs="unbounded" minOccurs="0" name="excludedAdUnits" type="tns:AdUnitTargeting">
<annotation>
<documentation> A list of excluded {@link AdUnitTargeting}. </documentation>
</annotation>
</element>
<element maxOccurs="unbounded" minOccurs="0" name="targetedPlacementIds" type="xsd:long">
<annotation>
<documentation> A list of targeted {@link Placement} ids. </documentation>
</annotation>
</element>
</sequence>
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
<complexType name="InventoryUnitError">
<annotation>
<documentation> Lists the generic errors associated with {@link AdUnit} objects. </documentation>
</annotation>
<complexContent>
<extension base="tns:ApiError">
<sequence>
<element maxOccurs="1" minOccurs="0" name="reason" type="tns:InventoryUnitError.Reason"/>
</sequence>
</extension>
</complexContent>
</complexType>
<complexType name="InventoryUrl">
<annotation>
<documentation> The representation of an inventory Url that is used in targeting. </documentation>
</annotation>
<sequence>
<element maxOccurs="1" minOccurs="0" name="id" type="xsd:long"/>
</sequence>
</complexType>
<complexType name="InventoryUrlTargeting">
<annotation>
<documentation> A collection of targeted inventory urls. </documentation>
</annotation>
<sequence>
<element maxOccurs="unbounded" minOccurs="0" name="targetedUrls" type="tns:InventoryUrl"/>
<element maxOccurs="unbounded" minOccurs="0" name="excludedUrls" type="tns:InventoryUrl"/>
</sequence>
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
<complexType name="LineItemActivityAssociation">
<annotation>
<documentation> A {@code LineItemActivityAssociation} associates a {@link LineItem} with an {@link Activity} so that the conversions of the {@link Activity} can be counted against the {@link LineItem}. </documentation>
</annotation>
<sequence>
<element maxOccurs="1" minOccurs="0" name="activityId" type="xsd:int">
<annotation>
<documentation> The ID of the {@link Activity} to which the {@link LineItem} should be associated. This attribute is required. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="clickThroughConversionCost" type="tns:Money">
<annotation>
<documentation> The amount of money to attribute per click through conversion. This attribute is required for creating a {@code LineItemActivityAssociation}. The currency code is readonly and should match the {@link LineItem}. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="viewThroughConversionCost" type="tns:Money">
<annotation>
<documentation> The amount of money to attribute per view through conversion. This attribute is required for creating a {@code LineItemActivityAssociation}. The currency code is readonly and should match the {@link LineItem}. </documentation>
</annotation>
</element>
</sequence>
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
<complexType name="LineItemDealInfoDto">
<annotation>
<documentation> Data transfer object for the exchange deal info of a line item. </documentation>
</annotation>
<sequence>
<element maxOccurs="1" minOccurs="0" name="externalDealId" type="xsd:long">
<annotation>
<documentation> The external deal ID shared between seller and buyer. This field is only present if the deal has been finalized. This attribute is read-only and is assigned by Google. </documentation>
</annotation>
</element>
</sequence>
</complexType>
<complexType name="LineItemDeliveryForecast">
<annotation>
<documentation> The forecasted delivery of a {@link ProspectiveLineItem}. </documentation>
</annotation>
<sequence>
<element maxOccurs="1" minOccurs="0" name="lineItemId" type="xsd:long">
<annotation>
<documentation> Uniquely identifies this line item delivery forecast. This value is read-only and will be either the ID of the {@link LineItem} object it represents, or {@code null} if the forecast represents a prospective line item. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="orderId" type="xsd:long">
<annotation>
<documentation> The unique ID for the {@link Order} object that this line item belongs to, or {@code null} if the forecast represents a prospective line item without an {@link LineItem#orderId} set. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="unitType" type="tns:UnitType">
<annotation>
<documentation> The unit with which the goal or cap of the {@link LineItem} is defined. Will be the same value as {@link Goal#unitType} for both a set line item or a prospective one. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="predictedDeliveryUnits" type="xsd:long">
<annotation>
<documentation> The number of units, defined by {@link Goal#unitType}, that will be delivered by the line item. Delivery of existing line items that are of same or lower priorities may be impacted. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="deliveredUnits" type="xsd:long">
<annotation>
<documentation> The number of units, defined by {@link Goal#unitType}, that have already been served if the reservation is already running. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="matchedUnits" type="xsd:long">
<annotation>
<documentation> The number of units, defined by {@link Goal#unitType}, that match the specified {@link LineItem#targeting} and delivery settings. </documentation>
</annotation>
</element>
</sequence>
</complexType>
<complexType name="LineItem">
<annotation>
<documentation> {@link LineItem} is an advertiser's commitment to purchase a specific number of ad impressions, clicks, or time. </documentation>
</annotation>
<complexContent>
<extension base="tns:LineItemSummary">
<sequence>
<element maxOccurs="1" minOccurs="0" name="targeting" type="tns:Targeting">
<annotation>
<documentation> Contains the targeting criteria for the ad campaign. This attribute is required. </documentation>
</annotation>
</element>
<element maxOccurs="unbounded" minOccurs="0" name="creativeTargetings" type="tns:CreativeTargeting">
<annotation>
<documentation> A list of {@link CreativeTargeting} objects that can be used to specify creative level targeting for this line item. Creative level targeting is specified in a creative placeholder's {@link CreativePlaceholder#targetingName} field by referencing the creative targeting's {@link CreativeTargeting#name name}. It also needs to be re-specified in the {@link LineItemCreativeAssociation#targetingName} field when associating a line item with a creative that fits into that placeholder. </documentation>
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
<complexType name="LineItemSummary">
<annotation>
<documentation> The {@code LineItemSummary} represents the base class from which a {@code LineItem} is derived. </documentation>
</annotation>
<sequence>
<element maxOccurs="1" minOccurs="0" name="orderId" type="xsd:long">
<annotation>
<documentation> The ID of the {@link Order} to which the {@code LineItem} belongs. This attribute is required. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="id" type="xsd:long">
<annotation>
<documentation> Uniquely identifies the {@code LineItem}. This attribute is read-only and is assigned by Google when a line item is created. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="name" type="xsd:string">
<annotation>
<documentation> The name of the line item. This attribute is required and has a maximum length of 255 characters. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="externalId" type="xsd:string">
<annotation>
<documentation> An identifier for the {@code LineItem} that is meaningful to the publisher. This attribute is optional and has a maximum length of 255 characters. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="orderName" type="xsd:string">
<annotation>
<documentation> The name of the {@link Order}. This value is read-only. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="startDateTime" type="tns:DateTime">
<annotation>
<documentation> The date and time on which the {@code LineItem} is enabled to begin serving. This attribute is required and must be in the future. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="startDateTimeType" type="tns:StartDateTimeType">
<annotation>
<documentation> Specifies whether to start serving to the {@code LineItem} right away, in an hour, etc. This attribute is optional and defaults to {@link StartDateTimeType#USE_START_DATE_TIME}. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="endDateTime" type="tns:DateTime">
<annotation>
<documentation> The date and time on which the {@code LineItem} will stop serving. This attribute is required unless {@link LineItem#unlimitedEndDateTime} is set to {@code true}. If specified, it must be after the {@link LineItem#startDateTime}. This end date and time does not include auto extension days. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="autoExtensionDays" type="xsd:int">
<annotation>
<documentation> The number of days to allow a line item to deliver past its {@link #endDateTime}. A maximum of 7 days is allowed. This is feature is only available for Ad Manager 360 accounts. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="unlimitedEndDateTime" type="xsd:boolean">
<annotation>
<documentation> Specifies whether or not the {@code LineItem} has an end time. This attribute is optional and defaults to false. It can be be set to {@code true} for only line items of type {@link LineItemType#SPONSORSHIP}, {@link LineItemType#NETWORK}, {@link LineItemType#PRICE_PRIORITY} and {@link LineItemType#HOUSE}. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="creativeRotationType" type="tns:CreativeRotationType">
<annotation>
<documentation> The strategy used for displaying multiple {@link Creative} objects that are associated with the {@code LineItem}. This attribute is required. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="deliveryRateType" type="tns:DeliveryRateType">
<annotation>
<documentation> The strategy for delivering ads over the course of the line item's duration. This attribute is optional and defaults to {@link DeliveryRateType#EVENLY} or {@link DeliveryRateType#FRONTLOADED} depending on the network's configuration. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="deliveryForecastSource" type="tns:DeliveryForecastSource">
<annotation>
<documentation> Strategy for choosing forecasted traffic shapes to pace line items. This field is optional and defaults to {@link DeliveryForecastSource#HISTORICAL}. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="customPacingCurve" type="tns:CustomPacingCurve">
<annotation>
<documentation> The curve that is used to pace the line item's delivery. This field is required if and only if the delivery forecast source is {@link DeliveryForecastSource#CUSTOM_PACING_CURVE}. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="roadblockingType" type="tns:RoadblockingType">
<annotation>
<documentation> The strategy for serving roadblocked creatives, i.e. instances where multiple creatives must be served together on a single web page. This attribute is optional and defaults to {@link RoadblockingType#ONE_OR_MORE}. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="skippableAdType" type="tns:SkippableAdType">
<annotation>
<documentation> The nature of the line item's creatives' skippability. This attribute is optional, only applicable for video line items, and defaults to {@link SkippableAdType#NOT_SKIPPABLE}. </documentation>
</annotation>
</element>
<element maxOccurs="unbounded" minOccurs="0" name="frequencyCaps" type="tns:FrequencyCap">
<annotation>
<documentation> The set of frequency capping units for this {@code LineItem}. This attribute is optional. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="lineItemType" type="tns:LineItemType">
<annotation>
<documentation> Indicates the line item type of a {@code LineItem}. This attribute is required. <p>The line item type determines the default priority of the line item. More information can be found on the <a href="https://support.google.com/admanager/answer/177279">Ad Manager Help Center</a>. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="priority" type="xsd:int">
<annotation>
<documentation> The priority for the line item. Valid values range from 1 to 16. This field is optional and defaults to the default priority of the {@link LineItemType}. <p>The following table shows the default, minimum, and maximum priority values are for each line item type: <table> <tr> <th colspan="2" scope="col"> LineItemType - default priority (minimum priority, maximum priority) </th> </tr> <tr> <td>{@link LineItemType#SPONSORSHIP}</td> <td>4 (2, 5)</td> </tr> <tr> <td>{@link LineItemType#STANDARD}</td> <td>8 (6, 10)</td> </tr> <tr> <td>{@link LineItemType#NETWORK}</td> <td>12 (11, 14)</td> </tr> <tr> <td>{@link LineItemType#BULK}</td> <td>12 (11, 14)</td> </tr> <tr> <td>{@link LineItemType#PRICE_PRIORITY}</td> <td>12 (11, 14)</td> </tr> <tr> <td>{@link LineItemType#HOUSE}</td> <td>16 (15, 16)</td> </tr> <tr> <td>{@link LineItemType#CLICK_TRACKING}</td> <td>16 (1, 16)</td> </tr> <tr> <td>{@link LineItemType#AD_EXCHANGE}</td> <td>12 (1, 16)</td> </tr> <td>{@link LineItemType#ADSENSE}</td> <td>12 (1, 16)</td> </tr> <td>{@link LineItemType#BUMPER}</td> <td>16 (15, 16)</td> </tr> </table> <p>This field can only be edited by certain networks, otherwise a {@link PermissionError} will occur. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="costPerUnit" type="tns:Money">
<annotation>
<documentation> The amount of money to spend per impression or click. This attribute is required for creating a {@code LineItem}. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="valueCostPerUnit" type="tns:Money">
<annotation>
<documentation> An amount to help the adserver rank inventory. {@link LineItem#valueCostPerUnit} artificially raises the value of inventory over the {@link LineItem#costPerUnit} but avoids raising the actual {@link LineItem#costPerUnit}. This attribute is optional and defaults to a {@link Money} object in the local currency with {@link Money#microAmount} 0. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="costType" type="tns:CostType">
<annotation>
<documentation> The method used for billing this {@code LineItem}. This attribute is required. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="discountType" type="tns:LineItemDiscountType">
<annotation>
<documentation> The type of discount being applied to a {@code LineItem}, either percentage based or absolute. This attribute is optional and defaults to {@link LineItemDiscountType#PERCENTAGE}. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="discount" type="xsd:double">
<annotation>
<documentation> The number here is either a percentage or an absolute value depending on the {@code LineItemDiscountType}. If the {@code LineItemDiscountType} is {@link LineItemDiscountType#PERCENTAGE}, then only non-fractional values are supported. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="contractedUnitsBought" type="xsd:long">
<annotation>
<documentation> This attribute is only applicable for certain {@link #lineItemType line item types} and acts as an "FYI" or note, which does not impact adserving or other backend systems. <p>For {@link LineItemType#SPONSORSHIP} line items, this represents the minimum quantity, which is a lifetime impression volume goal for reporting purposes only. <p>For {@link LineItemType#STANDARD} line items, this represent the contracted quantity, which is the number of units specified in the contract the advertiser has bought for this {@code LineItem}. This field is just a "FYI" for traffickers to manually intervene with the {@code LineItem} when needed. This attribute is only available for {@link LineItemType#STANDARD} line items if you have this feature enabled on your network. </documentation>
</annotation>
</element>
<element maxOccurs="unbounded" minOccurs="0" name="creativePlaceholders" type="tns:CreativePlaceholder">
<annotation>
<documentation> Details about the creatives that are expected to serve through this {@code LineItem}. This attribute is required and replaces the {@code creativeSizes} attribute. </documentation>
</annotation>
</element>
<element maxOccurs="unbounded" minOccurs="0" name="activityAssociations" type="tns:LineItemActivityAssociation">
<annotation>
<documentation> This attribute is required and meaningful only if the {@link LineItem#costType} is {@link CostType.CPA}. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="environmentType" type="tns:EnvironmentType">
<annotation>
<documentation> The environment that the {@code LineItem} is targeting. The default value is {@link EnvironmentType#BROWSER}. If this value is {@link EnvironmentType#VIDEO_PLAYER}, then this line item can only target {@code AdUnits} that have {@code AdUnitSizes} whose {@code environmentType} is also {@code VIDEO_PLAYER}. </documentation>
</annotation>
</element>
<element maxOccurs="unbounded" minOccurs="0" name="allowedFormats" type="tns:AllowedFormats">
<annotation>
<documentation> The set of {@link allowedFormats} that this programmatic line item can have. If the set is empty, this line item allows all formats. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="companionDeliveryOption" type="tns:CompanionDeliveryOption">
<annotation>
<documentation> The delivery option for companions. Setting this field is only meaningful if the following conditions are met: <ol> <li>The <b>Guaranteed roadblocks</b> feature is enabled on your network. <li>One of the following is true (both cannot be true, these are mutually exclusive). <ul> <li>The {@link #environmentType} is {@link EnvironmentType#VIDEO_PLAYER}. <li>The {@link #roadblockingType} is {@link RoadblockingType#CREATIVE_SET}. </ul> </ol> <p>This field is optional and defaults to {@link CompanionDeliveryOption#OPTIONAL} if the above conditions are met. In all other cases it defaults to {@link CompanionDeliveryOption#UNKNOWN} and is not meaningful. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="allowOverbook" type="xsd:boolean">
<annotation>
<documentation> The flag indicates whether overbooking should be allowed when creating or updating reservations of line item types {@link LineItemType#SPONSORSHIP} and {@link LineItemType#STANDARD}. When true, operations on this line item will never trigger a {@link ForecastError}, which corresponds to an overbook warning in the UI. The default value is false. <p>Note: this field will not persist on the line item itself, and the value will only affect the current request. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="skipInventoryCheck" type="xsd:boolean">
<annotation>
<documentation> The flag indicates whether the inventory check should be skipped when creating or updating a line item. The default value is false. <p>Note: this field will not persist on the line item itself, and the value will only affect the current request. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="skipCrossSellingRuleWarningChecks" type="xsd:boolean">
<annotation>
<documentation> True to skip checks for warnings from rules applied to line items targeting inventory shared by a distributor partner for cross selling when performing an action on this line item. The default is false. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="reserveAtCreation" type="xsd:boolean">
<annotation>
<documentation> The flag indicates whether inventory should be reserved when creating a line item of types {@link LineItemType#SPONSORSHIP} and {@link LineItemType#STANDARD} in an unapproved {@link Order}. The default value is false. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="stats" type="tns:Stats">
<annotation>
<documentation> Contains trafficking statistics for the line item. This attribute is readonly and is populated by Google. This will be {@code null} in case there are no statistics for a line item yet. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="deliveryIndicator" type="tns:DeliveryIndicator">
<annotation>
<documentation> Indicates how well the line item has been performing. This attribute is readonly and is populated by Google. This will be {@code null} if the delivery indicator information is not available due to one of the following reasons: <ol> <li>The line item is not delivering. <li>The line item has an unlimited goal or cap. <li>The line item has a percentage based goal or cap. </ol> </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="deliveryData" type="tns:DeliveryData">
<annotation>
<documentation> Delivery data provides the number of clicks or impressions delivered for a {@link LineItem} in the last 7 days. This attribute is readonly and is populated by Google. This will be {@code null} if the delivery data cannot be computed due to one of the following reasons: <ol> <li>The line item is not deliverable. <li>The line item has completed delivering more than 7 days ago. <li>The line item has an absolute-based goal. {@link LineItem#deliveryIndicator} should be used to track its progress in this case. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="budget" type="tns:Money">
<annotation>
<documentation> The amount of money allocated to the {@code LineItem}. This attribute is readonly and is populated by Google. The currency code is readonly. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="status" type="tns:ComputedStatus">
<annotation>
<documentation> The status of the {@code LineItem}. This attribute is readonly. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="reservationStatus" type="tns:LineItemSummary.ReservationStatus">
<annotation>
<documentation> Describes whether or not inventory has been reserved for the {@code LineItem}. This attribute is readonly and is assigned by Google. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="isArchived" type="xsd:boolean">
<annotation>
<documentation> The archival status of the {@code LineItem}. This attribute is readonly. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="webPropertyCode" type="xsd:string">
<annotation>
<documentation> The web property code used for dynamic allocation line items. This web property is only required with line item types {@link LineItemType#AD_EXCHANGE} and {@link LineItemType#ADSENSE}. </documentation>
</annotation>
</element>
<element maxOccurs="unbounded" minOccurs="0" name="appliedLabels" type="tns:AppliedLabel">
<annotation>
<documentation> The set of labels applied directly to this line item. </documentation>
</annotation>
</element>
<element maxOccurs="unbounded" minOccurs="0" name="effectiveAppliedLabels" type="tns:AppliedLabel">
<annotation>
<documentation> Contains the set of labels inherited from the order that contains this line item and the advertiser that owns the order. If a label has been negated, only the negated label is returned. This field is readonly and is assigned by Google. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="disableSameAdvertiserCompetitiveExclusion" type="xsd:boolean">
<annotation>
<documentation> If a line item has a series of competitive exclusions on it, it could be blocked from serving with line items from the same advertiser. Setting this to {@code true} will allow line items from the same advertiser to serve regardless of the other competitive exclusion labels being applied. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="lastModifiedByApp" type="xsd:string">
<annotation>
<documentation> The application that last modified this line item. This attribute is read only and is assigned by Google. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="notes" type="xsd:string">
<annotation>
<documentation> Provides any additional notes that may annotate the {@code LineItem}. This attribute is optional and has a maximum length of 65,535 characters. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="competitiveConstraintScope" type="tns:CompetitiveConstraintScope">
<annotation>
<documentation> The {@code CompetitiveConstraintScope} for the competitive exclusion labels assigned to this line item. This field is optional, defaults to {@link CompetitiveConstraintScope#POD}, and only applies to video line items. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="lastModifiedDateTime" type="tns:DateTime">
<annotation>
<documentation> The date and time this line item was last modified. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="creationDateTime" type="tns:DateTime">
<annotation>
<documentation> This attribute may be {@code null} for line items created before this feature was introduced. </documentation>
</annotation>
</element>
<element maxOccurs="unbounded" minOccurs="0" name="customFieldValues" type="tns:BaseCustomFieldValue">
<annotation>
<documentation> The values of the custom fields associated with this line item. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="isMissingCreatives" type="xsd:boolean">
<annotation>
<documentation> Indicates if a {@code LineItem} is missing any {@link Creative creatives} for the {@code creativePlaceholders} specified. <p>{@link Creative Creatives} can be considered missing for several reasons including: <ul> <li>Not enough {@link Creative creatives} of a certain size have been uploaded, as determined by {@link CreativePlaceholder#expectedCreativeCount}. For example a {@code LineItem} specifies 750x350, 400x200 but only a 750x350 was uploaded. Or {@code LineItem} specifies 750x350 with an expected count of 2, but only one was uploaded. <li>The {@link Creative#appliedLabels} of an associated {@code Creative} do not match the {@link CreativePlaceholder#effectiveAppliedLabels} of the {@code LineItem}. For example {@code LineItem} specifies 750x350 with a Foo {@code AppliedLabel} but a 750x350 creative without a {@code AppliedLabel} was uploaded. </ul> </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="programmaticCreativeSource" type="tns:ProgrammaticCreativeSource">
<annotation>
<documentation> Indicates the {@link ProgrammaticCreativeSource} of the programmatic line item. This is a read-only field. Any changes must be made on the {@link ProposalLineItem}. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="thirdPartyMeasurementSettings" type="tns:ThirdPartyMeasurementSettings"/>
<element maxOccurs="1" minOccurs="0" name="youtubeKidsRestricted" type="xsd:boolean">
<annotation>
<documentation> Designates this line item as intended for YT Kids app. If true, all creatives associated with this line item must be reviewed and approved. See the <a href="https://support.google.com/yt-partner-sales/answer/10015534">Ad Manager Help Center </a> for more information. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="videoMaxDuration" type="xsd:long">
<annotation>
<documentation> The max duration of a video creative associated with this {@code LineItem} in milliseconds. <p>This attribute is only meaningful for video line items. For version v202011 and earlier, this attribute is optional and defaults to 0. For version v202102 and later, this attribute is required for video line items and must be greater than 0. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="primaryGoal" type="tns:Goal">
<annotation>
<documentation> The primary goal that this {@code LineItem} is associated with, which is used in its pacing and budgeting. </documentation>
</annotation>
</element>
<element maxOccurs="unbounded" minOccurs="0" name="secondaryGoals" type="tns:Goal">
<annotation>
<documentation> The secondary goals that this {@code LineItem} is associated with. It is required and meaningful only if the {@link LineItem#costType} is {@link CostType.CPA} or if the {@link LineItem#lineItemType} is {@link LineItemType#SPONSORSHIP} and {@link LineItem#costType} is {@link CostType.CPM}. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="grpSettings" type="tns:GrpSettings">
<annotation>
<documentation> Contains the information for a line item which has a target GRP demographic. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="dealInfo" type="tns:LineItemDealInfoDto">
<annotation>
<documentation> The deal information associated with this line item, if it is programmatic. </documentation>
</annotation>
</element>
<element maxOccurs="unbounded" minOccurs="0" name="viewabilityProviderCompanyIds" type="xsd:long">
<annotation>
<documentation> Optional IDs of the {@link Company} that provide ad verification for this line item. {@link Company.Type#VIEWABILITY_PROVIDER}. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="childContentEligibility" type="tns:ChildContentEligibility">
<annotation>
<documentation> Child content eligibility designation for this line item. <p>This field is optional and defaults to {@link ChildContentEligibility#DISALLOWED}. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="customVastExtension" type="xsd:string">
<annotation>
<documentation> Custom XML to be rendered in a custom VAST response at serving time. </documentation>
</annotation>
</element>
</sequence>
</complexType>
<complexType name="Location">
<annotation>
<documentation> A {@link Location} represents a geographical entity that can be targeted. If a location type is not available because of the API version you are using, the location will be represented as just the base class, otherwise it will be sub-classed correctly. </documentation>
</annotation>
<sequence>
<element maxOccurs="1" minOccurs="0" name="id" type="xsd:long">
<annotation>
<documentation> Uniquely identifies each {@code Location}. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="type" type="xsd:string">
<annotation>
<documentation> The location type for this geographical entity (ex. "COUNTRY", "CITY", "STATE", "COUNTY", etc.) </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="canonicalParentId" type="xsd:int">
<annotation>
<documentation> The nearest location parent's ID for this geographical entity. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="displayName" type="xsd:string">
<annotation>
<documentation> The localized name of the geographical entity. </documentation>
</annotation>
</element>
</sequence>
</complexType>
<complexType name="MobileApplicationTargeting">
<annotation>
<documentation> Provides line items the ability to target or exclude users' mobile applications. </documentation>
</annotation>
<sequence>
<element maxOccurs="unbounded" minOccurs="0" name="mobileApplicationIds" type="xsd:long">
<annotation>
<documentation> The {@link MobileApplication#applicationId IDs} that are being targeted or excluded by the {@link LineItem}. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="isTargeted" type="xsd:boolean">
<annotation>
<documentation> Indicates whether mobile apps should be targeted or excluded. This attribute is optional and defaults to {@code true}. </documentation>
</annotation>
</element>
</sequence>
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
<complexType name="MobileCarrier">
<annotation>
<documentation> Represents a mobile carrier. Carrier targeting is only available to Ad Manager mobile publishers. For a list of current mobile carriers, you can use {@link PublisherQueryLanguageService#mobile_carrier}. </documentation>
</annotation>
<complexContent>
<extension base="tns:Technology">
<sequence/>
</extension>
</complexContent>
</complexType>
<complexType name="MobileCarrierTargeting">
<annotation>
<documentation> Represents mobile carriers that are being targeted or excluded by the {@link LineItem}. </documentation>
</annotation>
<sequence>
<element maxOccurs="1" minOccurs="0" name="isTargeted" type="xsd:boolean">
<annotation>
<documentation> Indicates whether mobile carriers should be targeted or excluded. This attribute is optional and defaults to {@code true}. </documentation>
</annotation>
</element>
<element maxOccurs="unbounded" minOccurs="0" name="mobileCarriers" type="tns:Technology">
<annotation>
<documentation> Mobile carriers that are being targeted or excluded by the {@link LineItem}. </documentation>
</annotation>
</element>
</sequence>
</complexType>
<complexType name="MobileDevice">
<annotation>
<documentation> Represents a Mobile Device. </documentation>
</annotation>
<complexContent>
<extension base="tns:Technology">
<sequence>
<element maxOccurs="1" minOccurs="0" name="manufacturerCriterionId" type="xsd:long">
<annotation>
<documentation> Manufacturer Id. </documentation>
</annotation>
</element>
</sequence>
</extension>
</complexContent>
</complexType>
<complexType name="MobileDeviceSubmodel">
<annotation>
<documentation> Represents a mobile device submodel. </documentation>
</annotation>
<complexContent>
<extension base="tns:Technology">
<sequence>
<element maxOccurs="1" minOccurs="0" name="mobileDeviceCriterionId" type="xsd:long">
<annotation>
<documentation> The mobile device id. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="deviceManufacturerCriterionId" type="xsd:long">
<annotation>
<documentation> The device manufacturer id. </documentation>
</annotation>
</element>
</sequence>
</extension>
</complexContent>
</complexType>
<complexType name="MobileDeviceSubmodelTargeting">
<annotation>
<documentation> Represents mobile devices that are being targeted or excluded by the {@link LineItem}. </documentation>
</annotation>
<sequence>
<element maxOccurs="unbounded" minOccurs="0" name="targetedMobileDeviceSubmodels" type="tns:Technology">
<annotation>
<documentation> Mobile device submodels that are being targeted by the {@link LineItem}. </documentation>
</annotation>
</element>
<element maxOccurs="unbounded" minOccurs="0" name="excludedMobileDeviceSubmodels" type="tns:Technology">
<annotation>
<documentation> Mobile device submodels that are being excluded by the {@link LineItem}. </documentation>
</annotation>
</element>
</sequence>
</complexType>
<complexType name="MobileDeviceTargeting">
<annotation>
<documentation> Represents mobile devices that are being targeted or excluded by the {@link LineItem}. </documentation>
</annotation>
<sequence>
<element maxOccurs="unbounded" minOccurs="0" name="targetedMobileDevices" type="tns:Technology">
<annotation>
<documentation> Mobile devices that are being targeted by the {@link LineItem}. </documentation>
</annotation>
</element>
<element maxOccurs="unbounded" minOccurs="0" name="excludedMobileDevices" type="tns:Technology">
<annotation>
<documentation> Mobile devices that are being excluded by the {@link LineItem}. </documentation>
</annotation>
</element>
</sequence>
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
<complexType name="OperatingSystem">
<annotation>
<documentation> Represents an Operating System, such as Linux, Mac OS or Windows. </documentation>
</annotation>
<complexContent>
<extension base="tns:Technology">
<sequence/>
</extension>
</complexContent>
</complexType>
<complexType name="OperatingSystemTargeting">
<annotation>
<documentation> Represents operating systems that are being targeted or excluded by the {@link LineItem}. </documentation>
</annotation>
<sequence>
<element maxOccurs="1" minOccurs="0" name="isTargeted" type="xsd:boolean">
<annotation>
<documentation> Indicates whether operating systems should be targeted or excluded. This attribute is optional and defaults to {@code true}. </documentation>
</annotation>
</element>
<element maxOccurs="unbounded" minOccurs="0" name="operatingSystems" type="tns:Technology">
<annotation>
<documentation> Operating systems that are being targeted or excluded by the {@link LineItem}. </documentation>
</annotation>
</element>
</sequence>
</complexType>
<complexType name="OperatingSystemVersion">
<annotation>
<documentation> Represents a specific version of an operating system. </documentation>
</annotation>
<complexContent>
<extension base="tns:Technology">
<sequence>
<element maxOccurs="1" minOccurs="0" name="majorVersion" type="xsd:int">
<annotation>
<documentation> The operating system major version. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="minorVersion" type="xsd:int">
<annotation>
<documentation> The operating system minor version. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="microVersion" type="xsd:int">
<annotation>
<documentation> The operating system micro version. </documentation>
</annotation>
</element>
</sequence>
</extension>
</complexContent>
</complexType>
<complexType name="OperatingSystemVersionTargeting">
<annotation>
<documentation> Represents operating system versions that are being targeted or excluded by the {@link LineItem}. </documentation>
</annotation>
<sequence>
<element maxOccurs="unbounded" minOccurs="0" name="targetedOperatingSystemVersions" type="tns:Technology">
<annotation>
<documentation> Operating system versions that are being targeted by the {@link LineItem}. </documentation>
</annotation>
</element>
<element maxOccurs="unbounded" minOccurs="0" name="excludedOperatingSystemVersions" type="tns:Technology">
<annotation>
<documentation> Operating system versions that are being excluded by the {@link LineItem}. </documentation>
</annotation>
</element>
</sequence>
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
<complexType name="PrecisionError">
<annotation>
<documentation> List all errors associated with number precisions. </documentation>
</annotation>
<complexContent>
<extension base="tns:ApiError">
<sequence>
<element maxOccurs="1" minOccurs="0" name="reason" type="tns:PrecisionError.Reason"/>
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
<complexType name="ProposalLineItem">
<annotation>
<documentation> A {@code ProposalLineItem} is added to a programmatic {@link Proposal} and is similar to a delivery {@link LineItem}. It contains delivery details including information like impression goal or quantity, start and end times, and targeting. </documentation>
</annotation>
<sequence>
<element maxOccurs="1" minOccurs="0" name="id" type="xsd:long">
<annotation>
<documentation> The unique ID of the {@code ProposalLineItem}. This attribute is read-only. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="proposalId" type="xsd:long">
<annotation>
<documentation> The unique ID of the {@link Proposal}, to which the {@code ProposalLineItem} belongs. This attribute is required for creation and then is readonly. <span class="constraint Required">This attribute is required.</span> </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="name" type="xsd:string">
<annotation>
<documentation> The name of the {@code ProposalLineItem} which should be unique under the same {@link Proposal}. This attribute has a maximum length of 255 characters. This attribute can be configured as editable after the proposal has been submitted. Please check with your network administrator for editable fields configuration. <span class="constraint Required">This attribute is required.</span> </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="startDateTime" type="tns:DateTime">
<annotation>
<documentation> The date and time at which the line item associated with the {@code ProposalLineItem} is enabled to begin serving. This attribute is optional during creation, but required and must be in the future when it turns into a line item. The {@link DateTime#timeZoneID} is required if start date time is not {@code null}. This attribute becomes readonly once the {@code ProposalLineItem} has started delivering. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="endDateTime" type="tns:DateTime">
<annotation>
<documentation> The date and time at which the line item associated with the {@code ProposalLineItem} stops beening served. This attribute is optional during creation, but required and must be after the {@link #startDateTime}. The {@link DateTime#timeZoneID} is required if end date time is not {@code null}. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="internalNotes" type="xsd:string">
<annotation>
<documentation> Provides any additional notes that may annotate the {@code ProposalLineItem}. This attribute is optional and has a maximum length of 65,535 characters. This attribute can be configured as editable after the proposal has been submitted. Please check with your network administrator for editable fields configuration. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="isArchived" type="xsd:boolean">
<annotation>
<documentation> The archival status of the {@code ProposalLineItem}. This attribute is read-only. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="goal" type="tns:Goal">
<annotation>
<documentation> The goal(i.e. contracted quantity, quantity or limit) that this {@code ProposalLineItem} is associated with, which is used in its pacing and budgeting. {@link Goal#units} must be greater than 0 when the proposal line item turns into a line item, {@link Goal#goalType} and {@link Goal#unitType} are readonly. For a Preferred deal {@code ProposalLineItem}, the goal type can only be {@link GoalType#NONE}. <span class="constraint Required">This attribute is required.</span> </documentation>
</annotation>
</element>
<element maxOccurs="unbounded" minOccurs="0" name="secondaryGoals" type="tns:Goal">
<annotation>
<documentation> The secondary goals that this {@code ProposalLineItem} is associated with. For a programmatic line item with the properties {@link RateType#CPM} and {@link LineItemType#SPONSORSHIP}, this field will have one goal which describes the impressions cap. For other cases, this field is an empty list. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="contractedUnitsBought" type="xsd:long">
<annotation>
<documentation> The contracted number of daily minimum impressions used for {@link LineItemType#SPONSORSHIP} {@code ProposalLineItem} deals with a rate type of {@link RateType#CPD}. <p>This attribute is required for percentage-based-goal {@link ProposalLineItem proposal line items}. It does not impact ad-serving and is for reporting purposes only. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="deliveryRateType" type="tns:DeliveryRateType">
<annotation>
<documentation> The strategy for delivering ads over the course of the {@code ProposalLineItem}'s duration. This attribute is required. For a Preferred deal {@code ProposalLineItem}, the value can only be {@link DeliveryRateType#FRONTLOADED}. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="roadblockingType" type="tns:RoadblockingType">
<annotation>
<documentation> The strategy for serving roadblocked creatives, i.e. instances where multiple creatives must be served together on a single web page. This attribute is optional during creation and defaults to the {@link Product#roadblockingType product's roadblocking type}, or {@link RoadblockingType#ONE_OR_MORE} if not specified by the product. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="companionDeliveryOption" type="tns:CompanionDeliveryOption">
<annotation>
<documentation> The delivery option for companions. This is only valid if the roadblocking type is {@link RoadblockingType#CREATIVE_SET}. The default value for roadblocking creatives is {@link CompanionDeliveryOption#OPTIONAL}. The default value in other cases is {@link CompanionDeliveryOption#UNKNOWN}. Providing something other than {@link CompanionDeliveryOption#UNKNOWN} will cause an error. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="videoMaxDuration" type="xsd:long">
<annotation>
<documentation> The max duration of a video creative associated with this {@code ProposalLineItem} in milliseconds. This attribute is optional, defaults to the {@link Product#videoMaxDuration} on the {@link Product} it was created with, and only meaningful if this is a video proposal line item. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="videoCreativeSkippableAdType" type="tns:SkippableAdType">
<annotation>
<documentation> The proposal line item's creatives' skippability. This attribute is optional, only applicable for video proposal line items, and defaults to {@link SkippableAdType#NOT_SKIPPABLE}. </documentation>
</annotation>
</element>
<element maxOccurs="unbounded" minOccurs="0" name="frequencyCaps" type="tns:FrequencyCap">
<annotation>
<documentation> The set of frequency capping units for this {@code ProposalLineItem}. This attribute is optional during creation and defaults to the {@link Product#frequencyCaps product's frequency caps} if {@link Product#allowFrequencyCapsCustomization} is {@code false}. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="dfpLineItemId" type="xsd:long">
<annotation>
<documentation> The unique ID of corresponding {@link LineItem}. This will be {@code null} if the {@link Proposal} has not been pushed to Ad Manager. This attribute is read-only. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="lineItemType" type="tns:LineItemType">
<annotation>
<documentation> The corresponding {@link LineItemType} of the {@code ProposalLineItem}. For a programmatic {@code ProposalLineItem}, the value can only be one of: <ul> <li>{@link LineItemType#SPONSORSHIP} <li>{@link LineItemType#STANDARD} <li>{@link LineItemType#PREFERRED_DEAL} </ul> <span class="constraint Required">This attribute is required.</span> </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="lineItemPriority" type="xsd:int">
<annotation>
<documentation> The priority for the corresponding {@link LineItem} of the {@code ProposalLineItem}. This attribute is optional during creation and defaults to the default priority of the {@link #lineItemType}. For forecasting, this attribute is optional and has a default value assigned by Google. See {@link LineItem#priority} for more information. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="rateType" type="tns:RateType">
<annotation>
<documentation> The method used for billing the {@code ProposalLineItem}. This attribute is read-only. <span class="constraint Required">This attribute is required.</span> </documentation>
</annotation>
</element>
<element maxOccurs="unbounded" minOccurs="0" name="creativePlaceholders" type="tns:CreativePlaceholder">
<annotation>
<documentation> Details about the creatives that are expected to serve through the {@code ProposalLineItem}. This attribute is optional during creation and defaults to the {@link Product#creativePlaceholders product's creative placeholders}. <span class="constraint Required">This attribute is required.</span> </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="targeting" type="tns:Targeting">
<annotation>
<documentation> Contains the targeting criteria for the {@code ProposalLineItem}. <span class="constraint Required">This attribute is required.</span> </documentation>
</annotation>
</element>
<element maxOccurs="unbounded" minOccurs="0" name="customFieldValues" type="tns:BaseCustomFieldValue">
<annotation>
<documentation> The values of the custom fields associated with the {@code ProposalLineItem}. This attribute is optional. This attribute can be configured as editable after the proposal has been submitted. Please check with your network administrator for editable fields configuration. </documentation>
</annotation>
</element>
<element maxOccurs="unbounded" minOccurs="0" name="appliedLabels" type="tns:AppliedLabel">
<annotation>
<documentation> The set of labels applied directly to the {@code ProposalLineItem}. This attribute is optional. </documentation>
</annotation>
</element>
<element maxOccurs="unbounded" minOccurs="0" name="effectiveAppliedLabels" type="tns:AppliedLabel">
<annotation>
<documentation> Contains the set of labels applied directly to the proposal as well as those inherited ones. If a label has been negated, only the negated label is returned. This attribute is read-only. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="disableSameAdvertiserCompetitiveExclusion" type="xsd:boolean">
<annotation>
<documentation> If a line item has a series of competitive exclusions on it, it could be blocked from serving with line items from the same advertiser. Setting this to {@code true} will allow line items from the same advertiser to serve regardless of the other competitive exclusion labels being applied. <p>This attribute is optional and defaults to false. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="isSold" type="xsd:boolean">
<annotation>
<documentation> Indicates whether this {@code ProposalLineItem} has been sold. This attribute is read-only. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="netRate" type="tns:Money">
<annotation>
<documentation> The amount of money to spend per impression or click in proposal currency. It supports precision of 4 decimal places in terms of the fundamental currency unit, so the {@link Money#getAmountInMicros} must be multiples of 100. It doesn't include agency commission. <p>For example, if {@link Proposal#currencyCode} is 'USD', then $123.4567 could be represented as 123456700, but further precision is not supported. <p>The field {@link ProposalLineItem#netRate} is required, and used to calculate {@link ProposalLineItem#netCost} if unspecified. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="netCost" type="tns:Money">
<annotation>
<documentation> The cost of the {@code ProposalLineItem} in proposal currency. It supports precision of 2 decimal places in terms of the fundamental currency unit, so the {@link Money#getAmountInMicros} must be multiples of 10000. It doesn't include agency commission. <p>For example, if {@link Proposal#currencyCode} is 'USD', then $123.45 could be represented as 123450000, but further precision is not supported. <p>The field {@link ProposalLineItem#netRate} is required, and used to calculate {@link ProposalLineItem#netCost} if unspecified. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="deliveryIndicator" type="tns:DeliveryIndicator">
<annotation>
<documentation> Indicates how well the line item generated from this proposal line item has been performing. This will be {@code null} if the delivery indicator information is not available due to one of the following reasons: <ol> <li>The proposal line item has not pushed to Ad Manager. <li>The line item is not delivering. <li>The line item has an unlimited goal or cap. <li>The line item has a percentage based goal or cap. </ol> This attribute is read-only. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="deliveryData" type="tns:DeliveryData">
<annotation>
<documentation> Delivery data provides the number of clicks or impressions delivered for the {@link LineItem} generated from this proposal line item in the last 7 days. This will be {@code null} if the delivery data cannot be computed due to one of the following reasons: <ol> <li>The proposal line item has not pushed to Ad Manager. <li>The line item is not deliverable. <li>The line item has completed delivering more than 7 days ago. <li>The line item has an absolute-based goal. {@link ProposalLineItem#deliveryIndicator} should be used to track its progress in this case. This attribute is read-only. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="computedStatus" type="tns:ComputedStatus">
<annotation>
<documentation> The status of the {@link LineItem} generated from this proposal line item. This will be {@code null} if the proposal line item has not pushed to Ad Manager. This attribute is read-only. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="lastModifiedDateTime" type="tns:DateTime">
<annotation>
<documentation> The date and time this {@code ProposalLineItem} was last modified. <p>This attribute is assigned by Google when a {@code ProposalLineItem} is updated. This attribute is read-only. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="reservationStatus" type="tns:ReservationStatus">
<annotation>
<documentation> The reservation status of the {@link ProposalLineItem}. This attribute is read-only. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="lastReservationDateTime" type="tns:DateTime">
<annotation>
<documentation> The last {@link DateTime} when the {@link ProposalLineItem} reserved inventory. This attribute is read-only. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="environmentType" type="tns:EnvironmentType">
<annotation>
<documentation> The environment that the {@code ProposalLineItem} is targeting. The default value is {@link EnvironmentType#BROWSER}. If this value is {@link EnvironmentType#VIDEO_PLAYER}, then this {@code ProposalLineItem} can only target {@link AdUnit ad units} that have {@link AdUnitSize sizes} whose {@link AdUnitSize#environmentType} is also {@link EnvironmentType#VIDEO_PLAYER}. <p>This field is read-only and set to {@link Product#environmentType} of the product this proposal line item was created from. </documentation>
</annotation>
</element>
<element maxOccurs="unbounded" minOccurs="0" name="allowedFormats" type="tns:AllowedFormats">
<annotation>
<documentation> The set of {@link AllowedFormats} that this proposal line item can have. If the set is empty, this proposal line item allows all formats. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="additionalTerms" type="xsd:string">
<annotation>
<documentation> Additional terms shown to the buyer in Marketplace. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="programmaticCreativeSource" type="tns:ProgrammaticCreativeSource">
<annotation>
<documentation> Indicates the {@link ProgrammaticCreativeSource} of the programmatic line item. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="grpSettings" type="tns:GrpSettings">
<annotation>
<documentation> Contains the information for a proposal line item which has a target GRP demographic. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="estimatedMinimumImpressions" type="xsd:long">
<annotation>
<documentation> The estimated minimum impressions that should be delivered for a proposal line item. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="thirdPartyMeasurementSettings" type="tns:ThirdPartyMeasurementSettings">
<annotation>
<documentation> Contains third party measurement settings for cross-sell Partners </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="makegoodInfo" type="tns:ProposalLineItemMakegoodInfo">
<annotation>
<documentation> Makegood info for this proposal line item. Immutable once created. <p>Null if this proposal line item is not a makegood. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="hasMakegood" type="xsd:boolean">
<annotation>
<documentation> Whether this proposal line item has an associated makegood. This attribute is read-only. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="canCreateMakegood" type="xsd:boolean">
<annotation>
<documentation> Whether a new makegood associated with this line item can be created. This attribute is read-only. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="pauseRole" type="tns:NegotiationRole">
<annotation>
<documentation> The {@link NegotiationRole} that paused the proposal line item, i.e. {@link NegotiationRole#seller} or {@link NegotiationRole#buyer}, or {@code null} when the proposal is not paused. This attribute is read-only. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="pauseReason" type="xsd:string">
<annotation>
<documentation> The reason for pausing the {@link ProposalLineItem}, provided by the {@link pauseRole}. It is {@code null} when the {@link ProposalLineItem} is not paused. This attribute is read-only. </documentation>
</annotation>
</element>
</sequence>
</complexType>
<complexType name="ProposalLineItemMakegoodInfo">
<annotation>
<documentation> Makegood info for a {@link ProposalLineItemDto}. </documentation>
</annotation>
<sequence>
<element maxOccurs="1" minOccurs="0" name="originalProposalLineItemId" type="xsd:long">
<annotation>
<documentation> The ID of the original proposal line item on which this makegood is based. This attribute is read-only. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="reason" type="xsd:string">
<annotation>
<documentation> The publisher-provided reason why this makegood was initiated. This is free form text. <p>The following predefined values can be used to render predefined options in the UI. <p>UNDERDELIVERY: 'Impression underdelivery', SECONDARY_DELIVERY_TERMS: 'Did not meet secondary delivery terms ', PERFORMANCE: 'Performance issues', </documentation>
</annotation>
</element>
</sequence>
</complexType>
<complexType name="ProspectiveLineItem">
<annotation>
<documentation> Represents a prospective line item to be forecasted. </documentation>
</annotation>
<sequence>
<element maxOccurs="1" minOccurs="0" name="lineItem" type="tns:LineItem">
<annotation>
<documentation> The target of the forecast. If {@link LineItem#id} is null or no line item exists with that ID, then a forecast is computed for the subject, predicting what would happen if it were added to the network. If a line item already exists with {@link LineItem#id}, the forecast is computed for the subject, predicting what would happen if the existing line item's settings were modified to match the subject. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="proposalLineItem" type="tns:ProposalLineItem">
<annotation>
<documentation> The target of the forecast if this prospective line item is a proposal line item. <p>If {@link ProposalLineItem#id} is null or no proposal line item exists with that ID, then a forecast is computed for the subject, predicting what would happen if it were added to the network. If a proposal line item already exists with {@link ProposalLineItem#id}, the forecast is computed for the subject, predicting what would happen if the existing proposal line item's settings were modified to match the subject. <p>A proposal line item can optionally correspond to an order {@link LineItem}, in which case, by forecasting a proposal line item, the corresponding line item is implicitly ignored in the forecasting. <p>Either {@link #lineItem} or {@link #proposalLineItem} should be specified but not both. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="advertiserId" type="xsd:long">
<annotation>
<documentation> When set, the line item is assumed to be from this advertiser, and unified blocking rules will apply accordingly. If absent, line items without an existing order won't be subject to unified blocking rules. </documentation>
</annotation>
</element>
</sequence>
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
<complexType name="RequestPlatformTargeting">
<annotation>
<documentation> Provides line items the ability to target the platform that requests and renders the ad. <p>The following rules apply for {@link RequestPlatformTargeting} <ul> <li>{@link RequestPlatformTargeting} must be specified for {@link ProposalLineItem}s. <li>{@link RequestPlatformTargeting} must be specified for video line items. Empty values for {@link RequestPlatformTargeting#targetedRequestPlatforms} mean that all request platforms will be targeted. <li>{@link RequestPlatformTargeting} is read-only and assigned by Google for non-video line items. <li>{@link RequestPlatformTargeting} is read-only and assigned by Google for line items generated from proposal line items. </ul> </documentation>
</annotation>
<sequence>
<element maxOccurs="unbounded" minOccurs="0" name="targetedRequestPlatforms" type="tns:RequestPlatform"/>
</sequence>
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
<complexType name="Size">
<annotation>
<documentation> Represents the dimensions of an {@link AdUnit}, {@link LineItem} or {@link Creative}. <p>For interstitial size (out-of-page), native, ignored and fluid size, {@link Size} must be 1x1. </documentation>
</annotation>
<sequence>
<element maxOccurs="1" minOccurs="0" name="width" type="xsd:int">
<annotation>
<documentation> The width of the {@link AdUnit}, {@link LineItem} or {@link Creative}. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="height" type="xsd:int">
<annotation>
<documentation> The height of the {@link AdUnit}, {@link LineItem} or {@link Creative}. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="isAspectRatio" type="xsd:boolean">
<annotation>
<documentation> Whether this size represents an aspect ratio. </documentation>
</annotation>
</element>
</sequence>
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
<complexType name="Stats">
<annotation>
<documentation> {@code Stats} contains trafficking statistics for {@link LineItem} and {@link LineItemCreativeAssociation} objects </documentation>
</annotation>
<sequence>
<element maxOccurs="1" minOccurs="0" name="impressionsDelivered" type="xsd:long">
<annotation>
<documentation> The number of impressions delivered. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="clicksDelivered" type="xsd:long">
<annotation>
<documentation> The number of clicks delivered. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="videoCompletionsDelivered" type="xsd:long">
<annotation>
<documentation> The number of video completions delivered. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="videoStartsDelivered" type="xsd:long">
<annotation>
<documentation> The number of video starts delivered. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="viewableImpressionsDelivered" type="xsd:long">
<annotation>
<documentation> The number of viewable impressions delivered. </documentation>
</annotation>
</element>
</sequence>
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
<complexType name="TargetedSize">
<annotation>
<documentation> A size that is targeted on a request. </documentation>
</annotation>
<sequence>
<element maxOccurs="1" minOccurs="0" name="size" type="tns:Size"/>
</sequence>
</complexType>
<complexType name="TargetingCriteriaBreakdown">
<annotation>
<documentation> A single targeting criteria breakdown result. </documentation>
</annotation>
<sequence>
<element maxOccurs="1" minOccurs="0" name="targetingDimension" type="tns:TargetingDimension">
<annotation>
<documentation> The dimension of this breakdown </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="targetingCriteriaId" type="xsd:long">
<annotation>
<documentation> The unique ID of the targeting criteria. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="targetingCriteriaName" type="xsd:string">
<annotation>
<documentation> The name of the targeting criteria. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="excluded" type="xsd:boolean">
<annotation>
<documentation> When true, the breakdown is negative. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="availableUnits" type="xsd:long">
<annotation>
<documentation> The available units for this breakdown. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="matchedUnits" type="xsd:long">
<annotation>
<documentation> The matched units for this breakdown. </documentation>
</annotation>
</element>
</sequence>
</complexType>
<complexType name="Targeting">
<annotation>
<documentation> Contains targeting criteria for {@link LineItem} objects. See {@link LineItem#targeting}. </documentation>
</annotation>
<sequence>
<element maxOccurs="1" minOccurs="0" name="geoTargeting" type="tns:GeoTargeting">
<annotation>
<documentation> Specifies what geographical locations are targeted by the {@link LineItem}. This attribute is optional. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="inventoryTargeting" type="tns:InventoryTargeting">
<annotation>
<documentation> Specifies what inventory is targeted by the {@link LineItem}. This attribute is required. The line item must target at least one ad unit or placement. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="dayPartTargeting" type="tns:DayPartTargeting">
<annotation>
<documentation> Specifies the days of the week and times that are targeted by the {@link LineItem}. This attribute is optional. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="dateTimeRangeTargeting" type="tns:DateTimeRangeTargeting">
<annotation>
<documentation> Specifies the dates and time ranges that are targeted by the {@link LineItem}. This attribute is optional. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="technologyTargeting" type="tns:TechnologyTargeting">
<annotation>
<documentation> Specifies the browsing technologies that are targeted by the {@link LineItem}. This attribute is optional. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="customTargeting" type="tns:CustomCriteriaSet">
<annotation>
<documentation> Specifies the collection of custom criteria that is targeted by the {@link LineItem}. <p>Once the {@link LineItem} is updated or modified with custom targeting, the server may return a normalized, but equivalent representation of the custom targeting expression. <p>{@code customTargeting} will have up to three levels of expressions including itself. <p>The top level {@code CustomCriteriaSet} i.e. the {@code customTargeting} object can only contain a {@link CustomCriteriaSet.LogicalOperator#OR} of all its children. <p>The second level of {@code CustomCriteriaSet} objects can only contain {@link CustomCriteriaSet.LogicalOperator#AND} of all their children. If a {@link CustomCriteria} is placed on this level, the server will wrap it in a {@link CustomCriteriaSet}. <p>The third level can only comprise of {@link CustomCriteria} objects. <p>The resulting custom targeting tree would be of the form: <br> <img src="https://chart.apis.google.com/chart?cht=gv&chl=digraph{customTargeting_LogicalOperator_OR-%3ECustomCriteriaSet_LogicalOperator_AND_1-%3ECustomCriteria_1;CustomCriteriaSet_LogicalOperator_AND_1-%3Eellipsis1;customTargeting_LogicalOperator_OR-%3Eellipsis2;ellipsis1[label=%22...%22,shape=none,fontsize=32];ellipsis2[label=%22...%22,shape=none,fontsize=32]}&chs=450x200"/> </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="userDomainTargeting" type="tns:UserDomainTargeting">
<annotation>
<documentation> Specifies the domains or subdomains that are targeted or excluded by the {@link LineItem}. Users visiting from an IP address associated with those domains will be targeted or excluded. This attribute is optional. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="contentTargeting" type="tns:ContentTargeting">
<annotation>
<documentation> Specifies the video categories and individual videos targeted by the {@link LineItem}. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="videoPositionTargeting" type="tns:VideoPositionTargeting">
<annotation>
<documentation> Specifies targeting against video position types. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="mobileApplicationTargeting" type="tns:MobileApplicationTargeting">
<annotation>
<documentation> Specifies targeting against mobile applications. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="buyerUserListTargeting" type="tns:BuyerUserListTargeting">
<annotation>
<documentation> Specifies whether buyer user lists are targeted on a programmatic {@link LineItem} or {@link ProposalLineItem}. This attribute is readonly and is populated by Google. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="inventoryUrlTargeting" type="tns:InventoryUrlTargeting">
<annotation>
<documentation> Specifies the URLs that are targeted by the entity. This is currently only supported by {@link YieldGroup}. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="verticalTargeting" type="tns:VerticalTargeting">
<annotation>
<documentation> Specifies the verticals that are targeted by the entity. The IDs listed here correspond to the IDs in the AD_CATEGORY table of type VERTICAL. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="contentLabelTargeting" type="tns:ContentLabelTargeting">
<annotation>
<documentation> Specifies the content labels that are excluded by the entity. The IDs listed here correspond to the IDs in the CONTENT_LABEL table. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="requestPlatformTargeting" type="tns:RequestPlatformTargeting">
<annotation>
<documentation> Specifies the request platforms that are targeted by the {@link LineItem}. This attribute is required for video line items and for {@link ProposalLineItem}. <p>This value is modifiable for video line items, but read-only for non-video line items. <p>This value is read-only for video line items generated from proposal line items. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="inventorySizeTargeting" type="tns:InventorySizeTargeting">
<annotation>
<documentation> Specifies the sizes that are targeted by the entity. This is currently only supported on {@link YieldGroup} and {@link TrafficDataRequest}. </documentation>
</annotation>
</element>
</sequence>
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
<complexType name="Technology">
<annotation>
<documentation> Represents a technology entity that can be targeted. </documentation>
</annotation>
<sequence>
<element maxOccurs="1" minOccurs="0" name="id" type="xsd:long">
<annotation>
<documentation> The unique ID of the {@code Technology}. This value is required for all forms of {@code TechnologyTargeting}. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="name" type="xsd:string">
<annotation>
<documentation> The name of the technology being targeting. This value is read-only and is assigned by Google. </documentation>
</annotation>
</element>
</sequence>
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
<complexType name="ThirdPartyMeasurementSettings">
<annotation>
<documentation> Contains third party auto-pixeling settings for cross-sell Partners. </documentation>
</annotation>
<sequence>
<element maxOccurs="1" minOccurs="0" name="viewabilityPartner" type="tns:ThirdPartyViewabilityIntegrationPartner">
<annotation>
<documentation> A field to determine the type of ThirdPartyViewabilityIntegrationPartner. This field default is NONE. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="viewabilityClientId" type="xsd:string">
<annotation>
<documentation> The third party partner id for YouTube viewability verification. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="viewabilityReportingId" type="xsd:string">
<annotation>
<documentation> The reporting id that maps viewability partner data with a campaign (or a group of related campaigns) specific data. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="publisherViewabilityPartner" type="tns:ThirdPartyViewabilityIntegrationPartner">
<annotation>
<documentation> A field to determine the type of publisher's viewability partner. This field default is NONE. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="publisherViewabilityClientId" type="xsd:string">
<annotation>
<documentation> The third party partner id for YouTube viewability verification for publisher. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="publisherViewabilityReportingId" type="xsd:string">
<annotation>
<documentation> The reporting id that maps viewability partner data with a campaign (or a group of related campaigns) specific data for publisher. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="brandLiftPartner" type="tns:ThirdPartyBrandLiftIntegrationPartner">
<annotation>
<documentation> A field to determine the type of ThirdPartyBrandLiftIntegrationPartner. This field default is NONE. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="brandLiftClientId" type="xsd:string">
<annotation>
<documentation> The third party partner id for YouTube brand lift verification. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="brandLiftReportingId" type="xsd:string">
<annotation>
<documentation> The reporting id that maps brand lift partner data with a campaign (or a group of related campaigns) specific data. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="reachPartner" type="tns:ThirdPartyReachIntegrationPartner">
<annotation>
<documentation> A field to determine the type of advertiser's ThirdPartyReachIntegrationPartner. This field default is UNKNOWN. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="reachClientId" type="xsd:string">
<annotation>
<documentation> The third party partner id for YouTube reach verification for advertiser. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="reachReportingId" type="xsd:string">
<annotation>
<documentation> The reporting id that maps reach partner data with a campaign (or a group of related campaigns) specific data for advertiser. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="publisherReachPartner" type="tns:ThirdPartyReachIntegrationPartner">
<annotation>
<documentation> A field to determine the type of publisher's ThirdPartyReachIntegrationPartner. This field default is UNKNOWN. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="publisherReachClientId" type="xsd:string">
<annotation>
<documentation> The third party partner id for YouTube reach verification for publisher. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="publisherReachReportingId" type="xsd:string">
<annotation>
<documentation> The reporting id that maps reach partner data with a campaign (or a group of related campaigns) specific data for publisher. </documentation>
</annotation>
</element>
</sequence>
</complexType>
<complexType name="TimeOfDay">
<annotation>
<documentation> Represents a specific time in a day. </documentation>
</annotation>
<sequence>
<element maxOccurs="1" minOccurs="0" name="hour" type="xsd:int">
<annotation>
<documentation> Hour in 24 hour time (0..24). This field must be between 0 and 24, inclusive. This field is required. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="minute" type="tns:MinuteOfHour">
<annotation>
<documentation> Minutes in an hour. Currently, only 0, 15, 30, and 45 are supported. This field is required. </documentation>
</annotation>
</element>
</sequence>
</complexType>
<complexType name="TimeSeries">
<annotation>
<documentation> Represents a chronological sequence of daily values. </documentation>
</annotation>
<sequence>
<element maxOccurs="1" minOccurs="0" name="timeSeriesDateRange" type="tns:DateRange">
<annotation>
<documentation> The date range of the time series. </documentation>
</annotation>
</element>
<element maxOccurs="unbounded" minOccurs="0" name="values" type="xsd:long">
<annotation>
<documentation> The daily values constituting the time series. <p>The number of time series values must equal the number of days spanned by the time series date range, inclusive. E.g.: {@code timeSeriesDateRange} of 2001-08-15 to 2001-08-17 should contain one value for the 15th, one value for the 16th, and one value for the 17th. </documentation>
</annotation>
</element>
</sequence>
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
<complexType name="TrafficDataRequest">
<annotation>
<documentation> Defines a segment of traffic for which traffic data should be returned. </documentation>
</annotation>
<sequence>
<element maxOccurs="1" minOccurs="0" name="targeting" type="tns:Targeting">
<annotation>
<documentation> The {@link TargetingDto} that defines a segment of traffic. <span class="constraint Required">This attribute is required.</span> </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="requestedDateRange" type="tns:DateRange">
<annotation>
<documentation> The date range for which traffic data are requested. This range may cover historical dates, future dates, or both. <p>The data returned are not guaranteed to cover the entire requested date range. If sufficient data are not available to cover the entire requested date range, a response may be returned with a later start date, earlier end date, or both. <span class="constraint Required">This attribute is required.</span> </documentation>
</annotation>
</element>
</sequence>
</complexType>
<complexType name="TrafficDataResponse">
<annotation>
<documentation> Contains forecasted and historical traffic volume data describing a segment of traffic. </documentation>
</annotation>
<sequence>
<element maxOccurs="1" minOccurs="0" name="historicalTimeSeries" type="tns:TimeSeries">
<annotation>
<documentation> Time series of historical traffic ad opportunity counts. <p>This may be null if the requested date range did not contain any historical dates, or if no historical data are available for the requested traffic segment. This attribute is read-only. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="forecastedTimeSeries" type="tns:TimeSeries">
<annotation>
<documentation> Time series of forecasted traffic ad opportunity counts. <p>This may be null if the requested date range did not contain any future dates, or if no forecasted data are available for the requested traffic segment. This attribute is read-only. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="forecastedAssignedTimeSeries" type="tns:TimeSeries">
<annotation>
<documentation> Time series of future traffic volumes forecasted to be sold. <p>This may be null if the requested date range did not contain any future dates, or if no sell-through data are available for the requested traffic segment. This attribute is read-only. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="overallDateRange" type="tns:DateRange">
<annotation>
<documentation> The overall date range spanned by the union of all time series in the response. <p>This is a summary field for convenience. The value will be set such that the start date is equal to the earliest start date of all time series included, and the end date is equal to the latest end date of all time series included. <p>If all time series fields are null, this field will also be null. This attribute is read-only. </documentation>
</annotation>
</element>
</sequence>
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
<complexType name="UserDomainTargeting">
<annotation>
<documentation> Provides line items the ability to target or exclude users visiting their websites from a list of domains or subdomains. </documentation>
</annotation>
<sequence>
<element maxOccurs="unbounded" minOccurs="0" name="domains" type="xsd:string">
<annotation>
<documentation> The domains or subdomains that are being targeted or excluded by the {@link LineItem}. This attribute is required and the maximum length of each domain is 67 characters. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="targeted" type="xsd:boolean">
<annotation>
<documentation> Indicates whether domains should be targeted or excluded. This attribute is optional and defaults to {@code true}. </documentation>
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
<complexType name="VerticalTargeting">
<annotation>
<documentation> Vertical targeting information. </documentation>
</annotation>
<sequence>
<element maxOccurs="unbounded" minOccurs="0" name="targetedVerticalIds" type="xsd:long"/>
<element maxOccurs="unbounded" minOccurs="0" name="excludedVerticalIds" type="xsd:long"/>
</sequence>
</complexType>
<complexType name="VideoPosition">
<annotation>
<documentation> Represents a targetable position within a video. A video ad can be targeted to a position (pre-roll, all mid-rolls, or post-roll), or to a specific mid-roll index. </documentation>
</annotation>
<sequence>
<element maxOccurs="1" minOccurs="0" name="positionType" type="tns:VideoPosition.Type">
<annotation>
<documentation> The type of video position (pre-roll, mid-roll, or post-roll). </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="midrollIndex" type="xsd:int">
<annotation>
<documentation> The index of the mid-roll to target. Only valid if the {@link positionType} is {@link VideoPositionType#MIDROLL}, otherwise this field will be ignored. </documentation>
</annotation>
</element>
</sequence>
</complexType>
<complexType name="VideoPositionTargeting">
<annotation>
<documentation> Represents positions within and around a video where ads can be targeted to. <p>Example positions could be {@code pre-roll} (before the video plays), {@code post-roll} (after a video has completed playback) and {@code mid-roll} (during video playback). <p>Empty video position targeting means that all video positions are allowed. If a bumper line item has empty video position targeting it will be updated to target all bumper positions. </documentation>
</annotation>
<sequence>
<element maxOccurs="unbounded" minOccurs="0" name="targetedPositions" type="tns:VideoPositionTarget">
<annotation>
<documentation> The {@link VideoTargetingPosition} objects being targeted by the video {@link LineItem}. </documentation>
</annotation>
</element>
</sequence>
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
<complexType name="VideoPositionWithinPod">
<annotation>
<documentation> Represents a targetable position within a pod within a video stream. A video ad can be targeted to any position in the pod (first, second, third ... last). If there is only 1 ad in a pod, either first or last will target that position. </documentation>
</annotation>
<sequence>
<element maxOccurs="1" minOccurs="0" name="index" type="xsd:int">
<annotation>
<documentation> The specific index of the pod. The index is defined as: <ul><li>1 = first</li> <li>2 = second</li> <li>3 = third</li> <li>....</li> <li>100 = last</li></ul> 100 will always be the last position. For example, for a pod with 5 positions, 100 would target position 5. Multiple targets against the index 100 can exist.<br> Positions over 100 are not supported. </documentation>
</annotation>
</element>
</sequence>
</complexType>
<complexType name="VideoPositionTarget">
<annotation>
<documentation> Represents the options for targetable positions within a video. </documentation>
</annotation>
<sequence>
<element maxOccurs="1" minOccurs="0" name="videoPosition" type="tns:VideoPosition">
<annotation>
<documentation> The video position to target. This attribute is required. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="videoBumperType" type="tns:VideoBumperType">
<annotation>
<documentation> The video bumper type to target. To target a video position or a pod position, this value must be null. To target a bumper position this value must be populated and the line item must have a bumper type. To target a custom ad spot, this value must be null. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="videoPositionWithinPod" type="tns:VideoPositionWithinPod">
<annotation>
<documentation> The video position within a pod to target. To target a video position or a bumper position, this value must be null. To target a position within a pod this value must be populated. To target a custom ad spot, this value must be null. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="adSpotId" type="xsd:long">
<annotation>
<documentation> A custom spot {@link AdSpot} to target. To target a video position, a bumper type or a video position within a pod this value must be null. </documentation>
</annotation>
</element>
</sequence>
</complexType>
<simpleType name="AdUnitCodeError.Reason">
<restriction base="xsd:string">
<enumeration value="INVALID_CHARACTERS">
<annotation>
<documentation> For {@link AdUnit#adUnitCode}, only alpha-numeric characters, underscores, hyphens, periods, asterisks, double quotes, back slashes, forward slashes, exclamations, left angle brackets, colons and parentheses are allowed. </documentation>
</annotation>
</enumeration>
<enumeration value="INVALID_CHARACTERS_WHEN_UTF_CHARACTERS_ARE_ALLOWED">
<annotation>
<documentation> For {@link AdUnit#adUnitCode}, only letters, numbers, underscores, hyphens, periods, asterisks, double quotes, back slashes, forward slashes, exclamations, left angle brackets, colons and parentheses are allowed. </documentation>
</annotation>
</enumeration>
<enumeration value="INVALID_CHARACTERS_FOR_LEGACY_AD_EXCHANGE_TAG">
<annotation>
<documentation> For {@link AdUnit#adUnitCode} representing slot codes, only alphanumeric characters, underscores, hyphens, periods and colons are allowed. </documentation>
</annotation>
</enumeration>
<enumeration value="LEADING_FORWARD_SLASH">
<annotation>
<documentation> For {@link AdUnit#adUnitCode}, forward slashes are not allowed as the first character. </documentation>
</annotation>
</enumeration>
<enumeration value="RESERVED_CODE">
<annotation>
<documentation> Specific codes matching ca-*pub-*-tag are reserved for "Web Property IUs" generated as part of the SlotCode migration. </documentation>
</annotation>
</enumeration>
<enumeration value="UNKNOWN">
<annotation>
<documentation> The value returned if the actual value is not exposed by the requested API version. </documentation>
</annotation>
</enumeration>
</restriction>
</simpleType>
<simpleType name="AllowedFormats">
<annotation>
<documentation> The formats that a publisher allows on their programmatic {@link LineItem} or {@link ProposalLineItem}. </documentation>
</annotation>
<restriction base="xsd:string">
<enumeration value="AUDIO">
<annotation>
<documentation> Audio format. This is only relevant for programmatic video line items. </documentation>
</annotation>
</enumeration>
<enumeration value="UNKNOWN">
<annotation>
<documentation> The value returned if the actual value is not exposed by the requested API version. </documentation>
</annotation>
</enumeration>
</restriction>
</simpleType>
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
<simpleType name="ChildContentEligibility">
<annotation>
<documentation> Child content eligibility designation. <p>This field is optional and defaults to {@link ChildContentEligibility#DISALLOWED}. This field has no effect on serving enforcement unless you opt to "Child content enforcement" in the network's Child Content settings. </documentation>
</annotation>
<restriction base="xsd:string">
<enumeration value="UNKNOWN"/>
<enumeration value="DISALLOWED">
<annotation>
<documentation> This line item is not eligible to serve on any requests that are child-directed. </documentation>
</annotation>
</enumeration>
<enumeration value="ALLOWED">
<annotation>
<documentation> This line item is eligible to serve on requests that are child-directed. </documentation>
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
<simpleType name="CompanionDeliveryOption">
<annotation>
<documentation> The delivery option for companions. Used for line items whose environmentType is {@link EnvironmentType#VIDEO_PLAYER}. </documentation>
</annotation>
<restriction base="xsd:string">
<enumeration value="OPTIONAL">
<annotation>
<documentation> Companions are not required to serve a creative set. The creative set can serve to inventory that has zero or more matching companions. </documentation>
</annotation>
</enumeration>
<enumeration value="AT_LEAST_ONE">
<annotation>
<documentation> At least one companion must be served in order for the creative set to be used. </documentation>
</annotation>
</enumeration>
<enumeration value="ALL">
<annotation>
<documentation> All companions in the set must be served in order for the creative set to be used. This can still serve to inventory that has more companions than can be filled. </documentation>
</annotation>
</enumeration>
<enumeration value="UNKNOWN">
<annotation>
<documentation> The delivery type is unknown. </documentation>
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
<simpleType name="CompetitiveConstraintScope">
<annotation>
<documentation> The scope to which the assignment of any competitive exclusion labels for a video line item is limited. </documentation>
</annotation>
<restriction base="xsd:string">
<enumeration value="POD">
<annotation>
<documentation> The competitive exclusion label applies to all line items within a single pod (or group). </documentation>
</annotation>
</enumeration>
<enumeration value="STREAM">
<annotation>
<documentation> The competitive exclusion label applies to all line items within the entire stream of content. </documentation>
</annotation>
</enumeration>
<enumeration value="UNKNOWN">
<annotation>
<documentation> The value returned if the actual value is not exposed by the requested API version. </documentation>
</annotation>
</enumeration>
</restriction>
</simpleType>
<simpleType name="ComputedStatus">
<annotation>
<documentation> Describes the computed {@link LineItem} status that is derived from the current state of the line item. </documentation>
</annotation>
<restriction base="xsd:string">
<enumeration value="DELIVERY_EXTENDED">
<annotation>
<documentation> The {@link LineItem} has past its {@link LineItem#endDateTime} with an auto extension, but hasn't met its goal. </documentation>
</annotation>
</enumeration>
<enumeration value="DELIVERING">
<annotation>
<documentation> The {@link LineItem} has begun serving. </documentation>
</annotation>
</enumeration>
<enumeration value="READY">
<annotation>
<documentation> The {@link LineItem} has been activated and is ready to serve. </documentation>
</annotation>
</enumeration>
<enumeration value="PAUSED">
<annotation>
<documentation> The {@link LineItem} has been paused from serving. </documentation>
</annotation>
</enumeration>
<enumeration value="INACTIVE">
<annotation>
<documentation> The {@link LineItem} is inactive. It is either caused by missing creatives or the network disabling auto-activation. </documentation>
</annotation>
</enumeration>
<enumeration value="PAUSED_INVENTORY_RELEASED">
<annotation>
<documentation> The {@link LineItem} has been paused and its reserved inventory has been released. The {@code LineItem} will not serve. </documentation>
</annotation>
</enumeration>
<enumeration value="PENDING_APPROVAL">
<annotation>
<documentation> The {@link LineItem} has been submitted for approval. </documentation>
</annotation>
</enumeration>
<enumeration value="COMPLETED">
<annotation>
<documentation> The {@link LineItem} has completed its run. </documentation>
</annotation>
</enumeration>
<enumeration value="DISAPPROVED">
<annotation>
<documentation> The {@link LineItem} has been disapproved and is not eligible to serve. </documentation>
</annotation>
</enumeration>
<enumeration value="DRAFT">
<annotation>
<documentation> The {@link LineItem} is still being drafted. </documentation>
</annotation>
</enumeration>
<enumeration value="CANCELED">
<annotation>
<documentation> The {@link LineItem} has been canceled and is no longer eligible to serve. This is a legacy status imported from Google Ad Manager orders. </documentation>
</annotation>
</enumeration>
</restriction>
</simpleType>
<simpleType name="CostType">
<annotation>
<documentation> Describes the {@link LineItem} actions that are billable. </documentation>
</annotation>
<restriction base="xsd:string">
<enumeration value="CPA">
<annotation>
<documentation> Starting February 22, 2024 the CPA {@link CostType} will be read only as part of Spotlight deprecation, <a href="https://support.google.com/admanager/answer/7519021#spotlight">learn more</a>. <p>Cost per action. The {@link LineItem#lineItemType} must be one of: <ul> <li>{@link LineItemType#SPONSORSHIP} <li>{@link LineItemType#STANDARD} <li>{@link LineItemType#BULK} <li>{@link LineItemType#NETWORK} </ul> </documentation>
</annotation>
</enumeration>
<enumeration value="CPC">
<annotation>
<documentation> Cost per click. The {@link LineItem#lineItemType} must be one of: <ul> <li>{@link LineItemType#SPONSORSHIP}</li> <li>{@link LineItemType#STANDARD}</li> <li>{@link LineItemType#BULK}</li> <li>{@link LineItemType#NETWORK}</li> <li>{@link LineItemType#PRICE_PRIORITY}</li> <li>{@link LineItemType#HOUSE}</li> </ul> </documentation>
</annotation>
</enumeration>
<enumeration value="CPD">
<annotation>
<documentation> Cost per day. The {@link LineItem#lineItemType} must be one of: <ul> <li>{@link LineItemType#SPONSORSHIP}<li> <li>{@link LineItemType#NETWORK}<li> </ul> </documentation>
</annotation>
</enumeration>
<enumeration value="CPM">
<annotation>
<documentation> Cost per mille (cost per thousand impressions). The {@link LineItem#lineItemType} must be one of: <ul> <li>{@link LineItemType#SPONSORSHIP}</li> <li>{@link LineItemType#STANDARD}</li> <li>{@link LineItemType#BULK}</li> <li>{@link LineItemType#NETWORK}</li> <li>{@link LineItemType#PRICE_PRIORITY}</li> <li>{@link LineItemType#HOUSE}</li> </ul> </documentation>
</annotation>
</enumeration>
<enumeration value="VCPM">
<annotation>
<documentation> Cost per thousand Active View viewable impressions. The {@link LineItem#lineItemType} must be {@link LineItemType#STANDARD}. </documentation>
</annotation>
</enumeration>
<enumeration value="CPM_IN_TARGET">
<annotation>
<documentation> Cost per thousand in-target impressions. The {@link LineItem#lineItemType} must be {@link LineItemType#STANDARD}. </documentation>
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
<simpleType name="CreativeRotationType">
<annotation>
<documentation> The strategy to use for displaying multiple {@link Creative} objects that are associated with a {@link LineItem}. </documentation>
</annotation>
<restriction base="xsd:string">
<enumeration value="EVEN">
<annotation>
<documentation> Creatives are displayed roughly the same number of times over the duration of the line item. </documentation>
</annotation>
</enumeration>
<enumeration value="OPTIMIZED">
<annotation>
<documentation> Creatives are served roughly proportionally to their performance. </documentation>
</annotation>
</enumeration>
<enumeration value="MANUAL">
<annotation>
<documentation> Creatives are served roughly proportionally to their weights, set on the {@link LineItemCreativeAssociation}. </documentation>
</annotation>
</enumeration>
<enumeration value="SEQUENTIAL">
<annotation>
<documentation> Creatives are served exactly in sequential order, aka Storyboarding. Set on the {@link LineItemCreativeAssociation}. </documentation>
</annotation>
</enumeration>
</restriction>
</simpleType>
<simpleType name="CreativeSizeType">
<annotation>
<documentation> Descriptions of the types of sizes a creative can be. Not all creatives can be described by a height-width pair, this provides additional context. </documentation>
</annotation>
<restriction base="xsd:string">
<enumeration value="PIXEL">
<annotation>
<documentation> Dimension based size, an actual height and width. </documentation>
</annotation>
</enumeration>
<enumeration value="ASPECT_RATIO">
<annotation>
<documentation> Mobile size, that is expressed as a ratio of say 4 by 1, that could be met by a 100 x 25 sized image. </documentation>
</annotation>
</enumeration>
<enumeration value="INTERSTITIAL">
<annotation>
<documentation> Out-of-page size, that is not related to the slot it is served. But rather is a function of the snippet, and the values set. This must be used with 1x1 size. </documentation>
</annotation>
</enumeration>
<enumeration value="IGNORED">
<annotation>
<documentation> Size has no meaning <p>1. For Click Tracking entities, where size doesn't matter 2. For entities that allow all requested sizes, where the size represents all sizes. </documentation>
</annotation>
</enumeration>
<enumeration value="NATIVE">
<annotation>
<documentation> Native size, which is a function of the how the client renders the creative. This must be used with 1x1 size. </documentation>
</annotation>
</enumeration>
<enumeration value="AUDIO">
<annotation>
<documentation> Audio size. Used with audio ads. This must be used with 1x1 size. </documentation>
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
<simpleType name="CustomCriteria.ComparisonOperator">
<annotation>
<documentation> Specifies the available comparison operators. </documentation>
</annotation>
<restriction base="xsd:string">
<enumeration value="IS"/>
<enumeration value="IS_NOT"/>
</restriction>
</simpleType>
<simpleType name="CustomCriteriaSet.LogicalOperator">
<annotation>
<documentation> Specifies the available logical operators. </documentation>
</annotation>
<restriction base="xsd:string">
<enumeration value="AND"/>
<enumeration value="OR"/>
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
<simpleType name="CustomPacingGoalUnit">
<annotation>
<documentation> Options for the unit of the custom pacing goal amounts. </documentation>
</annotation>
<restriction base="xsd:string">
<enumeration value="ABSOLUTE">
<annotation>
<documentation> The custom pacing goal amounts represent absolute numbers corresponding to the line item's {@link Goal#unitType}. </documentation>
</annotation>
</enumeration>
<enumeration value="MILLI_PERCENT">
<annotation>
<documentation> The custom pacing goal amounts represent a millipercent. For example, 15000 millipercent equals 15%. </documentation>
</annotation>
</enumeration>
<enumeration value="UNKNOWN">
<annotation>
<documentation> The value returned if the actual value is not exposed by the requested API version. </documentation>
</annotation>
</enumeration>
</restriction>
</simpleType>
<simpleType name="CmsMetadataCriteria.ComparisonOperator">
<annotation>
<documentation> Specifies the available comparison operators. </documentation>
</annotation>
<restriction base="xsd:string">
<enumeration value="EQUALS"/>
<enumeration value="NOT_EQUALS"/>
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
<simpleType name="AudienceSegmentCriteria.ComparisonOperator">
<annotation>
<documentation> Specifies the available comparison operators. </documentation>
</annotation>
<restriction base="xsd:string">
<enumeration value="IS"/>
<enumeration value="IS_NOT"/>
</restriction>
</simpleType>
<simpleType name="DateError.Reason">
<annotation>
<documentation> Enumerates all possible date specific errors. </documentation>
</annotation>
<restriction base="xsd:string">
<enumeration value="DATE_IN_PAST"/>
<enumeration value="START_DATE_AFTER_END_DATE"/>
<enumeration value="END_DATE_BEFORE_START_DATE"/>
<enumeration value="NOT_CERTAIN_DAY_OF_MONTH"/>
<enumeration value="INVALID_DATES"/>
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
<simpleType name="DayOfWeek">
<annotation>
<documentation> Days of the week. </documentation>
</annotation>
<restriction base="xsd:string">
<enumeration value="MONDAY">
<annotation>
<documentation> The day of week named Monday. </documentation>
</annotation>
</enumeration>
<enumeration value="TUESDAY">
<annotation>
<documentation> The day of week named Tuesday. </documentation>
</annotation>
</enumeration>
<enumeration value="WEDNESDAY">
<annotation>
<documentation> The day of week named Wednesday. </documentation>
</annotation>
</enumeration>
<enumeration value="THURSDAY">
<annotation>
<documentation> The day of week named Thursday. </documentation>
</annotation>
</enumeration>
<enumeration value="FRIDAY">
<annotation>
<documentation> The day of week named Friday. </documentation>
</annotation>
</enumeration>
<enumeration value="SATURDAY">
<annotation>
<documentation> The day of week named Saturday. </documentation>
</annotation>
</enumeration>
<enumeration value="SUNDAY">
<annotation>
<documentation> The day of week named Sunday. </documentation>
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
<simpleType name="DeliveryTimeZone">
<annotation>
<documentation> Represents the time zone to be used for {@link DayPartTargeting}. </documentation>
</annotation>
<restriction base="xsd:string">
<enumeration value="PUBLISHER">
<annotation>
<documentation> Use the time zone of the publisher. </documentation>
</annotation>
</enumeration>
<enumeration value="BROWSER">
<annotation>
<documentation> Use the time zone of the browser. </documentation>
</annotation>
</enumeration>
</restriction>
</simpleType>
<simpleType name="DeliveryForecastSource">
<annotation>
<documentation> Strategies for choosing forecasted traffic shapes to pace line items. </documentation>
</annotation>
<restriction base="xsd:string">
<enumeration value="HISTORICAL">
<annotation>
<documentation> The line item's historical traffic shape will be used to pace line item delivery. </documentation>
</annotation>
</enumeration>
<enumeration value="FORECASTING">
<annotation>
<documentation> The line item's projected future traffic will be used to pace line item delivery. </documentation>
</annotation>
</enumeration>
<enumeration value="CUSTOM_PACING_CURVE">
<annotation>
<documentation> A user specified custom pacing curve will be used to pace line item delivery. </documentation>
</annotation>
</enumeration>
<enumeration value="UNKNOWN">
<annotation>
<documentation> The value returned if the actual value is not exposed by the requested API version. </documentation>
</annotation>
</enumeration>
</restriction>
</simpleType>
<simpleType name="DeliveryRateType">
<annotation>
<documentation> Possible delivery rates for a {@link LineItem}, which dictate the manner in which they are served. </documentation>
</annotation>
<restriction base="xsd:string">
<enumeration value="EVENLY">
<annotation>
<documentation> Line items are served as evenly as possible across the number of days specified in a line item's {@link LineItem#duration}. </documentation>
</annotation>
</enumeration>
<enumeration value="FRONTLOADED">
<annotation>
<documentation> Line items are served more aggressively in the beginning of the flight date. </documentation>
</annotation>
</enumeration>
<enumeration value="AS_FAST_AS_POSSIBLE">
<annotation>
<documentation> The booked impressions for a line item may be delivered well before the {@link LineItem#endDateTime}. Other lower-priority or lower-value line items will be stopped from delivering until this line item meets the number of impressions or clicks it is booked for. </documentation>
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
<enumeration value="USER_TEAMS_LIMIT_REACHED">
<annotation>
<documentation> The number of teams on the user exceeds the max number allowed. </documentation>
</annotation>
</enumeration>
<enumeration value="UNKNOWN">
<annotation>
<documentation> The value returned if the actual value is not exposed by the requested API version. </documentation>
</annotation>
</enumeration>
</restriction>
</simpleType>
<simpleType name="EnvironmentType">
<annotation>
<documentation> Enum for the valid environments in which ads can be shown. </documentation>
</annotation>
<restriction base="xsd:string">
<enumeration value="BROWSER">
<annotation>
<documentation> A regular web browser. </documentation>
</annotation>
</enumeration>
<enumeration value="VIDEO_PLAYER">
<annotation>
<documentation> Video players. </documentation>
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
<annotation>
<documentation> The reasons for the frequency cap error. </documentation>
</annotation>
<restriction base="xsd:string">
<enumeration value="IMPRESSION_LIMIT_EXCEEDED"/>
<enumeration value="IMPRESSIONS_TOO_LOW"/>
<enumeration value="RANGE_LIMIT_EXCEEDED"/>
<enumeration value="RANGE_TOO_LOW"/>
<enumeration value="DUPLICATE_TIME_RANGE"/>
<enumeration value="DUPLICATE_TIME_UNIT"/>
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
<simpleType name="GoalType">
<annotation>
<documentation> Specifies the type of the goal for a {@link LineItem}. </documentation>
</annotation>
<restriction base="xsd:string">
<enumeration value="NONE">
<annotation>
<documentation> No goal is specified for the number of ads delivered. The {@link LineItem#lineItemType} must be one of: <ul> <li>{@link LineItemType#PRICE_PRIORITY}</li> <li>{@link LineItemType#AD_EXCHANGE}</li> <li>{@link LineItemType#CLICK_TRACKING}</li> </ul> </documentation>
</annotation>
</enumeration>
<enumeration value="LIFETIME">
<annotation>
<documentation> There is a goal on the number of ads delivered for this line item during its entire lifetime. The {@link LineItem#lineItemType} must be one of: <ul> <li>{@link LineItemType#STANDARD}</li> <li>{@link LineItemType#BULK}</li> <li>{@link LineItemType#PRICE_PRIORITY}</li> <li>{@link LineItemType#ADSENSE}</li> <li>{@link LineItemType#AD_EXCHANGE}</li> <li>{@link LineItemType#ADMOB}</li> <li>{@link LineItemType#CLICK_TRACKING}</li> </ul> </documentation>
</annotation>
</enumeration>
<enumeration value="DAILY">
<annotation>
<documentation> There is a daily goal on the number of ads delivered for this line item. The {@link LineItem#lineItemType} must be one of: <ul> <li>{@link LineItemType#SPONSORSHIP}</li> <li>{@link LineItemType#NETWORK}</li> <li>{@link LineItemType#PRICE_PRIORITY}</li> <li>{@link LineItemType#HOUSE}</li> <li>{@link LineItemType#ADSENSE}</li> <li>{@link LineItemType#AD_EXCHANGE}</li> <li>{@link LineItemType#ADMOB}</li> <li>{@link LineItemType#BUMPER}</li> </ul> </documentation>
</annotation>
</enumeration>
<enumeration value="UNKNOWN">
<annotation>
<documentation> The value returned if the actual value is not exposed by the requested API version. </documentation>
</annotation>
</enumeration>
</restriction>
</simpleType>
<simpleType name="GrpProvider">
<annotation>
<documentation> Represents available GRP providers that a line item will have its target demographic measured by. </documentation>
</annotation>
<restriction base="xsd:string">
<enumeration value="UNKNOWN">
<annotation>
<documentation> The value returned if the actual value is not exposed by the requested API version. </documentation>
</annotation>
</enumeration>
<enumeration value="NIELSEN"/>
<enumeration value="GOOGLE">
<annotation>
<documentation> Renamed to {@code GOOGLE} beginning in V201608. </documentation>
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
<simpleType name="GrpTargetGender">
<annotation>
<documentation> Represents the target gender for a GRP demographic targeted line item. </documentation>
</annotation>
<restriction base="xsd:string">
<enumeration value="UNKNOWN">
<annotation>
<documentation> The value returned if the actual value is not exposed by the requested API version. </documentation>
</annotation>
</enumeration>
<enumeration value="MALE">
<annotation>
<documentation> Indicates that the GRP target gender is Male. </documentation>
</annotation>
</enumeration>
<enumeration value="FEMALE">
<annotation>
<documentation> Indicates that the GRP target gender is Female. </documentation>
</annotation>
</enumeration>
<enumeration value="BOTH">
<annotation>
<documentation> Indicates that the GRP target gender is both male and female. </documentation>
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
<simpleType name="InventoryUnitError.Reason">
<annotation>
<documentation> Possible reasons for the error. </documentation>
</annotation>
<restriction base="xsd:string">
<enumeration value="EXPLICIT_TARGETING_NOT_ALLOWED">
<annotation>
<documentation> {@link AdUnit#explicitlyTargeted} can be set to {@code true} only in an Ad Manager 360 account. </documentation>
</annotation>
</enumeration>
<enumeration value="TARGET_PLATFORM_NOT_APPLICABLE">
<annotation>
<documentation> The specified target platform is not applicable for the inventory unit. </documentation>
</annotation>
</enumeration>
<enumeration value="ADSENSE_CANNOT_BE_ENABLED">
<annotation>
<documentation> AdSense cannot be enabled on this inventory unit if it is disabled for the network. </documentation>
</annotation>
</enumeration>
<enumeration value="ROOT_UNIT_CANNOT_BE_DEACTIVATED">
<annotation>
<documentation> A root unit cannot be deactivated. </documentation>
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
<simpleType name="LineItemDiscountType">
<annotation>
<documentation> Describes the possible discount types on the cost of booking a {@link LineItem}. </documentation>
</annotation>
<restriction base="xsd:string">
<enumeration value="ABSOLUTE_VALUE">
<annotation>
<documentation> An absolute value will be discounted from the line item's cost. </documentation>
</annotation>
</enumeration>
<enumeration value="PERCENTAGE">
<annotation>
<documentation> A percentage of the cost will be applied as discount for booking the line item. </documentation>
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
<simpleType name="LineItemSummary.ReservationStatus">
<annotation>
<documentation> Specifies the reservation status of the {@link LineItem}. </documentation>
</annotation>
<restriction base="xsd:string">
<enumeration value="RESERVED">
<annotation>
<documentation> Indicates that inventory has been reserved for the line item. </documentation>
</annotation>
</enumeration>
<enumeration value="UNRESERVED">
<annotation>
<documentation> Indicates that inventory has not been reserved for the line item. </documentation>
</annotation>
</enumeration>
</restriction>
</simpleType>
<simpleType name="LineItemType">
<annotation>
<documentation> {@code LineItemType} indicates the priority of a {@link LineItem}, determined by the way in which impressions are reserved to be served for it. </documentation>
</annotation>
<restriction base="xsd:string">
<enumeration value="SPONSORSHIP">
<annotation>
<documentation> The type of {@link LineItem} for which a percentage of all the impressions that are being sold are reserved. </documentation>
</annotation>
</enumeration>
<enumeration value="STANDARD">
<annotation>
<documentation> The type of {@link LineItem} for which a fixed quantity of impressions or clicks are reserved. </documentation>
</annotation>
</enumeration>
<enumeration value="NETWORK">
<annotation>
<documentation> The type of {@link LineItem} most commonly used to fill a site's unsold inventory if not contractually obligated to deliver a requested number of impressions. Users specify the daily percentage of unsold impressions or clicks when creating this line item. </documentation>
</annotation>
</enumeration>
<enumeration value="BULK">
<annotation>
<documentation> The type of {@link LineItem} for which a fixed quantity of impressions or clicks will be delivered at a priority lower than the {@link LineItemType#STANDARD} type. </documentation>
</annotation>
</enumeration>
<enumeration value="PRICE_PRIORITY">
<annotation>
<documentation> The type of {@link LineItem} most commonly used to fill a site's unsold inventory if not contractually obligated to deliver a requested number of impressions. Users specify the fixed quantity of unsold impressions or clicks when creating this line item. </documentation>
</annotation>
</enumeration>
<enumeration value="HOUSE">
<annotation>
<documentation> The type of {@link LineItem} typically used for ads that promote products and services chosen by the publisher. These usually do not generate revenue and have the lowest delivery priority. </documentation>
</annotation>
</enumeration>
<enumeration value="LEGACY_DFP">
<annotation>
<documentation> Represents a legacy {@link LineItem} that has been migrated from the DFP system. Such line items cannot be created any more. Also, these line items cannot be activated or resumed. </documentation>
</annotation>
</enumeration>
<enumeration value="CLICK_TRACKING">
<annotation>
<documentation> The type of {@link LineItem} used for ads that track ads being served externally of Ad Manager, for example an email newsletter. The click through would reference this ad, and the click would be tracked via this ad. </documentation>
</annotation>
</enumeration>
<enumeration value="ADSENSE">
<annotation>
<documentation> A {@link LineItem} using dynamic allocation backed by AdSense. </documentation>
</annotation>
</enumeration>
<enumeration value="AD_EXCHANGE">
<annotation>
<documentation> A {@link LineItem} using dynamic allocation backed by the Google Ad Exchange. </documentation>
</annotation>
</enumeration>
<enumeration value="BUMPER">
<annotation>
<documentation> Represents a non-monetizable video {@link LineItem} that targets one or more bumper positions, which are short house video messages used by publishers to separate content from ad breaks. </documentation>
</annotation>
</enumeration>
<enumeration value="ADMOB">
<annotation>
<documentation> A {@link LineItem} using dynamic allocation backed by AdMob. </documentation>
</annotation>
</enumeration>
<enumeration value="PREFERRED_DEAL">
<annotation>
<documentation> The type of {@link LineItem} for which there are no impressions reserved, and will serve for a second price bid. All {@link LineItem}s of type {@link LineItemType#PREFERRED_DEAL} should be created via a {@link ProposalLineItem} with a matching type. When creating a {@link LineItem} of type {@link LineItemType#PREFERRED_DEAL}, the {@link ProposalLineItem#estimatedMinimumImpressions} field is required. </documentation>
</annotation>
</enumeration>
<enumeration value="UNKNOWN">
<annotation>
<documentation> The value returned if the actual value is not exposed by the requested API version. </documentation>
</annotation>
</enumeration>
</restriction>
</simpleType>
<simpleType name="MinuteOfHour">
<annotation>
<documentation> Minutes in an hour. Currently, only 0, 15, 30, and 45 are supported. This field is required. </documentation>
</annotation>
<restriction base="xsd:string">
<enumeration value="ZERO">
<annotation>
<documentation> Zero minutes past hour. </documentation>
</annotation>
</enumeration>
<enumeration value="FIFTEEN">
<annotation>
<documentation> Fifteen minutes past hour. </documentation>
</annotation>
</enumeration>
<enumeration value="THIRTY">
<annotation>
<documentation> Thirty minutes past hour. </documentation>
</annotation>
</enumeration>
<enumeration value="FORTY_FIVE">
<annotation>
<documentation> Forty-five minutes past hour. </documentation>
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
<simpleType name="NegotiationRole">
<annotation>
<documentation> The role (buyer or seller) that performed an action in the negotiation of a {@code Proposal}. </documentation>
</annotation>
<restriction base="xsd:string">
<enumeration value="BUYER"/>
<enumeration value="SELLER"/>
<enumeration value="UNKNOWN"/>
</restriction>
</simpleType>
<simpleType name="NielsenCtvPacingType">
<annotation>
<documentation> Represents the pacing computation method for impressions on connected devices for a Nielsen measured line item. This only applies when Nielsen measurement is enabled for connected devices. </documentation>
</annotation>
<restriction base="xsd:string">
<enumeration value="UNKNOWN">
<annotation>
<documentation> The value returned if the actual value is not exposed by the requested API version. </documentation>
</annotation>
</enumeration>
<enumeration value="NONE">
<annotation>
<documentation> The value returned if Nielsen measurement is disabled for connected devices. </documentation>
</annotation>
</enumeration>
<enumeration value="COVIEW">
<annotation>
<documentation> Indicates that Nielsen impressions on connected devices are included, and we apply coviewing in pacing. </documentation>
</annotation>
</enumeration>
<enumeration value="STRICT_COVIEW">
<annotation>
<documentation> Indicates that Nielsen impressions on connected devices are included, and we apply strict coviewing in pacing. </documentation>
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
<simpleType name="PacingDeviceCategorizationType">
<annotation>
<documentation> Represents whose device categorization to use on Nielsen measured line item with auto-pacing enabled. </documentation>
</annotation>
<restriction base="xsd:string">
<enumeration value="UNKNOWN">
<annotation>
<documentation> The value returned if the actual value is not exposed by the requested API version. </documentation>
</annotation>
</enumeration>
<enumeration value="GOOGLE">
<annotation>
<documentation> Use Google's device categorization in auto-pacing. </documentation>
</annotation>
</enumeration>
<enumeration value="NIELSEN">
<annotation>
<documentation> Use Nielsen device categorization in auto-pacing </documentation>
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
<simpleType name="PrecisionError.Reason">
<annotation>
<documentation> Describes reasons for precision errors. </documentation>
</annotation>
<restriction base="xsd:string">
<enumeration value="WRONG_PRECISION">
<annotation>
<documentation> The lowest N digits of the number must be zero. </documentation>
</annotation>
</enumeration>
<enumeration value="UNKNOWN">
<annotation>
<documentation> The value returned if the actual value is not exposed by the requested API version. </documentation>
</annotation>
</enumeration>
</restriction>
</simpleType>
<simpleType name="ProgrammaticCreativeSource">
<annotation>
<documentation> Types of programmatic creative sources. </documentation>
</annotation>
<restriction base="xsd:string">
<enumeration value="PUBLISHER">
<annotation>
<documentation> Indicates that the programmatic line item is associated with creatives provided by the publisher. </documentation>
</annotation>
</enumeration>
<enumeration value="ADVERTISER">
<annotation>
<documentation> Indicates that the programmatic line item is associated with creatives provided by the advertiser. </documentation>
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
<enumeration value="SEGMENT_POPULATION_LIMIT">
<annotation>
<documentation> This network has exceeded the allowed number of identifiers uploaded within a 24 hour period. The recommended approach to handle this error is to wait 30 minutes and then retry the request. Note that this does not guarantee the request will succeed. If it fails again, try increasing the wait time. </documentation>
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
<simpleType name="RateType">
<annotation>
<documentation> Describes the type of event the advertiser is paying for. The values here correspond to the values for the {@link LineItem#costType} field. </documentation>
</annotation>
<restriction base="xsd:string">
<enumeration value="CPM">
<annotation>
<documentation> The rate applies to cost per mille (CPM) revenue. </documentation>
</annotation>
</enumeration>
<enumeration value="CPD">
<annotation>
<documentation> The rate applies to cost per day (CPD) revenue. </documentation>
</annotation>
</enumeration>
<enumeration value="VCPM">
<annotation>
<documentation> The rate applies to Active View viewable cost per mille (vCPM) revenue. </documentation>
</annotation>
</enumeration>
<enumeration value="CPM_IN_TARGET">
<annotation>
<documentation> The rate applies to cost per mille in-target (CPM In-Target). </documentation>
</annotation>
</enumeration>
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
<simpleType name="RequestPlatform">
<annotation>
<documentation> Represents the platform which requests and renders the ad. </documentation>
</annotation>
<restriction base="xsd:string">
<enumeration value="UNKNOWN">
<annotation>
<documentation> The value returned if the actual value is not exposed by the requested API version. </documentation>
</annotation>
</enumeration>
<enumeration value="BROWSER">
<annotation>
<documentation> Represents a request made from a web browser. This includes both desktop and mobile web. </documentation>
</annotation>
</enumeration>
<enumeration value="MOBILE_APP">
<annotation>
<documentation> Represents a request made from a mobile application. This includes mobile app interstitial and rewarded video requests. </documentation>
</annotation>
</enumeration>
<enumeration value="VIDEO_PLAYER">
<annotation>
<documentation> Represents a request made from a video player that is playing publisher content. This includes video players embedded in web pages and mobile applications, and connected TV screens. </documentation>
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
<enumeration value="REQUEST_PLATFORM_TYPE_NOT_SUPPORTED_BY_ENVIRONMENT_TYPE">
<annotation>
<documentation> The line item environment type does not support the targeted request platform type. </documentation>
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
<enumeration value="CPA_DEPRECATED">
<annotation>
<documentation> CPA {@link LineItem}s can't have end dates older than February 22, 2024. </documentation>
</annotation>
</enumeration>
<enumeration value="UNKNOWN">
<annotation>
<documentation> The value returned if the actual value is not exposed by the requested API version. </documentation>
</annotation>
</enumeration>
</restriction>
</simpleType>
<simpleType name="ReservationStatus">
<annotation>
<documentation> Represents the inventory reservation status for {@link ProposalLineItem} objects. </documentation>
</annotation>
<restriction base="xsd:string">
<enumeration value="RESERVED">
<annotation>
<documentation> The inventory is reserved. </documentation>
</annotation>
</enumeration>
<enumeration value="NOT_RESERVED">
<annotation>
<documentation> The proposal line item's inventory is never reserved. </documentation>
</annotation>
</enumeration>
<enumeration value="RELEASED">
<annotation>
<documentation> The inventory is once reserved and now released. </documentation>
</annotation>
</enumeration>
<enumeration value="CHECK_LINE_ITEM_RESERVATION_STATUS">
<annotation>
<documentation> The reservation status of the corresponding {@link LineItem} should be used for this {@link ProposalLineItem}. </documentation>
</annotation>
</enumeration>
<enumeration value="UNKNOWN">
<annotation>
<documentation> The value returned if the actual value is not exposed by the requested API version. </documentation>
</annotation>
</enumeration>
</restriction>
</simpleType>
<simpleType name="RoadblockingType">
<annotation>
<documentation> Describes the roadblocking types. </documentation>
</annotation>
<restriction base="xsd:string">
<enumeration value="ONLY_ONE">
<annotation>
<documentation> Only one creative from a line item can serve at a time. </documentation>
</annotation>
</enumeration>
<enumeration value="ONE_OR_MORE">
<annotation>
<documentation> Any number of creatives from a line item can serve together at a time. </documentation>
</annotation>
</enumeration>
<enumeration value="AS_MANY_AS_POSSIBLE">
<annotation>
<documentation> As many creatives from a line item as can fit on a page will serve. This could mean anywhere from one to all of a line item's creatives given the size constraints of ad slots on a page. </documentation>
</annotation>
</enumeration>
<enumeration value="ALL_ROADBLOCK">
<annotation>
<documentation> All or none of the creatives from a line item will serve. This option will only work if served to a GPT tag using SRA (single request architecture mode). </documentation>
</annotation>
</enumeration>
<enumeration value="CREATIVE_SET">
<annotation>
<documentation> A master/companion {@link CreativeSet} roadblocking type. A {@link LineItem#creativePlaceholders} must be set accordingly. </documentation>
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
<simpleType name="SkippableAdType">
<annotation>
<documentation> The different types of skippable ads. </documentation>
</annotation>
<restriction base="xsd:string">
<enumeration value="UNKNOWN">
<annotation>
<documentation> The value returned if the actual value is not exposed by the requested API version. </documentation>
</annotation>
</enumeration>
<enumeration value="DISABLED">
<annotation>
<documentation> Skippable ad type is disabled. </documentation>
</annotation>
</enumeration>
<enumeration value="ENABLED">
<annotation>
<documentation> Skippable ad type is enabled. </documentation>
</annotation>
</enumeration>
<enumeration value="INSTREAM_SELECT">
<annotation>
<documentation> Skippable in-stream ad type. </documentation>
</annotation>
</enumeration>
<enumeration value="ANY">
<annotation>
<documentation> Any skippable or not skippable. This is only for programmatic case when the creative skippability is decided by the buyside. </documentation>
</annotation>
</enumeration>
</restriction>
</simpleType>
<simpleType name="StartDateTimeType">
<annotation>
<documentation> Specifies the start type to use for an entity with a start date time field. For example, a {@link LineItem} or {@link LineItemCreativeAssociation}. </documentation>
</annotation>
<restriction base="xsd:string">
<enumeration value="USE_START_DATE_TIME">
<annotation>
<documentation> Use the value in {@link #startDateTime}. </documentation>
</annotation>
</enumeration>
<enumeration value="IMMEDIATELY">
<annotation>
<documentation> The entity will start serving immediately. {@link #startDateTime} in the request is ignored and will be set to the current time. Additionally, {@link #startDateTimeType} will be set to {@link StartDateTimeType#USE_START_DATE_TIME}. </documentation>
</annotation>
</enumeration>
<enumeration value="ONE_HOUR_FROM_NOW">
<annotation>
<documentation> The entity will start serving one hour from now. {@link #startDateTime} in the request is ignored and will be set to one hour from the current time. Additionally, {@link #startDateTimeType} will be set to {@link StartDateTimeType#USE_START_DATE_TIME}. </documentation>
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
<simpleType name="TargetingDimension">
<annotation>
<documentation> Targeting dimension of targeting breakdowns. </documentation>
</annotation>
<restriction base="xsd:string">
<enumeration value="CUSTOM_CRITERIA"/>
<enumeration value="GEOGRAPHY"/>
<enumeration value="BROWSER"/>
<enumeration value="BROWSER_LANGUAGE"/>
<enumeration value="BANDWIDTH_GROUP"/>
<enumeration value="OPERATING_SYSTEM"/>
<enumeration value="USER_DOMAIN"/>
<enumeration value="CONTENT"/>
<enumeration value="VIDEO_POSITION"/>
<enumeration value="AD_SIZE"/>
<enumeration value="AD_UNIT"/>
<enumeration value="PLACEMENT"/>
<enumeration value="MOBILE_CARRIER"/>
<enumeration value="DEVICE_CAPABILITY"/>
<enumeration value="DEVICE_CATEGORY"/>
<enumeration value="DEVICE_MANUFACTURER"/>
<enumeration value="MOBILE_APPLICATION"/>
<enumeration value="FORECASTED_CREATIVE_RESTRICTION"/>
<enumeration value="VERTICAL"/>
<enumeration value="CONTENT_LABEL"/>
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
<simpleType name="ThirdPartyBrandLiftIntegrationPartner">
<annotation>
<documentation> Possible options for third-party brand lift integration. </documentation>
</annotation>
<restriction base="xsd:string">
<enumeration value="UNKNOWN">
<annotation>
<documentation> The value returned if the actual value is not exposed by the requested API version. </documentation>
</annotation>
</enumeration>
<enumeration value="NONE">
<annotation>
<documentation> Indicates there's no third-party brand lift integration partner. </documentation>
</annotation>
</enumeration>
<enumeration value="KANTAR_MILLWARD_BROWN">
<annotation>
<documentation> Indicates third-party brand lift integration partner Kantar. </documentation>
</annotation>
</enumeration>
<enumeration value="DYNATA">
<annotation>
<documentation> Indicates third-party brand lift integration partner Dynata. </documentation>
</annotation>
</enumeration>
<enumeration value="INTAGE">
<annotation>
<documentation> Indicates third-party brand lift integration partner Intage. </documentation>
</annotation>
</enumeration>
<enumeration value="MACROMILL">
<annotation>
<documentation> Indicates third-party brand lift integration partner Macromill. </documentation>
</annotation>
</enumeration>
</restriction>
</simpleType>
<simpleType name="ThirdPartyReachIntegrationPartner">
<annotation>
<documentation> Possible options for third-party reach integration. </documentation>
</annotation>
<restriction base="xsd:string">
<enumeration value="NONE">
<annotation>
<documentation> Indicates there's no third-party reach integration partner. </documentation>
</annotation>
</enumeration>
<enumeration value="COMSCORE">
<annotation>
<documentation> Indicates third-party reach integration partner Comscore. </documentation>
</annotation>
</enumeration>
<enumeration value="NIELSEN">
<annotation>
<documentation> Indicates third-party reach integration partner Nielsen. </documentation>
</annotation>
</enumeration>
<enumeration value="KANTAR_MILLWARD_BROWN">
<annotation>
<documentation> Indicates third-party reach integration partner Kantar. </documentation>
</annotation>
</enumeration>
<enumeration value="VIDEO_RESEARCH">
<annotation>
<documentation> Indicates third-party reach integration partner Video Research. </documentation>
</annotation>
</enumeration>
<enumeration value="GEMIUS">
<annotation>
<documentation> Indicates third-party reach integration partner Gemius. </documentation>
</annotation>
</enumeration>
<enumeration value="VIDEO_AMP">
<annotation>
<documentation> Indicates third-party reach integration partner VideoAmp </documentation>
</annotation>
</enumeration>
<enumeration value="ISPOT_TV">
<annotation>
<documentation> Indicates third-party reach integration partner iSpot.TV </documentation>
</annotation>
</enumeration>
<enumeration value="AUDIENCE_PROJECT">
<annotation>
<documentation> Indicates third-party reach integration partner Audience Project </documentation>
</annotation>
</enumeration>
<enumeration value="UNKNOWN">
<annotation>
<documentation> The value returned if the actual value is not exposed by the requested API version. </documentation>
</annotation>
</enumeration>
</restriction>
</simpleType>
<simpleType name="ThirdPartyViewabilityIntegrationPartner">
<annotation>
<documentation> Possible options for third-party viewabitility integration. </documentation>
</annotation>
<restriction base="xsd:string">
<enumeration value="NONE">
<annotation>
<documentation> Indicates there's no third-party viewability integration partner. </documentation>
</annotation>
</enumeration>
<enumeration value="MOAT">
<annotation>
<documentation> Indicates third-party viewability integration partner Oracle Moat. </documentation>
</annotation>
</enumeration>
<enumeration value="DOUBLE_VERIFY">
<annotation>
<documentation> Indicates third-party viewability integration partner Double Verify. </documentation>
</annotation>
</enumeration>
<enumeration value="INTEGRAL_AD_SCIENCE">
<annotation>
<documentation> Indicates third-party viewability integration partner Integral Ad Science. </documentation>
</annotation>
</enumeration>
<enumeration value="COMSCORE">
<annotation>
<documentation> Indicates third-party viewability integration partner Comscore. </documentation>
</annotation>
</enumeration>
<enumeration value="TELEMETRY">
<annotation>
<documentation> Indicates third-party viewability integration partner Telemetry. </documentation>
</annotation>
</enumeration>
<enumeration value="UNKNOWN">
<annotation>
<documentation> The value returned if the actual value is not exposed by the requested API version. </documentation>
</annotation>
</enumeration>
</restriction>
</simpleType>
<simpleType name="TimeUnit">
<annotation>
<documentation> Represent the possible time units for frequency capping. </documentation>
</annotation>
<restriction base="xsd:string">
<enumeration value="MINUTE"/>
<enumeration value="HOUR"/>
<enumeration value="DAY"/>
<enumeration value="WEEK"/>
<enumeration value="MONTH"/>
<enumeration value="LIFETIME"/>
<enumeration value="POD">
<annotation>
<documentation> Per pod of ads in a video stream. Only valid for entities in a {@link EnvironmentType#VIDEO_PLAYER} environment. </documentation>
</annotation>
</enumeration>
<enumeration value="STREAM">
<annotation>
<documentation> Per video stream. Only valid for entities in a {@link EnvironmentType#VIDEO_PLAYER} environment. </documentation>
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
<simpleType name="UnitType">
<annotation>
<documentation> Indicates the type of unit used for defining a reservation. The {@link CostType} can differ from the {@link UnitType} - an ad can have an impression goal, but be billed by its click. Usually {@link CostType} and {@link UnitType} will refer to the same unit. </documentation>
</annotation>
<restriction base="xsd:string">
<enumeration value="IMPRESSIONS">
<annotation>
<documentation> The number of impressions served by creatives associated with the line item. Line items of all {@link LineItemType} support this {@code UnitType}. </documentation>
</annotation>
</enumeration>
<enumeration value="CLICKS">
<annotation>
<documentation> The number of clicks reported by creatives associated with the line item. The {@link LineItem#lineItemType} must be {@link LineItemType#STANDARD}, {@link LineItemType#BULK} or {@link LineItemType#PRICE_PRIORITY}. </documentation>
</annotation>
</enumeration>
<enumeration value="CLICK_THROUGH_CPA_CONVERSIONS">
<annotation>
<documentation> The number of click-through Cost-Per-Action (CPA) conversions from creatives associated with the line item. This is only supported as secondary goal and the {@link LineItem#costType} must be {@link CostType#CPA}. </documentation>
</annotation>
</enumeration>
<enumeration value="VIEW_THROUGH_CPA_CONVERSIONS">
<annotation>
<documentation> The number of view-through Cost-Per-Action (CPA) conversions from creatives associated with the line item. This is only supported as secondary goal and the {@link LineItem#costType} must be {@link CostType#CPA}. </documentation>
</annotation>
</enumeration>
<enumeration value="TOTAL_CPA_CONVERSIONS">
<annotation>
<documentation> The number of total Cost-Per-Action (CPA) conversions from creatives associated with the line item. This is only supported as secondary goal and the {@link LineItem#costType} must be {@link CostType#CPA}. </documentation>
</annotation>
</enumeration>
<enumeration value="VIEWABLE_IMPRESSIONS">
<annotation>
<documentation> The number of viewable impressions reported by creatives associated with the line item. The {@link LineItem#lineItemType} must be {@link LineItemType#STANDARD}. </documentation>
</annotation>
</enumeration>
<enumeration value="IN_TARGET_IMPRESSIONS">
<annotation>
<documentation> The number of in-target impressions reported by third party measurements. The {@link LineItem#lineItemType} must be {@link LineItemType#STANDARD}. </documentation>
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
<simpleType name="VideoBumperType">
<annotation>
<documentation> Represents the options for targetable bumper positions, surrounding an ad pod, within a video stream. This includes before and after the supported ad pod positions, {@link VideoPositionType#PREROLL}, {@link VideoPositionType#MIDROLL}, and {@link VideoPositionType#POSTROLL}. </documentation>
</annotation>
<restriction base="xsd:string">
<enumeration value="BEFORE">
<annotation>
<documentation> Represents the bumper position before the ad pod. </documentation>
</annotation>
</enumeration>
<enumeration value="AFTER">
<annotation>
<documentation> Represents the bumper position after the ad pod. </documentation>
</annotation>
</enumeration>
</restriction>
</simpleType>
<simpleType name="VideoPosition.Type">
<annotation>
<documentation> Represents a targetable position within a video. </documentation>
</annotation>
<restriction base="xsd:string">
<enumeration value="UNKNOWN">
<annotation>
<documentation> The value returned if the actual value is not exposed by the requested API version. </documentation>
</annotation>
</enumeration>
<enumeration value="ALL">
<annotation>
<documentation> This position targets all of the above video positions. </documentation>
</annotation>
</enumeration>
<enumeration value="PREROLL">
<annotation>
<documentation> The position defined as showing before the video starts playing. </documentation>
</annotation>
</enumeration>
<enumeration value="MIDROLL">
<annotation>
<documentation> The position defined as showing within the middle of the playing video. </documentation>
</annotation>
</enumeration>
<enumeration value="POSTROLL">
<annotation>
<documentation> The position defined as showing after the video is completed. </documentation>
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
<element name="getAvailabilityForecast">
<annotation>
<documentation> Gets the availability forecast for a {@link ProspectiveLineItem}. An availability forecast reports the maximum number of available units that the line item can book, and the total number of units matching the line item's targeting. </documentation>
</annotation>
<complexType>
<sequence>
<element maxOccurs="1" minOccurs="0" name="lineItem" type="tns:ProspectiveLineItem"/>
<element maxOccurs="1" minOccurs="0" name="forecastOptions" type="tns:AvailabilityForecastOptions"/>
</sequence>
</complexType>
</element>
<element name="getAvailabilityForecastResponse">
<complexType>
<sequence>
<element maxOccurs="1" minOccurs="0" name="rval" type="tns:AvailabilityForecast"/>
</sequence>
</complexType>
</element>
<element name="ApiExceptionFault" type="tns:ApiException">
<annotation>
<documentation> A fault element of type ApiException. </documentation>
</annotation>
</element>
<element name="getAvailabilityForecastById">
<annotation>
<documentation> Gets an {@link AvailabilityForecast} for an existing {@link LineItem} object. An availability forecast reports the maximum number of available units that the line item can be booked with, and also the total number of units matching the line item's targeting. <p>Only line items having type {@link LineItemType#SPONSORSHIP} or {@link LineItemType#STANDARD} are valid. Other types will result in {@link ReservationDetailsError.Reason#LINE_ITEM_TYPE_NOT_ALLOWED}. </documentation>
</annotation>
<complexType>
<sequence>
<element maxOccurs="1" minOccurs="0" name="lineItemId" type="xsd:long"/>
<element maxOccurs="1" minOccurs="0" name="forecastOptions" type="tns:AvailabilityForecastOptions"/>
</sequence>
</complexType>
</element>
<element name="getAvailabilityForecastByIdResponse">
<complexType>
<sequence>
<element maxOccurs="1" minOccurs="0" name="rval" type="tns:AvailabilityForecast"/>
</sequence>
</complexType>
</element>
<element name="getDeliveryForecast">
<annotation>
<documentation> Gets the delivery forecast for a list of {@link ProspectiveLineItem} objects in a single delivery simulation with line items potentially contending with each other. A delivery forecast reports the number of units that will be delivered to each line item given the line item goals and contentions from other line items. </documentation>
</annotation>
<complexType>
<sequence>
<element maxOccurs="unbounded" minOccurs="0" name="lineItems" type="tns:ProspectiveLineItem"/>
<element maxOccurs="1" minOccurs="0" name="forecastOptions" type="tns:DeliveryForecastOptions"/>
</sequence>
</complexType>
</element>
<element name="getDeliveryForecastResponse">
<complexType>
<sequence>
<element maxOccurs="1" minOccurs="0" name="rval" type="tns:DeliveryForecast"/>
</sequence>
</complexType>
</element>
<element name="getDeliveryForecastByIds">
<annotation>
<documentation> Gets the delivery forecast for a list of existing {@link LineItem} objects in a single delivery simulation. A delivery forecast reports the number of units that will be delivered to each line item given the line item goals and contentions from other line items. </documentation>
</annotation>
<complexType>
<sequence>
<element maxOccurs="unbounded" minOccurs="0" name="lineItemIds" type="xsd:long"/>
<element maxOccurs="1" minOccurs="0" name="forecastOptions" type="tns:DeliveryForecastOptions"/>
</sequence>
</complexType>
</element>
<element name="getDeliveryForecastByIdsResponse">
<complexType>
<sequence>
<element maxOccurs="1" minOccurs="0" name="rval" type="tns:DeliveryForecast"/>
</sequence>
</complexType>
</element>
<element name="getTrafficData">
<annotation>
<documentation> Returns forecasted and historical traffic data for the segment of traffic specified by the provided request. <p>Calling this endpoint programmatically is only available for Ad Manager 360 networks. </documentation>
</annotation>
<complexType>
<sequence>
<element maxOccurs="1" minOccurs="0" name="trafficDataRequest" type="tns:TrafficDataRequest"/>
</sequence>
</complexType>
</element>
<element name="getTrafficDataResponse">
<complexType>
<sequence>
<element maxOccurs="1" minOccurs="0" name="rval" type="tns:TrafficDataResponse"/>
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
<wsdl:message name="getAvailabilityForecastRequest">
<wsdl:part element="tns:getAvailabilityForecast" name="parameters"/>
</wsdl:message>
<wsdl:message name="getAvailabilityForecastResponse">
<wsdl:part element="tns:getAvailabilityForecastResponse" name="parameters"/>
</wsdl:message>
<wsdl:message name="ApiException">
<wsdl:part element="tns:ApiExceptionFault" name="ApiException"/>
</wsdl:message>
<wsdl:message name="getAvailabilityForecastByIdRequest">
<wsdl:part element="tns:getAvailabilityForecastById" name="parameters"/>
</wsdl:message>
<wsdl:message name="getAvailabilityForecastByIdResponse">
<wsdl:part element="tns:getAvailabilityForecastByIdResponse" name="parameters"/>
</wsdl:message>
<wsdl:message name="getDeliveryForecastRequest">
<wsdl:part element="tns:getDeliveryForecast" name="parameters"/>
</wsdl:message>
<wsdl:message name="getDeliveryForecastResponse">
<wsdl:part element="tns:getDeliveryForecastResponse" name="parameters"/>
</wsdl:message>
<wsdl:message name="getDeliveryForecastByIdsRequest">
<wsdl:part element="tns:getDeliveryForecastByIds" name="parameters"/>
</wsdl:message>
<wsdl:message name="getDeliveryForecastByIdsResponse">
<wsdl:part element="tns:getDeliveryForecastByIdsResponse" name="parameters"/>
</wsdl:message>
<wsdl:message name="getTrafficDataRequest">
<wsdl:part element="tns:getTrafficData" name="parameters"/>
</wsdl:message>
<wsdl:message name="getTrafficDataResponse">
<wsdl:part element="tns:getTrafficDataResponse" name="parameters"/>
</wsdl:message>
<wsdl:portType name="ForecastServiceInterface">
<wsdl:documentation> Provides methods for estimating traffic (clicks/impressions) for line items. Forecasts can be provided for {@link LineItem} objects that exist in the system or which have not had an ID set yet. <h4>Test network behavior</h4> <p>Test networks are unable to provide forecasts that would be comparable to the production environment because forecasts require traffic history. For test networks, a consistent behavior can be expected for forecast requests, according to the following rules: <table> <tr> <th colspan="2">Inputs<br/>({@link LineItem} Fields)</th> <th colspan="4">Outputs<br/>({@link Forecast} Fields)</th> </tr> <tr> <th>{@link LineItem#lineItemType lineItemType}</th> <th>{@link LineItem#unitsBought unitsBought}</th> <th>{@link Forecast#availableUnits availableUnits}</th> <th>{@link Forecast#forecastUnits forecastUnits (matchedUnits)}</th> <th>{@link Forecast#deliveredUnits deliveredUnits}</th> <th>Exception</td> </tr> <tr> <td>Sponsorship</td> <td>13</td> <td>&ndash;&ndash;</td> <td>&ndash;&ndash;</td> <td>&ndash;&ndash;</td> <td> {@link ForecastError.Reason#NO_FORECAST_YET NO_FORECAST_YET} </td> </tr> <tr> <td>Sponsorship</td> <td>20</td> <td>&ndash;&ndash;</td> <td>&ndash;&ndash;</td> <td>&ndash;&ndash;</td> <td> {@link ForecastError.Reason#SERVER_NOT_AVAILABLE SERVER_NOT_AVAILABLE} </td> </tr> <tr> <td>Sponsorship</td> <td>50</td> <td>1,200,000</td> <td>6,000,000</td> <td>600,000</td> <td>&ndash;&ndash;</td> </tr> <tr> <td>Sponsorship</td> <td>!= 20 and <br/> != 50</td> <td>1,200,000</td> <td>1,200,000</td> <td>600,000</td> <td>&ndash;&ndash;</td> </tr> <tr> <td>Not Sponsorship</td> <td>&lt;= 500,000</td> <td>3 * unitsBought / 2</td> <td>unitsBought * 6</td> <td>600,000</td> <td>&ndash;&ndash;</td> </tr> <tr> <td>Not Sponsorship</td> <td>&gt; 500,000 and &lt;= 1,000,000</td> <td>unitsBought / 2</td> <td>unitsBought * 6</td> <td>600,000</td> <td>&ndash;&ndash;</td> </tr> <tr> <td>Not Sponsorship</td> <td>&gt; 1,000,000 and &lt;= 1,500,000</td> <td>unitsBought / 2</td> <td>3 * unitsBought / 2</td> <td>600,000</td> <td>&ndash;&ndash;</td> </tr> <tr> <td>Not Sponsorship</td> <td>&gt; 1,500,000</td> <td>unitsBought / 4</td> <td>3 * unitsBought / 2</td> <td>600,000</td> <td>&ndash;&ndash;</td> </tr> </table> </wsdl:documentation>
<wsdl:operation name="getAvailabilityForecast">
<wsdl:documentation> Gets the availability forecast for a {@link ProspectiveLineItem}. An availability forecast reports the maximum number of available units that the line item can book, and the total number of units matching the line item's targeting. </wsdl:documentation>
<wsdl:input message="tns:getAvailabilityForecastRequest" name="getAvailabilityForecastRequest"/>
<wsdl:output message="tns:getAvailabilityForecastResponse" name="getAvailabilityForecastResponse"/>
<wsdl:fault message="tns:ApiException" name="ApiException"/>
</wsdl:operation>
<wsdl:operation name="getAvailabilityForecastById">
<wsdl:documentation> Gets an {@link AvailabilityForecast} for an existing {@link LineItem} object. An availability forecast reports the maximum number of available units that the line item can be booked with, and also the total number of units matching the line item's targeting. <p>Only line items having type {@link LineItemType#SPONSORSHIP} or {@link LineItemType#STANDARD} are valid. Other types will result in {@link ReservationDetailsError.Reason#LINE_ITEM_TYPE_NOT_ALLOWED}. </wsdl:documentation>
<wsdl:input message="tns:getAvailabilityForecastByIdRequest" name="getAvailabilityForecastByIdRequest"/>
<wsdl:output message="tns:getAvailabilityForecastByIdResponse" name="getAvailabilityForecastByIdResponse"/>
<wsdl:fault message="tns:ApiException" name="ApiException"/>
</wsdl:operation>
<wsdl:operation name="getDeliveryForecast">
<wsdl:documentation> Gets the delivery forecast for a list of {@link ProspectiveLineItem} objects in a single delivery simulation with line items potentially contending with each other. A delivery forecast reports the number of units that will be delivered to each line item given the line item goals and contentions from other line items. </wsdl:documentation>
<wsdl:input message="tns:getDeliveryForecastRequest" name="getDeliveryForecastRequest"/>
<wsdl:output message="tns:getDeliveryForecastResponse" name="getDeliveryForecastResponse"/>
<wsdl:fault message="tns:ApiException" name="ApiException"/>
</wsdl:operation>
<wsdl:operation name="getDeliveryForecastByIds">
<wsdl:documentation> Gets the delivery forecast for a list of existing {@link LineItem} objects in a single delivery simulation. A delivery forecast reports the number of units that will be delivered to each line item given the line item goals and contentions from other line items. </wsdl:documentation>
<wsdl:input message="tns:getDeliveryForecastByIdsRequest" name="getDeliveryForecastByIdsRequest"/>
<wsdl:output message="tns:getDeliveryForecastByIdsResponse" name="getDeliveryForecastByIdsResponse"/>
<wsdl:fault message="tns:ApiException" name="ApiException"/>
</wsdl:operation>
<wsdl:operation name="getTrafficData">
<wsdl:documentation> Returns forecasted and historical traffic data for the segment of traffic specified by the provided request. <p>Calling this endpoint programmatically is only available for Ad Manager 360 networks. </wsdl:documentation>
<wsdl:input message="tns:getTrafficDataRequest" name="getTrafficDataRequest"/>
<wsdl:output message="tns:getTrafficDataResponse" name="getTrafficDataResponse"/>
<wsdl:fault message="tns:ApiException" name="ApiException"/>
</wsdl:operation>
</wsdl:portType>
<wsdl:binding name="ForecastServiceSoapBinding" type="tns:ForecastServiceInterface">
<wsdlsoap:binding style="document" transport="http://schemas.xmlsoap.org/soap/http"/>
<wsdl:operation name="getAvailabilityForecast">
<wsdlsoap:operation soapAction=""/>
<wsdl:input name="getAvailabilityForecastRequest">
<wsdlsoap:header message="tns:RequestHeader" part="RequestHeader" use="literal"/>
<wsdlsoap:body use="literal"/>
</wsdl:input>
<wsdl:output name="getAvailabilityForecastResponse">
<wsdlsoap:header message="tns:ResponseHeader" part="ResponseHeader" use="literal"/>
<wsdlsoap:body use="literal"/>
</wsdl:output>
<wsdl:fault name="ApiException">
<wsdlsoap:fault name="ApiException" use="literal"/>
</wsdl:fault>
</wsdl:operation>
<wsdl:operation name="getAvailabilityForecastById">
<wsdlsoap:operation soapAction=""/>
<wsdl:input name="getAvailabilityForecastByIdRequest">
<wsdlsoap:header message="tns:RequestHeader" part="RequestHeader" use="literal"/>
<wsdlsoap:body use="literal"/>
</wsdl:input>
<wsdl:output name="getAvailabilityForecastByIdResponse">
<wsdlsoap:header message="tns:ResponseHeader" part="ResponseHeader" use="literal"/>
<wsdlsoap:body use="literal"/>
</wsdl:output>
<wsdl:fault name="ApiException">
<wsdlsoap:fault name="ApiException" use="literal"/>
</wsdl:fault>
</wsdl:operation>
<wsdl:operation name="getDeliveryForecast">
<wsdlsoap:operation soapAction=""/>
<wsdl:input name="getDeliveryForecastRequest">
<wsdlsoap:header message="tns:RequestHeader" part="RequestHeader" use="literal"/>
<wsdlsoap:body use="literal"/>
</wsdl:input>
<wsdl:output name="getDeliveryForecastResponse">
<wsdlsoap:header message="tns:ResponseHeader" part="ResponseHeader" use="literal"/>
<wsdlsoap:body use="literal"/>
</wsdl:output>
<wsdl:fault name="ApiException">
<wsdlsoap:fault name="ApiException" use="literal"/>
</wsdl:fault>
</wsdl:operation>
<wsdl:operation name="getDeliveryForecastByIds">
<wsdlsoap:operation soapAction=""/>
<wsdl:input name="getDeliveryForecastByIdsRequest">
<wsdlsoap:header message="tns:RequestHeader" part="RequestHeader" use="literal"/>
<wsdlsoap:body use="literal"/>
</wsdl:input>
<wsdl:output name="getDeliveryForecastByIdsResponse">
<wsdlsoap:header message="tns:ResponseHeader" part="ResponseHeader" use="literal"/>
<wsdlsoap:body use="literal"/>
</wsdl:output>
<wsdl:fault name="ApiException">
<wsdlsoap:fault name="ApiException" use="literal"/>
</wsdl:fault>
</wsdl:operation>
<wsdl:operation name="getTrafficData">
<wsdlsoap:operation soapAction=""/>
<wsdl:input name="getTrafficDataRequest">
<wsdlsoap:header message="tns:RequestHeader" part="RequestHeader" use="literal"/>
<wsdlsoap:body use="literal"/>
</wsdl:input>
<wsdl:output name="getTrafficDataResponse">
<wsdlsoap:header message="tns:ResponseHeader" part="ResponseHeader" use="literal"/>
<wsdlsoap:body use="literal"/>
</wsdl:output>
<wsdl:fault name="ApiException">
<wsdlsoap:fault name="ApiException" use="literal"/>
</wsdl:fault>
</wsdl:operation>
</wsdl:binding>
<wsdl:service name="ForecastService">
<wsdl:port binding="tns:ForecastServiceSoapBinding" name="ForecastServiceInterfacePort">
<wsdlsoap:address location="https://ads.google.com/apis/ads/publisher/v202408/ForecastService"/>
</wsdl:port>
</wsdl:service>
</wsdl:definitions>
"""
from __future__ import annotations
from typing import Optional, Any

from pydantic import Field

from rcplus_alloy_common.gam.vendor.common import (
    GAMSOAPBaseModel,
    Date,
)
from rcplus_alloy_common.gam.vendor.line_items import LineItem, Targeting, UnitType


class DateRange(GAMSOAPBaseModel):
    """
    <complexType name="DateRange">
    <annotation>
    <documentation> Represents a range of dates that has an upper and a lower bound. <p>An open ended date range can be described by only setting either one of the bounds, the upper bound or the lower bound. </documentation>
    </annotation>
    <sequence>
    <element maxOccurs="1" minOccurs="0" name="startDate" type="tns:Date">
    <annotation>
    <documentation> The start date of this range. This field is optional and if it is not set then there is no lower bound on the date range. If this field is not set then {@code endDate} must be specified. </documentation>
    </annotation>
    </element>
    <element maxOccurs="1" minOccurs="0" name="endDate" type="tns:Date">
    <annotation>
    <documentation> The end date of this range. This field is optional and if it is not set then there is no upper bound on the date range. If this field is not set then {@code startDate} must be specified. </documentation>
    </annotation>
    </element>
    </sequence>
    </complexType>
    """
    startDate: Optional[Date] = Field(
        None,
        description="The start date of this range. This field is optional and if it is not set then there is no lower bound on the date range. If this field is not set then endDate must be specified.",
    )
    endDate: Optional[Date] = Field(
        None,
        description="The end date of this range. This field is optional and if it is not set then there is no upper bound on the date range. If this field is not set then startDate must be specified.",
    )


class TrafficDataRequest(GAMSOAPBaseModel):
    """
    <complexType name="TrafficDataRequest">
    <annotation>
    <documentation> Defines a segment of traffic for which traffic data should be returned. </documentation>
    </annotation>
    <sequence>
    <element maxOccurs="1" minOccurs="0" name="targeting" type="tns:Targeting">
    <annotation>
    <documentation> The {@link TargetingDto} that defines a segment of traffic. <span class="constraint Required">This attribute is required.</span> </documentation>
    </annotation>
    </element>
    <element maxOccurs="1" minOccurs="0" name="requestedDateRange" type="tns:DateRange">
    <annotation>
    <documentation> The date range for which traffic data are requested. This range may cover historical dates, future dates, or both. <p>The data returned are not guaranteed to cover the entire requested date range. If sufficient data are not available to cover the entire requested date range, a response may be returned with a later start date, earlier end date, or both. <span class="constraint Required">This attribute is required.</span> </documentation>
    </annotation>
    </element>
    </sequence>
    </complexType>
    """
    targeting: Optional[Targeting] = Field(
        None,
        description="The TargetingDto that defines a segment of traffic.",
    )
    requestedDateRange: Optional[DateRange] = Field(
        None,
        description="The date range for which traffic data are requested. This range may cover historical dates, future dates, or both. The data returned are not guaranteed to cover the entire requested date range. If sufficient data are not available to cover the entire requested date range, a response may be returned with a later start date, earlier end date, or both.",
    )


class TimeSeries(GAMSOAPBaseModel):
    """
    <complexType name="TimeSeries">
    <annotation>
    <documentation> Represents a chronological sequence of daily values. </documentation>
    </annotation>
    <sequence>
    <element maxOccurs="1" minOccurs="0" name="timeSeriesDateRange" type="tns:DateRange">
    <annotation>
    <documentation> The date range of the time series. </documentation>
    </annotation>
    </element>
    <element maxOccurs="unbounded" minOccurs="0" name="values" type="xsd:long">
    <annotation>
    <documentation> The daily values constituting the time series. <p>The number of time series values must equal the number of days spanned by the time series date range, inclusive. E.g.: {@code timeSeriesDateRange} of 2001-08-15 to 2001-08-17 should contain one value for the 15th, one value for the 16th, and one value for the 17th. </documentation>
    </annotation>
    </element>
    </sequence>
    </complexType>
    """
    timeSeriesDateRange: Optional[DateRange] = Field(
        None,
        description="The date range of the time series.",
    )
    values: Optional[list[int]] = Field(
        None,
        description="The daily values constituting the time series. The number of time series values must equal the number of days spanned by the time series date range, inclusive. E.g.: timeSeriesDateRange of 2001-08-15 to 2001-08-17 should contain one value for the 15th, one value for the 16th, and one value for the 17th.",
    )


class TrafficDataResponse(GAMSOAPBaseModel):
    """
    <complexType name="TrafficDataResponse">
    <annotation>
    <documentation> Contains forecasted and historical traffic volume data describing a segment of traffic. </documentation>
    </annotation>
    <sequence>
    <element maxOccurs="1" minOccurs="0" name="historicalTimeSeries" type="tns:TimeSeries">
    <annotation>
    <documentation> Time series of historical traffic ad opportunity counts. <p>This may be null if the requested date range did not contain any historical dates, or if no historical data are available for the requested traffic segment. This attribute is read-only. </documentation>
    </annotation>
    </element>
    <element maxOccurs="1" minOccurs="0" name="forecastedTimeSeries" type="tns:TimeSeries">
    <annotation>
    <documentation> Time series of forecasted traffic ad opportunity counts. <p>This may be null if the requested date range did not contain any future dates, or if no forecasted data are available for the requested traffic segment. This attribute is read-only. </documentation>
    </annotation>
    </element>
    <element maxOccurs="1" minOccurs="0" name="forecastedAssignedTimeSeries" type="tns:TimeSeries">
    <annotation>
    <documentation> Time series of future traffic volumes forecasted to be sold. <p>This may be null if the requested date range did not contain any future dates, or if no sell-through data are available for the requested traffic segment. This attribute is read-only. </documentation>
    </annotation>
    </element>
    <element maxOccurs="1" minOccurs="0" name="overallDateRange" type="tns:DateRange">
    <annotation>
    <documentation> The overall date range spanned by the union of all time series in the response. <p>This is a summary field for convenience. The value will be set such that the start date is equal to the earliest start date of all time series included, and the end date is equal to the latest end date of all time series included. <p>If all time series fields are null, this field will also be null. This attribute is read-only. </documentation>
    </annotation>
    </element>
    </sequence>
    </complexType>
    """
    historicalTimeSeries: Optional[TimeSeries] = Field(
        None,
        description="Time series of historical traffic ad opportunity counts. This may be null if the requested date range did not contain any historical dates, or if no historical data are available for the requested traffic segment. This attribute is read-only.",
    )
    forecastedTimeSeries: Optional[TimeSeries] = Field(
        None,
        description="Time series of forecasted traffic ad opportunity counts. This may be null if the requested date range did not contain any future dates, or if no forecasted data are available for the requested traffic segment. This attribute is read-only.",
    )
    forecastedAssignedTimeSeries: Optional[TimeSeries] = Field(
        None,
        description="Time series of future traffic volumes forecasted to be sold. This may be null if the requested date range did not contain any future dates, or if no sell-through data are available for the requested traffic segment. This attribute is read-only.",
    )
    overallDateRange: Optional[DateRange] = Field(
        None,
        description="The overall date range spanned by the union of all time series in the response. This is a summary field for convenience. The value will be set such that the start date is equal to the earliest start date of all time series included, and the end date is equal to the latest end date of all time series included. If all time series fields are null, this field will also be null. This attribute is read-only.",
    )


class ProspectiveLineItem(GAMSOAPBaseModel):
    """
    <complexType name="ProspectiveLineItem">
    <annotation>
    <documentation> Represents a prospective line item to be forecasted. </documentation>
    </annotation>
    <sequence>
    <element maxOccurs="1" minOccurs="0" name="lineItem" type="tns:LineItem">
    <annotation>
    <documentation> The target of the forecast. If {@link LineItem#id} is null or no line item exists with that ID, then a forecast is computed for the subject, predicting what would happen if it were added to the network. If a line item already exists with {@link LineItem#id}, the forecast is computed for the subject, predicting what would happen if the existing line item's settings were modified to match the subject. </documentation>
    </annotation>
    </element>
    <element maxOccurs="1" minOccurs="0" name="proposalLineItem" type="tns:ProposalLineItem">
    <annotation>
    <documentation> The target of the forecast if this prospective line item is a proposal line item. <p>If {@link ProposalLineItem#id} is null or no proposal line item exists with that ID, then a forecast is computed for the subject, predicting what would happen if it were added to the network. If a proposal line item already exists with {@link ProposalLineItem#id}, the forecast is computed for the subject, predicting what would happen if the existing proposal line item's settings were modified to match the subject. <p>A proposal line item can optionally correspond to an order {@link LineItem}, in which case, by forecasting a proposal line item, the corresponding line item is implicitly ignored in the forecasting. <p>Either {@link #lineItem} or {@link #proposalLineItem} should be specified but not both. </documentation>
    </annotation>
    </element>
    <element maxOccurs="1" minOccurs="0" name="advertiserId" type="xsd:long">
    <annotation>
    <documentation> When set, the line item is assumed to be from this advertiser, and unified blocking rules will apply accordingly. If absent, line items without an existing order won't be subject to unified blocking rules. </documentation>
    </annotation>
    </element>
    </sequence>
    </complexType>
    """
    lineItem: Optional[LineItem] = Field(
        None,
        description="The target of the forecast. If LineItem.id is null or no line item exists with that ID, then a forecast is computed for the subject, predicting what would happen if it were added to the network. If a line item already exists with LineItem.id, the forecast is computed for the subject, predicting what would happen if the existing line item's settings were modified to match the subject.",
    )
    proposalLineItem: Optional[Any] = Field(  # TODO: port also ProposalLineItem from the ProposalLineItemService
        None,
        description="The target of the forecast if this prospective line item is a proposal line item. If ProposalLineItem.id is null or no proposal line item exists with that ID, then a forecast is computed for the subject, predicting what would happen if it were added to the network. If a proposal line item already exists with ProposalLineItem.id, the forecast is computed for the subject, predicting what would happen if the existing proposal line item's settings were modified to match the subject. A proposal line item can optionally correspond to an order LineItem, in which case, by forecasting a proposal line item, the corresponding line item is implicitly ignored in the forecasting. Either lineItem or proposalLineItem should be specified but not both.",
    )
    advertiserId: Optional[int] = Field(
        None,
        description="When set, the line item is assumed to be from this advertiser, and unified blocking rules will apply accordingly. If absent, line items without an existing order won't be subject to unified blocking rules.",
    )


class DeliveryForecastOptions(GAMSOAPBaseModel):
    """
    <complexType name="DeliveryForecastOptions">
    <annotation>
    <documentation> Forecasting options for line item delivery forecasts. </documentation>
    </annotation>
    <sequence>
    <element maxOccurs="unbounded" minOccurs="0" name="ignoredLineItemIds" type="xsd:long">
    <annotation>
    <documentation> Line item IDs to be ignored while performing the delivery simulation. </documentation>
    </annotation>
    </element>
    </sequence>
    </complexType>
    """
    ignoredLineItemIds: Optional[list[int]] = Field(
        None,
        description="Line item IDs to be ignored while performing the delivery simulation.",
    )


class LineItemDeliveryForecast(GAMSOAPBaseModel):
    """
    <complexType name="LineItemDeliveryForecast">
    <annotation>
    <documentation> The forecasted delivery of a {@link ProspectiveLineItem}. </documentation>
    </annotation>
    <sequence>
    <element maxOccurs="1" minOccurs="0" name="lineItemId" type="xsd:long">
    <annotation>
    <documentation> Uniquely identifies this line item delivery forecast. This value is read-only and will be either the ID of the {@link LineItem} object it represents, or {@code null} if the forecast represents a prospective line item. </documentation>
    </annotation>
    </element>
    <element maxOccurs="1" minOccurs="0" name="orderId" type="xsd:long">
    <annotation>
    <documentation> The unique ID for the {@link Order} object that this line item belongs to, or {@code null} if the forecast represents a prospective line item without an {@link LineItem#orderId} set. </documentation>
    </annotation>
    </element>
    <element maxOccurs="1" minOccurs="0" name="unitType" type="tns:
    <annotation>
    <documentation> The unit with which the goal or cap of the {@link LineItem} is defined. Will be the same value as {@link Goal#unitType} for both a set line item or a prospective one. </
    </annotation>
    </element>
    <element maxOccurs="1" minOccurs="0" name="predictedDeliveryUnits" type="xsd:long">
    <annotation>
    <documentation> The number of units, defined by {@link Goal#unitType}, that will be delivered by the line item. Delivery of existing line items that are of same or lower priorities may be impacted. </
    </annotation>
    </element>
    <element maxOccurs="1" minOccurs="0" name="deliveredUnits" type="xsd:long">
    <annotation>
    <documentation> The number of units, defined by {@link Goal#unitType}, that have already been served if the reservation is already running. </
    </annotation>
    </element>
    <element maxOccurs="1" minOccurs="0" name="matchedUnits" type="xsd:long">
    <annotation>
    <documentation> The number of units, defined by {@link Goal#unitType}, that match the specified {@link LineItem#targeting} and delivery settings. </
    </annotation>
    </element>
    </sequence>
    </complexType>
    """
    lineItemId: Optional[int] = Field(
        None,
        description="Uniquely identifies this line item delivery forecast. This value is read-only and will be either the ID of the LineItem object it represents, or null if the forecast represents a prospective line item.",
    )
    orderId: Optional[int] = Field(
        None,
        description="The unique ID for the Order object that this line item belongs to, or null if the forecast represents a prospective line item without an LineItem.orderId set.",
    )
    unitType: Optional[UnitType] = Field(
        None,
        description="The unit with which the goal or cap of the LineItem is defined. Will be the same value as Goal.unitType for both a set line item or a prospective one.",
    )
    predictedDeliveryUnits: Optional[int] = Field(
        None,
        description="The number of units, defined by Goal.unitType, that will be delivered by the line item. Delivery of existing line items that are of same or lower priorities may be impacted.",
    )
    deliveredUnits: Optional[int] = Field(
        None,
        description="The number of units, defined by Goal.unitType, that have already been served if the reservation is already running.",
    )
    matchedUnits: Optional[int] = Field(
        None,
        description="The number of units, defined by Goal.unitType, that match the specified LineItem.targeting and delivery settings.",
    )


class DeliveryForecast(GAMSOAPBaseModel):
    """
    <complexType name="DeliveryForecast">
    <annotation>
    <documentation> The forecast of delivery for a list of {@link ProspectiveLineItem} objects to be reserved at the same time. </documentation>
    </annotation>
    <sequence>
    <element maxOccurs="unbounded" minOccurs="0" name="lineItemDeliveryForecasts" type="tns:LineItemDeliveryForecast">
    <annotation>
    <documentation> The delivery forecasts of the forecasted line items. </documentation>
    </annotation>
    </element>
    </sequence>
    </complexType>
    """
    lineItemDeliveryForecasts: Optional[list[LineItemDeliveryForecast]] = Field(
        None,
        description="The delivery forecasts of the forecasted line items.",
    )
