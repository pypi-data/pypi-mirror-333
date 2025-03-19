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
<complexType name="ActivateAdUnits">
<annotation>
<documentation> The action used for activating {@link AdUnit} objects. </documentation>
</annotation>
<complexContent>
<extension base="tns:AdUnitAction">
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
<complexType name="AdSenseSettings">
<annotation>
<documentation> Contains the AdSense configuration for an {@link AdUnit}. </documentation>
</annotation>
<sequence>
<element maxOccurs="1" minOccurs="0" name="adSenseEnabled" type="xsd:boolean">
<annotation>
<documentation> Specifies whether or not the {@link AdUnit} is enabled for serving ads from the AdSense content network. This attribute is optional and defaults to the ad unit's parent or ancestor's setting if one has been set. If no ancestor of the ad unit has set {@code adSenseEnabled}, the attribute is defaulted to {@code true}. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="borderColor" type="xsd:string">
<annotation>
<documentation> Specifies the Hexadecimal border color, from {@code 000000} to {@code FFFFFF}. This attribute is optional and defaults to the ad unit's parent or ancestor's setting if one has been set. If no ancestor of the ad unit has set {@code borderColor}, the attribute is defaulted to {@code FFFFFF}. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="titleColor" type="xsd:string">
<annotation>
<documentation> Specifies the Hexadecimal title color of an ad, from {@code 000000} to {@code FFFFFF}. This attribute is optional and defaults to the ad unit's parent or ancestor's setting if one has been set. If no ancestor of the ad unit has set {@code titleColor}, the attribute is defaulted to {@code 0000FF}. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="backgroundColor" type="xsd:string">
<annotation>
<documentation> Specifies the Hexadecimal background color of an ad, from {@code 000000} to {@code FFFFFF}. This attribute is optional and defaults to the ad unit's parent or ancestor's setting if one has been set. If no ancestor of the ad unit has set {@code backgroundColor}, the attribute is defaulted to {@code FFFFFF}. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="textColor" type="xsd:string">
<annotation>
<documentation> Specifies the Hexadecimal color of the text of an ad, from {@code 000000} to {@code FFFFFF}. This attribute is optional and defaults to the ad unit's parent or ancestor's setting if one has been set. If no ancestor of the ad unit has set {@code textColor}, the attribute is defaulted to {@code 000000}. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="urlColor" type="xsd:string">
<annotation>
<documentation> Specifies the Hexadecimal color of the URL of an ad, from {@code 000000} to {@code FFFFFF}. This attribute is optional and defaults to the ad unit's parent or ancestor's setting if one has been set. If no ancestor of the ad unit has set {@code urlColor}, the attribute is defaulted to {@code 008000} . </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="adType" type="tns:AdSenseSettings.AdType">
<annotation>
<documentation> Specifies what kind of ad can be served by this {@link AdUnit} from the AdSense Content Network. This attribute is optional and defaults to the ad unit's parent or ancestor's setting if one has been set. If no ancestor of the ad unit has set {@code adType}, the attribute is defaulted to {@link AdType#TEXT_AND_IMAGE}. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="borderStyle" type="tns:AdSenseSettings.BorderStyle">
<annotation>
<documentation> Specifies the border-style of the {@link AdUnit}. This attribute is optional and defaults to the ad unit's parent or ancestor's setting if one has been set. If no ancestor of the ad unit has set {@code borderStyle}, the attribute is defaulted to {@link BorderStyle#DEFAULT}. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="fontFamily" type="tns:AdSenseSettings.FontFamily">
<annotation>
<documentation> Specifies the font family of the {@link AdUnit}. This attribute is optional and defaults to the ad unit's parent or ancestor's setting if one has been set. If no ancestor of the ad unit has set {@code fontFamily}, the attribute is defaulted to {@link FontFamily#DEFAULT}. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="fontSize" type="tns:AdSenseSettings.FontSize">
<annotation>
<documentation> Specifies the font size of the {@link AdUnit}. This attribute is optional and defaults to the ad unit's parent or ancestor's setting if one has been set. If no ancestor of the ad unit has set {@code fontSize}, the attribute is defaulted to {@link FontSize#DEFAULT}. </documentation>
</annotation>
</element>
</sequence>
</complexType>
<complexType abstract="true" name="AdUnitAction">
<annotation>
<documentation> Represents the actions that can be performed on {@link AdUnit} objects. </documentation>
</annotation>
<sequence/>
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
<complexType name="AdUnit">
<annotation>
<documentation> An {@code AdUnit} represents a chunk of identified inventory for the publisher. It contains all the settings that need to be associated with inventory in order to serve ads to it. An {@code AdUnit} can also be the parent of other ad units in the inventory hierarchy. </documentation>
</annotation>
<sequence>
<element maxOccurs="1" minOccurs="0" name="id" type="xsd:string">
<annotation>
<documentation> Uniquely identifies the {@code AdUnit}. This value is read-only and is assigned by Google when an ad unit is created. This attribute is required for updates. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="parentId" type="xsd:string">
<annotation>
<documentation> The ID of the ad unit's parent. Every ad unit has a parent except for the root ad unit, which is created by Google. This attribute is required when creating the ad unit. Once the ad unit is created this value will be read-only. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="hasChildren" type="xsd:boolean">
<annotation>
<documentation> This field is set to {@code true} if the ad unit has any children. This attribute is read-only and is populated by Google. </documentation>
</annotation>
</element>
<element maxOccurs="unbounded" minOccurs="0" name="parentPath" type="tns:AdUnitParent">
<annotation>
<documentation> The path to this ad unit in the ad unit hierarchy represented as a list from the root to this ad unit's parent. For root ad units, this list is empty. This attribute is read-only and is populated by Google. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="name" type="xsd:string">
<annotation>
<documentation> The name of the ad unit. This attribute is required and its maximum length is 255 characters. This attribute must also be case-insensitive unique. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="description" type="xsd:string">
<annotation>
<documentation> A description of the ad unit. This value is optional and its maximum length is 65,535 characters. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="targetWindow" type="tns:AdUnit.TargetWindow">
<annotation>
<documentation> The value to use for the HTML link's {@code target} attribute. This value is optional and will be interpreted as {@link TargetWindow#TOP} if left blank. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="status" type="tns:InventoryStatus">
<annotation>
<documentation> The status of this ad unit. It defaults to {@link InventoryStatus#ACTIVE}. This value cannot be updated directly using {@link InventoryService#updateAdUnit}. It can only be modified by performing actions via {@link InventoryService#performAdUnitAction}. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="adUnitCode" type="xsd:string">
<annotation>
<documentation> A string used to uniquely identify the ad unit for the purposes of serving the ad. This attribute is optional and can be set during ad unit creation. If it is not provided, it will be assigned by Google based off of the inventory unit ID. Once an ad unit is created, its {@code adUnitCode} cannot be changed. </documentation>
</annotation>
</element>
<element maxOccurs="unbounded" minOccurs="0" name="adUnitSizes" type="tns:AdUnitSize">
<annotation>
<documentation> The permissible creative sizes that can be served inside this ad unit. This attribute is optional. This attribute replaces the {@code sizes} attribute. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="isInterstitial" type="xsd:boolean">
<annotation>
<documentation> Whether this is an interstitial ad unit. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="isNative" type="xsd:boolean">
<annotation>
<documentation> Whether this is a native ad unit. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="isFluid" type="xsd:boolean">
<annotation>
<documentation> Whether this is a fluid ad unit. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="explicitlyTargeted" type="xsd:boolean">
<annotation>
<documentation> If this field is set to {@code true}, then the {@code AdUnit} will not be implicitly targeted when its parent is. Traffickers must explicitly target such an ad unit or else no line items will serve to it. This feature is only available for Ad Manager 360 accounts. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="adSenseSettings" type="tns:AdSenseSettings">
<annotation>
<documentation> AdSense specific settings. To overwrite this, set the {@link #adSenseSettingsSource} to {@link PropertySourceType#DIRECTLY_SPECIFIED} when setting the value of this field. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="adSenseSettingsSource" type="tns:ValueSourceType">
<annotation>
<documentation> Specifies the source of {@link #adSenseSettings} value. To revert an overridden value to its default, set this field to {@link PropertySourceType#PARENT}. </documentation>
</annotation>
</element>
<element maxOccurs="unbounded" minOccurs="0" name="appliedLabelFrequencyCaps" type="tns:LabelFrequencyCap">
<annotation>
<documentation> The set of label frequency caps applied directly to this ad unit. There is a limit of 10 label frequency caps per ad unit. </documentation>
</annotation>
</element>
<element maxOccurs="unbounded" minOccurs="0" name="effectiveLabelFrequencyCaps" type="tns:LabelFrequencyCap">
<annotation>
<documentation> Contains the set of labels applied directly to the ad unit as well as those inherited from parent ad units. This field is readonly and is assigned by Google. </documentation>
</annotation>
</element>
<element maxOccurs="unbounded" minOccurs="0" name="appliedLabels" type="tns:AppliedLabel">
<annotation>
<documentation> The set of labels applied directly to this ad unit. </documentation>
</annotation>
</element>
<element maxOccurs="unbounded" minOccurs="0" name="effectiveAppliedLabels" type="tns:AppliedLabel">
<annotation>
<documentation> Contains the set of labels applied directly to the ad unit as well as those inherited from the parent ad units. If a label has been negated, only the negated label is returned. This field is readonly and is assigned by Google. </documentation>
</annotation>
</element>
<element maxOccurs="unbounded" minOccurs="0" name="effectiveTeamIds" type="xsd:long">
<annotation>
<documentation> The IDs of all teams that this ad unit is on as well as those inherited from parent ad units. This value is read-only and is set by Google. </documentation>
</annotation>
</element>
<element maxOccurs="unbounded" minOccurs="0" name="appliedTeamIds" type="xsd:long">
<annotation>
<documentation> The IDs of all teams that this ad unit is on directly. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="lastModifiedDateTime" type="tns:DateTime">
<annotation>
<documentation> The date and time this ad unit was last modified. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="smartSizeMode" type="tns:SmartSizeMode">
<annotation>
<documentation> The smart size mode for this ad unit. This attribute is optional and defaults to {@link SmartSizeMode#NONE} for fixed sizes. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="refreshRate" type="xsd:int">
<annotation>
<documentation> The interval in seconds which ad units in mobile apps automatically refresh. Valid values are between 30 and 120 seconds. This attribute is optional and only applies to ad units in mobile apps. If this value is not set, then the mobile app ad will not refresh. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="externalSetTopBoxChannelId" type="xsd:string">
<annotation>
<documentation> Specifies an ID for a channel in an external set-top box campaign management system. This attribute is only meaningful if {@link #isSetTopBoxEnabled} is {@code true}. This attribute is read-only. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="isSetTopBoxEnabled" type="xsd:boolean">
<annotation>
<documentation> Flag that specifies whether this ad unit represents an external set-top box channel. This attribute is read-only. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="applicationId" type="xsd:long">
<annotation>
<documentation> The {@link MobileApplication#applicationId} for the CTV application that this ad unit is within. This attribute is optional. </documentation>
</annotation>
</element>
</sequence>
</complexType>
<complexType name="AdUnitHierarchyError">
<annotation>
<documentation> Caused by creating an {@link AdUnit} object with an invalid hierarchy. </documentation>
</annotation>
<complexContent>
<extension base="tns:ApiError">
<sequence>
<element maxOccurs="1" minOccurs="0" name="reason" type="tns:AdUnitHierarchyError.Reason"/>
</sequence>
</extension>
</complexContent>
</complexType>
<complexType name="AdUnitPage">
<annotation>
<documentation> Captures a page of {@link AdUnit} objects. </documentation>
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
<element maxOccurs="unbounded" minOccurs="0" name="results" type="tns:AdUnit">
<annotation>
<documentation> The collection of ad units contained within this page. </documentation>
</annotation>
</element>
</sequence>
</complexType>
<complexType name="AdUnitParent">
<annotation>
<documentation> The summary of a parent {@link AdUnit}. </documentation>
</annotation>
<sequence>
<element maxOccurs="1" minOccurs="0" name="id" type="xsd:string">
<annotation>
<documentation> The ID of the parent {@code AdUnit}. This value is readonly and is populated by Google. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="name" type="xsd:string">
<annotation>
<documentation> The name of the parent {@code AdUnit}. This value is readonly and is populated by Google. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="adUnitCode" type="xsd:string">
<annotation>
<documentation> A string used to uniquely identify the ad unit for the purposes of serving the ad. This attribute is read-only and is assigned by Google when an ad unit is created. </documentation>
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
<complexType name="ArchiveAdUnits">
<annotation>
<documentation> The action used for archiving {@link AdUnit} objects. </documentation>
</annotation>
<complexContent>
<extension base="tns:AdUnitAction">
<sequence/>
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
<complexType name="CompanyError">
<annotation>
<documentation> A list of all errors associated with companies. </documentation>
</annotation>
<complexContent>
<extension base="tns:ApiError">
<sequence>
<element maxOccurs="1" minOccurs="0" name="reason" type="tns:CompanyError.Reason"/>
</sequence>
</extension>
</complexContent>
</complexType>
<complexType name="CreativeWrapperError">
<annotation>
<documentation> Errors specific to creative wrappers. </documentation>
</annotation>
<complexContent>
<extension base="tns:ApiError">
<sequence>
<element maxOccurs="1" minOccurs="0" name="reason" type="tns:CreativeWrapperError.Reason">
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
<complexType name="DeactivateAdUnits">
<annotation>
<documentation> The action used for deactivating {@link AdUnit} objects. </documentation>
</annotation>
<complexContent>
<extension base="tns:AdUnitAction">
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
<complexType name="InvalidColorError">
<annotation>
<documentation> A list of all errors associated with a color attribute. </documentation>
</annotation>
<complexContent>
<extension base="tns:ApiError">
<sequence>
<element maxOccurs="1" minOccurs="0" name="reason" type="tns:InvalidColorError.Reason"/>
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
<complexType name="InventoryUnitRefreshRateError">
<annotation>
<documentation> Lists errors relating to {@link AdUnit#refreshRate}. </documentation>
</annotation>
<complexContent>
<extension base="tns:ApiError">
<sequence>
<element maxOccurs="1" minOccurs="0" name="reason" type="tns:InventoryUnitRefreshRateError.Reason"/>
</sequence>
</extension>
</complexContent>
</complexType>
<complexType name="AdUnitSize">
<annotation>
<documentation> An {@code AdUnitSize} represents the size of an ad in an ad unit. This also represents the environment and companions of a particular ad in an ad unit. In most cases, it is a simple size with just a width and a height (sometimes representing an aspect ratio). </documentation>
</annotation>
<sequence>
<element maxOccurs="1" minOccurs="0" name="size" type="tns:Size">
<annotation>
<documentation> The permissible creative size that can be served inside this ad unit. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="environmentType" type="tns:EnvironmentType">
<annotation>
<documentation> The environment type of the ad unit size. The default value is {@link EnvironmentType#BROWSER}. </documentation>
</annotation>
</element>
<element maxOccurs="unbounded" minOccurs="0" name="companions" type="tns:AdUnitSize">
<annotation>
<documentation> The companions for this ad unit size. Companions are only valid if the environment is {@link EnvironmentType#VIDEO_PLAYER}. If the environment is {@link EnvironmentType#BROWSER} including companions results in an error. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="fullDisplayString" type="xsd:string">
<annotation>
<documentation> The full (including companion sizes, if applicable) display string of the size, e.g. {@code "300x250"} or {@code "300x250v (180x150)"} </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="isAudio" type="xsd:boolean">
<annotation>
<documentation> Whether the inventory size is audio. If set to true, {@code Size} will be set to {@code "1x1"} and {@code EnvironmentType} will be set to {@link EnvironmentType#VIDEO_PLAYER} regardless of user input. </documentation>
</annotation>
</element>
</sequence>
</complexType>
<complexType name="InventoryUnitSizesError">
<annotation>
<documentation> An error specifically for InventoryUnitSizes. </documentation>
</annotation>
<complexContent>
<extension base="tns:ApiError">
<sequence>
<element maxOccurs="1" minOccurs="0" name="reason" type="tns:InventoryUnitSizesError.Reason"/>
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
<complexType name="LabelFrequencyCap">
<annotation>
<documentation> A {@code LabelFrequencyCap} assigns a frequency cap to a label. The frequency cap will limit the cumulative number of impressions of any ad units with this label that may be shown to a particular user over a time unit. </documentation>
</annotation>
<sequence>
<element maxOccurs="1" minOccurs="0" name="frequencyCap" type="tns:FrequencyCap">
<annotation>
<documentation> The frequency cap to be applied with this label. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="labelId" type="xsd:long">
<annotation>
<documentation> ID of the label being capped on the {@link AdUnit}. </documentation>
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
<simpleType name="AdSenseSettings.AdType">
<annotation>
<documentation> Specifies the type of ads that can be served through this {@link AdUnit}. </documentation>
</annotation>
<restriction base="xsd:string">
<enumeration value="TEXT">
<annotation>
<documentation> Allows text-only ads. </documentation>
</annotation>
</enumeration>
<enumeration value="IMAGE">
<annotation>
<documentation> Allows image-only ads. </documentation>
</annotation>
</enumeration>
<enumeration value="TEXT_AND_IMAGE">
<annotation>
<documentation> Allows both text and image ads. </documentation>
</annotation>
</enumeration>
</restriction>
</simpleType>
<simpleType name="AdSenseSettings.BorderStyle">
<annotation>
<documentation> Describes the border of the HTML elements used to surround an ad displayed by the {@link AdUnit}. </documentation>
</annotation>
<restriction base="xsd:string">
<enumeration value="DEFAULT">
<annotation>
<documentation> Uses the default border-style of the browser. </documentation>
</annotation>
</enumeration>
<enumeration value="NOT_ROUNDED">
<annotation>
<documentation> Uses a cornered border-style. </documentation>
</annotation>
</enumeration>
<enumeration value="SLIGHTLY_ROUNDED">
<annotation>
<documentation> Uses a slightly rounded border-style. </documentation>
</annotation>
</enumeration>
<enumeration value="VERY_ROUNDED">
<annotation>
<documentation> Uses a rounded border-style. </documentation>
</annotation>
</enumeration>
</restriction>
</simpleType>
<simpleType name="AdSenseSettings.FontFamily">
<annotation>
<documentation> List of all possible font families. </documentation>
</annotation>
<restriction base="xsd:string">
<enumeration value="DEFAULT"/>
<enumeration value="ARIAL"/>
<enumeration value="TAHOMA"/>
<enumeration value="GEORGIA"/>
<enumeration value="TIMES"/>
<enumeration value="VERDANA"/>
</restriction>
</simpleType>
<simpleType name="AdSenseSettings.FontSize">
<annotation>
<documentation> List of all possible font sizes the user can choose. </documentation>
</annotation>
<restriction base="xsd:string">
<enumeration value="DEFAULT"/>
<enumeration value="SMALL"/>
<enumeration value="MEDIUM"/>
<enumeration value="LARGE"/>
</restriction>
</simpleType>
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
<simpleType name="AdUnit.TargetWindow">
<annotation>
<documentation> Corresponds to an HTML link's {@code target} attribute. </documentation>
</annotation>
<restriction base="xsd:string">
<enumeration value="TOP">
<annotation>
<documentation> Specifies that the link should open in the full body of the page. </documentation>
</annotation>
</enumeration>
<enumeration value="BLANK">
<annotation>
<documentation> Specifies that the link should open in a new window. </documentation>
</annotation>
</enumeration>
</restriction>
</simpleType>
<simpleType name="AdUnitHierarchyError.Reason">
<restriction base="xsd:string">
<enumeration value="INVALID_DEPTH">
<annotation>
<documentation> The depth of the {@link AdUnit} in the inventory hierarchy is greater than is allowed. The maximum allowed depth is two below the effective root ad unit for Ad Manager 360 accounts and is one level below the effective root ad unit for Ad Manager accounts. </documentation>
</annotation>
</enumeration>
<enumeration value="INVALID_PARENT">
<annotation>
<documentation> The only valid {@link AdUnit#parentId} for an Ad Manager account is the {@link Network#effectiveRootAdUnitId}, Ad Manager 360 accounts can specify an ad unit hierarchy with more than two levels. </documentation>
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
<simpleType name="CompanyError.Reason">
<annotation>
<documentation> Enumerates all possible company specific errors. </documentation>
</annotation>
<restriction base="xsd:string">
<enumeration value="CANNOT_SET_THIRD_PARTY_COMPANY_DUE_TO_TYPE">
<annotation>
<documentation> Indicates that an attempt was made to set a third party company for a company whose type is not the same as the third party company. </documentation>
</annotation>
</enumeration>
<enumeration value="CANNOT_UPDATE_COMPANY_TYPE">
<annotation>
<documentation> Indicates that an invalid attempt was made to change a company's type. </documentation>
</annotation>
</enumeration>
<enumeration value="INVALID_COMPANY_TYPE">
<annotation>
<documentation> Indicates that this type of company is not supported. </documentation>
</annotation>
</enumeration>
<enumeration value="PRIMARY_CONTACT_DOES_NOT_BELONG_TO_THIS_COMPANY">
<annotation>
<documentation> Indicates that an attempt was made to assign a primary contact who does not belong to the specified company. </documentation>
</annotation>
</enumeration>
<enumeration value="THIRD_PARTY_STATS_PROVIDER_IS_WRONG_ROLE_TYPE">
<annotation>
<documentation> Indicates that the user specified as the third party stats provider is of the wrong role type. The user must have the third party stats provider role. </documentation>
</annotation>
</enumeration>
<enumeration value="INVALID_LABEL_ASSOCIATION">
<annotation>
<documentation> Labels can only be applied to {@link Company.Type#ADVERTISER}, {@link Company.Type#HOUSE_ADVERTISER}, and {@link Company.Type#AD_NETWORK} company types. </documentation>
</annotation>
</enumeration>
<enumeration value="INVALID_COMPANY_TYPE_FOR_DEFAULT_BILLING_SETTING">
<annotation>
<documentation> Indicates that the {@link Company.Type} does not support default billing settings. </documentation>
</annotation>
</enumeration>
<enumeration value="INVALID_DEFAULT_BILLING_SETTING">
<annotation>
<documentation> Indicates that the format of the default billing setting is wrong. </documentation>
</annotation>
</enumeration>
<enumeration value="COMPANY_HAS_ACTIVE_SHARE_ASSIGNMENTS">
<annotation>
<documentation> Cannot remove the cross selling config from a company that has active share assignments. </documentation>
</annotation>
</enumeration>
<enumeration value="UNKNOWN">
<annotation>
<documentation> The value returned if the actual value is not exposed by the requested API version. </documentation>
</annotation>
</enumeration>
</restriction>
</simpleType>
<simpleType name="CreativeWrapperError.Reason">
<annotation>
<documentation> The reasons for the creative wrapper error. </documentation>
</annotation>
<restriction base="xsd:string">
<enumeration value="LABEL_ALREADY_ASSOCIATED_WITH_CREATIVE_WRAPPER">
<annotation>
<documentation> The label is already associated with a {@link CreativeWrapper}. </documentation>
</annotation>
</enumeration>
<enumeration value="INVALID_LABEL_TYPE">
<annotation>
<documentation> The label type of a creative wrapper must be {@link LabelType#CREATIVE_WRAPPER}. </documentation>
</annotation>
</enumeration>
<enumeration value="UNRECOGNIZED_MACRO">
<annotation>
<documentation> A macro used inside the snippet is not recognized. </documentation>
</annotation>
</enumeration>
<enumeration value="NEITHER_HEADER_NOR_FOOTER_SPECIFIED">
<annotation>
<documentation> When creating a new creative wrapper, either header or footer should exist. </documentation>
</annotation>
</enumeration>
<enumeration value="NEITHER_HEADER_NOR_FOOTER_NOR_VIDEO_TRACKING_URLS_SPECIFIED">
<annotation>
<documentation> Creative wrapper must have either header and/or footer, or video tracking URLs. </documentation>
</annotation>
</enumeration>
<enumeration value="CANNOT_USE_CREATIVE_WRAPPER_TYPE">
<annotation>
<documentation> The network has not been enabled for creating labels of type {@link LabelType#CREATIVE_WRAPPER}. </documentation>
</annotation>
</enumeration>
<enumeration value="CANNOT_UPDATE_LABEL_ID">
<annotation>
<documentation> Cannot update {@link CreativeWrapper#labelId}. </documentation>
</annotation>
</enumeration>
<enumeration value="CANNOT_APPLY_TO_AD_UNIT_WITH_VIDEO_SIZES">
<annotation>
<documentation> Cannot apply {@link LabelType#CREATIVE_WRAPPER} labels to an ad unit if it has no descendants with {@link AdUnit#adUnitSizes} of {@code AdUnitSize#environmentType} as {@link EnvironmentType#BROWSER}. </documentation>
</annotation>
</enumeration>
<enumeration value="CANNOT_APPLY_TO_AD_UNIT_WITHOUT_VIDEO_SIZES">
<annotation>
<documentation> Cannot apply {@link LabelType#CREATIVE_WRAPPER} labels with a {@link CreativeWrapper#VIDEO_TRACKING_URL} type to an ad unit if it has no descendants with {@link AdUnit#adUnitSizes} of {@code AdUnitSize#environmentType} as {@link EnvironmentType#VIDEO_PLAYER}. </documentation>
</annotation>
</enumeration>
<enumeration value="CANNOT_APPLY_TO_AD_UNIT_WITHOUT_LABEL_ASSOCIATION">
<annotation>
<documentation> Cannot apply {@link LabelType#CREATIVE_WRAPPER} labels to an ad unit if the label is not associated with a creative wrapper. </documentation>
</annotation>
</enumeration>
<enumeration value="CANNOT_APPLY_TO_MOBILE_AD_UNIT">
<annotation>
<documentation> Cannot apply {@link LabelType#CREATIVE_WRAPPER} labels to an ad unit if {@link AdUnit#targetPlatform} is of type {@code TargetPlatform#MOBILE} </documentation>
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
<simpleType name="InvalidColorError.Reason">
<restriction base="xsd:string">
<enumeration value="INVALID_FORMAT">
<annotation>
<documentation> The provided value is not a valid hexadecimal color. </documentation>
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
<simpleType name="InventoryStatus">
<annotation>
<documentation> Represents the status of objects that represent inventory - ad units and placements. </documentation>
</annotation>
<restriction base="xsd:string">
<enumeration value="ACTIVE">
<annotation>
<documentation> The object is active. </documentation>
</annotation>
</enumeration>
<enumeration value="INACTIVE">
<annotation>
<documentation> The object is no longer active. </documentation>
</annotation>
</enumeration>
<enumeration value="ARCHIVED">
<annotation>
<documentation> The object has been archived. </documentation>
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
<simpleType name="InventoryUnitRefreshRateError.Reason">
<annotation>
<documentation> Reasons for the error. </documentation>
</annotation>
<restriction base="xsd:string">
<enumeration value="INVALID_RANGE">
<annotation>
<documentation> The refresh rate must be between 30 and 120 seconds. </documentation>
</annotation>
</enumeration>
<enumeration value="UNKNOWN">
<annotation>
<documentation> The value returned if the actual value is not exposed by the requested API version. </documentation>
</annotation>
</enumeration>
</restriction>
</simpleType>
<simpleType name="InventoryUnitSizesError.Reason">
<annotation>
<documentation> All possible reasons the error can be thrown. </documentation>
</annotation>
<restriction base="xsd:string">
<enumeration value="INVALID_SIZES">
<annotation>
<documentation> A size in the ad unit is too large or too small. </documentation>
</annotation>
</enumeration>
<enumeration value="INVALID_SIZE_FOR_PLATFORM">
<annotation>
<documentation> A size is an aspect ratio, but the ad unit is not a mobile ad unit. </documentation>
</annotation>
</enumeration>
<enumeration value="VIDEO_FEATURE_MISSING">
<annotation>
<documentation> A size is video, but the video feature is not enabled. </documentation>
</annotation>
</enumeration>
<enumeration value="VIDEO_MOBILE_LINE_ITEM_FEATURE_MISSING">
<annotation>
<documentation> A size is video in a mobile ad unit, but the mobile video feature is not enabled. </documentation>
</annotation>
</enumeration>
<enumeration value="INVALID_SIZE_FOR_MASTER">
<annotation>
<documentation> A size that has companions must have an environment of VIDEO_PLAYER. </documentation>
</annotation>
</enumeration>
<enumeration value="INVALID_SIZE_FOR_COMPANION">
<annotation>
<documentation> A size that is a companion must have an environment of BROWSER. </documentation>
</annotation>
</enumeration>
<enumeration value="DUPLICATE_MASTER_SIZES">
<annotation>
<documentation> Duplicate video master sizes are not allowed. </documentation>
</annotation>
</enumeration>
<enumeration value="ASPECT_RATIO_NOT_SUPPORTED">
<annotation>
<documentation> A size is an aspect ratio, but aspect ratio sizes are not enabled. </documentation>
</annotation>
</enumeration>
<enumeration value="VIDEO_COMPANIONS_NOT_SUPPORTED">
<annotation>
<documentation> A video size has companions, but companions are not allowed for the network </documentation>
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
<simpleType name="ValueSourceType">
<annotation>
<documentation> Identifies the source of a field's value. </documentation>
</annotation>
<restriction base="xsd:string">
<enumeration value="PARENT">
<annotation>
<documentation> The field's value is inherited from the parent object. </documentation>
</annotation>
</enumeration>
<enumeration value="DIRECTLY_SPECIFIED">
<annotation>
<documentation> The field's value is user specified and not inherited. </documentation>
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
<simpleType name="SmartSizeMode">
<annotation>
<documentation> Represents smart size modes. </documentation>
</annotation>
<restriction base="xsd:string">
<enumeration value="UNKNOWN">
<annotation>
<documentation> The value returned if the actual value is not exposed by the requested API version. </documentation>
</annotation>
</enumeration>
<enumeration value="NONE">
<annotation>
<documentation> Fixed size mode (default). </documentation>
</annotation>
</enumeration>
<enumeration value="SMART_BANNER">
<annotation>
<documentation> The height is fixed for the request, the width is a range. </documentation>
</annotation>
</enumeration>
<enumeration value="DYNAMIC_SIZE">
<annotation>
<documentation> Height and width are ranges. </documentation>
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
<element name="createAdUnits">
<annotation>
<documentation> Creates new {@link AdUnit} objects. </documentation>
</annotation>
<complexType>
<sequence>
<element maxOccurs="unbounded" minOccurs="0" name="adUnits" type="tns:AdUnit"/>
</sequence>
</complexType>
</element>
<element name="createAdUnitsResponse">
<complexType>
<sequence>
<element maxOccurs="unbounded" minOccurs="0" name="rval" type="tns:AdUnit"/>
</sequence>
</complexType>
</element>
<element name="ApiExceptionFault" type="tns:ApiException">
<annotation>
<documentation> A fault element of type ApiException. </documentation>
</annotation>
</element>
<element name="getAdUnitSizesByStatement">
<annotation>
<documentation> Returns a set of all relevant {@link AdUnitSize} objects. <p>The given {@link Statement} is currently ignored but may be honored in future versions. </documentation>
</annotation>
<complexType>
<sequence>
<element maxOccurs="1" minOccurs="0" name="filterStatement" type="tns:Statement"/>
</sequence>
</complexType>
</element>
<element name="getAdUnitSizesByStatementResponse">
<complexType>
<sequence>
<element maxOccurs="unbounded" minOccurs="0" name="rval" type="tns:AdUnitSize"/>
</sequence>
</complexType>
</element>
<element name="getAdUnitsByStatement">
<annotation>
<documentation> Gets a {@link AdUnitPage} of {@link AdUnit} objects that satisfy the given {@link Statement#query}. The following fields are supported for filtering: <table> <tr> <th scope="col">PQL Property</th> <th scope="col">Object Property</th> </tr> <tr> <td>{@code adUnitCode}</td> <td>{@link AdUnit#adUnitCode}</td> </tr> <tr> <td>{@code id}</td> <td>{@link AdUnit#id}</td> </tr> <tr> <td>{@code name}</td> <td>{@link AdUnit#name}</td> </tr> <tr> <td>{@code parentId}</td> <td>{@link AdUnit#parentId}</td> </tr> <tr> <td>{@code status}</td> <td>{@link AdUnit#status}</td> </tr> <tr> <td>{@code lastModifiedDateTime}</td> <td>{@link AdUnit#lastModifiedDateTime}</td> </tr> </table> </documentation>
</annotation>
<complexType>
<sequence>
<element maxOccurs="1" minOccurs="0" name="filterStatement" type="tns:Statement"/>
</sequence>
</complexType>
</element>
<element name="getAdUnitsByStatementResponse">
<complexType>
<sequence>
<element maxOccurs="1" minOccurs="0" name="rval" type="tns:AdUnitPage"/>
</sequence>
</complexType>
</element>
<element name="performAdUnitAction">
<annotation>
<documentation> Performs actions on {@link AdUnit} objects that match the given {@link Statement#query}. </documentation>
</annotation>
<complexType>
<sequence>
<element maxOccurs="1" minOccurs="0" name="adUnitAction" type="tns:AdUnitAction"/>
<element maxOccurs="1" minOccurs="0" name="filterStatement" type="tns:Statement"/>
</sequence>
</complexType>
</element>
<element name="performAdUnitActionResponse">
<complexType>
<sequence>
<element maxOccurs="1" minOccurs="0" name="rval" type="tns:UpdateResult"/>
</sequence>
</complexType>
</element>
<element name="updateAdUnits">
<annotation>
<documentation> Updates the specified {@link AdUnit} objects. </documentation>
</annotation>
<complexType>
<sequence>
<element maxOccurs="unbounded" minOccurs="0" name="adUnits" type="tns:AdUnit"/>
</sequence>
</complexType>
</element>
<element name="updateAdUnitsResponse">
<complexType>
<sequence>
<element maxOccurs="unbounded" minOccurs="0" name="rval" type="tns:AdUnit"/>
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
<wsdl:message name="createAdUnitsRequest">
<wsdl:part element="tns:createAdUnits" name="parameters"/>
</wsdl:message>
<wsdl:message name="createAdUnitsResponse">
<wsdl:part element="tns:createAdUnitsResponse" name="parameters"/>
</wsdl:message>
<wsdl:message name="ApiException">
<wsdl:part element="tns:ApiExceptionFault" name="ApiException"/>
</wsdl:message>
<wsdl:message name="getAdUnitSizesByStatementRequest">
<wsdl:part element="tns:getAdUnitSizesByStatement" name="parameters"/>
</wsdl:message>
<wsdl:message name="getAdUnitSizesByStatementResponse">
<wsdl:part element="tns:getAdUnitSizesByStatementResponse" name="parameters"/>
</wsdl:message>
<wsdl:message name="getAdUnitsByStatementRequest">
<wsdl:part element="tns:getAdUnitsByStatement" name="parameters"/>
</wsdl:message>
<wsdl:message name="getAdUnitsByStatementResponse">
<wsdl:part element="tns:getAdUnitsByStatementResponse" name="parameters"/>
</wsdl:message>
<wsdl:message name="performAdUnitActionRequest">
<wsdl:part element="tns:performAdUnitAction" name="parameters"/>
</wsdl:message>
<wsdl:message name="performAdUnitActionResponse">
<wsdl:part element="tns:performAdUnitActionResponse" name="parameters"/>
</wsdl:message>
<wsdl:message name="updateAdUnitsRequest">
<wsdl:part element="tns:updateAdUnits" name="parameters"/>
</wsdl:message>
<wsdl:message name="updateAdUnitsResponse">
<wsdl:part element="tns:updateAdUnitsResponse" name="parameters"/>
</wsdl:message>
<wsdl:portType name="InventoryServiceInterface">
<wsdl:documentation> Provides operations for creating, updating and retrieving {@link AdUnit} objects. <p>Line items connect a creative with its associated ad unit through targeting. <p>An ad unit represents a piece of inventory within a publisher. It contains all the settings that need to be associated with the inventory in order to serve ads. For example, the ad unit contains creative size restrictions and AdSense settings. </wsdl:documentation>
<wsdl:operation name="createAdUnits">
<wsdl:documentation> Creates new {@link AdUnit} objects. </wsdl:documentation>
<wsdl:input message="tns:createAdUnitsRequest" name="createAdUnitsRequest"/>
<wsdl:output message="tns:createAdUnitsResponse" name="createAdUnitsResponse"/>
<wsdl:fault message="tns:ApiException" name="ApiException"/>
</wsdl:operation>
<wsdl:operation name="getAdUnitSizesByStatement">
<wsdl:documentation> Returns a set of all relevant {@link AdUnitSize} objects. <p>The given {@link Statement} is currently ignored but may be honored in future versions. </wsdl:documentation>
<wsdl:input message="tns:getAdUnitSizesByStatementRequest" name="getAdUnitSizesByStatementRequest"/>
<wsdl:output message="tns:getAdUnitSizesByStatementResponse" name="getAdUnitSizesByStatementResponse"/>
<wsdl:fault message="tns:ApiException" name="ApiException"/>
</wsdl:operation>
<wsdl:operation name="getAdUnitsByStatement">
<wsdl:documentation> Gets a {@link AdUnitPage} of {@link AdUnit} objects that satisfy the given {@link Statement#query}. The following fields are supported for filtering: <table> <tr> <th scope="col">PQL Property</th> <th scope="col">Object Property</th> </tr> <tr> <td>{@code adUnitCode}</td> <td>{@link AdUnit#adUnitCode}</td> </tr> <tr> <td>{@code id}</td> <td>{@link AdUnit#id}</td> </tr> <tr> <td>{@code name}</td> <td>{@link AdUnit#name}</td> </tr> <tr> <td>{@code parentId}</td> <td>{@link AdUnit#parentId}</td> </tr> <tr> <td>{@code status}</td> <td>{@link AdUnit#status}</td> </tr> <tr> <td>{@code lastModifiedDateTime}</td> <td>{@link AdUnit#lastModifiedDateTime}</td> </tr> </table> </wsdl:documentation>
<wsdl:input message="tns:getAdUnitsByStatementRequest" name="getAdUnitsByStatementRequest"/>
<wsdl:output message="tns:getAdUnitsByStatementResponse" name="getAdUnitsByStatementResponse"/>
<wsdl:fault message="tns:ApiException" name="ApiException"/>
</wsdl:operation>
<wsdl:operation name="performAdUnitAction">
<wsdl:documentation> Performs actions on {@link AdUnit} objects that match the given {@link Statement#query}. </wsdl:documentation>
<wsdl:input message="tns:performAdUnitActionRequest" name="performAdUnitActionRequest"/>
<wsdl:output message="tns:performAdUnitActionResponse" name="performAdUnitActionResponse"/>
<wsdl:fault message="tns:ApiException" name="ApiException"/>
</wsdl:operation>
<wsdl:operation name="updateAdUnits">
<wsdl:documentation> Updates the specified {@link AdUnit} objects. </wsdl:documentation>
<wsdl:input message="tns:updateAdUnitsRequest" name="updateAdUnitsRequest"/>
<wsdl:output message="tns:updateAdUnitsResponse" name="updateAdUnitsResponse"/>
<wsdl:fault message="tns:ApiException" name="ApiException"/>
</wsdl:operation>
</wsdl:portType>
<wsdl:binding name="InventoryServiceSoapBinding" type="tns:InventoryServiceInterface">
<wsdlsoap:binding style="document" transport="http://schemas.xmlsoap.org/soap/http"/>
<wsdl:operation name="createAdUnits">
<wsdlsoap:operation soapAction=""/>
<wsdl:input name="createAdUnitsRequest">
<wsdlsoap:header message="tns:RequestHeader" part="RequestHeader" use="literal"/>
<wsdlsoap:body use="literal"/>
</wsdl:input>
<wsdl:output name="createAdUnitsResponse">
<wsdlsoap:header message="tns:ResponseHeader" part="ResponseHeader" use="literal"/>
<wsdlsoap:body use="literal"/>
</wsdl:output>
<wsdl:fault name="ApiException">
<wsdlsoap:fault name="ApiException" use="literal"/>
</wsdl:fault>
</wsdl:operation>
<wsdl:operation name="getAdUnitSizesByStatement">
<wsdlsoap:operation soapAction=""/>
<wsdl:input name="getAdUnitSizesByStatementRequest">
<wsdlsoap:header message="tns:RequestHeader" part="RequestHeader" use="literal"/>
<wsdlsoap:body use="literal"/>
</wsdl:input>
<wsdl:output name="getAdUnitSizesByStatementResponse">
<wsdlsoap:header message="tns:ResponseHeader" part="ResponseHeader" use="literal"/>
<wsdlsoap:body use="literal"/>
</wsdl:output>
<wsdl:fault name="ApiException">
<wsdlsoap:fault name="ApiException" use="literal"/>
</wsdl:fault>
</wsdl:operation>
<wsdl:operation name="getAdUnitsByStatement">
<wsdlsoap:operation soapAction=""/>
<wsdl:input name="getAdUnitsByStatementRequest">
<wsdlsoap:header message="tns:RequestHeader" part="RequestHeader" use="literal"/>
<wsdlsoap:body use="literal"/>
</wsdl:input>
<wsdl:output name="getAdUnitsByStatementResponse">
<wsdlsoap:header message="tns:ResponseHeader" part="ResponseHeader" use="literal"/>
<wsdlsoap:body use="literal"/>
</wsdl:output>
<wsdl:fault name="ApiException">
<wsdlsoap:fault name="ApiException" use="literal"/>
</wsdl:fault>
</wsdl:operation>
<wsdl:operation name="performAdUnitAction">
<wsdlsoap:operation soapAction=""/>
<wsdl:input name="performAdUnitActionRequest">
<wsdlsoap:header message="tns:RequestHeader" part="RequestHeader" use="literal"/>
<wsdlsoap:body use="literal"/>
</wsdl:input>
<wsdl:output name="performAdUnitActionResponse">
<wsdlsoap:header message="tns:ResponseHeader" part="ResponseHeader" use="literal"/>
<wsdlsoap:body use="literal"/>
</wsdl:output>
<wsdl:fault name="ApiException">
<wsdlsoap:fault name="ApiException" use="literal"/>
</wsdl:fault>
</wsdl:operation>
<wsdl:operation name="updateAdUnits">
<wsdlsoap:operation soapAction=""/>
<wsdl:input name="updateAdUnitsRequest">
<wsdlsoap:header message="tns:RequestHeader" part="RequestHeader" use="literal"/>
<wsdlsoap:body use="literal"/>
</wsdl:input>
<wsdl:output name="updateAdUnitsResponse">
<wsdlsoap:header message="tns:ResponseHeader" part="ResponseHeader" use="literal"/>
<wsdlsoap:body use="literal"/>
</wsdl:output>
<wsdl:fault name="ApiException">
<wsdlsoap:fault name="ApiException" use="literal"/>
</wsdl:fault>
</wsdl:operation>
</wsdl:binding>
<wsdl:service name="InventoryService">
<wsdl:port binding="tns:InventoryServiceSoapBinding" name="InventoryServiceInterfacePort">
<wsdlsoap:address location="https://ads.google.com/apis/ads/publisher/v202408/InventoryService"/>
</wsdl:port>
</wsdl:service>
</wsdl:definitions>
"""


from __future__ import annotations
from typing import List, Optional, Any
from enum import Enum

from pydantic import Field

from rcplus_alloy_common.gam.vendor.common import (
    GAMSOAPBaseModel,
    DateTime,
    Size,
    AppliedLabel,
    FrequencyCap,
    EnvironmentType,
)


class SmartSizeMode(str, Enum):
    """
    <simpleType name="SmartSizeMode">
    <annotation>
    <documentation> Represents smart size modes. </documentation>
    </annotation>
    <restriction base="xsd:string">
    <enumeration value="UNKNOWN">
    <annotation>
    <documentation> The value returned if the actual value is not exposed by the requested API version. </documentation>
    </annotation>
    </enumeration>
    <enumeration value="NONE">
    <annotation>
    <documentation> Fixed size mode (default). </documentation>
    </annotation>
    </enumeration>
    <enumeration value="SMART_BANNER">
    <annotation>
    <documentation> The height is fixed for the request, the width is a range. </documentation>
    </annotation>
    </enumeration>
    <enumeration value="DYNAMIC_SIZE">
    <annotation>
    <documentation> Height and width are ranges. </documentation>
    </annotation>
    </enumeration>
    </restriction>
    </simpleType>
    """
    UNKNOWN = "UNKNOWN"
    NONE = "NONE"
    SMART_BANNER = "SMART_BANNER"
    DYNAMIC_SIZE = "DYNAMIC_SIZE"


class LabelFrequencyCap(GAMSOAPBaseModel):
    """
    <complexType name="LabelFrequencyCap">
    <annotation>
    <documentation> A {@code LabelFrequencyCap} assigns a frequency cap to a label. The frequency cap will limit the cumulative number of impressions of any ad units with this label that may be shown to a particular user over a time unit. </documentation>
    </annotation>
    <sequence>
    <element maxOccurs="1" minOccurs="0" name="frequencyCap" type="tns:FrequencyCap">
    <annotation>
    <documentation> The frequency cap to be applied with this label. </documentation>
    </annotation>
    </element>
    <element maxOccurs="1" minOccurs="0" name="labelId" type="xsd:long">
    <annotation>
    <documentation> ID of the label being capped on the {@link AdUnit}. </documentation>
    </annotation>
    </element>
    </sequence>
    </complexType>
    """
    frequencyCap: Optional[FrequencyCap] = Field(description="The frequency cap to be applied with this label.")
    labelId: Optional[int] = Field(description="ID of the label being capped on the AdUnit.")


class ValueSourceType(str, Enum):
    """
    <simpleType name="ValueSourceType">
    <annotation>
    <documentation> Identifies the source of a field's value. </documentation>
    </annotation>
    <restriction base="xsd:string">
    <enumeration value="PARENT">
    <annotation>
    <documentation> The field's value is inherited from the parent object. </documentation>
    </annotation>
    </enumeration>
    <enumeration value="DIRECTLY_SPECIFIED">
    <annotation>
    <documentation> The field's value is user specified and not inherited. </documentation>
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
    PARENT = "PARENT"
    DIRECTLY_SPECIFIED = "DIRECTLY_SPECIFIED"
    UNKNOWN = "UNKNOWN"


class InventoryStatus(str, Enum):
    """
    <simpleType name="InventoryStatus">
    <annotation>
    <documentation> Represents the status of objects that represent inventory - ad units and placements. </documentation>
    </annotation>
    <restriction base="xsd:string">
    <enumeration value="ACTIVE">
    <annotation>
    <documentation> The object is active. </documentation>
    </annotation>
    </enumeration>
    <enumeration value="INACTIVE">
    <annotation>
    <documentation> The object is no longer active. </documentation>
    </annotation>
    </enumeration>
    <enumeration value="ARCHIVED">
    <annotation>
    <documentation> The object has been archived. </documentation>
    </annotation>
    </enumeration>
    </restriction>
    </simpleType>
    """
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    ARCHIVED = "ARCHIVED"


class AdUnitParent(GAMSOAPBaseModel):
    """
    <complexType name="AdUnitParent">
    <annotation>
    <documentation> The summary of a parent {@link AdUnit}. </documentation>
    </annotation>
    <sequence>
    <element maxOccurs="1" minOccurs="0" name="id" type="xsd:string">
    <annotation>
    <documentation> The ID of the parent {@code AdUnit}. This value is readonly and is populated by Google. </documentation>
    </annotation>
    </element>
    <element maxOccurs="1" minOccurs="0" name="name" type="xsd:string">
    <annotation>
    <documentation> The name of the parent {@code AdUnit}. This value is readonly and is populated by Google. </documentation>
    </annotation>
    </element>
    <element maxOccurs="1" minOccurs="0" name="adUnitCode" type="xsd:string">
    <annotation>
    <documentation> A string used to uniquely identify the ad unit for the purposes of serving the ad. This attribute is read-only and is assigned by Google when an ad unit is created. </documentation>
    </annotation>
    </element>
    </sequence>
    </complexType>
    """
    id: str = Field(description="The ID of the parent AdUnit. This value is readonly and is populated by Google.")
    name: str = Field(description="The name of the parent AdUnit. This value is readonly and is populated by Google.")
    adUnitCode: str = Field(description="A string used to uniquely identify the ad unit for the purposes of serving the ad. This attribute is read-only and is assigned by Google when an ad unit is created.")


class AdUnitTargetWindow(str, Enum):
    """
    <simpleType name="AdUnit.TargetWindow">
    <annotation>
    <documentation> Corresponds to an HTML link's {@code target} attribute. </documentation>
    </annotation>
    <restriction base="xsd:string">
    <enumeration value="TOP">
    <annotation>
    <documentation> Specifies that the link should open in the full body of the page. </documentation>
    </annotation>
    </enumeration>
    <enumeration value="BLANK">
    <annotation>
    <documentation> Specifies that the link should open in a new window. </documentation>
    </annotation>
    </enumeration>
    </restriction>
    </simpleType>
    """
    TOP = "TOP"
    BLANK = "BLANK"


class AdUnitSize(GAMSOAPBaseModel):
    """
    <complexType name="AdUnitSize">
    <annotation>
    <documentation> An {@code AdUnitSize} represents the size of an ad in an ad unit. This also represents the environment and companions of a particular ad in an ad unit. In most cases, it is a simple size with just a width and a height (sometimes representing an aspect ratio). </documentation>
    </annotation>
    <sequence>
    <element maxOccurs="1" minOccurs="0" name="size" type="tns:Size">
    <annotation>
    <documentation> The permissible creative size that can be served inside this ad unit. </documentation>
    </annotation>
    </element>
    <element maxOccurs="1" minOccurs="0" name="environmentType" type="tns:EnvironmentType">
    <annotation>
    <documentation> The environment type of the ad unit size. The default value is {@link EnvironmentType#BROWSER}. </documentation>
    </annotation>
    </element>
    <element maxOccurs="unbounded" minOccurs="0" name="companions" type="tns:AdUnitSize">
    <annotation>
    <documentation> The companions for this ad unit size. Companions are only valid if the environment is {@link EnvironmentType#VIDEO_PLAYER}. If the environment is {@link EnvironmentType#BROWSER} including companions results in an error. </documentation>
    </annotation>
    </element>
    <element maxOccurs="1" minOccurs="0" name="fullDisplayString" type="xsd:string">
    <annotation>
    <documentation> The full (including companion sizes, if applicable) display string of the size, e.g. {@code "300x250"} or {@code "300x250v (180x150)"} </documentation>
    </annotation>
    </element>
    <element maxOccurs="1" minOccurs="0" name="isAudio" type="xsd:boolean">
    <annotation>
    <documentation> Whether the inventory size is audio. If set to true, {@code Size} will be set to {@code "1x1"} and {@code EnvironmentType} will be set to {@link EnvironmentType#VIDEO_PLAYER} regardless of user input. </documentation>
    </annotation>
    </element>
    </sequence>
    </complexType>
    """
    size: Optional[Size] = Field(None, description="The permissible creative size that can be served inside this ad unit.")
    environmentType: Optional[EnvironmentType] = Field(None, description="The environment type of the ad unit size. The default value is EnvironmentType.BROWSER.")
    companions: Optional[List[AdUnitSize]] = Field(None, description="The companions for this ad unit size. Companions are only valid if the environment is EnvironmentType.VIDEO_PLAYER. If the environment is EnvironmentType.BROWSER including companions results in an error.")
    fullDisplayString: Optional[str] = Field(None, description="The full (including companion sizes, if applicable) display string of the size, e.g. 300x250 or 300x250v (180x150)")
    isAudio: Optional[bool] = Field(None, description="Whether the inventory size is audio. If set to true, Size will be set to 1x1 and EnvironmentType will be set to EnvironmentType.VIDEO_PLAYER regardless of user input.")


class AdUnit(GAMSOAPBaseModel):
    """
    <complexType name="AdUnit">
    <annotation>
    <documentation> An {@code AdUnit} represents a chunk of identified inventory for the publisher. It contains all the settings that need to be associated with inventory in order to serve ads to it. An {@code AdUnit} can also be the parent of other ad units in the inventory hierarchy. </documentation>
    </annotation>
    <sequence>
    <element maxOccurs="1" minOccurs="0" name="id" type="xsd:string">
    <annotation>
    <documentation> Uniquely identifies the {@code AdUnit}. This value is read-only and is assigned by Google when an ad unit is created. This attribute is required for updates. </documentation>
    </annotation>
    </element>
    <element maxOccurs="1" minOccurs="0" name="parentId" type="xsd:string">
    <annotation>
    <documentation> The ID of the ad unit's parent. Every ad unit has a parent except for the root ad unit, which is created by Google. This attribute is required when creating the ad unit. Once the ad unit is created this value will be read-only. </documentation>
    </annotation>
    </element>
    <element maxOccurs="1" minOccurs="0" name="hasChildren" type="xsd:boolean">
    <annotation>
    <documentation> This field is set to {@code true} if the ad unit has any children. This attribute is read-only and is populated by Google. </documentation>
    </annotation>
    </element>
    <element maxOccurs="unbounded" minOccurs="0" name="parentPath" type="tns:AdUnitParent">
    <annotation>
    <documentation> The path to this ad unit in the ad unit hierarchy represented as a list from the root to this ad unit's parent. For root ad units, this list is empty. This attribute is read-only and is populated by Google. </documentation>
    </annotation>
    </element>
    <element maxOccurs="1" minOccurs="0" name="name" type="xsd:string">
    <annotation>
    <documentation> The name of the ad unit. This attribute is required and its maximum length is 255 characters. This attribute must also be case-insensitive unique. </documentation>
    </annotation>
    </element>
    <element maxOccurs="1" minOccurs="0" name="description" type="xsd:string">
    <annotation>
    <documentation> A description of the ad unit. This value is optional and its maximum length is 65,535 characters. </documentation>
    </annotation>
    </element>
    <element maxOccurs="1" minOccurs="0" name="targetWindow" type="tns:AdUnit.TargetWindow">
    <annotation>
    <documentation> The value to use for the HTML link's {@code target} attribute. This value is optional and will be interpreted as {@link TargetWindow#TOP} if left blank. </documentation>
    </annotation>
    </element>
    <element maxOccurs="1" minOccurs="0" name="status" type="tns:InventoryStatus">
    <annotation>
    <documentation> The status of this ad unit. It defaults to {@link InventoryStatus#ACTIVE}. This value cannot be updated directly using {@link InventoryService#updateAdUnit}. It can only be modified by performing actions via {@link InventoryService#performAdUnitAction}. </documentation>
    </annotation>
    </element>
    <element maxOccurs="1" minOccurs="0" name="adUnitCode" type="xsd:string">
    <annotation>
    <documentation> A string used to uniquely identify the ad unit for the purposes of serving the ad. This attribute is optional and can be set during ad unit creation. If it is not provided, it will be assigned by Google based off of the inventory unit ID. Once an ad unit is created, its {@code adUnitCode} cannot be changed. </documentation>
    </annotation>
    </element>
    <element maxOccurs="unbounded" minOccurs="0" name="adUnitSizes" type="tns:AdUnitSize">
    <annotation>
    <documentation> The permissible creative sizes that can be served inside this ad unit. This attribute is optional. This attribute replaces the {@code sizes} attribute. </documentation>
    </annotation>
    </element>
    <element maxOccurs="1" minOccurs="0" name="isInterstitial" type="xsd:boolean">
    <annotation>
    <documentation> Whether this is an interstitial ad unit. </documentation>
    </annotation>
    </element>
    <element maxOccurs="1" minOccurs="0" name="isNative" type="xsd:boolean">
    <annotation>
    <documentation> Whether this is a native ad unit. </documentation>
    </annotation>
    </element>
    <element maxOccurs="1" minOccurs="0" name="isFluid" type="xsd:boolean">
    <annotation>
    <documentation> Whether this is a fluid ad unit. </documentation>
    </annotation>
    </element>
    <element maxOccurs="1" minOccurs="0" name="explicitlyTargeted" type="xsd:boolean">
    <annotation>
    <documentation> If this field is set to {@code true}, then the {@code AdUnit} will not be implicitly targeted when its parent is. Traffickers must explicitly target such an ad unit or else no line items will serve to it. This feature is only available for Ad Manager 360 accounts. </documentation>
    </annotation>
    </element>
    <element maxOccurs="1" minOccurs="0" name="adSenseSettings" type="tns:AdSenseSettings">
    <annotation>
    <documentation> AdSense specific settings. To overwrite this, set the {@link #adSenseSettingsSource} to {@link PropertySourceType#DIRECTLY_SPECIFIED} when setting the value of this field. </documentation>
    </annotation>
    </element>
    <element maxOccurs="1" minOccurs="0" name="adSenseSettingsSource" type="tns:ValueSourceType">
    <annotation>
    <documentation> Specifies the source of {@link #adSenseSettings} value. To revert an overridden value to its default, set this field to {@link PropertySourceType#PARENT}. </documentation>
    </annotation>
    </element>
    <element maxOccurs="unbounded" minOccurs="0" name="appliedLabelFrequencyCaps" type="tns:LabelFrequencyCap">
    <annotation>
    <documentation> The set of label frequency caps applied directly to this ad unit. There is a limit of 10 label frequency caps per ad unit. </documentation>
    </annotation>
    </element>
    <element maxOccurs="unbounded" minOccurs="0" name="effectiveLabelFrequencyCaps" type="tns:LabelFrequencyCap">
    <annotation>
    <documentation> Contains the set of labels applied directly to the ad unit as well as those inherited from parent ad units. This field is readonly and is assigned by Google. </documentation>
    </annotation>
    </element>
    <element maxOccurs="unbounded" minOccurs="0" name="appliedLabels" type="tns:AppliedLabel">
    <annotation>
    <documentation> The set of labels applied directly to this ad unit. </documentation>
    </annotation>
    </element>
    <element maxOccurs="unbounded" minOccurs="0" name="effectiveAppliedLabels" type="tns:AppliedLabel">
    <annotation>
    <documentation> Contains the set of labels applied directly to the ad unit as well as those inherited from the parent ad units. If a label has been negated, only the negated label is returned. This field is readonly and is assigned by Google. </documentation>
    </annotation>
    </element>
    <element maxOccurs="unbounded" minOccurs="0" name="effectiveTeamIds" type="xsd:long">
    <annotation>
    <documentation> The IDs of all teams that this ad unit is on as well as those inherited from parent ad units. This value is read-only and is set by Google. </documentation>
    </annotation>
    </element>
    <element maxOccurs="unbounded" minOccurs="0" name="appliedTeamIds" type="xsd:long">
    <annotation>
    <documentation> The IDs of all teams that this ad unit is on directly. </documentation>
    </annotation>
    </element>
    <element maxOccurs="1" minOccurs="0" name="lastModifiedDateTime" type="tns:DateTime">
    <annotation>
    <documentation> The date and time this ad unit was last modified. </documentation>
    </annotation>
    </element>
    <element maxOccurs="1" minOccurs="0" name="smartSizeMode" type="tns:SmartSizeMode">
    <annotation>
    <documentation> The smart size mode for this ad unit. This attribute is optional and defaults to {@link SmartSizeMode#NONE} for fixed sizes. </documentation>
    </annotation>
    </element>
    <element maxOccurs="1" minOccurs="0" name="refreshRate" type="xsd:int">
    <annotation>
    <documentation> The interval in seconds which ad units in mobile apps automatically refresh. Valid values are between 30 and 120 seconds. This attribute is optional and only applies to ad units in mobile apps. If this value is not set, then the mobile app ad will not refresh. </documentation>
    </annotation>
    </element>
    <element maxOccurs="1" minOccurs="0" name="externalSetTopBoxChannelId" type="xsd:string">
    <annotation>
    <documentation> Specifies an ID for a channel in an external set-top box campaign management system. This attribute is only meaningful if {@link #isSetTopBoxEnabled} is {@code true}. This attribute is read-only. </documentation>
    </annotation>
    </element>
    <element maxOccurs="1" minOccurs="0" name="isSetTopBoxEnabled" type="xsd:boolean">
    <annotation>
    <documentation> Flag that specifies whether this ad unit represents an external set-top box channel. This attribute is read-only. </documentation>
    </annotation>
    </element>
    <element maxOccurs="1" minOccurs="0" name="applicationId" type="xsd:long">
    <annotation>
    <documentation> The {@link MobileApplication#applicationId} for the CTV application that this ad unit is within. This attribute is optional. </documentation>
    </annotation>
    </element>
    </sequence>
    </complexType>
    """

    id: Optional[str] = Field(
        None,
        description="Uniquely identifies the {@code AdUnit}. This value is read-only and is assigned by Google when an ad unit is created. This attribute is required for updates.",
    )
    parentId: Optional[str] = Field(
        None,
        description="The ID of the ad unit's parent. Every ad unit has a parent except for the root ad unit, which is created by Google. This attribute is required when creating the ad unit. Once the ad unit is created this value will be read-only.",
    )
    hasChildren: Optional[bool] = Field(
        None,
        description="This field is set to {@code true} if the ad unit has any children. This attribute is read-only and is populated by Google.",
    )
    parentPath: Optional[List[AdUnitParent]] = Field(
        None,
        description="The path to this ad unit in the ad unit hierarchy represented as a list from the root to this ad unit's parent. For root ad units, this list is empty. This attribute is read-only and is populated by Google.",
    )
    name: Optional[str] = Field(
        None,
        description="The name of the ad unit. This attribute is required and its maximum length is 255 characters. This attribute must also be case-insensitive unique.",
    )
    description: Optional[str] = Field(
        None,
        description="A description of the ad unit. This value is optional and its maximum length is 65,535 characters.",
    )
    targetWindow: Optional[AdUnitTargetWindow] = Field(
        None,
        description="The value to use for the HTML link's {@code target} attribute. This value is optional and will be interpreted as {@link TargetWindow#TOP} if left blank.",
    )
    status: Optional[InventoryStatus] = Field(
        None,
        description="The status of this ad unit. It defaults to {@link InventoryStatus#ACTIVE}. This value cannot be updated directly using {@link InventoryService#updateAdUnit}. It can only be modified by performing actions via {@link InventoryService#performAdUnitAction}.",
    )
    adUnitCode: Optional[str] = Field(
        None,
        description="A string used to uniquely identify the ad unit for the purposes of serving the ad. This attribute is optional and can be set during ad unit creation. If it is not provided, it will be assigned by Google based off of the inventory unit ID. Once an ad unit is created, its {@code adUnitCode} cannot be changed.",
    )
    adUnitSizes: Optional[List[AdUnitSize]] = Field(
        None,
        description="The permissible creative sizes that can be served inside this ad unit. This attribute is optional. This attribute replaces the {@code sizes} attribute.",
    )
    isInterstitial: Optional[bool] = Field(
        None,
        description="Whether this is an interstitial ad unit.",
    )
    isNative: Optional[bool] = Field(
        None,
        description="Whether this is a native ad unit.",
    )
    isFluid: Optional[bool] = Field(
        None,
        description="Whether this is a fluid ad unit.",
    )
    explicitlyTargeted: Optional[bool] = Field(
        None,
        description="If this field is set to {@code true}, then the {@code AdUnit} will not be implicitly targeted when its parent is. Traffickers must explicitly target such an ad unit or else no line items will serve to it. This feature is only available for Ad Manager 360 accounts.",
    )
    adSenseSettings: Optional[Any] = Field(  # TODO: AdSenseSettings
        None,
        description="AdSense specific settings. To overwrite this, set the {@link #adSenseSettingsSource} to {@link PropertySourceType#DIRECTLY_SPECIFIED} when setting the value of this field.",
    )
    adSenseSettingsSource: Optional[ValueSourceType] = Field(
        None,
        description="Specifies the source of {@link #adSenseSettings} value. To revert an overridden value to its default, set this field to {@link PropertySourceType#PARENT}.",
    )
    appliedLabelFrequencyCaps: Optional[List[LabelFrequencyCap]] = Field(
        None,
        description="The set of label frequency caps applied directly to this ad unit. There is a limit of 10 label frequency caps per ad unit.",
    )
    effectiveLabelFrequencyCaps: Optional[List[LabelFrequencyCap]] = Field(
        None,
        description="Contains the set of labels applied directly to the ad unit as well as those inherited from parent ad units. This field is readonly and is assigned by Google.",
    )
    appliedLabels: Optional[List[AppliedLabel]] = Field(
        None,
        description="The set of labels applied directly to this ad unit.",
    )
    effectiveAppliedLabels: Optional[List[AppliedLabel]] = Field(
        None,
        description="Contains the set of labels applied directly to the ad unit as well as those inherited from the parent ad units. If a label has been negated, only the negated label is returned. This field is readonly and is assigned by Google.",
    )
    effectiveTeamIds: Optional[List[int]] = Field(
        None,
        description="The IDs of all teams that this ad unit is on as well as those inherited from parent ad units. This value is read-only and is set by Google.",
    )
    appliedTeamIds: Optional[List[int]] = Field(
        None,
        description="The IDs of all teams that this ad unit is on directly.",
    )
    lastModifiedDateTime: Optional[DateTime] = Field(
        None,
        description="The date and time this ad unit was last modified.",
    )
    smartSizeMode: Optional[SmartSizeMode] = Field(
        None,
        description="The smart size mode for this ad unit. This attribute is optional and defaults to {@link SmartSizeMode#NONE} for fixed sizes.",
    )
    refreshRate: Optional[int] = Field(
        None,
        description="The interval in seconds which ad units in mobile apps automatically refresh. Valid values are between 30 and 120 seconds. This attribute is optional and only applies to ad units in mobile apps. If this value is not set, then the mobile app ad will not refresh.",
    )
    externalSetTopBoxChannelId: Optional[str] = Field(
        None,
        description="Specifies an ID for a channel in an external set-top box campaign management system. This attribute is only meaningful if {@link #isSetTopBoxEnabled} is {@code true}. This attribute is read-only.",
    )
    isSetTopBoxEnabled: Optional[bool] = Field(
        None,
        description="Flag that specifies whether this ad unit represents an external set-top box channel. This attribute is read-only.",
    )
    applicationId: Optional[int] = Field(
        None,
        description="The {@link MobileApplication#applicationId} for the CTV application that this ad unit is within. This attribute is optional.",
    )
