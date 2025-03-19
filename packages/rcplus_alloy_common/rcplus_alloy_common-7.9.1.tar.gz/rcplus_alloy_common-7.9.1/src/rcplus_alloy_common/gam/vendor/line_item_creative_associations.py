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
<complexType name="ActivateLineItemCreativeAssociations">
<annotation>
<documentation> The action used for activating {@link LineItemCreativeAssociation} objects. </documentation>
</annotation>
<complexContent>
<extension base="tns:LineItemCreativeAssociationAction">
<sequence/>
</extension>
</complexContent>
</complexType>
<complexType name="AdSenseAccountError">
<annotation>
<documentation> Error for AdSense related API calls. </documentation>
</annotation>
<complexContent>
<extension base="tns:ApiError">
<sequence>
<element maxOccurs="1" minOccurs="0" name="reason" type="tns:AdSenseAccountError.Reason"/>
</sequence>
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
<complexType name="CreativeAssetMacroError">
<annotation>
<documentation> Lists all errors associated with creative asset macros. </documentation>
</annotation>
<complexContent>
<extension base="tns:ApiError">
<sequence>
<element maxOccurs="1" minOccurs="0" name="reason" type="tns:CreativeAssetMacroError.Reason">
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
<complexType name="CreativeNativeStylePreview">
<annotation>
<documentation> Represents the {@link NativeStyle} of a {@link Creative} and its corresponding preview URL. </documentation>
</annotation>
<sequence>
<element maxOccurs="1" minOccurs="0" name="nativeStyleId" type="xsd:long">
<annotation>
<documentation> The id of the {@link NativeStyle}. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="previewUrl" type="xsd:string">
<annotation>
<documentation> The URL for previewing this creative using this particular {@link NativeStyle} </documentation>
</annotation>
</element>
</sequence>
</complexType>
<complexType name="CreativePreviewError">
<annotation>
<documentation> Errors associated with generation of creative preview URIs. </documentation>
</annotation>
<complexContent>
<extension base="tns:ApiError">
<sequence>
<element maxOccurs="1" minOccurs="0" name="reason" type="tns:CreativePreviewError.Reason"/>
</sequence>
</extension>
</complexContent>
</complexType>
<complexType name="CreativePushOptions">
<annotation>
<documentation> Data needed to push a creative to a mobile device. </documentation>
</annotation>
<sequence>
<element maxOccurs="1" minOccurs="0" name="lineItemId" type="xsd:long">
<annotation>
<documentation> The ID of the LineItem to preview. <p>This field is required. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="creativeId" type="xsd:long">
<annotation>
<documentation> The ID of the Creative to preview. <p>This field is required. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="nativeStyleId" type="xsd:long">
<annotation>
<documentation> The ID of the native style to preview the creative with. <p>This field is optional but the referenced object must exist. </documentation>
</annotation>
</element>
</sequence>
</complexType>
<complexType name="CreativeSetError">
<annotation>
<documentation> Errors relating to creative sets & subclasses. </documentation>
</annotation>
<complexContent>
<extension base="tns:ApiError">
<sequence>
<element maxOccurs="1" minOccurs="0" name="reason" type="tns:CreativeSetError.Reason">
<annotation>
<documentation> The error reason represented by an enum. </documentation>
</annotation>
</element>
</sequence>
</extension>
</complexContent>
</complexType>
<complexType name="CreativeTemplateError">
<annotation>
<documentation> A catch-all error that lists all generic errors associated with CreativeTemplate. </documentation>
</annotation>
<complexContent>
<extension base="tns:ApiError">
<sequence>
<element maxOccurs="1" minOccurs="0" name="reason" type="tns:CreativeTemplateError.Reason">
<annotation>
<documentation> The error reason represented by an enum. </documentation>
</annotation>
</element>
</sequence>
</extension>
</complexContent>
</complexType>
<complexType name="CreativeTemplateOperationError">
<annotation>
<documentation> An error that can occur while performing an operation on a creative template. </documentation>
</annotation>
<complexContent>
<extension base="tns:ApiError">
<sequence>
<element maxOccurs="1" minOccurs="0" name="reason" type="tns:CreativeTemplateOperationError.Reason">
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
<complexType name="CustomCreativeError">
<annotation>
<documentation> Lists all errors associated with custom creatives. </documentation>
</annotation>
<complexContent>
<extension base="tns:ApiError">
<sequence>
<element maxOccurs="1" minOccurs="0" name="reason" type="tns:CustomCreativeError.Reason">
<annotation>
<documentation> The error reason represented by an enum. </documentation>
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
<complexType name="DeactivateLineItemCreativeAssociations">
<annotation>
<documentation> The action used for deactivating {@link LineItemCreativeAssociation} objects. </documentation>
</annotation>
<complexContent>
<extension base="tns:LineItemCreativeAssociationAction">
<sequence/>
</extension>
</complexContent>
</complexType>
<complexType name="DeleteLineItemCreativeAssociations">
<annotation>
<documentation> The action used for deleting {@link LineItemCreativeAssociation} objects. </documentation>
</annotation>
<complexContent>
<extension base="tns:LineItemCreativeAssociationAction">
<sequence/>
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
<complexType name="FileError">
<annotation>
<documentation> A list of all errors to be used for problems related to files. </documentation>
</annotation>
<complexContent>
<extension base="tns:ApiError">
<sequence>
<element maxOccurs="1" minOccurs="0" name="reason" type="tns:FileError.Reason"/>
</sequence>
</extension>
</complexContent>
</complexType>
<complexType name="HtmlBundleProcessorError">
<annotation>
<documentation> Lists all errors associated with html5 file processing. </documentation>
</annotation>
<complexContent>
<extension base="tns:ApiError">
<sequence>
<element maxOccurs="1" minOccurs="0" name="reason" type="tns:HtmlBundleProcessorError.Reason">
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
<complexType name="InvalidPhoneNumberError">
<annotation>
<documentation> Lists all errors associated with phone numbers. </documentation>
</annotation>
<complexContent>
<extension base="tns:ApiError">
<sequence>
<element maxOccurs="1" minOccurs="0" name="reason" type="tns:InvalidPhoneNumberError.Reason"/>
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
<complexType abstract="true" name="LineItemCreativeAssociationAction">
<annotation>
<documentation> Represents the actions that can be performed on {@link LineItemCreativeAssociation} objects. </documentation>
</annotation>
<sequence/>
</complexType>
<complexType name="LineItemCreativeAssociation">
<annotation>
<documentation> A {@code LineItemCreativeAssociation} associates a {@link Creative} or {@link CreativeSet} with a {@link LineItem} so that the creative can be served in ad units targeted by the line item. </documentation>
</annotation>
<sequence>
<element maxOccurs="1" minOccurs="0" name="lineItemId" type="xsd:long">
<annotation>
<documentation> The ID of the {@link LineItem} to which the {@link Creative} should be associated. This attribute is required. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="creativeId" type="xsd:long">
<annotation>
<documentation> The ID of the {@link Creative} being associated with a {@link LineItem}. <p>This attribute is required if this is an association between a line item and a creative. <br> This attribute is ignored if this is an association between a line item and a creative set. <p>If this is an association between a line item and a creative, when retrieving the line item creative association, the {@link #creativeId} will be the creative's ID. <br> If this is an association between a line item and a creative set, when retrieving the line item creative association, the {@link #creativeId} will be the ID of the {@link CreativeSet#masterCreativeId master creative}. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="creativeSetId" type="xsd:long">
<annotation>
<documentation> The ID of the {@link CreativeSet} being associated with a {@link LineItem}. This attribute is required if this is an association between a line item and a creative set. <p>This field will be {@code null} when retrieving associations between line items and creatives not belonging to a set. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="manualCreativeRotationWeight" type="xsd:double">
<annotation>
<documentation> The weight of the {@link Creative}. This value is only used if the line item's {@code creativeRotationType} is set to {@link CreativeRotationType#MANUAL}. This attribute is optional and defaults to 10. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="sequentialCreativeRotationIndex" type="xsd:int">
<annotation>
<documentation> The sequential rotation index of the {@link Creative}. This value is used only if the associated line item's {@link LineItem#creativeRotationType} is set to {@link CreativeRotationType#SEQUENTIAL}. This attribute is optional and defaults to 1. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="startDateTime" type="tns:DateTime">
<annotation>
<documentation> Overrides the value set for {@link LineItem#startDateTime}. This value is optional and is only valid for Ad Manager 360 networks. If unset, the {@link LineItem#startDateTime} will be used. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="startDateTimeType" type="tns:StartDateTimeType">
<annotation>
<documentation> Specifies whether to start serving to the {@code LineItemCreativeAssociation} right away, in an hour, etc. This attribute is optional and defaults to {@link StartDateTimeType#USE_START_DATE_TIME}. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="endDateTime" type="tns:DateTime">
<annotation>
<documentation> Overrides {@link LineItem#endDateTime}. This value is optional and is only valid for Ad Manager 360 networks. If unset, the {@link LineItem#endDateTime} will be used. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="destinationUrl" type="xsd:string">
<annotation>
<documentation> Overrides the value set for {@link HasDestinationUrlCreative#destinationUrl}. This value is optional and is only valid for Ad Manager 360 networks. </documentation>
</annotation>
</element>
<element maxOccurs="unbounded" minOccurs="0" name="sizes" type="tns:Size">
<annotation>
<documentation> Overrides the value set for {@link Creative#size}, which allows the creative to be served to ad units that would otherwise not be compatible for its actual size. This value is optional. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="status" type="tns:LineItemCreativeAssociation.Status">
<annotation>
<documentation> The status of the association. This attribute is read-only. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="stats" type="tns:LineItemCreativeAssociationStats">
<annotation>
<documentation> Contains trafficking statistics for the association. This attribute is readonly and is populated by Google. This will be {@code null} in case there are no statistics for the association yet. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="lastModifiedDateTime" type="tns:DateTime">
<annotation>
<documentation> The date and time this association was last modified. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="targetingName" type="xsd:string">
<annotation>
<documentation> Specifies {@link CreativeTargeting} for this line item creative association. <p>This attribute is optional. It should match the creative targeting specified on the corresponding {@link CreativePlaceholder} in the {@link LineItem} that is being associated with the {@link Creative}. </documentation>
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
<complexType name="LineItemCreativeAssociationOperationError">
<annotation>
<documentation> Lists all errors for executing operations on line item-to-creative associations </documentation>
</annotation>
<complexContent>
<extension base="tns:ApiError">
<sequence>
<element maxOccurs="1" minOccurs="0" name="reason" type="tns:LineItemCreativeAssociationOperationError.Reason">
<annotation>
<documentation> The error reason represented by an enum. </documentation>
</annotation>
</element>
</sequence>
</extension>
</complexContent>
</complexType>
<complexType name="LineItemCreativeAssociationPage">
<annotation>
<documentation> Captures a page of {@link LineItemCreativeAssociation} objects. </documentation>
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
<element maxOccurs="unbounded" minOccurs="0" name="results" type="tns:LineItemCreativeAssociation">
<annotation>
<documentation> The collection of line item creative associations contained within this page. </documentation>
</annotation>
</element>
</sequence>
</complexType>
<complexType name="LineItemCreativeAssociationStats">
<annotation>
<documentation> Contains statistics such as impressions, clicks delivered and cost for {@link LineItemCreativeAssociation} objects. </documentation>
</annotation>
<sequence>
<element maxOccurs="1" minOccurs="0" name="stats" type="tns:Stats">
<annotation>
<documentation> A {@link Stats} object that holds delivered impressions and clicks statistics. </documentation>
</annotation>
</element>
<element maxOccurs="unbounded" minOccurs="0" name="creativeSetStats" type="tns:Long_StatsMapEntry">
<annotation>
<documentation> A map containing {@link Stats} objects for each creative belonging to a creative set, {@code null} for non creative set associations. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="costInOrderCurrency" type="tns:Money">
<annotation>
<documentation> The revenue generated thus far by the creative from its association with the particular line item in the publisher's currency. </documentation>
</annotation>
</element>
</sequence>
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
<complexType name="Long_StatsMapEntry">
<annotation>
<documentation> This represents an entry in a map with a key of type Long and value of type Stats. </documentation>
</annotation>
<sequence>
<element maxOccurs="1" minOccurs="0" name="key" type="xsd:long"/>
<element maxOccurs="1" minOccurs="0" name="value" type="tns:Stats"/>
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
<documentation> Caused by supplying a non-null value for an attribute that should be null. </documentation>
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
<complexType name="RichMediaStudioCreativeError">
<annotation>
<documentation> Lists all errors associated with Studio creatives. </documentation>
</annotation>
<complexContent>
<extension base="tns:ApiError">
<sequence>
<element maxOccurs="1" minOccurs="0" name="reason" type="tns:RichMediaStudioCreativeError.Reason">
<annotation>
<documentation> The error reason represented by an enum. </documentation>
</annotation>
</element>
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
<complexType name="SetTopBoxCreativeError">
<annotation>
<documentation> Errors associated with {@link SetTopBoxCreative set-top box creatives}. </documentation>
</annotation>
<complexContent>
<extension base="tns:ApiError">
<sequence>
<element maxOccurs="1" minOccurs="0" name="reason" type="tns:SetTopBoxCreativeError.Reason">
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
<complexType name="String_ValueMapEntry">
<annotation>
<documentation> This represents an entry in a map with a key of type String and value of type Value. </documentation>
</annotation>
<sequence>
<element maxOccurs="1" minOccurs="0" name="key" type="xsd:string"/>
<element maxOccurs="1" minOccurs="0" name="value" type="tns:Value"/>
</sequence>
</complexType>
<complexType name="SwiffyConversionError">
<annotation>
<documentation> Error for converting flash to swiffy asset. </documentation>
</annotation>
<complexContent>
<extension base="tns:ApiError">
<sequence>
<element maxOccurs="1" minOccurs="0" name="reason" type="tns:SwiffyConversionError.Reason"/>
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
<complexType abstract="true" name="Value">
<annotation>
<documentation> {@code Value} represents a value. </documentation>
</annotation>
<sequence/>
</complexType>
<simpleType name="AdSenseAccountError.Reason">
<restriction base="xsd:string">
<enumeration value="ASSOCIATE_ACCOUNT_API_ERROR">
<annotation>
<documentation> An error occurred while trying to associate an AdSense account with Ad Manager. Unable to create an association with AdSense or Ad Exchange account. </documentation>
</annotation>
</enumeration>
<enumeration value="CANNOT_ACCESS_INVALID_ACCOUNT">
<annotation>
<documentation> An error occurred while a user without a valid AdSense account trying to access an Ads frontend. </documentation>
</annotation>
</enumeration>
<enumeration value="ACCOUNT_ACCESS_DENIED">
<annotation>
<documentation> An error occurred while AdSense denied access. </documentation>
</annotation>
</enumeration>
<enumeration value="GET_AD_SLOT_API_ERROR">
<annotation>
<documentation> An error occurred while trying to get an associated web property's ad slots. Unable to retrieve ad slot information from AdSense or Ad Exchange account. </documentation>
</annotation>
</enumeration>
<enumeration value="GET_CHANNEL_API_ERROR">
<annotation>
<documentation> An error occurred while trying to get an associated web property's ad channels. </documentation>
</annotation>
</enumeration>
<enumeration value="GET_BULK_ACCOUNT_STATUSES_API_ERROR">
<annotation>
<documentation> An error occurred while trying to retrieve account statues from AdSense API. Unable to retrieve account status information. Please try again later. </documentation>
</annotation>
</enumeration>
<enumeration value="RESEND_VERIFICATION_EMAIL_ERROR">
<annotation>
<documentation> An error occurred while trying to resend the account association verification email. Error resending verification email. Please try again. </documentation>
</annotation>
</enumeration>
<enumeration value="UNEXPECTED_API_RESPONSE_ERROR">
<annotation>
<documentation> An error occurred while trying to retrieve a response from the AdSense API. There was a problem processing your request. Please try again later. </documentation>
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
<simpleType name="CreativeAssetMacroError.Reason">
<annotation>
<documentation> The reasons for the target error. </documentation>
</annotation>
<restriction base="xsd:string">
<enumeration value="INVALID_MACRO_NAME">
<annotation>
<documentation> Invalid macro name specified. Macro names must start with an alpha character and consist only of alpha-numeric characters and underscores and be between 1 and 64 characters. </documentation>
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
<simpleType name="CreativePreviewError.Reason">
<restriction base="xsd:string">
<enumeration value="CANNOT_GENERATE_PREVIEW_URL">
<annotation>
<documentation> The creative cannot be previewed on this page. </documentation>
</annotation>
</enumeration>
<enumeration value="CANNOT_GENERATE_PREVIEW_URL_FOR_NATIVE_CREATIVES">
<annotation>
<documentation> Preview URLs for native creatives must be retrieved with {@link LineItemCreativeAssociationService#getPreviewUrlsForNativeStyles}. </documentation>
</annotation>
</enumeration>
<enumeration value="HTML_SNIPPET_REQUIRED_FOR_THIRD_PARTY_CREATIVE">
<annotation>
<documentation> Third party creatives must have an html snippet set in order to obtain a preview URL. </documentation>
</annotation>
</enumeration>
<enumeration value="UNKNOWN">
<annotation>
<documentation> The value returned if the actual value is not exposed by the requested API version. </documentation>
</annotation>
</enumeration>
</restriction>
</simpleType>
<simpleType name="CreativeSetError.Reason">
<annotation>
<documentation> The reasons for the target error. </documentation>
</annotation>
<restriction base="xsd:string">
<enumeration value="VIDEO_FEATURE_REQUIRED">
<annotation>
<documentation> The 'video' feature is required but not enabled. </documentation>
</annotation>
</enumeration>
<enumeration value="CANNOT_CREATE_OR_UPDATE_VIDEO_CREATIVES">
<annotation>
<documentation> Video creatives (including overlays, VAST redirects, etc..) cannot be created or updated through the API. </documentation>
</annotation>
</enumeration>
<enumeration value="ROADBLOCK_FEATURE_REQUIRED">
<annotation>
<documentation> The 'roadblock' feature is required but not enabled. </documentation>
</annotation>
</enumeration>
<enumeration value="MASTER_CREATIVE_CANNOT_BE_COMPANION">
<annotation>
<documentation> A master creative cannot be a companion creative in the same creative set. </documentation>
</annotation>
</enumeration>
<enumeration value="INVALID_ADVERTISER">
<annotation>
<documentation> Creatives in a creative set must be for the same advertiser. </documentation>
</annotation>
</enumeration>
<enumeration value="UPDATE_MASTER_CREATIVE_NOT_ALLOWED">
<annotation>
<documentation> Updating a master creative in a creative set is not allowed. </documentation>
</annotation>
</enumeration>
<enumeration value="MASTER_CREATIVE_CANNOT_BELONG_TO_MULTIPLE_VIDEO_CREATIVE_SETS">
<annotation>
<documentation> A master creative must belong to only one video creative set. </documentation>
</annotation>
</enumeration>
<enumeration value="SKIPPABLE_AD_TYPE_NOT_ALLOWED">
<annotation>
<documentation> The {@Code SkippableAdType} is not allowed. </documentation>
</annotation>
</enumeration>
<enumeration value="UNKNOWN">
<annotation>
<documentation> The value returned if the actual value is not exposed by the requested API version. </documentation>
</annotation>
</enumeration>
</restriction>
</simpleType>
<simpleType name="CreativeTemplateError.Reason">
<annotation>
<documentation> The reasons for the target error. </documentation>
</annotation>
<restriction base="xsd:string">
<enumeration value="CANNOT_PARSE_CREATIVE_TEMPLATE">
<annotation>
<documentation> The XML of the creative template definition is malformed and cannot be parsed. </documentation>
</annotation>
</enumeration>
<enumeration value="VARIABLE_DUPLICATE_UNIQUE_NAME">
<annotation>
<documentation> A creative template has multiple variables with the same uniqueName. </documentation>
</annotation>
</enumeration>
<enumeration value="VARIABLE_INVALID_UNIQUE_NAME">
<annotation>
<documentation> The creative template contains a variable with invalid characters. Valid characters are letters, numbers, spaces, forward slashes, dashes, and underscores. </documentation>
</annotation>
</enumeration>
<enumeration value="LIST_CHOICE_DUPLICATE_VALUE">
<annotation>
<documentation> Multiple choices for a CreativeTemplateListStringVariable have the same value. </documentation>
</annotation>
</enumeration>
<enumeration value="LIST_CHOICE_NEEDS_DEFAULT">
<annotation>
<documentation> The choices for a CreativeTemplateListStringVariable do not contain the default value. </documentation>
</annotation>
</enumeration>
<enumeration value="LIST_CHOICES_EMPTY">
<annotation>
<documentation> There are no choices specified for the list variable. </documentation>
</annotation>
</enumeration>
<enumeration value="NO_TARGET_PLATFORMS">
<annotation>
<documentation> No target platform is assigned to a creative template. </documentation>
</annotation>
</enumeration>
<enumeration value="MULTIPLE_TARGET_PLATFORMS">
<annotation>
<documentation> More than one target platform is assigned to a single creative template. </documentation>
</annotation>
</enumeration>
<enumeration value="UNRECOGNIZED_PLACEHOLDER">
<annotation>
<documentation> The formatter contains a placeholder which is not defined as a variable. </documentation>
</annotation>
</enumeration>
<enumeration value="PLACEHOLDERS_NOT_IN_FORMATTER">
<annotation>
<documentation> There are variables defined which are not being used in the formatter. </documentation>
</annotation>
</enumeration>
<enumeration value="MISSING_INTERSTITIAL_MACRO">
<annotation>
<documentation> The creative template is interstitial, but the formatter doesn't contain an interstitial macro. </documentation>
</annotation>
</enumeration>
<enumeration value="UNKNOWN">
<annotation>
<documentation> The value returned if the actual value is not exposed by the requested API version. </documentation>
</annotation>
</enumeration>
</restriction>
</simpleType>
<simpleType name="CreativeTemplateOperationError.Reason">
<annotation>
<documentation> The reasons for the target error. </documentation>
</annotation>
<restriction base="xsd:string">
<enumeration value="NOT_ALLOWED">
<annotation>
<documentation> The current user is not allowed to modify this creative template. </documentation>
</annotation>
</enumeration>
<enumeration value="NOT_APPLICABLE">
<annotation>
<documentation> The operation is not applicable to the current state. (e.g. Trying to activate an active creative template) </documentation>
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
<simpleType name="CustomCreativeError.Reason">
<annotation>
<documentation> The reasons for the target error. </documentation>
</annotation>
<restriction base="xsd:string">
<enumeration value="DUPLICATE_MACRO_NAME_FOR_CREATIVE">
<annotation>
<documentation> Macros associated with a single custom creative must have unique names. </documentation>
</annotation>
</enumeration>
<enumeration value="SNIPPET_REFERENCES_MISSING_MACRO">
<annotation>
<documentation> The file macro referenced in the snippet does not exist. </documentation>
</annotation>
</enumeration>
<enumeration value="UNRECOGNIZED_MACRO">
<annotation>
<documentation> The macro referenced in the snippet is not valid. </documentation>
</annotation>
</enumeration>
<enumeration value="CUSTOM_CREATIVE_NOT_ALLOWED">
<annotation>
<documentation> Custom creatives are not allowed in this context. </documentation>
</annotation>
</enumeration>
<enumeration value="MISSING_INTERSTITIAL_MACRO">
<annotation>
<documentation> The custom creative is an interstitial, but the snippet is missing an interstitial macro. </documentation>
</annotation>
</enumeration>
<enumeration value="DUPLICATE_ASSET_IN_MACROS">
<annotation>
<documentation> Macros associated with the same custom creative cannot share the same asset. </documentation>
</annotation>
</enumeration>
<enumeration value="UNKNOWN">
<annotation>
<documentation> The value returned if the actual value is not exposed by the requested API version. </documentation>
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
<simpleType name="FileError.Reason">
<restriction base="xsd:string">
<enumeration value="MISSING_CONTENTS">
<annotation>
<documentation> The provided byte array is empty. </documentation>
</annotation>
</enumeration>
<enumeration value="SIZE_TOO_LARGE">
<annotation>
<documentation> The provided file is larger than the maximum size defined for the network. </documentation>
</annotation>
</enumeration>
<enumeration value="UNKNOWN">
<annotation>
<documentation> The value returned if the actual value is not exposed by the requested API version. </documentation>
</annotation>
</enumeration>
</restriction>
</simpleType>
<simpleType name="HtmlBundleProcessorError.Reason">
<annotation>
<documentation> Error reasons that may arise during HTML5 bundle processing. </documentation>
</annotation>
<restriction base="xsd:string">
<enumeration value="CANNOT_EXTRACT_FILES_FROM_BUNDLE">
<annotation>
<documentation> Cannot extract files from HTML5 bundle. </documentation>
</annotation>
</enumeration>
<enumeration value="CLICK_TAG_HARD_CODED">
<annotation>
<documentation> Bundle cannot have hard-coded click tag url(s). </documentation>
</annotation>
</enumeration>
<enumeration value="CLICK_TAG_IN_GWD_UNUPPORTED">
<annotation>
<documentation> Bundles created using GWD (Google Web Designer) cannot have click tags. GWD-published bundles should use exit events instead of defining var {@code clickTAG}. </documentation>
</annotation>
</enumeration>
<enumeration value="CLICK_TAG_NOT_IN_PRIMARY_HTML">
<annotation>
<documentation> Click tag detected outside of primary HTML file. </documentation>
</annotation>
</enumeration>
<enumeration value="CLICK_TAG_INVALID">
<annotation>
<documentation> Click tag or exit function has invalid name or url. </documentation>
</annotation>
</enumeration>
<enumeration value="FILE_SIZE_TOO_LARGE">
<annotation>
<documentation> HTML5 bundle or total size of extracted files cannot be more than 1000 KB. </documentation>
</annotation>
</enumeration>
<enumeration value="FILES_TOO_MANY">
<annotation>
<documentation> HTML5 bundle cannot have more than 50 files. </documentation>
</annotation>
</enumeration>
<enumeration value="FLASH_UNSUPPORTED">
<annotation>
<documentation> Flash files in HTML5 bundles are not supported. Any file with a .swf or .flv extension causes this error. </documentation>
</annotation>
</enumeration>
<enumeration value="GWD_COMPONENTS_UNSUPPORTED">
<annotation>
<documentation> The HTML5 bundle contains unsupported GWD component(s). </documentation>
</annotation>
</enumeration>
<enumeration value="GWD_ENABLER_METHODS_UNSUPPORTED">
<annotation>
<documentation> The HTML5 bundle contains Unsupported GWD Enabler method(s). </documentation>
</annotation>
</enumeration>
<enumeration value="GWD_PROPERTIES_INVALID">
<annotation>
<documentation> GWD properties are invalid. </documentation>
</annotation>
</enumeration>
<enumeration value="LINKED_FILES_NOT_FOUND">
<annotation>
<documentation> The HTML5 bundle contains broken relative file reference(s). </documentation>
</annotation>
</enumeration>
<enumeration value="PRIMARY_HTML_MISSING">
<annotation>
<documentation> No primary HTML file detected. </documentation>
</annotation>
</enumeration>
<enumeration value="PRIMARY_HTML_UNDETERMINED">
<annotation>
<documentation> Multiple HTML files are detected. One of them should be named as {@code index.html} </documentation>
</annotation>
</enumeration>
<enumeration value="SVG_BLOCK_INVALID">
<annotation>
<documentation> An SVG block could not be parsed. </documentation>
</annotation>
</enumeration>
<enumeration value="CANNOT_DECODE_BUNDLE">
<annotation>
<documentation> The HTML5 bundle cannot be decoded. </documentation>
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
<simpleType name="InvalidPhoneNumberError.Reason">
<restriction base="xsd:string">
<enumeration value="INVALID_FORMAT">
<annotation>
<documentation> The phone number is invalid. </documentation>
</annotation>
</enumeration>
<enumeration value="TOO_SHORT">
<annotation>
<documentation> The phone number is too short. </documentation>
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
<simpleType name="LineItemCreativeAssociation.Status">
<annotation>
<documentation> Describes the status of the association. </documentation>
</annotation>
<restriction base="xsd:string">
<enumeration value="ACTIVE">
<annotation>
<documentation> The association is active and the associated {@link Creative} can be served. </documentation>
</annotation>
</enumeration>
<enumeration value="NOT_SERVING">
<annotation>
<documentation> The association is active but the associated {@link Creative} may not be served, because its size is not targeted by the line item. </documentation>
</annotation>
</enumeration>
<enumeration value="INACTIVE">
<annotation>
<documentation> The association is inactive and the associated {@link Creative} is ineligible for being served. </documentation>
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
<simpleType name="LineItemCreativeAssociationOperationError.Reason">
<annotation>
<documentation> The reasons for the target error. </documentation>
</annotation>
<restriction base="xsd:string">
<enumeration value="NOT_ALLOWED">
<annotation>
<documentation> The operation is not allowed due to permissions </documentation>
</annotation>
</enumeration>
<enumeration value="NOT_APPLICABLE">
<annotation>
<documentation> The operation is not applicable to the current state </documentation>
</annotation>
</enumeration>
<enumeration value="CANNOT_ACTIVATE_INVALID_CREATIVE">
<annotation>
<documentation> Cannot activate an invalid creative </documentation>
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
<documentation> The reasons for the target error. </documentation>
</annotation>
<restriction base="xsd:string">
<enumeration value="NOT_NULL"/>
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
<simpleType name="RichMediaStudioCreativeError.Reason">
<annotation>
<documentation> The reasons for the target error. </documentation>
</annotation>
<restriction base="xsd:string">
<enumeration value="CREATION_NOT_ALLOWED">
<annotation>
<documentation> Only Studio can create a {@code RichMediaStudioCreative}. </documentation>
</annotation>
</enumeration>
<enumeration value="UKNOWN_ERROR">
<annotation>
<documentation> Unknown error </documentation>
</annotation>
</enumeration>
<enumeration value="INVALID_CODE_GENERATION_REQUEST">
<annotation>
<documentation> Invalid request indicating missing/invalid request parameters. </documentation>
</annotation>
</enumeration>
<enumeration value="INVALID_CREATIVE_OBJECT">
<annotation>
<documentation> Invalid creative object. </documentation>
</annotation>
</enumeration>
<enumeration value="STUDIO_CONNECTION_ERROR">
<annotation>
<documentation> Unable to connect to Rich Media Studio to save the creative. Please try again later. </documentation>
</annotation>
</enumeration>
<enumeration value="PUSHDOWN_DURATION_NOT_ALLOWED">
<annotation>
<documentation> The push down duration is not allowed </documentation>
</annotation>
</enumeration>
<enumeration value="INVALID_POSITION">
<annotation>
<documentation> The position is invalid </documentation>
</annotation>
</enumeration>
<enumeration value="INVALID_Z_INDEX">
<annotation>
<documentation> The Z-index is invalid </documentation>
</annotation>
</enumeration>
<enumeration value="INVALID_PUSHDOWN_DURATION">
<annotation>
<documentation> The push-down duration is invalid </documentation>
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
<simpleType name="SetTopBoxCreativeError.Reason">
<annotation>
<documentation> Error reasons for set-top box creatives. </documentation>
</annotation>
<restriction base="xsd:string">
<enumeration value="EXTERNAL_ASSET_ID_IMMUTABLE">
<annotation>
<documentation> Set-top box creative external asset IDs are immutable after creation. </documentation>
</annotation>
</enumeration>
<enumeration value="EXTERNAL_ASSET_ID_REQUIRED">
<annotation>
<documentation> Set-top box creatives require an external asset ID. </documentation>
</annotation>
</enumeration>
<enumeration value="PROVIDER_ID_IMMUTABLE">
<annotation>
<documentation> Set-top box creative provider IDs are immutable after creation. </documentation>
</annotation>
</enumeration>
<enumeration value="UNKNOWN">
<annotation>
<documentation> The value returned if the actual value is not exposed by the requested API version. </documentation>
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
<simpleType name="SwiffyConversionError.Reason">
<annotation>
<documentation> Error reason for {@link SwiffyConversionError}. </documentation>
</annotation>
<restriction base="xsd:string">
<enumeration value="SERVER_ERROR">
<annotation>
<documentation> Indicates the Swiffy service has an internal error that prevents the flash asset being converted. </documentation>
</annotation>
</enumeration>
<enumeration value="INVALID_FLASH_FILE">
<annotation>
<documentation> Indicates the uploaded flash asset is not a valid flash file. </documentation>
</annotation>
</enumeration>
<enumeration value="UNSUPPORTED_FLASH">
<annotation>
<documentation> Indicates the Swiffy service currently does not support converting this flash asset. </documentation>
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
<element name="createLineItemCreativeAssociations">
<annotation>
<documentation> Creates new {@link LineItemCreativeAssociation} objects </documentation>
</annotation>
<complexType>
<sequence>
<element maxOccurs="unbounded" minOccurs="0" name="lineItemCreativeAssociations" type="tns:LineItemCreativeAssociation"/>
</sequence>
</complexType>
</element>
<element name="createLineItemCreativeAssociationsResponse">
<complexType>
<sequence>
<element maxOccurs="unbounded" minOccurs="0" name="rval" type="tns:LineItemCreativeAssociation"/>
</sequence>
</complexType>
</element>
<element name="ApiExceptionFault" type="tns:ApiException">
<annotation>
<documentation> A fault element of type ApiException. </documentation>
</annotation>
</element>
<element name="getLineItemCreativeAssociationsByStatement">
<annotation>
<documentation> Gets a {@link LineItemCreativeAssociationPage} of {@link LineItemCreativeAssociation} objects that satisfy the given {@link Statement#query}. The following fields are supported for filtering: <table> <tr> <th scope="col">PQL Property</th> <th scope="col">Object Property</th> </tr> <tr> <td>{@code creativeId}</td> <td>{@link LineItemCreativeAssociation#creativeId}</td> </tr> <tr> <td>{@code manualCreativeRotationWeight}</td> <td>{@link LineItemCreativeAssociation#manualCreativeRotationWeight}</td> </tr> <tr> <td>{@code destinationUrl}</td> <td>{@link LineItemCreativeAssociation#destinationUrl}</td> </tr> <tr> <td>{@code lineItemId}</td> <td>{@link LineItemCreativeAssociation#lineItemId}</td> </tr> <tr> <td>{@code status}</td> <td>{@link LineItemCreativeAssociation#status}</td> </tr> <tr> <td>{@code lastModifiedDateTime}</td> <td>{@link LineItemCreativeAssociation#lastModifiedDateTime}</td> </tr> </table> </documentation>
</annotation>
<complexType>
<sequence>
<element maxOccurs="1" minOccurs="0" name="filterStatement" type="tns:Statement"/>
</sequence>
</complexType>
</element>
<element name="getLineItemCreativeAssociationsByStatementResponse">
<complexType>
<sequence>
<element maxOccurs="1" minOccurs="0" name="rval" type="tns:LineItemCreativeAssociationPage"/>
</sequence>
</complexType>
</element>
<element name="getPreviewUrl">
<annotation>
<documentation> Returns an insite preview URL that references the specified site URL with the specified creative from the association served to it. For Creative Set previewing you may specify the master creative Id. </documentation>
</annotation>
<complexType>
<sequence>
<element maxOccurs="1" minOccurs="0" name="lineItemId" type="xsd:long"/>
<element maxOccurs="1" minOccurs="0" name="creativeId" type="xsd:long"/>
<element maxOccurs="1" minOccurs="0" name="siteUrl" type="xsd:string"/>
</sequence>
</complexType>
</element>
<element name="getPreviewUrlResponse">
<complexType>
<sequence>
<element maxOccurs="1" minOccurs="0" name="rval" type="xsd:string"/>
</sequence>
</complexType>
</element>
<element name="getPreviewUrlsForNativeStyles">
<annotation>
<documentation> Returns a list of URLs that reference the specified site URL with the specified creative from the association served to it. For Creative Set previewing you may specify the master creative Id. Each URL corresponds to one available native style for previewing the specified creative. </documentation>
</annotation>
<complexType>
<sequence>
<element maxOccurs="1" minOccurs="0" name="lineItemId" type="xsd:long"/>
<element maxOccurs="1" minOccurs="0" name="creativeId" type="xsd:long"/>
<element maxOccurs="1" minOccurs="0" name="siteUrl" type="xsd:string"/>
</sequence>
</complexType>
</element>
<element name="getPreviewUrlsForNativeStylesResponse">
<complexType>
<sequence>
<element maxOccurs="unbounded" minOccurs="0" name="rval" type="tns:CreativeNativeStylePreview"/>
</sequence>
</complexType>
</element>
<element name="performLineItemCreativeAssociationAction">
<annotation>
<documentation> Performs actions on {@link LineItemCreativeAssociation} objects that match the given {@link Statement#query}. </documentation>
</annotation>
<complexType>
<sequence>
<element maxOccurs="1" minOccurs="0" name="lineItemCreativeAssociationAction" type="tns:LineItemCreativeAssociationAction"/>
<element maxOccurs="1" minOccurs="0" name="filterStatement" type="tns:Statement"/>
</sequence>
</complexType>
</element>
<element name="performLineItemCreativeAssociationActionResponse">
<complexType>
<sequence>
<element maxOccurs="1" minOccurs="0" name="rval" type="tns:UpdateResult"/>
</sequence>
</complexType>
</element>
<element name="pushCreativeToDevices">
<annotation>
<documentation> Pushes a creative to devices that that satisfy the given {@link Statement#query}. * </documentation>
</annotation>
<complexType>
<sequence>
<element maxOccurs="1" minOccurs="0" name="filterStatement" type="tns:Statement"/>
<element maxOccurs="1" minOccurs="0" name="options" type="tns:CreativePushOptions"/>
</sequence>
</complexType>
</element>
<element name="pushCreativeToDevicesResponse">
<complexType>
<sequence>
<element maxOccurs="1" minOccurs="0" name="rval" type="tns:UpdateResult"/>
</sequence>
</complexType>
</element>
<element name="updateLineItemCreativeAssociations">
<annotation>
<documentation> Updates the specified {@link LineItemCreativeAssociation} objects </documentation>
</annotation>
<complexType>
<sequence>
<element maxOccurs="unbounded" minOccurs="0" name="lineItemCreativeAssociations" type="tns:LineItemCreativeAssociation"/>
</sequence>
</complexType>
</element>
<element name="updateLineItemCreativeAssociationsResponse">
<complexType>
<sequence>
<element maxOccurs="unbounded" minOccurs="0" name="rval" type="tns:LineItemCreativeAssociation"/>
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
<wsdl:message name="createLineItemCreativeAssociationsRequest">
<wsdl:part element="tns:createLineItemCreativeAssociations" name="parameters"/>
</wsdl:message>
<wsdl:message name="createLineItemCreativeAssociationsResponse">
<wsdl:part element="tns:createLineItemCreativeAssociationsResponse" name="parameters"/>
</wsdl:message>
<wsdl:message name="ApiException">
<wsdl:part element="tns:ApiExceptionFault" name="ApiException"/>
</wsdl:message>
<wsdl:message name="getLineItemCreativeAssociationsByStatementRequest">
<wsdl:part element="tns:getLineItemCreativeAssociationsByStatement" name="parameters"/>
</wsdl:message>
<wsdl:message name="getLineItemCreativeAssociationsByStatementResponse">
<wsdl:part element="tns:getLineItemCreativeAssociationsByStatementResponse" name="parameters"/>
</wsdl:message>
<wsdl:message name="getPreviewUrlRequest">
<wsdl:part element="tns:getPreviewUrl" name="parameters"/>
</wsdl:message>
<wsdl:message name="getPreviewUrlResponse">
<wsdl:part element="tns:getPreviewUrlResponse" name="parameters"/>
</wsdl:message>
<wsdl:message name="getPreviewUrlsForNativeStylesRequest">
<wsdl:part element="tns:getPreviewUrlsForNativeStyles" name="parameters"/>
</wsdl:message>
<wsdl:message name="getPreviewUrlsForNativeStylesResponse">
<wsdl:part element="tns:getPreviewUrlsForNativeStylesResponse" name="parameters"/>
</wsdl:message>
<wsdl:message name="performLineItemCreativeAssociationActionRequest">
<wsdl:part element="tns:performLineItemCreativeAssociationAction" name="parameters"/>
</wsdl:message>
<wsdl:message name="performLineItemCreativeAssociationActionResponse">
<wsdl:part element="tns:performLineItemCreativeAssociationActionResponse" name="parameters"/>
</wsdl:message>
<wsdl:message name="pushCreativeToDevicesRequest">
<wsdl:part element="tns:pushCreativeToDevices" name="parameters"/>
</wsdl:message>
<wsdl:message name="pushCreativeToDevicesResponse">
<wsdl:part element="tns:pushCreativeToDevicesResponse" name="parameters"/>
</wsdl:message>
<wsdl:message name="updateLineItemCreativeAssociationsRequest">
<wsdl:part element="tns:updateLineItemCreativeAssociations" name="parameters"/>
</wsdl:message>
<wsdl:message name="updateLineItemCreativeAssociationsResponse">
<wsdl:part element="tns:updateLineItemCreativeAssociationsResponse" name="parameters"/>
</wsdl:message>
<wsdl:portType name="LineItemCreativeAssociationServiceInterface">
<wsdl:documentation> Provides operations for creating, updating and retrieving {@link LineItemCreativeAssociation} objects. <p>A line item creative association (LICA) associates a {@link Creative} with a {@link LineItem}. When a line item is selected to serve, the LICAs specify which creatives can appear for the ad units that are targeted by the line item. In order to be associated with a line item, the creative must have a size that exists within the attribute {@link LineItem#creativePlaceholders}. <p>Each LICA has a start and end date and time that defines when the creative should be displayed. <p>To read more about associating creatives with line items, see this <a href="https://support.google.com/admanager/answer/3187916">Ad Manager Help Center</a> article. </wsdl:documentation>
<wsdl:operation name="createLineItemCreativeAssociations">
<wsdl:documentation> Creates new {@link LineItemCreativeAssociation} objects </wsdl:documentation>
<wsdl:input message="tns:createLineItemCreativeAssociationsRequest" name="createLineItemCreativeAssociationsRequest"/>
<wsdl:output message="tns:createLineItemCreativeAssociationsResponse" name="createLineItemCreativeAssociationsResponse"/>
<wsdl:fault message="tns:ApiException" name="ApiException"/>
</wsdl:operation>
<wsdl:operation name="getLineItemCreativeAssociationsByStatement">
<wsdl:documentation> Gets a {@link LineItemCreativeAssociationPage} of {@link LineItemCreativeAssociation} objects that satisfy the given {@link Statement#query}. The following fields are supported for filtering: <table> <tr> <th scope="col">PQL Property</th> <th scope="col">Object Property</th> </tr> <tr> <td>{@code creativeId}</td> <td>{@link LineItemCreativeAssociation#creativeId}</td> </tr> <tr> <td>{@code manualCreativeRotationWeight}</td> <td>{@link LineItemCreativeAssociation#manualCreativeRotationWeight}</td> </tr> <tr> <td>{@code destinationUrl}</td> <td>{@link LineItemCreativeAssociation#destinationUrl}</td> </tr> <tr> <td>{@code lineItemId}</td> <td>{@link LineItemCreativeAssociation#lineItemId}</td> </tr> <tr> <td>{@code status}</td> <td>{@link LineItemCreativeAssociation#status}</td> </tr> <tr> <td>{@code lastModifiedDateTime}</td> <td>{@link LineItemCreativeAssociation#lastModifiedDateTime}</td> </tr> </table> </wsdl:documentation>
<wsdl:input message="tns:getLineItemCreativeAssociationsByStatementRequest" name="getLineItemCreativeAssociationsByStatementRequest"/>
<wsdl:output message="tns:getLineItemCreativeAssociationsByStatementResponse" name="getLineItemCreativeAssociationsByStatementResponse"/>
<wsdl:fault message="tns:ApiException" name="ApiException"/>
</wsdl:operation>
<wsdl:operation name="getPreviewUrl">
<wsdl:documentation> Returns an insite preview URL that references the specified site URL with the specified creative from the association served to it. For Creative Set previewing you may specify the master creative Id. </wsdl:documentation>
<wsdl:input message="tns:getPreviewUrlRequest" name="getPreviewUrlRequest"/>
<wsdl:output message="tns:getPreviewUrlResponse" name="getPreviewUrlResponse"/>
<wsdl:fault message="tns:ApiException" name="ApiException"/>
</wsdl:operation>
<wsdl:operation name="getPreviewUrlsForNativeStyles">
<wsdl:documentation> Returns a list of URLs that reference the specified site URL with the specified creative from the association served to it. For Creative Set previewing you may specify the master creative Id. Each URL corresponds to one available native style for previewing the specified creative. </wsdl:documentation>
<wsdl:input message="tns:getPreviewUrlsForNativeStylesRequest" name="getPreviewUrlsForNativeStylesRequest"/>
<wsdl:output message="tns:getPreviewUrlsForNativeStylesResponse" name="getPreviewUrlsForNativeStylesResponse"/>
<wsdl:fault message="tns:ApiException" name="ApiException"/>
</wsdl:operation>
<wsdl:operation name="performLineItemCreativeAssociationAction">
<wsdl:documentation> Performs actions on {@link LineItemCreativeAssociation} objects that match the given {@link Statement#query}. </wsdl:documentation>
<wsdl:input message="tns:performLineItemCreativeAssociationActionRequest" name="performLineItemCreativeAssociationActionRequest"/>
<wsdl:output message="tns:performLineItemCreativeAssociationActionResponse" name="performLineItemCreativeAssociationActionResponse"/>
<wsdl:fault message="tns:ApiException" name="ApiException"/>
</wsdl:operation>
<wsdl:operation name="pushCreativeToDevices">
<wsdl:documentation> Pushes a creative to devices that that satisfy the given {@link Statement#query}. * </wsdl:documentation>
<wsdl:input message="tns:pushCreativeToDevicesRequest" name="pushCreativeToDevicesRequest"/>
<wsdl:output message="tns:pushCreativeToDevicesResponse" name="pushCreativeToDevicesResponse"/>
<wsdl:fault message="tns:ApiException" name="ApiException"/>
</wsdl:operation>
<wsdl:operation name="updateLineItemCreativeAssociations">
<wsdl:documentation> Updates the specified {@link LineItemCreativeAssociation} objects </wsdl:documentation>
<wsdl:input message="tns:updateLineItemCreativeAssociationsRequest" name="updateLineItemCreativeAssociationsRequest"/>
<wsdl:output message="tns:updateLineItemCreativeAssociationsResponse" name="updateLineItemCreativeAssociationsResponse"/>
<wsdl:fault message="tns:ApiException" name="ApiException"/>
</wsdl:operation>
</wsdl:portType>
<wsdl:binding name="LineItemCreativeAssociationServiceSoapBinding" type="tns:LineItemCreativeAssociationServiceInterface">
<wsdlsoap:binding style="document" transport="http://schemas.xmlsoap.org/soap/http"/>
<wsdl:operation name="createLineItemCreativeAssociations">
<wsdlsoap:operation soapAction=""/>
<wsdl:input name="createLineItemCreativeAssociationsRequest">
<wsdlsoap:header message="tns:RequestHeader" part="RequestHeader" use="literal"/>
<wsdlsoap:body use="literal"/>
</wsdl:input>
<wsdl:output name="createLineItemCreativeAssociationsResponse">
<wsdlsoap:header message="tns:ResponseHeader" part="ResponseHeader" use="literal"/>
<wsdlsoap:body use="literal"/>
</wsdl:output>
<wsdl:fault name="ApiException">
<wsdlsoap:fault name="ApiException" use="literal"/>
</wsdl:fault>
</wsdl:operation>
<wsdl:operation name="getLineItemCreativeAssociationsByStatement">
<wsdlsoap:operation soapAction=""/>
<wsdl:input name="getLineItemCreativeAssociationsByStatementRequest">
<wsdlsoap:header message="tns:RequestHeader" part="RequestHeader" use="literal"/>
<wsdlsoap:body use="literal"/>
</wsdl:input>
<wsdl:output name="getLineItemCreativeAssociationsByStatementResponse">
<wsdlsoap:header message="tns:ResponseHeader" part="ResponseHeader" use="literal"/>
<wsdlsoap:body use="literal"/>
</wsdl:output>
<wsdl:fault name="ApiException">
<wsdlsoap:fault name="ApiException" use="literal"/>
</wsdl:fault>
</wsdl:operation>
<wsdl:operation name="getPreviewUrl">
<wsdlsoap:operation soapAction=""/>
<wsdl:input name="getPreviewUrlRequest">
<wsdlsoap:header message="tns:RequestHeader" part="RequestHeader" use="literal"/>
<wsdlsoap:body use="literal"/>
</wsdl:input>
<wsdl:output name="getPreviewUrlResponse">
<wsdlsoap:header message="tns:ResponseHeader" part="ResponseHeader" use="literal"/>
<wsdlsoap:body use="literal"/>
</wsdl:output>
<wsdl:fault name="ApiException">
<wsdlsoap:fault name="ApiException" use="literal"/>
</wsdl:fault>
</wsdl:operation>
<wsdl:operation name="getPreviewUrlsForNativeStyles">
<wsdlsoap:operation soapAction=""/>
<wsdl:input name="getPreviewUrlsForNativeStylesRequest">
<wsdlsoap:header message="tns:RequestHeader" part="RequestHeader" use="literal"/>
<wsdlsoap:body use="literal"/>
</wsdl:input>
<wsdl:output name="getPreviewUrlsForNativeStylesResponse">
<wsdlsoap:header message="tns:ResponseHeader" part="ResponseHeader" use="literal"/>
<wsdlsoap:body use="literal"/>
</wsdl:output>
<wsdl:fault name="ApiException">
<wsdlsoap:fault name="ApiException" use="literal"/>
</wsdl:fault>
</wsdl:operation>
<wsdl:operation name="performLineItemCreativeAssociationAction">
<wsdlsoap:operation soapAction=""/>
<wsdl:input name="performLineItemCreativeAssociationActionRequest">
<wsdlsoap:header message="tns:RequestHeader" part="RequestHeader" use="literal"/>
<wsdlsoap:body use="literal"/>
</wsdl:input>
<wsdl:output name="performLineItemCreativeAssociationActionResponse">
<wsdlsoap:header message="tns:ResponseHeader" part="ResponseHeader" use="literal"/>
<wsdlsoap:body use="literal"/>
</wsdl:output>
<wsdl:fault name="ApiException">
<wsdlsoap:fault name="ApiException" use="literal"/>
</wsdl:fault>
</wsdl:operation>
<wsdl:operation name="pushCreativeToDevices">
<wsdlsoap:operation soapAction=""/>
<wsdl:input name="pushCreativeToDevicesRequest">
<wsdlsoap:header message="tns:RequestHeader" part="RequestHeader" use="literal"/>
<wsdlsoap:body use="literal"/>
</wsdl:input>
<wsdl:output name="pushCreativeToDevicesResponse">
<wsdlsoap:header message="tns:ResponseHeader" part="ResponseHeader" use="literal"/>
<wsdlsoap:body use="literal"/>
</wsdl:output>
<wsdl:fault name="ApiException">
<wsdlsoap:fault name="ApiException" use="literal"/>
</wsdl:fault>
</wsdl:operation>
<wsdl:operation name="updateLineItemCreativeAssociations">
<wsdlsoap:operation soapAction=""/>
<wsdl:input name="updateLineItemCreativeAssociationsRequest">
<wsdlsoap:header message="tns:RequestHeader" part="RequestHeader" use="literal"/>
<wsdlsoap:body use="literal"/>
</wsdl:input>
<wsdl:output name="updateLineItemCreativeAssociationsResponse">
<wsdlsoap:header message="tns:ResponseHeader" part="ResponseHeader" use="literal"/>
<wsdlsoap:body use="literal"/>
</wsdl:output>
<wsdl:fault name="ApiException">
<wsdlsoap:fault name="ApiException" use="literal"/>
</wsdl:fault>
</wsdl:operation>
</wsdl:binding>
<wsdl:service name="LineItemCreativeAssociationService">
<wsdl:port binding="tns:LineItemCreativeAssociationServiceSoapBinding" name="LineItemCreativeAssociationServiceInterfacePort">
<wsdlsoap:address location="https://ads.google.com/apis/ads/publisher/v202408/LineItemCreativeAssociationService"/>
</wsdl:port>
</wsdl:service>
</wsdl:definitions>
"""

from __future__ import annotations

from typing import List, Optional
from enum import Enum

from pydantic import Field

from rcplus_alloy_common.gam.vendor.common import (
    GAMSOAPBaseModel,
    DateTime,
    Size,
    Money,
    Stats,
)


class StartDateTimeType(str, Enum):
    """
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
    """
    USE_START_DATE_TIME = "USE_START_DATE_TIME"
    IMMEDIATELY = "IMMEDIATELY"
    ONE_HOUR_FROM_NOW = "ONE_HOUR_FROM_NOW"
    UNKNOWN = "UNKNOWN"


class LineItemCreativeAssociationStatus(str, Enum):
    """
    <simpleType name="LineItemCreativeAssociation.Status">
    <annotation>
    <documentation> Describes the status of the association. </documentation>
    </annotation>
    <restriction base="xsd:string">
    <enumeration value="ACTIVE">
    <annotation>
    <documentation> The association is active and the associated {@link Creative} can be served. </documentation>
    </annotation>
    </enumeration>
    <enumeration value="NOT_SERVING">
    <annotation>
    <documentation> The association is active but the associated {@link Creative} may not be served, because its size is not targeted by the line item. </documentation>
    </annotation>
    </enumeration>
    <enumeration value="INACTIVE">
    <annotation>
    <documentation> The association is inactive and the associated {@link Creative} is ineligible for being served. </documentation>
    </annotation>
    </enumeration>
    <enumeration value="UNKNOWN">
    <annotation>
    <documentation> The value returned if the actual value is not exposed by the requested API version. </documentation>
    </annotation>
    </enumeration>
    </restriction>
    </simpleType>
    """
    ACTIVE = "ACTIVE"
    NOT_SERVING = "NOT_SERVING"
    INACTIVE = "INACTIVE"
    UNKNOWN = "UNKNOWN"


class Long_StatsMapEntry(GAMSOAPBaseModel):
    """
    <complexType name="Long_StatsMapEntry">
    <annotation>
    <documentation> This represents an entry in a map with a key of type Long and value of type Stats. </documentation>
    </annotation>
    <sequence>
    <element maxOccurs="1" minOccurs="0" name="key" type="xsd:long"/>
    <element maxOccurs="1" minOccurs="0" name="value" type="tns:Stats"/>
    </sequence>
    </complexType>
    """
    key: Optional[int] = Field(
        None,
        description=""
    )
    value: Optional[Stats] = Field(
        None,
        description=""
    )


class LineItemCreativeAssociationStats(GAMSOAPBaseModel):
    """
    <complexType name="LineItemCreativeAssociationStats">
    <annotation>
    <documentation> Contains statistics such as impressions, clicks delivered and cost for {@link LineItemCreativeAssociation} objects. </documentation>
    </annotation>
    <sequence>
    <element maxOccurs="1" minOccurs="0" name="stats" type="tns:Stats">
    <annotation>
    <documentation> A {@link Stats} object that holds delivered impressions and clicks statistics. </documentation>
    </annotation>
    </element>
    <element maxOccurs="unbounded" minOccurs="0" name="creativeSetStats" type="tns:Long_StatsMapEntry">
    <annotation>
    <documentation> A map containing {@link Stats} objects for each creative belonging to a creative set, {@code null} for non creative set associations. </documentation>
    </annotation>
    </element>
    <element maxOccurs="1" minOccurs="0" name="costInOrderCurrency" type="tns:Money">
    <annotation>
    <documentation> The revenue generated thus far by the creative from its association with the particular line item in the publisher's currency. </documentation>
    </annotation>
    </element>
    </sequence>
    </complexType>
    """
    stats: Optional[Stats] = Field(
        None,
        description="A Stats object that holds delivered impressions and clicks statistics."
    )
    creativeSetStats: Optional[List[Long_StatsMapEntry]] = Field(
        None,
        description="A map containing Stats objects for each creative belonging to a creative set, null for non creative set associations."
    )
    costInOrderCurrency: Optional[Money] = Field(
        None,
        description="The revenue generated thus far by the creative from its association with the particular line item in the publisher's currency."
    )


class LineItemCreativeAssociation(GAMSOAPBaseModel):
    """
    complexType name="LineItemCreativeAssociation">
    <annotation>
    <documentation> A {@code LineItemCreativeAssociation} associates a {@link Creative} or {@link CreativeSet} with a {@link LineItem} so that the creative can be served in ad units targeted by the line item. </documentation>
    </annotation>
    <sequence>
    <element maxOccurs="1" minOccurs="0" name="lineItemId" type="xsd:long">
    <annotation>
    <documentation> The ID of the {@link LineItem} to which the {@link Creative} should be associated. This attribute is required. </documentation>
    </annotation>
    </element>
    <element maxOccurs="1" minOccurs="0" name="creativeId" type="xsd:long">
    <annotation>
    <documentation> The ID of the {@link Creative} being associated with a {@link LineItem}. <p>This attribute is required if this is an association between a line item and a creative. <br> This attribute is ignored if this is an association between a line item and a creative set. <p>If this is an association between a line item and a creative, when retrieving the line item creative association, the {@link #creativeId} will be the creative's ID. <br> If this is an association between a line item and a creative set, when retrieving the line item creative association, the {@link #creativeId} will be the ID of the {@link CreativeSet#masterCreativeId master creative}. </documentation>
    </annotation>
    </element>
    <element maxOccurs="1" minOccurs="0" name="creativeSetId" type="xsd:long">
    <annotation>
    <documentation> The ID of the {@link CreativeSet} being associated with a {@link LineItem}. This attribute is required if this is an association between a line item and a creative set. <p>This field will be {@code null} when retrieving associations between line items and creatives not belonging to a set. </documentation>
    </annotation>
    </element>
    <element maxOccurs="1" minOccurs="0" name="manualCreativeRotationWeight" type="xsd:double">
    <annotation>
    <documentation> The weight of the {@link Creative}. This value is only used if the line item's {@code creativeRotationType} is set to {@link CreativeRotationType#MANUAL}. This attribute is optional and defaults to 10. </documentation>
    </annotation>
    </element>
    <element maxOccurs="1" minOccurs="0" name="sequentialCreativeRotationIndex" type="xsd:int">
    <annotation>
    <documentation> The sequential rotation index of the {@link Creative}. This value is used only if the associated line item's {@link LineItem#creativeRotationType} is set to {@link CreativeRotationType#SEQUENTIAL}. This attribute is optional and defaults to 1. </documentation>
    </annotation>
    </element>
    <element maxOccurs="1" minOccurs="0" name="startDateTime" type="tns:DateTime">
    <annotation>
    <documentation> Overrides the value set for {@link LineItem#startDateTime}. This value is optional and is only valid for Ad Manager 360 networks. If unset, the {@link LineItem#startDateTime} will be used. </documentation>
    </annotation>
    </element>
    <element maxOccurs="1" minOccurs="0" name="startDateTimeType" type="tns:StartDateTimeType">
    <annotation>
    <documentation> Specifies whether to start serving to the {@code LineItemCreativeAssociation} right away, in an hour, etc. This attribute is optional and defaults to {@link StartDateTimeType#USE_START_DATE_TIME}. </documentation>
    </annotation>
    </element>
    <element maxOccurs="1" minOccurs="0" name="endDateTime" type="tns:DateTime">
    <annotation>
    <documentation> Overrides {@link LineItem#endDateTime}. This value is optional and is only valid for Ad Manager 360 networks. If unset, the {@link LineItem#endDateTime} will be used. </documentation>
    </annotation>
    </element>
    <element maxOccurs="1" minOccurs="0" name="destinationUrl" type="xsd:string">
    <annotation>
    <documentation> Overrides the value set for {@link HasDestinationUrlCreative#destinationUrl}. This value is optional and is only valid for Ad Manager 360 networks. </documentation>
    </annotation>
    </element>
    <element maxOccurs="unbounded" minOccurs="0" name="sizes" type="tns:Size">
    <annotation>
    <documentation> Overrides the value set for {@link Creative#size}, which allows the creative to be served to ad units that would otherwise not be compatible for its actual size. This value is optional. </documentation>
    </annotation>
    </element>
    <element maxOccurs="1" minOccurs="0" name="status" type="tns:LineItemCreativeAssociation.Status">
    <annotation>
    <documentation> The status of the association. This attribute is read-only. </documentation>
    </annotation>
    </element>
    <element maxOccurs="1" minOccurs="0" name="stats" type="tns:LineItemCreativeAssociationStats">
    <annotation>
    <documentation> Contains trafficking statistics for the association. This attribute is readonly and is populated by Google. This will be {@code null} in case there are no statistics for the association yet. </documentation>
    </annotation>
    </element>
    <element maxOccurs="1" minOccurs="0" name="lastModifiedDateTime" type="tns:DateTime">
    <annotation>
    <documentation> The date and time this association was last modified. </documentation>
    </annotation>
    </element>
    <element maxOccurs="1" minOccurs="0" name="targetingName" type="xsd:string">
    <annotation>
    <documentation> Specifies {@link CreativeTargeting} for this line item creative association. <p>This attribute is optional. It should match the creative targeting specified on the corresponding {@link CreativePlaceholder} in the {@link LineItem} that is being associated with the {@link Creative}. </documentation>
    </annotation>
    </element>
    </sequence>
    </complexType>
    """
    lineItemId: int = Field(
        description="The ID of the LineItem to which the Creative should be associated. This attribute is required."
    )
    creativeId: Optional[int] = Field(
        None,
        description="The ID of the Creative being associated with a LineItem. This attribute is required if this is an association between a line item and a creative. This attribute is ignored if this is an association between a line item and a creative set. If this is an association between a line item and a creative, when retrieving the line item creative association, the creativeId will be the creative's ID. If this is an association between a line item and a creative set, when retrieving the line item creative association, the creativeId will be the ID of the CreativeSet#masterCreativeId master creative.",
    )
    creativeSetId: Optional[int] = Field(
        None,
        description="The ID of the CreativeSet being associated with a LineItem. This attribute is required if this is an association between a line item and a creative set. This field will be null when retrieving associations between line items and creatives not belonging to a set.",
    )
    manualCreativeRotationWeight: Optional[float] = Field(
        None,
        description="The weight of the Creative. This value is only used if the line item's creativeRotationType is set to CreativeRotationType#MANUAL. This attribute is optional and defaults to 10.",
    )
    sequentialCreativeRotationIndex: Optional[int] = Field(
        None,
        description="The sequential rotation index of the Creative. This value is used only if the associated line item's LineItem#creativeRotationType is set to CreativeRotationType#SEQUENTIAL. This attribute is optional and defaults to 1.",
    )
    startDateTime: Optional[DateTime] = Field(
        None,
        description="Overrides the value set for LineItem#startDateTime. This value is optional and is only valid for Ad Manager 360 networks. If unset, the LineItem#startDateTime will be used.",
    )
    startDateTimeType: Optional[StartDateTimeType] = Field(
        None,
        description="Specifies whether to start serving to the LineItemCreativeAssociation right away, in an hour, etc. This attribute is optional and defaults to StartDateTimeType#USE_START_DATE_TIME.",
    )
    endDateTime: Optional[DateTime] = Field(
        None,
        description="Overrides LineItem#endDateTime . This value is optional and is only valid for Ad Manager 360 networks. If unset, the LineItem#endDateTime will be used.",
    )
    destinationUrl: Optional[str] = Field(
        None,
        description="Overrides the value set for HasDestinationUrlCreative#destinationUrl. This value is optional and is only valid for Ad Manager 360 networks.",
    )
    sizes: Optional[List[Size]] = Field(
        None,
        description="Overrides the value set for Creative#size, which allows the creative to be served to ad units that would otherwise not be compatible for its actual size. This value is optional.",
    )
    status: Optional[LineItemCreativeAssociationStatus] = Field(
        None, description="The status of the association. This attribute is read-only."
    )
    stats: Optional[LineItemCreativeAssociationStats] = Field(
        None,
        description="Contains trafficking statistics for the association. This attribute is readonly and is populated by Google. This will be null in case there are no statistics for the association yet.",
    )
    lastModifiedDateTime: Optional[DateTime] = Field(
        None, description="The date and time this association was last modified."
    )
    targetingName: Optional[str] = Field(
        None,
        description="Specifies CreativeTargeting for this line item creative association. This attribute is optional. It should match the creative targeting specified on the corresponding CreativePlaceholder in the LineItem that is being associated with the Creative.",
    )
