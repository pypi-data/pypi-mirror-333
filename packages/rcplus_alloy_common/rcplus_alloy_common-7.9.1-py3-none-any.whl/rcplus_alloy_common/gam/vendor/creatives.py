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
<complexType abstract="true" name="BaseDynamicAllocationCreative">
<annotation>
<documentation> A base class for dynamic allocation creatives. </documentation>
</annotation>
<complexContent>
<extension base="tns:Creative">
<sequence/>
</extension>
</complexContent>
</complexType>
<complexType abstract="true" name="BaseCreativeTemplateVariableValue">
<annotation>
<documentation> A base class for storing values of the {@link CreativeTemplateVariable}. </documentation>
</annotation>
<sequence>
<element maxOccurs="1" minOccurs="0" name="uniqueName" type="xsd:string">
<annotation>
<documentation> A uniqueName of the {@link CreativeTemplateVariable}. </documentation>
</annotation>
</element>
</sequence>
</complexType>
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
<complexType name="ActivateCreatives">
<annotation>
<documentation> The action used for activating {@link Creative} objects. </documentation>
</annotation>
<complexContent>
<extension base="tns:CreativeAction">
<sequence/>
</extension>
</complexContent>
</complexType>
<complexType name="AdExchangeCreative">
<annotation>
<documentation> An Ad Exchange dynamic allocation creative. </documentation>
</annotation>
<complexContent>
<extension base="tns:HasHtmlSnippetDynamicAllocationCreative">
<sequence>
<element maxOccurs="1" minOccurs="0" name="isNativeEligible" type="xsd:boolean">
<annotation>
<documentation> Whether this creative is eligible for native ad-serving. This value is optional and defaults to {@code false}. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="isInterstitial" type="xsd:boolean">
<annotation>
<documentation> {@code true} if this creative is interstitial. An interstitial creative will not consider an impression served until it is fully rendered in the browser. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="isAllowsAllRequestedSizes" type="xsd:boolean">
<annotation>
<documentation> {@code true} if this creative is eligible for all requested sizes. </documentation>
</annotation>
</element>
</sequence>
</extension>
</complexContent>
</complexType>
<complexType name="AdSenseCreative">
<annotation>
<documentation> An AdSense dynamic allocation creative. </documentation>
</annotation>
<complexContent>
<extension base="tns:HasHtmlSnippetDynamicAllocationCreative">
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
<complexType name="AspectRatioImageCreative">
<annotation>
<documentation> A {@code Creative} intended for mobile platforms that displays an image, whose {@link LineItem#creativePlaceholders size} is defined as an {@link CreativeSizeType#ASPECT_RATIO aspect ratio}, i.e. {@link Size#isAspectRatio}. It can have multiple images whose dimensions conform to that aspect ratio. </documentation>
</annotation>
<complexContent>
<extension base="tns:HasDestinationUrlCreative">
<sequence>
<element maxOccurs="unbounded" minOccurs="0" name="imageAssets" type="tns:CreativeAsset">
<annotation>
<documentation> The images associated with this creative. The ad server will choose one based on the capabilities of the device. Each asset should have a size which is of the same aspect ratio as the {@link Creative#size}. This attribute is required and must have at least one asset. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="altText" type="xsd:string">
<annotation>
<documentation> The text that is served along with the image creative, primarily for accessibility. If no suitable image size is available for the device, this text replaces the image completely. This field is optional and has a maximum length of 500 characters. </documentation>
</annotation>
</element>
<element maxOccurs="unbounded" minOccurs="0" name="thirdPartyImpressionTrackingUrls" type="xsd:string">
<annotation>
<documentation> A list of impression tracking URL to ping when this creative is displayed. This field is optional and each string has a maximum length of 1024 characters. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="overrideSize" type="xsd:boolean">
<annotation>
<documentation> Allows the actual image asset sizes to differ from the creative size. This attribute is optional. </documentation>
</annotation>
</element>
</sequence>
</extension>
</complexContent>
</complexType>
<complexType name="AssetCreativeTemplateVariableValue">
<annotation>
<documentation> Stores values of {@link CreativeTemplateVariable} of {@link VariableType#ASSET}. </documentation>
</annotation>
<complexContent>
<extension base="tns:BaseCreativeTemplateVariableValue">
<sequence>
<element maxOccurs="1" minOccurs="0" name="asset" type="tns:CreativeAsset">
<annotation>
<documentation> The associated asset. This attribute is required when creating a new {@code TemplateCreative}. To view the asset, use {@link CreativeAsset#assetUrl}. </documentation>
</annotation>
</element>
</sequence>
</extension>
</complexContent>
</complexType>
<complexType abstract="true" name="Asset">
<annotation>
<documentation> Base asset properties. </documentation>
</annotation>
<sequence/>
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
<complexType name="AudioCreative">
<annotation>
<documentation> A {@code Creative} that contains Ad Manager hosted audio ads and is served via VAST XML. This creative is read-only. </documentation>
</annotation>
<complexContent>
<extension base="tns:BaseAudioCreative">
<sequence>
<element maxOccurs="1" minOccurs="0" name="audioSourceUrl" type="xsd:string">
<annotation>
<documentation> A URL that points to the source media that will be used for transcoding. </documentation>
</annotation>
</element>
</sequence>
</extension>
</complexContent>
</complexType>
<complexType name="AudioRedirectCreative">
<annotation>
<documentation> A {@code Creative} that contains externally hosted audio ads and is served via VAST XML. </documentation>
</annotation>
<complexContent>
<extension base="tns:BaseAudioCreative">
<sequence>
<element maxOccurs="unbounded" minOccurs="0" name="audioAssets" type="tns:VideoRedirectAsset">
<annotation>
<documentation> The audio creative assets. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="mezzanineFile" type="tns:VideoRedirectAsset">
<annotation>
<documentation> The high quality mezzanine audio asset. </documentation>
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
<complexType abstract="true" name="BaseAudioCreative">
<annotation>
<documentation> A base type for audio creatives. </documentation>
</annotation>
<complexContent>
<extension base="tns:HasDestinationUrlCreative">
<sequence>
<element maxOccurs="1" minOccurs="0" name="duration" type="xsd:int">
<annotation>
<documentation> The expected duration of this creative in milliseconds. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="allowDurationOverride" type="xsd:boolean">
<annotation>
<documentation> Allows the creative duration to differ from the actual asset durations. This attribute is optional. </documentation>
</annotation>
</element>
<element maxOccurs="unbounded" minOccurs="0" name="trackingUrls" type="tns:ConversionEvent_TrackingUrlsMapEntry">
<annotation>
<documentation> A map from {@code ConversionEvent} to a list of URLs that will be pinged when the event happens. This attribute is optional. </documentation>
</annotation>
</element>
<element maxOccurs="unbounded" minOccurs="0" name="companionCreativeIds" type="xsd:long">
<annotation>
<documentation> The IDs of the companion creatives that are associated with this creative. This attribute is optional. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="customParameters" type="xsd:string">
<annotation>
<documentation> A comma separated key=value list of parameters that will be supplied to the creative, written into the VAST {@code AdParameters} node. This attribute is optional. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="adId" type="xsd:string">
<annotation>
<documentation> The ad id associated with the video as defined by the {@code adIdType} registry. This field is required if {@code adIdType} is not {@link AdIdType#NONE}. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="adIdType" type="tns:AdIdType">
<annotation>
<documentation> The registry which the ad id of this creative belongs to. This field is optional and defaults to {@link AdIdType#NONE}. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="skippableAdType" type="tns:SkippableAdType">
<annotation>
<documentation> The type of skippable ad. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="vastPreviewUrl" type="xsd:string">
<annotation>
<documentation> An ad tag URL that will return a preview of the VAST XML response specific to this creative. This attribute is read-only. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="sslScanResult" type="tns:SslScanResult">
<annotation>
<documentation> The SSL compatibility scan result of this creative. <p>This attribute is read-only and determined by Google. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="sslManualOverride" type="tns:SslManualOverride">
<annotation>
<documentation> The manual override for the SSL compatibility of this creative. <p>This attribute is optional and defaults to {@link SslManualOverride#NO_OVERRIDE}. </documentation>
</annotation>
</element>
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
<complexType abstract="true" name="BaseImageCreative">
<annotation>
<documentation> The base type for creatives that display an image. </documentation>
</annotation>
<complexContent>
<extension base="tns:HasDestinationUrlCreative">
<sequence>
<element maxOccurs="1" minOccurs="0" name="overrideSize" type="xsd:boolean">
<annotation>
<documentation> Allows the creative size to differ from the actual image asset size. This attribute is optional. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="primaryImageAsset" type="tns:CreativeAsset">
<annotation>
<documentation> The primary image asset associated with this creative. This attribute is required. </documentation>
</annotation>
</element>
</sequence>
</extension>
</complexContent>
</complexType>
<complexType abstract="true" name="BaseImageRedirectCreative">
<annotation>
<documentation> The base type for creatives that load an image asset from a specified URL. </documentation>
</annotation>
<complexContent>
<extension base="tns:HasDestinationUrlCreative">
<sequence>
<element maxOccurs="1" minOccurs="0" name="imageUrl" type="xsd:string">
<annotation>
<documentation> The URL where the actual asset resides. This attribute is required and has a maximum length of 1024 characters. </documentation>
</annotation>
</element>
</sequence>
</extension>
</complexContent>
</complexType>
<complexType abstract="true" name="BaseRichMediaStudioCreative">
<annotation>
<documentation> A {@code Creative} that is created by a Rich Media Studio. </documentation>
</annotation>
<complexContent>
<extension base="tns:Creative">
<sequence>
<element maxOccurs="1" minOccurs="0" name="studioCreativeId" type="xsd:long">
<annotation>
<documentation> The creative ID as known by Rich Media Studio creative. This attribute is readonly. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="creativeFormat" type="tns:RichMediaStudioCreativeFormat">
<annotation>
<documentation> The creative format of the Rich Media Studio creative. This attribute is readonly. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="artworkType" type="tns:RichMediaStudioCreativeArtworkType">
<annotation>
<documentation> The type of artwork used in this creative. This attribute is readonly. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="totalFileSize" type="xsd:long">
<annotation>
<documentation> The total size of all assets in bytes. This attribute is readonly. </documentation>
</annotation>
</element>
<element maxOccurs="unbounded" minOccurs="0" name="adTagKeys" type="xsd:string">
<annotation>
<documentation> Ad tag keys. This attribute is optional and updatable. </documentation>
</annotation>
</element>
<element maxOccurs="unbounded" minOccurs="0" name="customKeyValues" type="xsd:string">
<annotation>
<documentation> Custom key values. This attribute is optional and updatable. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="surveyUrl" type="xsd:string">
<annotation>
<documentation> The survey URL for this creative. This attribute is optional and updatable. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="allImpressionsUrl" type="xsd:string">
<annotation>
<documentation> The tracking URL to be triggered when an ad starts to play, whether Rich Media or backup content is displayed. Behaves like the {@code /imp} URL that DART used to track impressions. This URL can't exceed 1024 characters and must start with http:// or https://. This attribute is optional and updatable. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="richMediaImpressionsUrl" type="xsd:string">
<annotation>
<documentation> The tracking URL to be triggered when any rich media artwork is displayed in an ad. Behaves like the {@code /imp} URL that DART used to track impressions. This URL can't exceed 1024 characters and must start with http:// or https://. This attribute is optional and updatable. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="backupImageImpressionsUrl" type="xsd:string">
<annotation>
<documentation> The tracking URL to be triggered when the Rich Media backup image is served. This attribute is optional and updatable. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="overrideCss" type="xsd:string">
<annotation>
<documentation> The override CSS. You can put custom CSS code here to repair creative styling; e.g. {@code tr td { background-color:#FBB; }}. This attribute is optional and updatable. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="requiredFlashPluginVersion" type="xsd:string">
<annotation>
<documentation> The Flash plugin version required to view this creative; e.g. {@code Flash 10.2/AS 3}. This attribute is read only. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="duration" type="xsd:int">
<annotation>
<documentation> The duration of the creative in milliseconds. This attribute is optional and updatable. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="billingAttribute" type="tns:RichMediaStudioCreativeBillingAttribute">
<annotation>
<documentation> The billing attribute associated with this creative. This attribute is read only. </documentation>
</annotation>
</element>
<element maxOccurs="unbounded" minOccurs="0" name="richMediaStudioChildAssetProperties" type="tns:RichMediaStudioChildAssetProperty">
<annotation>
<documentation> The list of child assets associated with this creative. This attribute is read only. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="sslScanResult" type="tns:SslScanResult">
<annotation>
<documentation> The SSL compatibility scan result of this creative. <p>This attribute is read-only and determined by Google. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="sslManualOverride" type="tns:SslManualOverride">
<annotation>
<documentation> The manual override for the SSL compatibility of this creative. <p>This attribute is optional and defaults to {@link SslManualOverride#NO_OVERRIDE}. </documentation>
</annotation>
</element>
</sequence>
</extension>
</complexContent>
</complexType>
<complexType abstract="true" name="BaseVideoCreative">
<annotation>
<documentation> A base type for video creatives. </documentation>
</annotation>
<complexContent>
<extension base="tns:HasDestinationUrlCreative">
<sequence>
<element maxOccurs="1" minOccurs="0" name="duration" type="xsd:int">
<annotation>
<documentation> The expected duration of this creative in milliseconds. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="allowDurationOverride" type="xsd:boolean">
<annotation>
<documentation> Allows the creative duration to differ from the actual asset durations. This attribute is optional. </documentation>
</annotation>
</element>
<element maxOccurs="unbounded" minOccurs="0" name="trackingUrls" type="tns:ConversionEvent_TrackingUrlsMapEntry">
<annotation>
<documentation> A map from {@code ConversionEvent} to a list of URLs that will be pinged when the event happens. This attribute is optional. </documentation>
</annotation>
</element>
<element maxOccurs="unbounded" minOccurs="0" name="companionCreativeIds" type="xsd:long">
<annotation>
<documentation> The IDs of the companion creatives that are associated with this creative. This attribute is optional. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="customParameters" type="xsd:string">
<annotation>
<documentation> A comma separated key=value list of parameters that will be supplied to the creative, written into the VAST {@code AdParameters} node. This attribute is optional. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="adId" type="xsd:string">
<annotation>
<documentation> The ad id associated with the video as defined by the {@code adIdType} registry. This field is required if {@code adIdType} is not {@link AdIdType#NONE}. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="adIdType" type="tns:AdIdType">
<annotation>
<documentation> The registry which the ad id of this creative belongs to. This field is optional and defaults to {@link AdIdType#NONE}. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="skippableAdType" type="tns:SkippableAdType">
<annotation>
<documentation> The type of skippable ad. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="vastPreviewUrl" type="xsd:string">
<annotation>
<documentation> An ad tag URL that will return a preview of the VAST XML response specific to this creative. This attribute is read-only. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="sslScanResult" type="tns:SslScanResult">
<annotation>
<documentation> The SSL compatibility scan result of this creative. <p>This attribute is read-only and determined by Google. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="sslManualOverride" type="tns:SslManualOverride">
<annotation>
<documentation> The manual override for the SSL compatibility of this creative. <p>This attribute is optional and defaults to {@link SslManualOverride#NO_OVERRIDE}. </documentation>
</annotation>
</element>
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
<complexType name="ClickTag">
<annotation>
<documentation> Click tags define click-through URLs for each exit on an HTML5 creative. An exit is any area that can be clicked that directs the browser to a landing page. Each click tag defines the click-through URL for a different exit. In Ad Manager, tracking pixels are attached to the click tags if URLs are valid. </documentation>
</annotation>
<sequence>
<element maxOccurs="1" minOccurs="0" name="name" type="xsd:string">
<annotation>
<documentation> Name of the click tag, follows the regex "clickTag\\d*" </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="url" type="xsd:string">
<annotation>
<documentation> URL of the click tag. </documentation>
</annotation>
</element>
</sequence>
</complexType>
<complexType name="ClickTrackingCreative">
<annotation>
<documentation> A creative that is used for tracking clicks on ads that are served directly from the customers' web servers or media servers. NOTE: The size attribute is not used for click tracking creative and it will not be persisted upon save. </documentation>
</annotation>
<complexContent>
<extension base="tns:Creative">
<sequence>
<element maxOccurs="1" minOccurs="0" name="clickTrackingUrl" type="xsd:string">
<annotation>
<documentation> The click tracking URL. This attribute is required. </documentation>
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
<complexType name="ConversionEvent_TrackingUrlsMapEntry">
<annotation>
<documentation> This represents an entry in a map with a key of type ConversionEvent and value of type TrackingUrls. </documentation>
</annotation>
<sequence>
<element maxOccurs="1" minOccurs="0" name="key" type="tns:ConversionEvent"/>
<element maxOccurs="1" minOccurs="0" name="value" type="tns:TrackingUrls"/>
</sequence>
</complexType>
<complexType abstract="true" name="CreativeAction">
<annotation>
<documentation> Represents the actions that can be performed on {@link Creative} objects. </documentation>
</annotation>
<sequence/>
</complexType>
<complexType name="CreativeAsset">
<annotation>
<documentation> A {@code CreativeAsset} is an asset that can be used in creatives. </documentation>
</annotation>
<sequence>
<element maxOccurs="1" minOccurs="0" name="assetId" type="xsd:long">
<annotation>
<documentation> The ID of the asset. This attribute is generated by Google upon creation. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="assetByteArray" type="xsd:base64Binary">
<annotation>
<documentation> The content of the asset as a byte array. This attribute is required when creating the creative that contains this asset if an {@code assetId} is not provided. <p>When updating the content, pass a new byte array, and set {@code assetId} to null. Otherwise, this field can be null. <p>The {@code assetByteArray} will be {@code null} when the creative is retrieved. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="fileName" type="xsd:string">
<annotation>
<documentation> The file name of the asset. This attribute is required when creating a new asset (e.g. when {@link #assetByteArray} is not null). </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="fileSize" type="xsd:long">
<annotation>
<documentation> The file size of the asset in bytes. This attribute is read-only. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="assetUrl" type="xsd:string">
<annotation>
<documentation> A URL where the asset can be previewed at. This field is read-only and set by Google. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="size" type="tns:Size">
<annotation>
<documentation> The size of the asset. Note that this may not always reflect the actual physical size of the asset, but may reflect the expected size. This attribute is read-only and is populated by Google. </documentation>
</annotation>
</element>
<element maxOccurs="unbounded" minOccurs="0" name="clickTags" type="tns:ClickTag">
<annotation>
<documentation> The click tags of the asset. This field is read-only. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="imageDensity" type="tns:ImageDensity">
<annotation>
<documentation> The display density of the image. This is the ratio between a dimension in pixels of the image and the dimension in pixels that it should occupy in device-independent pixels when displayed. This attribute is optional and defaults to ONE_TO_ONE. </documentation>
</annotation>
</element>
</sequence>
</complexType>
<complexType name="CustomCreativeAsset">
<annotation>
<documentation> A {@code CustomCreativeAsset} is an association between a {@link CustomCreative} and an asset. Any assets that are associated with a creative can be inserted into its HTML snippet. </documentation>
</annotation>
<sequence>
<element maxOccurs="1" minOccurs="0" name="macroName" type="xsd:string">
<annotation>
<documentation> The name by which the associated asset will be referenced. For example, if the value is "foo", then the asset can be inserted into an HTML snippet using the macro: "%%FILE:foo%%". </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="asset" type="tns:CreativeAsset">
<annotation>
<documentation> The asset. This attribute is required. To view the asset, use {@link CreativeAsset#assetUrl}. </documentation>
</annotation>
</element>
</sequence>
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
<complexType abstract="true" name="Creative">
<annotation>
<documentation> A {@code Creative} represents the media for the ad being served. <p>Read more about creatives on the <a href="https://support.google.com/admanager/answer/3185155">Ad Manager Help Center</a>. </documentation>
</annotation>
<sequence>
<element maxOccurs="1" minOccurs="0" name="advertiserId" type="xsd:long">
<annotation>
<documentation> The ID of the advertiser that owns the creative. This attribute is required. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="id" type="xsd:long">
<annotation>
<documentation> Uniquely identifies the {@code Creative}. This value is read-only and is assigned by Google when the creative is created. This attribute is required for updates. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="name" type="xsd:string">
<annotation>
<documentation> The name of the creative. This attribute is required and has a maximum length of 255 characters. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="size" type="tns:Size">
<annotation>
<documentation> The {@link Size} of the creative. This attribute is required for creation and then is read-only. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="previewUrl" type="xsd:string">
<annotation>
<documentation> The URL of the creative for previewing the media. This attribute is read-only and is assigned by Google when a creative is created. </documentation>
</annotation>
</element>
<element maxOccurs="unbounded" minOccurs="0" name="policyLabels" type="tns:CreativePolicyViolation">
<annotation>
<documentation> Set of policy labels detected for this creative. This attribute is read-only. </documentation>
</annotation>
</element>
<element maxOccurs="unbounded" minOccurs="0" name="appliedLabels" type="tns:AppliedLabel">
<annotation>
<documentation> The set of labels applied to this creative. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="lastModifiedDateTime" type="tns:DateTime">
<annotation>
<documentation> The date and time this creative was last modified. </documentation>
</annotation>
</element>
<element maxOccurs="unbounded" minOccurs="0" name="customFieldValues" type="tns:BaseCustomFieldValue">
<annotation>
<documentation> The values of the custom fields associated with this creative. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="thirdPartyDataDeclaration" type="tns:ThirdPartyDataDeclaration">
<annotation>
<documentation> The third party companies associated with this creative. <p>This is distinct from any associated companies that Google may detect programmatically. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="adBadgingEnabled" type="xsd:boolean">
<annotation>
<documentation> Whether the creative has ad badging enabled. <p>Defaults to false for {@code CreativeType.VAST_REDIRECT}, {@code CreativeType.THIRD_PARTY}, {@code CreativeType.AUDIO_VAST_REDIRECT}, {@code CreativeType.PROGRAMMATIC}, {@code CreativeType.DFP_MOBILE_CREATIVE}, {@code CreativeType.FLASH_OVERLAY}, {@code CreativeType.GRAPHICAL_INTERSTITIAL}, {@code CreativeType.LEGACY_DFP_CREATIVE}, {@code CreativeType.MOBILE_AD_NETWORK_BACKFILL}, {@code CreativeType.MOBILE_VIDEO_INTERSTITIAL}, {@code CreativeType.SDK_MEDIATION} and {@code CreativeType.STANDARD_FLASH} creative types. <p>. Defaults to true for all other creative types. </documentation>
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
<complexType name="CreativePage">
<annotation>
<documentation> Captures a page of {@link Creative} objects. </documentation>
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
<element maxOccurs="unbounded" minOccurs="0" name="results" type="tns:Creative">
<annotation>
<documentation> The collection of creatives contained within this page. </documentation>
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
<complexType name="CustomCreative">
<annotation>
<documentation> A {@code Creative} that contains an arbitrary HTML snippet and file assets. </documentation>
</annotation>
<complexContent>
<extension base="tns:HasDestinationUrlCreative">
<sequence>
<element maxOccurs="1" minOccurs="0" name="htmlSnippet" type="xsd:string">
<annotation>
<documentation> The HTML snippet that this creative delivers. This attribute is required. </documentation>
</annotation>
</element>
<element maxOccurs="unbounded" minOccurs="0" name="customCreativeAssets" type="tns:CustomCreativeAsset">
<annotation>
<documentation> A list of file assets that are associated with this creative, and can be referenced in the snippet. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="isInterstitial" type="xsd:boolean">
<annotation>
<documentation> {@code true} if this custom creative is interstitial. An interstitial creative will not consider an impression served until it is fully rendered in the browser. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="lockedOrientation" type="tns:LockedOrientation">
<annotation>
<documentation> A locked orientation for this creative to be displayed in. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="sslScanResult" type="tns:SslScanResult">
<annotation>
<documentation> The SSL compatibility scan result of this creative. <p>This attribute is read-only and determined by Google. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="sslManualOverride" type="tns:SslManualOverride">
<annotation>
<documentation> The manual override for the SSL compatibility of this creative. <p>This attribute is optional and defaults to {@link SslManualOverride#NO_OVERRIDE}. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="isSafeFrameCompatible" type="xsd:boolean">
<annotation>
<documentation> Whether the {@link Creative} is compatible for SafeFrame rendering. <p>This attribute is optional and defaults to {@code true}. </documentation>
</annotation>
</element>
<element maxOccurs="unbounded" minOccurs="0" name="thirdPartyImpressionTrackingUrls" type="xsd:string">
<annotation>
<documentation> A list of impression tracking URLs to ping when this creative is displayed. This field is optional. </documentation>
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
<complexType name="DeactivateCreatives">
<annotation>
<documentation> The action used for deactivating {@link Creative} objects. </documentation>
</annotation>
<complexContent>
<extension base="tns:CreativeAction">
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
<complexType abstract="true" name="HasDestinationUrlCreative">
<annotation>
<documentation> A {@code Creative} that has a destination url </documentation>
</annotation>
<complexContent>
<extension base="tns:Creative">
<sequence>
<element maxOccurs="1" minOccurs="0" name="destinationUrl" type="xsd:string">
<annotation>
<documentation> The URL that the user is directed to if they click on the creative. This attribute is required unless the {@link destinationUrlType} is {@link DestinationUrlType#NONE}, and has a maximum length of 1024 characters. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="destinationUrlType" type="tns:DestinationUrlType">
<annotation>
<documentation> The action that should be performed if the user clicks on the creative. This attribute is optional and defaults to {@link DestinationUrlType#CLICK_TO_WEB}. </documentation>
</annotation>
</element>
</sequence>
</extension>
</complexContent>
</complexType>
<complexType abstract="true" name="HasHtmlSnippetDynamicAllocationCreative">
<annotation>
<documentation> Dynamic allocation creative with a backfill code snippet. </documentation>
</annotation>
<complexContent>
<extension base="tns:BaseDynamicAllocationCreative">
<sequence>
<element maxOccurs="1" minOccurs="0" name="codeSnippet" type="xsd:string">
<annotation>
<documentation> The code snippet (ad tag) from Ad Exchange or AdSense to traffic the dynamic allocation creative. Only valid Ad Exchange or AdSense parameters will be considered. Any extraneous HTML or JavaScript will be ignored. </documentation>
</annotation>
</element>
</sequence>
</extension>
</complexContent>
</complexType>
<complexType name="Html5Creative">
<annotation>
<documentation> A {@code Creative} that contains a zipped HTML5 bundle asset, a list of third party impression trackers, and a third party click tracker. </documentation>
</annotation>
<complexContent>
<extension base="tns:Creative">
<sequence>
<element maxOccurs="1" minOccurs="0" name="overrideSize" type="xsd:boolean">
<annotation>
<documentation> Allows the creative size to differ from the actual HTML5 asset size. This attribute is optional. </documentation>
</annotation>
</element>
<element maxOccurs="unbounded" minOccurs="0" name="thirdPartyImpressionTrackingUrls" type="xsd:string">
<annotation>
<documentation> Impression tracking URLs to ping when this creative is displayed. This field is optional. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="thirdPartyClickTrackingUrl" type="xsd:string">
<annotation>
<documentation> A click tracking URL to ping when this creative is clicked. This field is optional. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="lockedOrientation" type="tns:LockedOrientation">
<annotation>
<documentation> A locked orientation for this creative to be displayed in. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="sslScanResult" type="tns:SslScanResult">
<annotation>
<documentation> The SSL compatibility scan result of this creative. <p>This attribute is read-only and determined by Google. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="sslManualOverride" type="tns:SslManualOverride">
<annotation>
<documentation> The manual override for the SSL compatibility of this creative. <p>This attribute is optional and defaults to {@link SslManualOverride#NO_OVERRIDE}. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="isSafeFrameCompatible" type="xsd:boolean">
<annotation>
<documentation> Whether the {@link Creative} is compatible for SafeFrame rendering. <p>This attribute is optional and defaults to {@code true}. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="html5Asset" type="tns:CreativeAsset">
<annotation>
<documentation> The HTML5 asset. To preview the HTML5 asset, use the {@link CreativeAsset#assetUrl}. In this field, the {@link CreativeAsset#assetByteArray} must be a zip bundle and the {@link CreativeAsset#fileName} must have a zip extension. This attribute is required. </documentation>
</annotation>
</element>
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
<complexType name="ImageCreative">
<annotation>
<documentation> A {@code Creative} that displays an image. </documentation>
</annotation>
<complexContent>
<extension base="tns:BaseImageCreative">
<sequence>
<element maxOccurs="1" minOccurs="0" name="altText" type="xsd:string">
<annotation>
<documentation> Alternative text to be rendered along with the creative used mainly for accessibility. This field is optional and has a maximum length of 500 characters. </documentation>
</annotation>
</element>
<element maxOccurs="unbounded" minOccurs="0" name="thirdPartyImpressionTrackingUrls" type="xsd:string">
<annotation>
<documentation> A list of impression tracking URL to ping when this creative is displayed. This field is optional and each string has a maximum length of 1024 characters. </documentation>
</annotation>
</element>
<element maxOccurs="unbounded" minOccurs="0" name="secondaryImageAssets" type="tns:CreativeAsset">
<annotation>
<documentation> The list of secondary image assets associated with this creative. This attribute is optional. <p>Secondary image assets can be used to store different resolution versions of the primary asset for use on non-standard density screens. </documentation>
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
<complexType name="ImageOverlayCreative">
<annotation>
<documentation> An overlay {@code Creative} that displays an image and is served via VAST 2.0 XML. Overlays cover part of the video content they are displayed on top of. This creative is read only prior to v201705. </documentation>
</annotation>
<complexContent>
<extension base="tns:BaseImageCreative">
<sequence>
<element maxOccurs="unbounded" minOccurs="0" name="companionCreativeIds" type="xsd:long">
<annotation>
<documentation> The IDs of the companion creatives that are associated with this creative. This attribute is optional. This attribute is read-only. </documentation>
</annotation>
</element>
<element maxOccurs="unbounded" minOccurs="0" name="trackingUrls" type="tns:ConversionEvent_TrackingUrlsMapEntry">
<annotation>
<documentation> A map from {@code ConversionEvent} to a list of URLs that will be pinged when the event happens. This attribute is optional. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="lockedOrientation" type="tns:LockedOrientation">
<annotation>
<documentation> A locked orientation for this creative to be displayed in. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="customParameters" type="xsd:string">
<annotation>
<documentation> A comma separated key=value list of parameters that will be supplied to the creative, written into the VAST {@code AdParameters} node. This attribute is optional. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="duration" type="xsd:int">
<annotation>
<documentation> Minimum suggested duration in milliseconds. This attribute is optional. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="vastPreviewUrl" type="xsd:string">
<annotation>
<documentation> An ad tag URL that will return a preview of the VAST XML response specific to this creative. This attribute is read-only. </documentation>
</annotation>
</element>
</sequence>
</extension>
</complexContent>
</complexType>
<complexType name="ImageRedirectCreative">
<annotation>
<documentation> A {@code Creative} that loads an image asset from a specified URL. </documentation>
</annotation>
<complexContent>
<extension base="tns:BaseImageRedirectCreative">
<sequence>
<element maxOccurs="1" minOccurs="0" name="altText" type="xsd:string">
<annotation>
<documentation> Alternative text to be rendered along with the creative used mainly for accessibility. This field is optional and has a maximum length of 500 characters. </documentation>
</annotation>
</element>
<element maxOccurs="unbounded" minOccurs="0" name="thirdPartyImpressionTrackingUrls" type="xsd:string">
<annotation>
<documentation> A list of impression tracking URL to ping when this creative is displayed. This field is optional and each string has a maximum length of 1024 characters. </documentation>
</annotation>
</element>
</sequence>
</extension>
</complexContent>
</complexType>
<complexType name="ImageRedirectOverlayCreative">
<annotation>
<documentation> An overlay {@code Creative} that loads an image asset from a specified URL and is served via VAST XML. Overlays cover part of the video content they are displayed on top of. This creative is read only. </documentation>
</annotation>
<complexContent>
<extension base="tns:BaseImageRedirectCreative">
<sequence>
<element maxOccurs="1" minOccurs="0" name="assetSize" type="tns:Size">
<annotation>
<documentation> The size of the image asset. Note that this may differ from {@link #size} if the asset is not expected to fill the entire video player. This attribute is optional. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="duration" type="xsd:int">
<annotation>
<documentation> Minimum suggested duration in milliseconds. This attribute is optional. </documentation>
</annotation>
</element>
<element maxOccurs="unbounded" minOccurs="0" name="companionCreativeIds" type="xsd:long">
<annotation>
<documentation> The IDs of the companion creatives that are associated with this creative. This attribute is optional. </documentation>
</annotation>
</element>
<element maxOccurs="unbounded" minOccurs="0" name="trackingUrls" type="tns:ConversionEvent_TrackingUrlsMapEntry">
<annotation>
<documentation> A map from {@code ConversionEvent} to a list of URLs that will be pinged when the event happens. This attribute is optional. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="customParameters" type="xsd:string">
<annotation>
<documentation> A comma separated key=value list of parameters that will be supplied to the creative, written into the VAST {@code AdParameters} node. This attribute is optional. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="vastPreviewUrl" type="xsd:string">
<annotation>
<documentation> An ad tag URL that will return a preview of the VAST XML response specific to this creative. This attribute is read-only. </documentation>
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
<complexType name="InternalRedirectCreative">
<annotation>
<documentation> A {@code Creative} hosted by Campaign Manager 360. <p>Similar to third-party creatives, a Campaign Manager 360 tag is used to retrieve a creative asset. However, Campaign Manager 360 tags are not sent to the user's browser. Instead, they are processed internally within the Google Marketing Platform system.. </documentation>
</annotation>
<complexContent>
<extension base="tns:Creative">
<sequence>
<element maxOccurs="1" minOccurs="0" name="lockedOrientation" type="tns:LockedOrientation">
<annotation>
<documentation> A locked orientation for this creative to be displayed in. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="assetSize" type="tns:Size">
<annotation>
<documentation> The asset size of an internal redirect creative. Note that this may differ from {@code size} if users set {@code overrideSize} to true. This attribute is read-only and is populated by Google. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="internalRedirectUrl" type="xsd:string">
<annotation>
<documentation> The internal redirect URL of the DFA or DART for Publishers hosted creative. This attribute is required and has a maximum length of 1024 characters. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="overrideSize" type="xsd:boolean">
<annotation>
<documentation> Allows the creative size to differ from the actual size specified in the internal redirect's url. This attribute is optional. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="isInterstitial" type="xsd:boolean">
<annotation>
<documentation> {@code true} if this internal redirect creative is interstitial. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="sslScanResult" type="tns:SslScanResult">
<annotation>
<documentation> The SSL compatibility scan result for this creative. <p>This attribute is read-only and determined by Google. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="sslManualOverride" type="tns:SslManualOverride">
<annotation>
<documentation> The manual override for the SSL compatibility of this creative. <p>This attribute is optional and defaults to {@link SslManualOverride#NO_OVERRIDE}. </documentation>
</annotation>
</element>
<element maxOccurs="unbounded" minOccurs="0" name="thirdPartyImpressionTrackingUrls" type="xsd:string">
<annotation>
<documentation> A list of impression tracking URLs to ping when this creative is displayed. This field is optional. </documentation>
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
<complexType name="LegacyDfpCreative">
<annotation>
<documentation> A {@code Creative} that isn't supported by Google DFP, but was migrated from DART. Creatives of this type cannot be created or modified. </documentation>
</annotation>
<complexContent>
<extension base="tns:Creative">
<sequence/>
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
<complexType name="LongCreativeTemplateVariableValue">
<annotation>
<documentation> Stores values of {@link CreativeTemplateVariable} of {@link VariableType#LONG}. </documentation>
</annotation>
<complexContent>
<extension base="tns:BaseCreativeTemplateVariableValue">
<sequence>
<element maxOccurs="1" minOccurs="0" name="value" type="xsd:long">
<annotation>
<documentation> The long value of {@link CreativeTemplateVariable} </documentation>
</annotation>
</element>
</sequence>
</extension>
</complexContent>
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
<complexType name="ProgrammaticCreative">
<annotation>
<documentation> A {@code Creative} used for programmatic trafficking. This creative will be auto-created with the right approval from the buyer. This creative cannot be created through the API. This creative can be updated. </documentation>
</annotation>
<complexContent>
<extension base="tns:Creative">
<sequence/>
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
<complexType abstract="true" name="RedirectAsset">
<annotation>
<documentation> An externally hosted asset. </documentation>
</annotation>
<complexContent>
<extension base="tns:Asset">
<sequence>
<element maxOccurs="1" minOccurs="0" name="redirectUrl" type="xsd:string">
<annotation>
<documentation> The URL where the asset is hosted. </documentation>
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
<complexType name="RichMediaStudioChildAssetProperty">
<annotation>
<documentation> Represents a child asset in {@code RichMediaStudioCreative}. </documentation>
</annotation>
<sequence>
<element maxOccurs="1" minOccurs="0" name="name" type="xsd:string">
<annotation>
<documentation> The name of the asset as known by Rich Media Studio. This attribute is readonly. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="type" type="tns:RichMediaStudioChildAssetProperty.Type">
<annotation>
<documentation> Required file type of the asset. This attribute is readonly. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="totalFileSize" type="xsd:long">
<annotation>
<documentation> The total size of the asset in bytes. This attribute is readonly. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="width" type="xsd:int">
<annotation>
<documentation> Width of the widget in pixels. This attribute is readonly. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="height" type="xsd:int">
<annotation>
<documentation> Height of the widget in pixels. This attribute is readonly. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="url" type="xsd:string">
<annotation>
<documentation> The URL of the asset. This attribute is readonly. </documentation>
</annotation>
</element>
</sequence>
</complexType>
<complexType name="RichMediaStudioCreative">
<annotation>
<documentation> A {@code Creative} that is created by a Rich Media Studio. You cannot create this creative, but you can update some fields of this creative. </documentation>
</annotation>
<complexContent>
<extension base="tns:BaseRichMediaStudioCreative">
<sequence>
<element maxOccurs="1" minOccurs="0" name="lockedOrientation" type="tns:LockedOrientation">
<annotation>
<documentation> A locked orientation for this creative to be displayed in. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="isInterstitial" type="xsd:boolean">
<annotation>
<documentation> {@code true} if this is interstitial. An interstitial creative will not consider an impression served until it is fully rendered in the browser. This attribute is readonly. </documentation>
</annotation>
</element>
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
<complexType name="SetTopBoxCreative">
<annotation>
<documentation> A {@code Creative} that will be served into cable set-top boxes. There are no assets for this creative type, as they are hosted by external cable systems. </documentation>
</annotation>
<complexContent>
<extension base="tns:BaseVideoCreative">
<sequence>
<element maxOccurs="1" minOccurs="0" name="externalAssetId" type="xsd:string">
<annotation>
<documentation> An external asset identifier that is used in the cable system. This attribute is read-only after creation. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="providerId" type="xsd:string">
<annotation>
<documentation> An identifier for the provider in the cable system. This attribute is read-only after creation. </documentation>
</annotation>
</element>
<element maxOccurs="unbounded" minOccurs="0" name="availabilityRegionIds" type="xsd:string">
<annotation>
<documentation> IDs of regions where the creative is available to serve from a local cable video-on-demand server. This attribute is optional. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="licenseWindowStartDateTime" type="tns:DateTime">
<annotation>
<documentation> The date and time that this creative can begin serving from a local cable video-on-demand server. This attribute is optional. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="licenseWindowEndDateTime" type="tns:DateTime">
<annotation>
<documentation> The date and time that this creative can no longer be served from a local cable video-on-demand server. This attribute is optional. </documentation>
</annotation>
</element>
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
<complexType name="StringCreativeTemplateVariableValue">
<annotation>
<documentation> Stores values of {@link CreativeTemplateVariable} of {@link VariableType#STRING} and {@link VariableType#LIST}. </documentation>
</annotation>
<complexContent>
<extension base="tns:BaseCreativeTemplateVariableValue">
<sequence>
<element maxOccurs="1" minOccurs="0" name="value" type="xsd:string">
<annotation>
<documentation> The string value of {@link CreativeTemplateVariable} </documentation>
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
<complexType name="TemplateCreative">
<annotation>
<documentation> A {@code Creative} that is created by the specified creative template. </documentation>
</annotation>
<complexContent>
<extension base="tns:Creative">
<sequence>
<element maxOccurs="1" minOccurs="0" name="creativeTemplateId" type="xsd:long">
<annotation>
<documentation> Creative template ID that this creative is created from. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="isInterstitial" type="xsd:boolean">
<annotation>
<documentation> {@code true} if this template instantiated creative is interstitial. This attribute is read-only and is assigned by Google based on the creative template. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="isNativeEligible" type="xsd:boolean">
<annotation>
<documentation> {@code true} if this template instantiated creative is eligible for native adserving. This attribute is read-only and is assigned by Google based on the creative template. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="isSafeFrameCompatible" type="xsd:boolean">
<annotation>
<documentation> Whether the {@link Creative} is compatible for SafeFrame rendering. <p>This attribute is read-only and is assigned by Google based on the {@link CreativeTemplate}. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="destinationUrl" type="xsd:string">
<annotation>
<documentation> The URL the user is directed to if they click on the creative. This attribute is only required if the template snippet contains the {@code %u} or {@code %%DEST_URL%%} macro. It has a maximum length of 1024 characters. </documentation>
</annotation>
</element>
<element maxOccurs="unbounded" minOccurs="0" name="creativeTemplateVariableValues" type="tns:BaseCreativeTemplateVariableValue">
<annotation>
<documentation> Stores values of {@link CreativeTemplateVariable} in the {@link CreativeTemplate}. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="sslScanResult" type="tns:SslScanResult">
<annotation>
<documentation> The SSL compatibility scan result for this creative. <p>This attribute is read-only and determined by Google. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="sslManualOverride" type="tns:SslManualOverride">
<annotation>
<documentation> The manual override for the SSL compatibility of this creative. <p>This attribute is optional and defaults to {@link SslManualOverride#NO_OVERRIDE}. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="lockedOrientation" type="tns:LockedOrientation">
<annotation>
<documentation> A locked orientation for this creative to be displayed in. </documentation>
</annotation>
</element>
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
<complexType name="ThirdPartyCreative">
<annotation>
<documentation> A {@code Creative} that is served by a 3rd-party vendor. </documentation>
</annotation>
<complexContent>
<extension base="tns:Creative">
<sequence>
<element maxOccurs="1" minOccurs="0" name="snippet" type="xsd:string">
<annotation>
<documentation> The HTML snippet that this creative delivers. This attribute is required. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="expandedSnippet" type="xsd:string">
<annotation>
<documentation> The HTML snippet that this creative delivers with macros expanded. This attribute is read-only and is set by Google. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="sslScanResult" type="tns:SslScanResult">
<annotation>
<documentation> The SSL compatibility scan result for this creative. <p>This attribute is read-only and determined by Google. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="sslManualOverride" type="tns:SslManualOverride">
<annotation>
<documentation> The manual override for the SSL compatibility of this creative. <p>This attribute is optional and defaults to {@link SslManualOverride#NO_OVERRIDE}. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="lockedOrientation" type="tns:LockedOrientation">
<annotation>
<documentation> A locked orientation for this creative to be displayed in. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="isSafeFrameCompatible" type="xsd:boolean">
<annotation>
<documentation> Whether the {@link Creative} is compatible for SafeFrame rendering. <p>This attribute is optional and defaults to {@code true}. </documentation>
</annotation>
</element>
<element maxOccurs="unbounded" minOccurs="0" name="thirdPartyImpressionTrackingUrls" type="xsd:string">
<annotation>
<documentation> A list of impression tracking URLs to ping when this creative is displayed. This field is optional. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="ampRedirectUrl" type="xsd:string">
<annotation>
<documentation> The URL of the AMP creative. </documentation>
</annotation>
</element>
</sequence>
</extension>
</complexContent>
</complexType>
<complexType name="ThirdPartyDataDeclaration">
<annotation>
<documentation> Represents a set of declarations about what (if any) third party companies are associated with a given creative. <p>This can be set at the network level, as a default for all creatives, or overridden for a particular creative. </documentation>
</annotation>
<sequence>
<element maxOccurs="1" minOccurs="0" name="declarationType" type="tns:DeclarationType"/>
<element maxOccurs="unbounded" minOccurs="0" name="thirdPartyCompanyIds" type="xsd:long"/>
</sequence>
</complexType>
<complexType name="TrackingUrls">
<annotation>
<documentation> A list of URLs that should be pinged for a conversion event. </documentation>
</annotation>
<sequence>
<element maxOccurs="unbounded" minOccurs="0" name="urls" type="xsd:string">
<annotation>
<documentation> A list of all URLs that should be pinged. </documentation>
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
<complexType name="UnsupportedCreative">
<annotation>
<documentation> A {@code Creative} that isn't supported by this version of the API. This object is readonly and when encountered should be reported on the Ad Manager API forum. </documentation>
</annotation>
<complexContent>
<extension base="tns:Creative">
<sequence>
<element maxOccurs="1" minOccurs="0" name="unsupportedCreativeType" type="xsd:string">
<annotation>
<documentation> The creative type that is unsupported by this API version. </documentation>
</annotation>
</element>
</sequence>
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
<complexType name="UrlCreativeTemplateVariableValue">
<annotation>
<documentation> Stores values of {@link CreativeTemplateVariable} of {@link VariableType#URL}. </documentation>
</annotation>
<complexContent>
<extension base="tns:BaseCreativeTemplateVariableValue">
<sequence>
<element maxOccurs="1" minOccurs="0" name="value" type="xsd:string">
<annotation>
<documentation> The url value of {@link CreativeTemplateVariable} </documentation>
</annotation>
</element>
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
<complexType name="VastRedirectCreative">
<annotation>
<documentation> A {@code Creative} that points to an externally hosted VAST ad and is served via VAST XML as a VAST Wrapper. </documentation>
</annotation>
<complexContent>
<extension base="tns:Creative">
<sequence>
<element maxOccurs="1" minOccurs="0" name="vastXmlUrl" type="xsd:string">
<annotation>
<documentation> The URL where the 3rd party VAST XML is hosted. This attribute is required. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="vastRedirectType" type="tns:VastRedirectType">
<annotation>
<documentation> The type of VAST ad that this redirects to. This attribute is required. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="duration" type="xsd:int">
<annotation>
<documentation> The duration of the VAST ad in milliseconds. This attribute is required. </documentation>
</annotation>
</element>
<element maxOccurs="unbounded" minOccurs="0" name="companionCreativeIds" type="xsd:long">
<annotation>
<documentation> The IDs of the companion creatives that are associated with this creative. This attribute is optional. </documentation>
</annotation>
</element>
<element maxOccurs="unbounded" minOccurs="0" name="trackingUrls" type="tns:ConversionEvent_TrackingUrlsMapEntry">
<annotation>
<documentation> A map from {@code ConversionEvent} to a list of URLs that will be pinged when the event happens. This attribute is optional. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="vastPreviewUrl" type="xsd:string">
<annotation>
<documentation> An ad tag URL that will return a preview of the VAST XML response specific to this creative. This attribute is read-only. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="sslScanResult" type="tns:SslScanResult">
<annotation>
<documentation> The SSL compatibility scan result for this creative. <p>This attribute is read-only and determined by Google. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="sslManualOverride" type="tns:SslManualOverride">
<annotation>
<documentation> The manual override for the SSL compatibility of this creative. <p>This attribute is optional and defaults to {@link SslManualOverride#NO_OVERRIDE}. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="isAudio" type="xsd:boolean">
<annotation>
<documentation> Whether the 3rd party VAST XML points to an audio ad. When true, {@link VastRedirectCreative#size} will always be 1x1. </documentation>
</annotation>
</element>
</sequence>
</extension>
</complexContent>
</complexType>
<complexType name="VideoCreative">
<annotation>
<documentation> A {@code Creative} that contains Ad Manager hosted video ads and is served via VAST XML. </documentation>
</annotation>
<complexContent>
<extension base="tns:BaseVideoCreative">
<sequence>
<element maxOccurs="1" minOccurs="0" name="videoSourceUrl" type="xsd:string">
<annotation>
<documentation> A URL that points to the source media that will be used for transcoding. </documentation>
</annotation>
</element>
</sequence>
</extension>
</complexContent>
</complexType>
<complexType name="VideoMetadata">
<annotation>
<documentation> Metadata for a video asset. </documentation>
</annotation>
<sequence>
<element maxOccurs="1" minOccurs="0" name="scalableType" type="tns:ScalableType">
<annotation>
<documentation> The scalable type of the asset. This attribute is required. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="duration" type="xsd:int">
<annotation>
<documentation> The duration of the asset in milliseconds. This attribute is required. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="bitRate" type="xsd:int">
<annotation>
<documentation> The bit rate of the asset in kbps. If the asset can play at a range of bit rates (such as an Http Live Streaming video), then set the bit rate to zero and populate the minimum and maximum bit rate instead. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="minimumBitRate" type="xsd:int">
<annotation>
<documentation> The minimum bitrate of the video in kbps. Only set this if the asset can play at a range of bit rates. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="maximumBitRate" type="xsd:int">
<annotation>
<documentation> The maximum bitrate of the video in kbps. Only set this if the asset can play at a range of bit rates. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="size" type="tns:Size">
<annotation>
<documentation> The size (width and height) of the asset. This attribute is required. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="mimeType" type="tns:MimeType">
<annotation>
<documentation> The mime type of the asset. This attribute is required. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="deliveryType" type="tns:VideoDeliveryType">
<annotation>
<documentation> The delivery type of the asset. This attribute is required. </documentation>
</annotation>
</element>
<element maxOccurs="unbounded" minOccurs="0" name="codecs" type="xsd:string">
<annotation>
<documentation> The codecs of the asset. This attribute is optional and defaults to an empty list. </documentation>
</annotation>
</element>
</sequence>
</complexType>
<complexType name="VideoRedirectAsset">
<annotation>
<documentation> An externally-hosted video asset. </documentation>
</annotation>
<complexContent>
<extension base="tns:RedirectAsset">
<sequence>
<element maxOccurs="1" minOccurs="0" name="metadata" type="tns:VideoMetadata">
<annotation>
<documentation> Metadata related to the asset. This attribute is required. </documentation>
</annotation>
</element>
</sequence>
</extension>
</complexContent>
</complexType>
<complexType name="VideoRedirectCreative">
<annotation>
<documentation> A {@code Creative} that contains externally hosted video ads and is served via VAST XML. </documentation>
</annotation>
<complexContent>
<extension base="tns:BaseVideoCreative">
<sequence>
<element maxOccurs="unbounded" minOccurs="0" name="videoAssets" type="tns:VideoRedirectAsset">
<annotation>
<documentation> The video creative assets. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="mezzanineFile" type="tns:VideoRedirectAsset">
<annotation>
<documentation> The high quality mezzanine video asset. </documentation>
</annotation>
</element>
</sequence>
</extension>
</complexContent>
</complexType>
<simpleType name="AdIdType">
<annotation>
<documentation> The registry that an ad ID belongs to. </documentation>
</annotation>
<restriction base="xsd:string">
<enumeration value="UNKNOWN">
<annotation>
<documentation> The value returned if the actual value is not exposed by the requested API version. </documentation>
</annotation>
</enumeration>
<enumeration value="AD_ID">
<annotation>
<documentation> The ad ID is registered with ad-id.org. </documentation>
</annotation>
</enumeration>
<enumeration value="CLEARCAST">
<annotation>
<documentation> The ad ID is registered with clearcast.co.uk. </documentation>
</annotation>
</enumeration>
<enumeration value="NONE">
<annotation>
<documentation> The creative does not have an ad ID outside of Ad Manager. </documentation>
</annotation>
</enumeration>
<enumeration value="ARPP">
<annotation>
<documentation> The ad ID is registered with ARPP Pub-ID. </documentation>
</annotation>
</enumeration>
<enumeration value="CUSV">
<annotation>
<documentation> The ad ID is registered with Auditel Spot ID. </documentation>
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
<simpleType name="ConversionEvent">
<annotation>
<documentation> All possible tracking event types. Not all events are supported by every kind of creative. </documentation>
</annotation>
<restriction base="xsd:string">
<enumeration value="UNKNOWN">
<annotation>
<documentation> The value returned if the actual value is not exposed by the requested API version. </documentation>
</annotation>
</enumeration>
<enumeration value="CREATIVE_VIEW">
<annotation>
<documentation> Corresponds to the {@code creativeView} tracking event. </documentation>
</annotation>
</enumeration>
<enumeration value="START">
<annotation>
<documentation> Corresponds to the {@code start} tracking event. </documentation>
</annotation>
</enumeration>
<enumeration value="SKIP_SHOWN">
<annotation>
<documentation> An event that is fired when a video skip button is shown, usually after 5 seconds of viewing the video. This event does not correspond to any VAST element and is implemented using an extension. </documentation>
</annotation>
</enumeration>
<enumeration value="FIRST_QUARTILE">
<annotation>
<documentation> Corresponds to the {@code firstQuartile} tracking event. </documentation>
</annotation>
</enumeration>
<enumeration value="MIDPOINT">
<annotation>
<documentation> Corresponds to the {@code midpoint} tracking event. </documentation>
</annotation>
</enumeration>
<enumeration value="THIRD_QUARTILE">
<annotation>
<documentation> Corresponds to the {@code thirdQuartile} tracking event. </documentation>
</annotation>
</enumeration>
<enumeration value="ENGAGED_VIEW">
<annotation>
<documentation> An event that is fired after 30 seconds of viewing the video or when the video finished (if the video duration is less than 30 seconds). This event does not correspond to any VAST element and is implemented using an extension. </documentation>
</annotation>
</enumeration>
<enumeration value="COMPLETE">
<annotation>
<documentation> Corresponds to the {@code complete} tracking event. </documentation>
</annotation>
</enumeration>
<enumeration value="MUTE">
<annotation>
<documentation> Corresponds to the {@code mute} tracking event. </documentation>
</annotation>
</enumeration>
<enumeration value="UNMUTE">
<annotation>
<documentation> Corresponds to the {@code unmute} tracking event. </documentation>
</annotation>
</enumeration>
<enumeration value="PAUSE">
<annotation>
<documentation> Corresponds to the {@code pause} tracking event. </documentation>
</annotation>
</enumeration>
<enumeration value="REWIND">
<annotation>
<documentation> Corresponds to the {@code rewind} tracking event. </documentation>
</annotation>
</enumeration>
<enumeration value="RESUME">
<annotation>
<documentation> Corresponds to the {@code resume} tracking event. </documentation>
</annotation>
</enumeration>
<enumeration value="SKIPPED">
<annotation>
<documentation> An event that is fired when a video was skipped. This event does not correspond to any VAST element and is implemented using an extension. </documentation>
</annotation>
</enumeration>
<enumeration value="FULLSCREEN">
<annotation>
<documentation> Corresponds to the {@code fullscreen} tracking event. </documentation>
</annotation>
</enumeration>
<enumeration value="EXPAND">
<annotation>
<documentation> Corresponds to the {@code expand} tracking event. </documentation>
</annotation>
</enumeration>
<enumeration value="COLLAPSE">
<annotation>
<documentation> Corresponds to the {@code collapse} tracking event. </documentation>
</annotation>
</enumeration>
<enumeration value="ACCEPT_INVITATION">
<annotation>
<documentation> Corresponds to the {@code acceptInvitation} tracking event. </documentation>
</annotation>
</enumeration>
<enumeration value="CLOSE">
<annotation>
<documentation> Corresponds to the {@code close} tracking event. </documentation>
</annotation>
</enumeration>
<enumeration value="CLICK_TRACKING">
<annotation>
<documentation> Corresponds to the {@code Linear.VideoClicks.ClickTracking} node. </documentation>
</annotation>
</enumeration>
<enumeration value="SURVEY">
<annotation>
<documentation> Corresponds to the {@code InLine.Survey} node. </documentation>
</annotation>
</enumeration>
<enumeration value="CUSTOM_CLICK">
<annotation>
<documentation> Corresponds to the {@code Linear.VideoClicks.CustomClick} node. </documentation>
</annotation>
</enumeration>
<enumeration value="MEASURABLE_IMPRESSION">
<annotation>
<documentation> Corresponds to the {@code measurableImpression} tracking event. </documentation>
</annotation>
</enumeration>
<enumeration value="VIEWABLE_IMPRESSION">
<annotation>
<documentation> Corresponds to the {@code viewableImpression} tracking event. </documentation>
</annotation>
</enumeration>
<enumeration value="VIDEO_ABANDON">
<annotation>
<documentation> Corresponds to the {@code abandon} tracking event. </documentation>
</annotation>
</enumeration>
<enumeration value="FULLY_VIEWABLE_AUDIBLE_HALF_DURATION_IMPRESSION">
<annotation>
<documentation> Corresponds to the {@code fullyViewableAudibleHalfDurationImpression} tracking event. </documentation>
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
<simpleType name="CreativePolicyViolation">
<annotation>
<documentation> Represents the different types of policy violations that may be detected on a given creative. <p>For more information about the various types of policy violations, see <a href="https://support.google.com/adspolicy/answer/6008942">here</a>. </documentation>
</annotation>
<restriction base="xsd:string">
<enumeration value="MALWARE_IN_CREATIVE">
<annotation>
<documentation> Malware was found in the creative. <p>For more information see <a href="https://support.google.com/adspolicy/answer/1308246">here</a>. </documentation>
</annotation>
</enumeration>
<enumeration value="MALWARE_IN_LANDING_PAGE">
<annotation>
<documentation> Malware was found in the landing page. <p>For more information see <a href="https://support.google.com/adspolicy/answer/1308246">here</a>. </documentation>
</annotation>
</enumeration>
<enumeration value="LEGALLY_BLOCKED_REDIRECT_URL">
<annotation>
<documentation> The redirect url contains legally objectionable content. </documentation>
</annotation>
</enumeration>
<enumeration value="MISREPRESENTATION_OF_PRODUCT">
<annotation>
<documentation> The creative misrepresents the product or service being advertised. <p>For more information see <a href="https://support.google.com/adspolicy/answer/6020955">here</a>. </documentation>
</annotation>
</enumeration>
<enumeration value="SELF_CLICKING_CREATIVE">
<annotation>
<documentation> The creative has been determined to be self clicking. </documentation>
</annotation>
</enumeration>
<enumeration value="GAMING_GOOGLE_NETWORK">
<annotation>
<documentation> The creative has been determined as attempting to game the Google network. <p>For more information see <a href="https://support.google.com/adspolicy/answer/6020954#319">here</a>. </documentation>
</annotation>
</enumeration>
<enumeration value="DYNAMIC_DNS">
<annotation>
<documentation> The landing page for the creative uses a dynamic DNS. <p>For more information see <a href="https://support.google.com/adspolicy/answer/6020954">here</a>. </documentation>
</annotation>
</enumeration>
<enumeration value="CIRCUMVENTING_SYSTEMS">
<annotation>
<documentation> The creative has been determined as attempting to circumvent Google advertising systems. </documentation>
</annotation>
</enumeration>
<enumeration value="PHISHING">
<annotation>
<documentation> Phishing found in creative or landing page. <p>For more information see <a href="https://support.google.com/adspolicy/answer/6020955">here</a>. </documentation>
</annotation>
</enumeration>
<enumeration value="DOWNLOAD_PROMPT_IN_CREATIVE">
<annotation>
<documentation> The creative prompts the user to download a file. <p>For more information see <a href="https://support.google.com/admanager/answer/7513391">here</a> </documentation>
</annotation>
</enumeration>
<enumeration value="UNAUTHORIZED_COOKIE_DETECTED">
<annotation>
<documentation> The creative sets an unauthorized cookie on a Google domain. <p>For more information see <a href="https://support.google.com/admanager/answer/7513391">here</a> </documentation>
</annotation>
</enumeration>
<enumeration value="TEMPORARY_PAUSE_FOR_VENDOR_INVESTIGATION">
<annotation>
<documentation> The creative has been temporarily paused while we investigate. </documentation>
</annotation>
</enumeration>
<enumeration value="ABUSIVE_EXPERIENCE">
<annotation>
<documentation> The landing page contains an abusive experience. <p>For more information see <a href="https://support.google.com/webtools/answer/7347327">here</a>. </documentation>
</annotation>
</enumeration>
<enumeration value="TRICK_TO_CLICK">
<annotation>
<documentation> The creative is designed to mislead or trick the user into interacting with it. <p>For more information see <a href="https://support.google.com/adwordspolicy/answer/6020955#357">here</a>. </documentation>
</annotation>
</enumeration>
<enumeration value="USE_OF_NON_ALLOWLISTED_OMID_VERIFICATION_SCRIPT">
<annotation>
<documentation> Non-allowlisted OMID verification script. <p>For more information see <a href="https://support.google.com/authorizedbuyers/answer/9115752">here</a>. </documentation>
</annotation>
</enumeration>
<enumeration value="MISUSE_OF_OMID_API">
<annotation>
<documentation> OMID sdk injected by creative. < p>For more information see <a href="https://support.google.com/authorizedbuyers/answer/9115752">here</a>. </documentation>
</annotation>
</enumeration>
<enumeration value="UNACCEPTABLE_HTML_AD">
<annotation>
<documentation> Unacceptable HTML5 ad. <p>For more information see <a href="https://support.google.com/adspolicy/answer/6088505#266">here</a>. </documentation>
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
<simpleType name="DeclarationType">
<annotation>
<documentation> The declaration about third party data usage on the associated entity. </documentation>
</annotation>
<restriction base="xsd:string">
<enumeration value="NONE">
<annotation>
<documentation> There are no companies associated. Functionally the same as DECLARED, combined with an empty company list. </documentation>
</annotation>
</enumeration>
<enumeration value="DECLARED">
<annotation>
<documentation> There is a set of {@link RichMediaAdsCompany}s associated with this entity. </documentation>
</annotation>
</enumeration>
<enumeration value="UNKNOWN">
<annotation>
<documentation> The value returned if the actual value is not exposed by the requested API version. </documentation>
</annotation>
</enumeration>
</restriction>
</simpleType>
<simpleType name="DestinationUrlType">
<annotation>
<documentation> The valid actions that a destination URL may perform if the user clicks on the ad. </documentation>
</annotation>
<restriction base="xsd:string">
<enumeration value="UNKNOWN">
<annotation>
<documentation> The value returned if the actual value is not exposed by the requested API version. </documentation>
</annotation>
</enumeration>
<enumeration value="CLICK_TO_WEB">
<annotation>
<documentation> Navigate to a web page. (a.k.a. "Click-through URL"). </documentation>
</annotation>
</enumeration>
<enumeration value="CLICK_TO_APP">
<annotation>
<documentation> Start an application. </documentation>
</annotation>
</enumeration>
<enumeration value="CLICK_TO_CALL">
<annotation>
<documentation> Make a phone call. </documentation>
</annotation>
</enumeration>
<enumeration value="NONE">
<annotation>
<documentation> Destination URL not present. Useful for video creatives where a landing page or a product isn't necessarily applicable. </documentation>
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
<simpleType name="ImageDensity">
<annotation>
<documentation> Image densities. </documentation>
</annotation>
<restriction base="xsd:string">
<enumeration value="ONE_TO_ONE">
<annotation>
<documentation> Indicates that there is a 1:1 ratio between the dimensions of the raw image and the dimensions that it should be displayed at in device-independent pixels. </documentation>
</annotation>
</enumeration>
<enumeration value="THREE_TO_TWO">
<annotation>
<documentation> Indicates that there is a 3:2 ratio between the dimensions of the raw image and the dimensions that it should be displayed at in device-independent pixels. </documentation>
</annotation>
</enumeration>
<enumeration value="TWO_TO_ONE">
<annotation>
<documentation> Indicates that there is a 2:1 ratio between the dimensions of the raw image and the dimensions that it should be displayed at in device-independent pixels. </documentation>
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
<simpleType name="LockedOrientation">
<annotation>
<documentation> Describes the orientation that a creative should be served with. </documentation>
</annotation>
<restriction base="xsd:string">
<enumeration value="UNKNOWN">
<annotation>
<documentation> The value returned if the actual value is not exposed by the requested API version. </documentation>
</annotation>
</enumeration>
<enumeration value="FREE_ORIENTATION"/>
<enumeration value="PORTRAIT_ONLY"/>
<enumeration value="LANDSCAPE_ONLY"/>
</restriction>
</simpleType>
<simpleType name="MimeType">
<annotation>
<documentation> Enum of supported mime types </documentation>
</annotation>
<restriction base="xsd:string">
<enumeration value="UNKNOWN">
<annotation>
<documentation> The value returned if the actual value is not exposed by the requested API version. </documentation>
</annotation>
</enumeration>
<enumeration value="ASP">
<annotation>
<documentation> application/x-asp </documentation>
</annotation>
</enumeration>
<enumeration value="AUDIO_AIFF">
<annotation>
<documentation> audio/aiff </documentation>
</annotation>
</enumeration>
<enumeration value="AUDIO_BASIC">
<annotation>
<documentation> audio/basic </documentation>
</annotation>
</enumeration>
<enumeration value="AUDIO_FLAC">
<annotation>
<documentation> audio/flac </documentation>
</annotation>
</enumeration>
<enumeration value="AUDIO_MID">
<annotation>
<documentation> audio/mid </documentation>
</annotation>
</enumeration>
<enumeration value="AUDIO_MP3">
<annotation>
<documentation> audio/mpeg </documentation>
</annotation>
</enumeration>
<enumeration value="AUDIO_MP4">
<annotation>
<documentation> audio/mp4 </documentation>
</annotation>
</enumeration>
<enumeration value="AUDIO_MPEG_URL">
<annotation>
<documentation> audio/x-mpegurl </documentation>
</annotation>
</enumeration>
<enumeration value="AUDIO_MS_WMA">
<annotation>
<documentation> audio/x-ms-wma </documentation>
</annotation>
</enumeration>
<enumeration value="AUDIO_OGG">
<annotation>
<documentation> audio/ogg </documentation>
</annotation>
</enumeration>
<enumeration value="AUDIO_REAL_AUDIO_PLUGIN">
<annotation>
<documentation> audio/x-pn-realaudio-plugin </documentation>
</annotation>
</enumeration>
<enumeration value="AUDIO_WAV">
<annotation>
<documentation> audio/x-wav </documentation>
</annotation>
</enumeration>
<enumeration value="BINARY">
<annotation>
<documentation> application/binary </documentation>
</annotation>
</enumeration>
<enumeration value="DASH">
<annotation>
<documentation> application/dash+xml </documentation>
</annotation>
</enumeration>
<enumeration value="DIRECTOR">
<annotation>
<documentation> application/x-director </documentation>
</annotation>
</enumeration>
<enumeration value="FLASH">
<annotation>
<documentation> application/x-shockwave-flash </documentation>
</annotation>
</enumeration>
<enumeration value="GRAPHIC_CONVERTER">
<annotation>
<documentation> application/graphicconverter </documentation>
</annotation>
</enumeration>
<enumeration value="JAVASCRIPT">
<annotation>
<documentation> application/x-javascript </documentation>
</annotation>
</enumeration>
<enumeration value="JSON">
<annotation>
<documentation> application/json </documentation>
</annotation>
</enumeration>
<enumeration value="IMAGE_BITMAP">
<annotation>
<documentation> image/x-win-bitmap </documentation>
</annotation>
</enumeration>
<enumeration value="IMAGE_BMP">
<annotation>
<documentation> image/bmp </documentation>
</annotation>
</enumeration>
<enumeration value="IMAGE_GIF">
<annotation>
<documentation> image/gif </documentation>
</annotation>
</enumeration>
<enumeration value="IMAGE_JPEG">
<annotation>
<documentation> image/jpeg </documentation>
</annotation>
</enumeration>
<enumeration value="IMAGE_PHOTOSHOP">
<annotation>
<documentation> image/photoshop </documentation>
</annotation>
</enumeration>
<enumeration value="IMAGE_PNG">
<annotation>
<documentation> image/png </documentation>
</annotation>
</enumeration>
<enumeration value="IMAGE_TIFF">
<annotation>
<documentation> image/tiff </documentation>
</annotation>
</enumeration>
<enumeration value="IMAGE_WBMP">
<annotation>
<documentation> image/vnd.wap.wbmp </documentation>
</annotation>
</enumeration>
<enumeration value="M3U8">
<annotation>
<documentation> application/x-mpegURL </documentation>
</annotation>
</enumeration>
<enumeration value="MAC_BIN_HEX_40">
<annotation>
<documentation> application/mac-binhex40 </documentation>
</annotation>
</enumeration>
<enumeration value="MS_EXCEL">
<annotation>
<documentation> application/vnd.ms-excel </documentation>
</annotation>
</enumeration>
<enumeration value="MS_POWERPOINT">
<annotation>
<documentation> application/ms-powerpoint </documentation>
</annotation>
</enumeration>
<enumeration value="MS_WORD">
<annotation>
<documentation> application/msword </documentation>
</annotation>
</enumeration>
<enumeration value="OCTET_STREAM">
<annotation>
<documentation> application/octet-stream </documentation>
</annotation>
</enumeration>
<enumeration value="PDF">
<annotation>
<documentation> application/pdf </documentation>
</annotation>
</enumeration>
<enumeration value="POSTSCRIPT">
<annotation>
<documentation> application/postscript </documentation>
</annotation>
</enumeration>
<enumeration value="RN_REAL_MEDIA">
<annotation>
<documentation> application/vnd.rn-realmedia </documentation>
</annotation>
</enumeration>
<enumeration value="RFC_822">
<annotation>
<documentation> message/rfc822 </documentation>
</annotation>
</enumeration>
<enumeration value="RTF">
<annotation>
<documentation> application/rtf </documentation>
</annotation>
</enumeration>
<enumeration value="TEXT_CALENDAR">
<annotation>
<documentation> text/calendar </documentation>
</annotation>
</enumeration>
<enumeration value="TEXT_CSS">
<annotation>
<documentation> text/css </documentation>
</annotation>
</enumeration>
<enumeration value="TEXT_CSV">
<annotation>
<documentation> text/csv </documentation>
</annotation>
</enumeration>
<enumeration value="TEXT_HTML">
<annotation>
<documentation> text/html </documentation>
</annotation>
</enumeration>
<enumeration value="TEXT_JAVA">
<annotation>
<documentation> text/java </documentation>
</annotation>
</enumeration>
<enumeration value="TEXT_PLAIN">
<annotation>
<documentation> text/plain </documentation>
</annotation>
</enumeration>
<enumeration value="VIDEO_3GPP">
<annotation>
<documentation> video/3gpp </documentation>
</annotation>
</enumeration>
<enumeration value="VIDEO_3GPP2">
<annotation>
<documentation> video/3gpp2 </documentation>
</annotation>
</enumeration>
<enumeration value="VIDEO_AVI">
<annotation>
<documentation> video/avi </documentation>
</annotation>
</enumeration>
<enumeration value="VIDEO_FLV">
<annotation>
<documentation> video/x-flv </documentation>
</annotation>
</enumeration>
<enumeration value="VIDEO_MP4">
<annotation>
<documentation> video/mp4 </documentation>
</annotation>
</enumeration>
<enumeration value="VIDEO_MP4V_ES">
<annotation>
<documentation> video/mp4v-es </documentation>
</annotation>
</enumeration>
<enumeration value="VIDEO_MPEG">
<annotation>
<documentation> video/mpeg </documentation>
</annotation>
</enumeration>
<enumeration value="VIDEO_MS_ASF">
<annotation>
<documentation> video/x-ms-asf </documentation>
</annotation>
</enumeration>
<enumeration value="VIDEO_MS_WM">
<annotation>
<documentation> video/x-ms-wm </documentation>
</annotation>
</enumeration>
<enumeration value="VIDEO_MS_WMV">
<annotation>
<documentation> video/x-ms-wmv </documentation>
</annotation>
</enumeration>
<enumeration value="VIDEO_MS_WVX">
<annotation>
<documentation> video/x-ms-wvx </documentation>
</annotation>
</enumeration>
<enumeration value="VIDEO_OGG">
<annotation>
<documentation> video/ogg </documentation>
</annotation>
</enumeration>
<enumeration value="VIDEO_QUICKTIME">
<annotation>
<documentation> video/x-quicktime </documentation>
</annotation>
</enumeration>
<enumeration value="VIDEO_WEBM">
<annotation>
<documentation> video/webm </documentation>
</annotation>
</enumeration>
<enumeration value="XAML">
<annotation>
<documentation> application/xaml+xml </documentation>
</annotation>
</enumeration>
<enumeration value="XHTML">
<annotation>
<documentation> application/xhtml+xml </documentation>
</annotation>
</enumeration>
<enumeration value="XML">
<annotation>
<documentation> application/xml </documentation>
</annotation>
</enumeration>
<enumeration value="ZIP">
<annotation>
<documentation> application/zip </documentation>
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
<simpleType name="RichMediaStudioChildAssetProperty.Type">
<annotation>
<documentation> Type of {@code RichMediaStudioChildAssetProperty} </documentation>
</annotation>
<restriction base="xsd:string">
<enumeration value="FLASH">
<annotation>
<documentation> SWF files </documentation>
</annotation>
</enumeration>
<enumeration value="VIDEO">
<annotation>
<documentation> FLVS and any other video file types </documentation>
</annotation>
</enumeration>
<enumeration value="IMAGE">
<annotation>
<documentation> Image files </documentation>
</annotation>
</enumeration>
<enumeration value="DATA">
<annotation>
<documentation> The rest of the supported file types .txt, .xml, etc. </documentation>
</annotation>
</enumeration>
</restriction>
</simpleType>
<simpleType name="RichMediaStudioCreativeArtworkType">
<annotation>
<documentation> Rich Media Studio creative artwork types. </documentation>
</annotation>
<restriction base="xsd:string">
<enumeration value="FLASH">
<annotation>
<documentation> The creative is a Flash creative. </documentation>
</annotation>
</enumeration>
<enumeration value="HTML5">
<annotation>
<documentation> The creative is HTML5. </documentation>
</annotation>
</enumeration>
<enumeration value="MIXED">
<annotation>
<documentation> The creative is Flash if available, and HTML5 otherwise. </documentation>
</annotation>
</enumeration>
</restriction>
</simpleType>
<simpleType name="RichMediaStudioCreativeBillingAttribute">
<annotation>
<documentation> Rich Media Studio creative supported billing attributes. <p> This is determined by Rich Media Studio based on the content of the creative and is not updateable. </documentation>
</annotation>
<restriction base="xsd:string">
<enumeration value="IN_PAGE">
<annotation>
<documentation> Applies to any {@link RichMediaStudioCreativeFormat#IN_PAGE}, without Video. </documentation>
</annotation>
</enumeration>
<enumeration value="FLOATING_EXPANDING">
<annotation>
<documentation> Applies to any of these following {@link RichMediaStudioCreativeFormat}, without Video: {@link RichMediaStudioCreativeFormat#EXPANDING}, {@link RichMediaStudioCreativeFormat#IM_EXPANDING}, {@link RichMediaStudioCreativeFormat#FLOATING}, {@link RichMediaStudioCreativeFormat#PEEL_DOWN}, {@link RichMediaStudioCreativeFormat#IN_PAGE_WITH_FLOATING} </documentation>
</annotation>
</enumeration>
<enumeration value="VIDEO">
<annotation>
<documentation> Applies to any creatives that includes a video. </documentation>
</annotation>
</enumeration>
<enumeration value="FLASH_IN_FLASH">
<annotation>
<documentation> Applies to any {@link RichMediaStudioCreativeFormat#FLASH_IN_FLASH}, without Video. </documentation>
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
<simpleType name="RichMediaStudioCreativeFormat">
<annotation>
<documentation> Different creative format supported by Rich Media Studio creative. </documentation>
</annotation>
<restriction base="xsd:string">
<enumeration value="IN_PAGE">
<annotation>
<documentation> In-page creatives are served into an ad slot on publishers page. In-page implies that they maintain a static size, e.g, 468x60 and do not break out of these dimensions. </documentation>
</annotation>
</enumeration>
<enumeration value="EXPANDING">
<annotation>
<documentation> Expanding creatives expand/collapse on user interaction such as mouse over. It consists of an initial, or collapsed and an expanded creative area. </documentation>
</annotation>
</enumeration>
<enumeration value="IM_EXPANDING">
<annotation>
<documentation> Creatives that are served in an instant messenger application such as AOL Instant Messanger or Yahoo! Messenger. This can also be used in desktop applications such as weatherbug. </documentation>
</annotation>
</enumeration>
<enumeration value="FLOATING">
<annotation>
<documentation> Floating creatives float on top of publishers page and can be closed with a close button. </documentation>
</annotation>
</enumeration>
<enumeration value="PEEL_DOWN">
<annotation>
<documentation> Peel-down creatives show a glimpse of your ad in the corner of a web page. When the user interacts, the rest of the ad peels down to reveal the full message. </documentation>
</annotation>
</enumeration>
<enumeration value="IN_PAGE_WITH_FLOATING">
<annotation>
<documentation> An In-Page with Floating creative is a dual-asset creative consisting of an in-page asset and a floating asset. This creative type lets you deliver a static primary ad to a webpage, while inviting a user to find out more through a floating asset delivered when the user interacts with the creative. </documentation>
</annotation>
</enumeration>
<enumeration value="FLASH_IN_FLASH">
<annotation>
<documentation> A Flash ad that renders in a Flash environment. The adserver will serve this using VAST, but it is not a proper VAST XML ad. It's an amalgamation of the proprietary InStream protocol, rendered inside VAST so that we can capture some standard behavior such as companions. </documentation>
</annotation>
</enumeration>
<enumeration value="FLASH_IN_FLASH_EXPANDING">
<annotation>
<documentation> An expanding flash ad that renders in a Flash environment. The adserver will serve this using VAST, but it is not a proper VAST XML ad. It's an amalgamation of the proprietary InStream protocol, rendered inside VAST so that we can capture some standard behavior such as companions. </documentation>
</annotation>
</enumeration>
<enumeration value="IN_APP">
<annotation>
<documentation> In-app creatives are served into an ad slot within a publisher's app. In-app implies that they maintain a static size, e.g, 468x60 and do not break out of these dimensions. </documentation>
</annotation>
</enumeration>
<enumeration value="UNKNOWN">
<annotation>
<documentation> The creative format is unknown or not supported in the API version in use. </documentation>
</annotation>
</enumeration>
</restriction>
</simpleType>
<simpleType name="ScalableType">
<annotation>
<documentation> The different ways a video/flash can scale. </documentation>
</annotation>
<restriction base="xsd:string">
<enumeration value="UNKNOWN">
<annotation>
<documentation> The value returned if the actual value is not exposed by the requested API version. </documentation>
</annotation>
</enumeration>
<enumeration value="NOT_SCALABLE">
<annotation>
<documentation> The creative should not be scaled. </documentation>
</annotation>
</enumeration>
<enumeration value="RATIO_SCALABLE">
<annotation>
<documentation> The creative can be scaled and its aspect-ratio must be maintained. </documentation>
</annotation>
</enumeration>
<enumeration value="STRETCH_SCALABLE">
<annotation>
<documentation> The creative can be scaled and its aspect-ratio can be distorted. </documentation>
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
<simpleType name="SslManualOverride">
<annotation>
<documentation> Enum to store the creative SSL compatibility manual override. Its three states are similar to that of {@link SslScanResult}. </documentation>
</annotation>
<restriction base="xsd:string">
<enumeration value="UNKNOWN">
<annotation>
<documentation> The value returned if the actual value is not exposed by the requested API version. </documentation>
</annotation>
</enumeration>
<enumeration value="NO_OVERRIDE"/>
<enumeration value="SSL_COMPATIBLE"/>
<enumeration value="NOT_SSL_COMPATIBLE"/>
</restriction>
</simpleType>
<simpleType name="SslScanResult">
<annotation>
<documentation> Enum to store the creative SSL compatibility scan result. </documentation>
</annotation>
<restriction base="xsd:string">
<enumeration value="UNKNOWN">
<annotation>
<documentation> The value returned if the actual value is not exposed by the requested API version. </documentation>
</annotation>
</enumeration>
<enumeration value="UNSCANNED"/>
<enumeration value="SCANNED_SSL"/>
<enumeration value="SCANNED_NON_SSL"/>
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
<simpleType name="VastRedirectType">
<annotation>
<documentation> The types of VAST ads that a {@link VastRedirectCreative} can point to. </documentation>
</annotation>
<restriction base="xsd:string">
<enumeration value="LINEAR">
<annotation>
<documentation> The VAST XML contains only {@code linear} ads. </documentation>
</annotation>
</enumeration>
<enumeration value="NON_LINEAR">
<annotation>
<documentation> The VAST XML contains only {@code nonlinear} ads. </documentation>
</annotation>
</enumeration>
<enumeration value="LINEAR_AND_NON_LINEAR">
<annotation>
<documentation> The VAST XML contains both {@code linear} and {@code nonlinear} ads. </documentation>
</annotation>
</enumeration>
</restriction>
</simpleType>
<simpleType name="VideoDeliveryType">
<annotation>
<documentation> The video delivery type. </documentation>
</annotation>
<restriction base="xsd:string">
<enumeration value="UNKNOWN">
<annotation>
<documentation> The value returned if the actual value is not exposed by the requested API version. </documentation>
</annotation>
</enumeration>
<enumeration value="PROGRESSIVE">
<annotation>
<documentation> Video will be served through a progressive download. </documentation>
</annotation>
</enumeration>
<enumeration value="STREAMING">
<annotation>
<documentation> Video will be served via a streaming protocol like HLS or DASH. </documentation>
</annotation>
</enumeration>
</restriction>
</simpleType>
<element name="createCreatives">
<annotation>
<documentation> Creates new {@link Creative} objects. </documentation>
</annotation>
<complexType>
<sequence>
<element maxOccurs="unbounded" minOccurs="0" name="creatives" type="tns:Creative"/>
</sequence>
</complexType>
</element>
<element name="createCreativesResponse">
<complexType>
<sequence>
<element maxOccurs="unbounded" minOccurs="0" name="rval" type="tns:Creative"/>
</sequence>
</complexType>
</element>
<element name="ApiExceptionFault" type="tns:ApiException">
<annotation>
<documentation> A fault element of type ApiException. </documentation>
</annotation>
</element>
<element name="getCreativesByStatement">
<annotation>
<documentation> Gets a {@link CreativePage} of {@link Creative} objects that satisfy the given {@link Statement#query}. The following fields are supported for filtering: <table> <tr> <th scope="col">PQL Property</th> <th scope="col">Object Property</th> </tr> <tr> <td>{@code id}</td> <td>{@link Creative#id}</td> </tr> <tr> <td>{@code name}</td> <td>{@link Creative#name}</td> </tr> <tr> <td>{@code advertiserId}</td> <td>{@link Creative#advertiserId}</td> </tr> <tr> <td>{@code width}</td> <td>{@link Creative#size}</td> </tr> <tr> <td>{@code height}</td> <td>{@link Creative#size}</td> </tr> <tr> <td>{@code lastModifiedDateTime}</td> <td>{@link Creative#lastModifiedDateTime}</td> </tr> </table> </documentation>
</annotation>
<complexType>
<sequence>
<element maxOccurs="1" minOccurs="0" name="filterStatement" type="tns:Statement"/>
</sequence>
</complexType>
</element>
<element name="getCreativesByStatementResponse">
<complexType>
<sequence>
<element maxOccurs="1" minOccurs="0" name="rval" type="tns:CreativePage"/>
</sequence>
</complexType>
</element>
<element name="performCreativeAction">
<annotation>
<documentation> Performs action on {@link Creative} objects that match the given {@link Statement#query}. </documentation>
</annotation>
<complexType>
<sequence>
<element maxOccurs="1" minOccurs="0" name="creativeAction" type="tns:CreativeAction"/>
<element maxOccurs="1" minOccurs="0" name="filterStatement" type="tns:Statement"/>
</sequence>
</complexType>
</element>
<element name="performCreativeActionResponse">
<complexType>
<sequence>
<element maxOccurs="1" minOccurs="0" name="rval" type="tns:UpdateResult"/>
</sequence>
</complexType>
</element>
<element name="updateCreatives">
<annotation>
<documentation> Updates the specified {@link Creative} objects. </documentation>
</annotation>
<complexType>
<sequence>
<element maxOccurs="unbounded" minOccurs="0" name="creatives" type="tns:Creative"/>
</sequence>
</complexType>
</element>
<element name="updateCreativesResponse">
<complexType>
<sequence>
<element maxOccurs="unbounded" minOccurs="0" name="rval" type="tns:Creative"/>
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
<wsdl:message name="createCreativesRequest">
<wsdl:part element="tns:createCreatives" name="parameters"/>
</wsdl:message>
<wsdl:message name="createCreativesResponse">
<wsdl:part element="tns:createCreativesResponse" name="parameters"/>
</wsdl:message>
<wsdl:message name="ApiException">
<wsdl:part element="tns:ApiExceptionFault" name="ApiException"/>
</wsdl:message>
<wsdl:message name="getCreativesByStatementRequest">
<wsdl:part element="tns:getCreativesByStatement" name="parameters"/>
</wsdl:message>
<wsdl:message name="getCreativesByStatementResponse">
<wsdl:part element="tns:getCreativesByStatementResponse" name="parameters"/>
</wsdl:message>
<wsdl:message name="performCreativeActionRequest">
<wsdl:part element="tns:performCreativeAction" name="parameters"/>
</wsdl:message>
<wsdl:message name="performCreativeActionResponse">
<wsdl:part element="tns:performCreativeActionResponse" name="parameters"/>
</wsdl:message>
<wsdl:message name="updateCreativesRequest">
<wsdl:part element="tns:updateCreatives" name="parameters"/>
</wsdl:message>
<wsdl:message name="updateCreativesResponse">
<wsdl:part element="tns:updateCreativesResponse" name="parameters"/>
</wsdl:message>
<wsdl:portType name="CreativeServiceInterface">
<wsdl:documentation> Provides methods for adding, updating and retrieving {@link Creative} objects. <p>For a creative to run, it must be associated with a {@link LineItem} managed by the {@link LineItemCreativeAssociationService}. <p>Read more about creatives on the <a href="https://support.google.com/admanager/answer/3185155">Ad Manager Help Center</a>. </wsdl:documentation>
<wsdl:operation name="createCreatives">
<wsdl:documentation> Creates new {@link Creative} objects. </wsdl:documentation>
<wsdl:input message="tns:createCreativesRequest" name="createCreativesRequest"/>
<wsdl:output message="tns:createCreativesResponse" name="createCreativesResponse"/>
<wsdl:fault message="tns:ApiException" name="ApiException"/>
</wsdl:operation>
<wsdl:operation name="getCreativesByStatement">
<wsdl:documentation> Gets a {@link CreativePage} of {@link Creative} objects that satisfy the given {@link Statement#query}. The following fields are supported for filtering: <table> <tr> <th scope="col">PQL Property</th> <th scope="col">Object Property</th> </tr> <tr> <td>{@code id}</td> <td>{@link Creative#id}</td> </tr> <tr> <td>{@code name}</td> <td>{@link Creative#name}</td> </tr> <tr> <td>{@code advertiserId}</td> <td>{@link Creative#advertiserId}</td> </tr> <tr> <td>{@code width}</td> <td>{@link Creative#size}</td> </tr> <tr> <td>{@code height}</td> <td>{@link Creative#size}</td> </tr> <tr> <td>{@code lastModifiedDateTime}</td> <td>{@link Creative#lastModifiedDateTime}</td> </tr> </table> </wsdl:documentation>
<wsdl:input message="tns:getCreativesByStatementRequest" name="getCreativesByStatementRequest"/>
<wsdl:output message="tns:getCreativesByStatementResponse" name="getCreativesByStatementResponse"/>
<wsdl:fault message="tns:ApiException" name="ApiException"/>
</wsdl:operation>
<wsdl:operation name="performCreativeAction">
<wsdl:documentation> Performs action on {@link Creative} objects that match the given {@link Statement#query}. </wsdl:documentation>
<wsdl:input message="tns:performCreativeActionRequest" name="performCreativeActionRequest"/>
<wsdl:output message="tns:performCreativeActionResponse" name="performCreativeActionResponse"/>
<wsdl:fault message="tns:ApiException" name="ApiException"/>
</wsdl:operation>
<wsdl:operation name="updateCreatives">
<wsdl:documentation> Updates the specified {@link Creative} objects. </wsdl:documentation>
<wsdl:input message="tns:updateCreativesRequest" name="updateCreativesRequest"/>
<wsdl:output message="tns:updateCreativesResponse" name="updateCreativesResponse"/>
<wsdl:fault message="tns:ApiException" name="ApiException"/>
</wsdl:operation>
</wsdl:portType>
<wsdl:binding name="CreativeServiceSoapBinding" type="tns:CreativeServiceInterface">
<wsdlsoap:binding style="document" transport="http://schemas.xmlsoap.org/soap/http"/>
<wsdl:operation name="createCreatives">
<wsdlsoap:operation soapAction=""/>
<wsdl:input name="createCreativesRequest">
<wsdlsoap:header message="tns:RequestHeader" part="RequestHeader" use="literal"/>
<wsdlsoap:body use="literal"/>
</wsdl:input>
<wsdl:output name="createCreativesResponse">
<wsdlsoap:header message="tns:ResponseHeader" part="ResponseHeader" use="literal"/>
<wsdlsoap:body use="literal"/>
</wsdl:output>
<wsdl:fault name="ApiException">
<wsdlsoap:fault name="ApiException" use="literal"/>
</wsdl:fault>
</wsdl:operation>
<wsdl:operation name="getCreativesByStatement">
<wsdlsoap:operation soapAction=""/>
<wsdl:input name="getCreativesByStatementRequest">
<wsdlsoap:header message="tns:RequestHeader" part="RequestHeader" use="literal"/>
<wsdlsoap:body use="literal"/>
</wsdl:input>
<wsdl:output name="getCreativesByStatementResponse">
<wsdlsoap:header message="tns:ResponseHeader" part="ResponseHeader" use="literal"/>
<wsdlsoap:body use="literal"/>
</wsdl:output>
<wsdl:fault name="ApiException">
<wsdlsoap:fault name="ApiException" use="literal"/>
</wsdl:fault>
</wsdl:operation>
<wsdl:operation name="performCreativeAction">
<wsdlsoap:operation soapAction=""/>
<wsdl:input name="performCreativeActionRequest">
<wsdlsoap:header message="tns:RequestHeader" part="RequestHeader" use="literal"/>
<wsdlsoap:body use="literal"/>
</wsdl:input>
<wsdl:output name="performCreativeActionResponse">
<wsdlsoap:header message="tns:ResponseHeader" part="ResponseHeader" use="literal"/>
<wsdlsoap:body use="literal"/>
</wsdl:output>
<wsdl:fault name="ApiException">
<wsdlsoap:fault name="ApiException" use="literal"/>
</wsdl:fault>
</wsdl:operation>
<wsdl:operation name="updateCreatives">
<wsdlsoap:operation soapAction=""/>
<wsdl:input name="updateCreativesRequest">
<wsdlsoap:header message="tns:RequestHeader" part="RequestHeader" use="literal"/>
<wsdlsoap:body use="literal"/>
</wsdl:input>
<wsdl:output name="updateCreativesResponse">
<wsdlsoap:header message="tns:ResponseHeader" part="ResponseHeader" use="literal"/>
<wsdlsoap:body use="literal"/>
</wsdl:output>
<wsdl:fault name="ApiException">
<wsdlsoap:fault name="ApiException" use="literal"/>
</wsdl:fault>
</wsdl:operation>
</wsdl:binding>
<wsdl:service name="CreativeService">
<wsdl:port binding="tns:CreativeServiceSoapBinding" name="CreativeServiceInterfacePort">
<wsdlsoap:address location="https://ads.google.com/apis/ads/publisher/v202408/CreativeService"/>
</wsdl:port>
</wsdl:service>
</wsdl:definitions>
"""

from __future__ import annotations
from typing import List, Optional
from enum import Enum

from pydantic import Field, StrictBytes, field_validator

from rcplus_alloy_common.gam.vendor.common import (
    GAMSOAPBaseModel,
    BaseCustomFieldValue,
    DateTime,
    Size,
    AppliedLabel,
)


class DeclarationType(str, Enum):
    """
    <simpleType name="DeclarationType">
    <annotation>
    <documentation> The declaration about third party data usage on the associated entity. </documentation>
    </annotation>
    <restriction base="xsd:string">
    <enumeration value="NONE">
    <annotation>
    <documentation> There are no companies associated. Functionally the same as DECLARED, combined with an empty company list. </documentation>
    </annotation>
    </enumeration>
    <enumeration value="DECLARED">
    <annotation>
    <documentation> There is a set of {@link RichMediaAdsCompany}s associated with this entity. </documentation>
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

    NONE = "NONE"
    DECLARED = "DECLARED"
    UNKNOWN = "UNKNOWN"


class ThirdPartyDataDeclaration(GAMSOAPBaseModel):
    """
    <complexType name="ThirdPartyDataDeclaration">
    <annotation>
    <documentation> Represents a set of declarations about what (if any) third party companies are associated with a given creative. <p>This can be set at the network level, as a default for all creatives, or overridden for a particular creative. </documentation>
    </annotation>
    <sequence>
    <element maxOccurs="1" minOccurs="0" name="declarationType" type="tns:DeclarationType"/>
    <element maxOccurs="unbounded" minOccurs="0" name="thirdPartyCompanyIds" type="xsd:long"/>
    </sequence>
    </complexType>
    """
    declarationType: Optional[DeclarationType] = Field(
        None, description="The type of declaration being made"
    )
    thirdPartyCompanyIds: Optional[List[int]] = Field(
        None, description="The IDs of the third party companies associated with the creative"
    )


class CreativePolicyViolation(str, Enum):
    """
    Represents the different types of policy violations that may be detected on a given creative. <p>For more information about the various types of policy violations, see <a href="https://support.google.com/adspolicy/answer/6008942">here</a>.
    <simpleType name="CreativePolicyViolation">
    <annotation>
    <documentation> Represents the different types of policy violations that may be detected on a given creative. <p>For more information about the various types of policy violations, see <a href="https://support.google.com/adspolicy/answer/6008942">here</a>. </documentation>
    </annotation>
    <restriction base="xsd:string">
    <enumeration value="MALWARE_IN_CREATIVE">
    <annotation>
    <documentation> Malware was found in the creative. <p>For more information see <a href="https://support.google.com/adspolicy/answer/1308246">here</a>. </documentation>
    </annotation>
    </enumeration>
    <enumeration value="MALWARE_IN_LANDING_PAGE">
    <annotation>
    <documentation> Malware was found in the landing page. <p>For more information see <a href="https://support.google.com/adspolicy/answer/1308246">here</a>. </documentation>
    </annotation>
    </enumeration>
    <enumeration value="LEGALLY_BLOCKED_REDIRECT_URL">
    <annotation>
    <documentation> The redirect url contains legally objectionable content. </documentation>
    </annotation>
    </enumeration>
    <enumeration value="MISREPRESENTATION_OF_PRODUCT">
    <annotation>
    <documentation> The creative misrepresents the product or service being advertised. <p>For more information see <a href="https://support.google.com/adspolicy/answer/6020955">here</a>. </documentation>
    </annotation>
    </enumeration>
    <enumeration value="SELF_CLICKING_CREATIVE">
    <annotation>
    <documentation> The creative has been determined to be self clicking. </documentation>
    </annotation>
    </enumeration>
    <enumeration value="GAMING_GOOGLE_NETWORK">
    <annotation>
    <documentation> The creative has been determined as attempting to game the Google network. <p>For more information see <a href="https://support.google.com/adspolicy/answer/6020954#319">here</a>. </documentation>
    </annotation>
    </enumeration>
    <enumeration value="DYNAMIC_DNS">
    <annotation>
    <documentation> The landing page for the creative uses a dynamic DNS. <p>For more information see <a href="https://support.google.com/adspolicy/answer/6020954">here</a>. </documentation>
    </annotation>
    </enumeration>
    <enumeration value="CIRCUMVENTING_SYSTEMS">
    <annotation>
    <documentation> The creative has been determined as attempting to circumvent Google advertising systems. </documentation>
    </annotation>
    </enumeration>
    <enumeration value="PHISHING">
    <annotation>
    <documentation> Phishing found in creative or landing page. <p>For more information see <a href="https://support.google.com/adspolicy/answer/6020955">here</a>. </documentation>
    </annotation>
    </enumeration>
    <enumeration value="DOWNLOAD_PROMPT_IN_CREATIVE">
    <annotation>
    <documentation> The creative prompts the user to download a file. <p>For more information see <a href="https://support.google.com/admanager/answer/7513391">here</a> </documentation>
    </annotation>
    </enumeration>
    <enumeration value="UNAUTHORIZED_COOKIE_DETECTED">
    <annotation>
    <documentation> The creative sets an unauthorized cookie on a Google domain. <p>For more information see <a href="https://support.google.com/admanager/answer/7513391">here</a> </documentation>
    </annotation>
    </enumeration>
    <enumeration value="TEMPORARY_PAUSE_FOR_VENDOR_INVESTIGATION">
    <annotation>
    <documentation> The creative has been temporarily paused while we investigate. </documentation>
    </annotation>
    </enumeration>
    <enumeration value="ABUSIVE_EXPERIENCE">
    <annotation>
    <documentation> The landing page contains an abusive experience. <p>For more information see <a href="https://support.google.com/webtools/answer/7347327">here</a>. </documentation>
    </annotation>
    </enumeration>
    <enumeration value="TRICK_TO_CLICK">
    <annotation>
    <documentation> The creative is designed to mislead or trick the user into interacting with it. <p>For more information see <a href="https://support.google.com/adwordspolicy/answer/6020955#357">here</a>. </documentation>
    </annotation>
    </enumeration>
    <enumeration value="USE_OF_NON_ALLOWLISTED_OMID_VERIFICATION_SCRIPT">
    <annotation>
    <documentation> Non-allowlisted OMID verification script. <p>For more information see <a href="https://support.google.com/authorizedbuyers/answer/9115752">here</a>. </documentation>
    </annotation>
    </enumeration>
    <enumeration value="MISUSE_OF_OMID_API">
    <annotation>
    <documentation> OMID sdk injected by creative. < p>For more information see <a href="https://support.google.com/authorizedbuyers/answer/9115752">here</a>. </documentation>
    </annotation>
    </enumeration>
    <enumeration value="UNACCEPTABLE_HTML_AD">
    <annotation>
    <documentation> Unacceptable HTML5 ad. <p>For more information see <a href="https://support.google.com/adspolicy/answer/6088505#266">here</a>. </documentation>
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
    MALWARE_IN_CREATIVE = "MALWARE_IN_CREATIVE"
    MALWARE_IN_LANDING_PAGE = "MALWARE_IN_LANDING_PAGE"
    LEGALLY_BLOCKED_REDIRECT_URL = "LEGALLY_BLOCKED_REDIRECT_URL"
    MISREPRESENTATION_OF_PRODUCT = "MISREPRESENTATION_OF_PRODUCT"
    SELF_CLICKING_CREATIVE = "SELF_CLICKING_CREATIVE"
    GAMING_GOOGLE_NETWORK = "GAMING_GOOGLE_NETWORK"
    DYNAMIC_DNS = "DYNAMIC_DNS"
    CIRCUMVENTING_SYSTEMS = "CIRCUMVENTING_SYSTEMS"
    PHISHING = "PHISHING"
    DOWNLOAD_PROMPT_IN_CREATIVE = "DOWNLOAD_PROMPT_IN_CREATIVE"
    UNAUTHORIZED_COOKIE_DETECTED = "UNAUTHORIZED_COOKIE_DETECTED"
    TEMPORARY_PAUSE_FOR_VENDOR_INVESTIGATION = "TEMPORARY_PAUSE_FOR_VENDOR_INVESTIGATION"
    ABUSIVE_EXPERIENCE = "ABUSIVE_EXPERIENCE"
    TRICK_TO_CLICK = "TRICK_TO_CLICK"
    USE_OF_NON_ALLOWLISTED_OMID_VERIFICATION_SCRIPT = "USE_OF_NON_ALLOWLISTED_OMID_VERIFICATION_SCRIPT"
    MISUSE_OF_OMID_API = "MISUSE_OF_OMID_API"
    UNACCEPTABLE_HTML_AD = "UNACCEPTABLE_HTML_AD"
    UNKNOWN = "UNKNOWN"


class Creative(GAMSOAPBaseModel):
    """
    <complexType abstract="true" name="Creative">
    <annotation>
    <documentation> A {@code Creative} represents the media for the ad being served. <p>Read more about creatives on the <a href="https://support.google.com/admanager/answer/3185155">Ad Manager Help Center</a>. </documentation>
    </annotation>
    <sequence>
    <element maxOccurs="1" minOccurs="0" name="advertiserId" type="xsd:long">
    <annotation>
    <documentation> The ID of the advertiser that owns the creative. This attribute is required. </documentation>
    </annotation>
    </element>
    <element maxOccurs="1" minOccurs="0" name="id" type="xsd:long">
    <annotation>
    <documentation> Uniquely identifies the {@code Creative}. This value is read-only and is assigned by Google when the creative is created. This attribute is required for updates. </documentation>
    </annotation>
    </element>
    <element maxOccurs="1" minOccurs="0" name="name" type="xsd:string">
    <annotation>
    <documentation> The name of the creative. This attribute is required and has a maximum length of 255 characters. </documentation>
    </annotation>
    </element>
    <element maxOccurs="1" minOccurs="0" name="size" type="tns:Size">
    <annotation>
    <documentation> The {@link Size} of the creative. This attribute is required for creation and then is read-only. </documentation>
    </annotation>
    </element>
    <element maxOccurs="1" minOccurs="0" name="previewUrl" type="xsd:string">
    <annotation>
    <documentation> The URL of the creative for previewing the media. This attribute is read-only and is assigned by Google when a creative is created. </documentation>
    </annotation>
    </element>
    <element maxOccurs="unbounded" minOccurs="0" name="policyLabels" type="tns:CreativePolicyViolation">
    <annotation>
    <documentation> Set of policy labels detected for this creative. This attribute is read-only. </documentation>
    </annotation>
    </element>
    <element maxOccurs="unbounded" minOccurs="0" name="appliedLabels" type="tns:AppliedLabel">
    <annotation>
    <documentation> The set of labels applied to this creative. </documentation>
    </annotation>
    </element>
    <element maxOccurs="1" minOccurs="0" name="lastModifiedDateTime" type="tns:DateTime">
    <annotation>
    <documentation> The date and time this creative was last modified. </documentation>
    </annotation>
    </element>
    <element maxOccurs="unbounded" minOccurs="0" name="customFieldValues" type="tns:BaseCustomFieldValue">
    <annotation>
    <documentation> The values of the custom fields associated with this creative. </documentation>
    </annotation>
    </element>
    <element maxOccurs="1" minOccurs="0" name="thirdPartyDataDeclaration" type="tns:ThirdPartyDataDeclaration">
    <annotation>
    <documentation> The third party companies associated with this creative. <p>This is distinct from any associated companies that Google may detect programmatically. </documentation>
    </annotation>
    </element>
    <element maxOccurs="1" minOccurs="0" name="adBadgingEnabled" type="xsd:boolean">
    <annotation>
    <documentation> Whether the creative has ad badging enabled. <p>Defaults to false for {@code CreativeType.VAST_REDIRECT}, {@code CreativeType.THIRD_PARTY}, {@code CreativeType.AUDIO_VAST_REDIRECT}, {@code CreativeType.PROGRAMMATIC}, {@code CreativeType.DFP_MOBILE_CREATIVE}, {@code CreativeType.FLASH_OVERLAY}, {@code CreativeType.GRAPHICAL_INTERSTITIAL}, {@code CreativeType.LEGACY_DFP_CREATIVE}, {@code CreativeType.MOBILE_AD_NETWORK_BACKFILL}, {@code CreativeType.MOBILE_VIDEO_INTERSTITIAL}, {@code CreativeType.SDK_MEDIATION} and {@code CreativeType.STANDARD_FLASH} creative types. <p>. Defaults to true for all other creative types. </documentation>
    </annotation>
    </element>
    </sequence>
    </complexType>
    """
    advertiserId: Optional[int] = Field(
        None, description="The ID of the advertiser that owns the creative. This attribute is required."
    )
    id: Optional[int] = Field(
        None,
        description="Uniquely identifies the {@code Creative}. This value is read-only and is assigned by Google when the creative is created. This attribute is required for updates.",
    )
    name: str = Field(
        ...,
        description="The name of the creative. This attribute is required and has a maximum length of 255 characters."
    )
    size: Optional[Size] = Field(
        None, description="The {@link Size} of the creative. This attribute is required for creation and then is read-only."
    )
    previewUrl: Optional[str] = Field(
        None,
        description="The URL of the creative for previewing the media. This attribute is read-only and is assigned by Google when a creative is created.",
    )
    policyLabels: Optional[List[CreativePolicyViolation]] = Field(
        None, description="Set of policy labels detected for this creative. This attribute is read-only."
    )
    appliedLabels: Optional[List[AppliedLabel]] = Field(None, description="The set of labels applied to this creative.")
    lastModifiedDateTime: Optional[DateTime] = Field(None, description="The date and time this creative was last modified.")
    customFieldValues: Optional[List[BaseCustomFieldValue]] = Field(
        None, description="The values of the custom fields associated with this creative."
    )
    thirdPartyDataDeclaration: Optional[ThirdPartyDataDeclaration] = Field(
        None,
        description="The third party companies associated with this creative. <p>This is distinct from any associated companies that Google may detect programmatically.",
    )
    adBadgingEnabled: Optional[bool] = Field(
        None, description=(
            "Whether the creative has ad badging enabled. "
            "<p>Defaults to false for "
            "{@code CreativeType.VAST_REDIRECT}, "
            "{@code CreativeType.THIRD_PARTY}, "
            "{@code CreativeType.AUDIO_VAST_REDIRECT}, "
            "{@code CreativeType.PROGRAMMATIC}, "
            "{@code CreativeType.DFP_MOBILE_CREATIVE}, "
            "{@code CreativeType.FLASH_OVERLAY}, "
            "{@code CreativeType.GRAPHICAL_INTERSTITIAL}, "
            "{@code CreativeType.LEGACY_DFP_CREATIVE}, "
            "{@code CreativeType.MOBILE_AD_NETWORK_BACKFILL}, "
            "{@code CreativeType.MOBILE_VIDEO_INTERSTITIAL}, "
            "{@code CreativeType.SDK_MEDIATION} and "
            "{@code CreativeType.STANDARD_FLASH} creative types. <p>. "
            "Defaults to true for all other creative types."
        )
    )


class ClickTag(GAMSOAPBaseModel):
    """
    <complexType name="ClickTag">
    <annotation>
    <documentation> Click tags define click-through URLs for each exit on an HTML5 creative. An exit is any area that can be clicked that directs the browser to a landing page. Each click tag defines the click-through URL for a different exit. In Ad Manager, tracking pixels are attached to the click tags if URLs are valid. </documentation>
    </annotation>
    <sequence>
    <element maxOccurs="1" minOccurs="0" name="name" type="xsd:string">
    <annotation>
    <documentation> Name of the click tag, follows the regex "clickTag\\d*" </documentation>
    </annotation>
    </element>
    <element maxOccurs="1" minOccurs="0" name="url" type="xsd:string">
    <annotation>
    <documentation> URL of the click tag. </documentation>
    </annotation>
    </element>
    </sequence>
    </complexType>
    """
    name: Optional[str] = Field(None, description="Name of the click tag, follows the regex 'clickTag\\d*'")
    url: Optional[str] = Field(None, description="URL of the click tag.")


class ImageDensity(str, Enum):
    """
    <simpleType name="ImageDensity">
    <annotation>
    <documentation> Image densities. </documentation>
    </annotation>
    <restriction base="xsd:string">
    <enumeration value="ONE_TO_ONE">
    <annotation>
    <documentation> Indicates that there is a 1:1 ratio between the dimensions of the raw image and the dimensions that it should be displayed at in device-independent pixels. </documentation>
    </annotation>
    </enumeration>
    <enumeration value="THREE_TO_TWO">
    <annotation>
    <documentation> Indicates that there is a 3:2 ratio between the dimensions of the raw image and the dimensions that it should be displayed at in device-independent pixels. </documentation>
    </annotation>
    </enumeration>
    <enumeration value="TWO_TO_ONE">
    <annotation>
    <documentation> Indicates that there is a 2:1 ratio between the dimensions of the raw image and the dimensions that it should be displayed at in device-independent pixels. </documentation>
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
    ONE_TO_ONE = "ONE_TO_ONE"
    THREE_TO_TWO = "THREE_TO_TWO"
    TWO_TO_ONE = "TWO_TO_ONE"
    UNKNOWN = "UNKNOWN"


class CreativeAsset(GAMSOAPBaseModel):
    """
    <complexType name="CreativeAsset">
    <annotation>
    <documentation> A {@code CreativeAsset} is an asset that can be used in creatives. </documentation>
    </annotation>
    <sequence>
    <element maxOccurs="1" minOccurs="0" name="assetId" type="xsd:long">
    <annotation>
    <documentation> The ID of the asset. This attribute is generated by Google upon creation. </documentation>
    </annotation>
    </element>
    <element maxOccurs="1" minOccurs="0" name="assetByteArray" type="xsd:base64Binary">
    <annotation>
    <documentation> The content of the asset as a byte array. This attribute is required when creating the creative that contains this asset if an {@code assetId} is not provided. <p>When updating the content, pass a new byte array, and set {@code assetId} to null. Otherwise, this field can be null. <p>The {@code assetByteArray} will be {@code null} when the creative is retrieved. </documentation>
    </annotation>
    </element>
    <element maxOccurs="1" minOccurs="0" name="fileName" type="xsd:string">
    <annotation>
    <documentation> The file name of the asset. This attribute is required when creating a new asset (e.g. when {@link #assetByteArray} is not null). </documentation>
    </annotation>
    </element>
    <element maxOccurs="1" minOccurs="0" name="fileSize" type="xsd:long">
    <annotation>
    <documentation> The file size of the asset in bytes. This attribute is read-only. </documentation>
    </annotation>
    </element>
    <element maxOccurs="1" minOccurs="0" name="assetUrl" type="xsd:string">
    <annotation>
    <documentation> A URL where the asset can be previewed at. This field is read-only and set by Google. </documentation>
    </annotation>
    </element>
    <element maxOccurs="1" minOccurs="0" name="size" type="tns:Size">
    <annotation>
    <documentation> The size of the asset. Note that this may not always reflect the actual physical size of the asset, but may reflect the expected size. This attribute is read-only and is populated by Google. </documentation>
    </annotation>
    </element>
    <element maxOccurs="unbounded" minOccurs="0" name="clickTags" type="tns:ClickTag">
    <annotation>
    <documentation> The click tags of the asset. This field is read-only. </documentation>
    </annotation>
    </element>
    <element maxOccurs="1" minOccurs="0" name="imageDensity" type="tns:ImageDensity">
    <annotation>
    <documentation> The display density of the image. This is the ratio between a dimension in pixels of the image and the dimension in pixels that it should occupy in device-independent pixels when displayed. This attribute is optional and defaults to ONE_TO_ONE. </documentation>
    </annotation>
    </element>
    </sequence>
    </complexType>
    """
    assetId: Optional[int] = Field(
        None, description="The ID of the asset. This attribute is generated by Google upon creation."
    )
    assetByteArray: Optional[StrictBytes] = Field(
        None,
        description="The content of the asset as a byte array. This attribute is required when creating the creative that contains this asset if an {@code assetId} is not provided. <p>When updating the content, pass a new byte array, and set {@code assetId} to null. Otherwise, this field can be null. <p>The {@code assetByteArray} will be {@code null} when the creative is retrieved.",
    )
    fileName: Optional[str] = Field(
        None, description="The file name of the asset. This attribute is required when creating a new asset (e.g. when {@link #assetByteArray} is not null)."
    )
    fileSize: Optional[int] = Field(None, description="The file size of the asset in bytes. This attribute is read-only.")
    assetUrl: Optional[str] = Field(
        None, description="A URL where the asset can be previewed at. This field is read-only and set by Google."
    )
    size: Optional[Size] = Field(
        None,
        description="The size of the asset. Note that this may not always reflect the actual physical size of the asset, but may reflect the expected size. This attribute is read-only and is populated by Google.",
    )
    clickTags: Optional[List[ClickTag]] = Field(None, description="The click tags of the asset. This field is read-only.")
    imageDensity: Optional[ImageDensity] = Field(
        None,
        description="The display density of the image. This is the ratio between a dimension in pixels of the image and the dimension in pixels that it should occupy in device-independent pixels when displayed. This attribute is optional and defaults to ONE_TO_ONE.",
    )

    @field_validator("assetByteArray", mode="before")
    @classmethod
    def asset_bytes_array(cls, v):
        if v is not None and isinstance(v, str):
            return v.encode()
        return v


class DestinationUrlType(str, Enum):
    """
    simpleType name="DestinationUrlType">
    <annotation>
    <documentation> The valid actions that a destination URL may perform if the user clicks on the ad. </documentation>
    </annotation>
    <restriction base="xsd:string">
    <enumeration value="UNKNOWN">
    <annotation>
    <documentation> The value returned if the actual value is not exposed by the requested API version. </documentation>
    </annotation>
    </enumeration>
    <enumeration value="CLICK_TO_WEB">
    <annotation>
    <documentation> Navigate to a web page. (a.k.a. "Click-through URL"). </documentation>
    </annotation>
    </enumeration>
    <enumeration value="CLICK_TO_APP">
    <annotation>
    <documentation> Start an application. </documentation>
    </annotation>
    </enumeration>
    <enumeration value="CLICK_TO_CALL">
    <annotation>
    <documentation> Make a phone call. </documentation>
    </annotation>
    </enumeration>
    <enumeration value="NONE">
    <annotation>
    <documentation> Destination URL not present. Useful for video creatives where a landing page or a product isn't necessarily applicable. </documentation>
    </annotation>
    </enumeration>
    </restriction>
    </simpleType>
    """
    UNKNOWN = "UNKNOWN"
    CLICK_TO_WEB = "CLICK_TO_WEB"
    CLICK_TO_APP = "CLICK_TO_APP"
    CLICK_TO_CALL = "CLICK_TO_CALL"
    NONE = "NONE"


class HasDestinationUrlCreative(Creative):
    """
    <complexType abstract="true" name="HasDestinationUrlCreative">
    <annotation>
    <documentation> A {@code Creative} that has a destination url </documentation>
    </annotation>
    <complexContent>
    <extension base="tns:Creative">
    <sequence>
    <element maxOccurs="1" minOccurs="0" name="destinationUrl" type="xsd:string">
    <annotation>
    <documentation> The URL that the user is directed to if they click on the creative. This attribute is required unless the {@link destinationUrlType} is {@link DestinationUrlType#NONE}, and has a maximum length of 1024 characters. </documentation>
    </annotation>
    </element>
    <element maxOccurs="1" minOccurs="0" name="destinationUrlType" type="tns:DestinationUrlType">
    <annotation>
    <documentation> The action that should be performed if the user clicks on the creative. This attribute is optional and defaults to {@link DestinationUrlType#CLICK_TO_WEB}. </documentation>
    </annotation>
    </element>
    </sequence>
    </extension>
    </complexContent>
    </complexType>
    """
    destinationUrl: Optional[str] = Field(
        None,
        max_length=1024,
        description=(
            "The URL that the user is directed to if they click on the creative. "
            "This attribute is required unless the {@link destinationUrlType} is {@link DestinationUrlType#NONE}, "
            "and has a maximum length of 1024 characters."
        ),
    )
    destinationUrlType: Optional[DestinationUrlType] = Field(
        None,
        description=(
            "The action that should be performed if the user clicks on the creative. "
            "This attribute is optional and defaults to {@link DestinationUrlType#CLICK_TO_WEB}."
        ),
    )


class BaseImageCreative(HasDestinationUrlCreative):
    """
    <complexType abstract="true" name="BaseImageCreative">
    <annotation>
    <documentation> The base type for creatives that display an image. </documentation>
    </annotation>
    <complexContent>
    <extension base="tns:HasDestinationUrlCreative">
    <sequence>
    <element maxOccurs="1" minOccurs="0" name="overrideSize" type="xsd:boolean">
    <annotation>
    <documentation> Allows the creative size to differ from the actual image asset size. This attribute is optional. </documentation>
    </annotation>
    </element>
    <element maxOccurs="1" minOccurs="0" name="primaryImageAsset" type="tns:CreativeAsset">
    <annotation>
    <documentation> The primary image asset associated with this creative. This attribute is required. </documentation>
    </annotation>
    </element>
    </sequence>
    </extension>
    </complexContent>
    </complexType>
    """
    overrideSize: Optional[bool] = Field(
        None, description=(
            "Allows the creative size to differ from the actual image asset size. This attribute is optional."
        )
    )
    primaryImageAsset: Optional[CreativeAsset] = Field(
        None, description="The primary image asset associated with this creative. This attribute is required."
    )


class ImageCreative(BaseImageCreative):
    """
    <complexType name="ImageCreative">
    <annotation>
    <documentation> A {@code Creative} that displays an image. </documentation>
    </annotation>
    <complexContent>
    <extension base="tns:BaseImageCreative">
    <sequence>
    <element maxOccurs="1" minOccurs="0" name="altText" type="xsd:string">
    <annotation>
    <documentation> Alternative text to be rendered along with the creative used mainly for accessibility. This field is optional and has a maximum length of 500 characters. </documentation>
    </annotation>
    </element>
    <element maxOccurs="unbounded" minOccurs="0" name="thirdPartyImpressionTrackingUrls" type="xsd:string">
    <annotation>
    <documentation> A list of impression tracking URL to ping when this creative is displayed. This field is optional and each string has a maximum length of 1024 characters. </documentation>
    </annotation>
    </element>
    <element maxOccurs="unbounded" minOccurs="0" name="secondaryImageAssets" type="tns:CreativeAsset">
    <annotation>
    <documentation> The list of secondary image assets associated with this creative. This attribute is optional. <p>Secondary image assets can be used to store different resolution versions of the primary asset for use on non-standard density screens. </documentation>
    </annotation>
    </element>
    </sequence>
    </extension>
    </complexContent>
    </complexType>
    """
    altText: Optional[str] = Field(
        None,
        max_length=500,
        description=(
            "Alternative text to be rendered along with the creative used mainly for accessibility. "
            "This field is optional and has a maximum length of 500 characters."
        )
    )
    thirdPartyImpressionTrackingUrls: Optional[List[str]] = Field(
        None,
        max_length=1024,
        description=(
            "A list of impression tracking URL to ping when this creative is displayed. "
            "This field is optional and each string has a maximum length of 1024 characters."
        )
    )
    secondaryImageAssets: Optional[List[CreativeAsset]] = Field(
        None,
        description=(
            (
                "The list of secondary image assets associated with this creative. "
                "This attribute is optional. "
                "<p>Secondary image assets can be used to store different resolution versions "
                "of the primary asset for use on non-standard density screens."
            )
        )
    )


class LockedOrientation(str, Enum):
    """
    <simpleType name="LockedOrientation">
    <annotation>
    <documentation> Describes the orientation that a creative should be served with. </documentation>
    </annotation>
    <restriction base="xsd:string">
    <enumeration value="UNKNOWN">
    <annotation>
    <documentation> The value returned if the actual value is not exposed by the requested API version. </documentation>
    </annotation>
    </enumeration>
    <enumeration value="FREE_ORIENTATION"/>
    <enumeration value="PORTRAIT_ONLY"/>
    <enumeration value="LANDSCAPE_ONLY"/>
    </restriction>
    </simpleType>
    """
    UNKNOWN = "UNKNOWN"
    FREE_ORIENTATION = "FREE_ORIENTATION"
    PORTRAIT_ONLY = "PORTRAIT_ONLY"
    LANDSCAPE_ONLY = "LANDSCAPE_ONLY"


class SslScanResult(str, Enum):
    """
    <simpleType name="SslScanResult">
    <annotation>
    <documentation> Enum to store the creative SSL compatibility scan result. </documentation>
    </annotation>
    <restriction base="xsd:string">
    <enumeration value="UNKNOWN">
    <annotation>
    <documentation> The value returned if the actual value is not exposed by the requested API version. </documentation>
    </annotation>
    </enumeration>
    <enumeration value="UNSCANNED"/>
    <enumeration value="SCANNED_SSL"/>
    <enumeration value="SCANNED_NON_SSL"/>
    </restriction>
    </simpleType>
    """
    UNKNOWN = "UNKNOWN"
    UNSCANNED = "UNSCANNED"
    SCANNED_SSL = "SCANNED_SSL"
    SCANNED_NON_SSL = "SCANNED_NON_SSL"


class SslManualOverride(str, Enum):
    """
    <simpleType name="SslManualOverride">
    <annotation>
    <documentation> Enum to store the creative SSL compatibility manual override. Its three states are similar to that of {@link SslScanResult}. </documentation>
    </annotation>
    <restriction base="xsd:string">
    <enumeration value="UNKNOWN">
    <annotation>
    <documentation> The value returned if the actual value is not exposed by the requested API version. </documentation>
    </annotation>
    </enumeration>
    <enumeration value="NO_OVERRIDE"/>
    <enumeration value="SSL_COMPATIBLE"/>
    <enumeration value="NOT_SSL_COMPATIBLE"/>
    </restriction>
    </simpleType>
    """
    UNKNOWN = "UNKNOWN"
    NO_OVERRIDE = "NO_OVERRIDE"
    SSL_COMPATIBLE = "SSL_COMPATIBLE"
    NOT_SSL_COMPATIBLE = "NOT_SSL_COMPATIBLE"


class Html5Creative(Creative):
    """
    complexType name="Html5Creative">
    <annotation>
    <documentation> A {@code Creative} that contains a zipped HTML5 bundle asset, a list of third party impression trackers, and a third party click tracker. </documentation>
    </annotation>
    <complexContent>
    <extension base="tns:Creative">
    <sequence>
    <element maxOccurs="1" minOccurs="0" name="overrideSize" type="xsd:boolean">
    <annotation>
    <documentation> Allows the creative size to differ from the actual HTML5 asset size. This attribute is optional. </documentation>
    </annotation>
    </element>
    <element maxOccurs="unbounded" minOccurs="0" name="thirdPartyImpressionTrackingUrls" type="xsd:string">
    <annotation>
    <documentation> Impression tracking URLs to ping when this creative is displayed. This field is optional. </documentation>
    </annotation>
    </element>
    <element maxOccurs="1" minOccurs="0" name="thirdPartyClickTrackingUrl" type="xsd:string">
    <annotation>
    <documentation> A click tracking URL to ping when this creative is clicked. This field is optional. </documentation>
    </annotation>
    </element>
    <element maxOccurs="1" minOccurs="0" name="lockedOrientation" type="tns:LockedOrientation">
    <annotation>
    <documentation> A locked orientation for this creative to be displayed in. </documentation>
    </annotation>
    </element>
    <element maxOccurs="1" minOccurs="0" name="sslScanResult" type="tns:SslScanResult">
    <annotation>
    <documentation> The SSL compatibility scan result of this creative. <p>This attribute is read-only and determined by Google. </documentation>
    </annotation>
    </element>
    <element maxOccurs="1" minOccurs="0" name="sslManualOverride" type="tns:SslManualOverride">
    <annotation>
    <documentation> The manual override for the SSL compatibility of this creative. <p>This attribute is optional and defaults to {@link SslManualOverride#NO_OVERRIDE}. </documentation>
    </annotation>
    </element>
    <element maxOccurs="1" minOccurs="0" name="isSafeFrameCompatible" type="xsd:boolean">
    <annotation>
    <documentation> Whether the {@link Creative} is compatible for SafeFrame rendering. <p>This attribute is optional and defaults to {@code true}. </documentation>
    </annotation>
    </element>
    <element maxOccurs="1" minOccurs="0" name="html5Asset" type="tns:CreativeAsset">
    <annotation>
    <documentation> The HTML5 asset. To preview the HTML5 asset, use the {@link CreativeAsset#assetUrl}. In this field, the {@link CreativeAsset#assetByteArray} must be a zip bundle and the {@link CreativeAsset#fileName} must have a zip extension. This attribute is required. </documentation>
    </annotation>
    </element>
    </sequence>
    </extension>
    </complexContent>
    </complexType>
    """
    overrideSize: Optional[bool] = Field(
        None, description="Allows the creative size to differ from the actual HTML5 asset size. This attribute is optional."
    )
    thirdPartyImpressionTrackingUrls: Optional[List[str]] = Field(
        None, description="Impression tracking URLs to ping when this creative is displayed. This field is optional."
    )
    thirdPartyClickTrackingUrl: Optional[str] = Field(
        None, description="A click tracking URL to ping when this creative is clicked. This field is optional."
    )
    lockedOrientation: Optional[LockedOrientation] = Field(
        None, description="A locked orientation for this creative to be displayed in."
    )
    sslScanResult: Optional[SslScanResult] = Field(
        None,
        description=(
            "The SSL compatibility scan result of this creative. "
            "<p>This attribute is read-only and determined by Google."
        )
    )
    sslManualOverride: Optional[SslManualOverride] = Field(
        None,
        description=(
            "The manual override for the SSL compatibility of this creative. "
            "<p>This attribute is optional and defaults to {@link SslManualOverride#NO_OVERRIDE}."
        )
    )
    isSafeFrameCompatible: Optional[bool] = Field(
        None,
        description=(
            "Whether the {@link Creative} is compatible for SafeFrame rendering. "
            "<p>This attribute is optional and defaults to {@code true}."
        )
    )
    html5Asset: Optional[CreativeAsset] = Field(
        None,
        description=(
            "The HTML5 asset. To preview the HTML5 asset, use the {@link CreativeAsset#assetUrl}. "
            "In this field, the {@link CreativeAsset#assetByteArray} must be a zip bundle and the "
            "{@link CreativeAsset#fileName} must have a zip extension. This attribute is required."
        )
    )


class ConversionEvent(str, Enum):
    """
    <simpleType name="ConversionEvent">
    <annotation>
    <documentation> All possible tracking event types. Not all events are supported by every kind of creative. </documentation>
    </annotation>
    <restriction base="xsd:string">
    <enumeration value="UNKNOWN">
    <annotation>
    <documentation> The value returned if the actual value is not exposed by the requested API version. </documentation>
    </annotation>
    </enumeration>
    <enumeration value="CREATIVE_VIEW">
    <annotation>
    <documentation> Corresponds to the {@code creativeView} tracking event. </documentation>
    </annotation>
    </enumeration>
    <enumeration value="START">
    <annotation>
    <documentation> Corresponds to the {@code start} tracking event. </documentation>
    </annotation>
    </enumeration>
    <enumeration value="SKIP_SHOWN">
    <annotation>
    <documentation> An event that is fired when a video skip button is shown, usually after 5 seconds of viewing the video. This event does not correspond to any VAST element and is implemented using an extension. </documentation>
    </annotation>
    </enumeration>
    <enumeration value="FIRST_QUARTILE">
    <annotation>
    <documentation> Corresponds to the {@code firstQuartile} tracking event. </documentation>
    </annotation>
    </enumeration>
    <enumeration value="MIDPOINT">
    <annotation>
    <documentation> Corresponds to the {@code midpoint} tracking event. </documentation>
    </annotation>
    </enumeration>
    <enumeration value="THIRD_QUARTILE">
    <annotation>
    <documentation> Corresponds to the {@code thirdQuartile} tracking event. </documentation>
    </annotation>
    </enumeration>
    <enumeration value="ENGAGED_VIEW">
    <annotation>
    <documentation> An event that is fired after 30 seconds of viewing the video or when the video finished (if the video duration is less than 30 seconds). This event does not correspond to any VAST element and is implemented using an extension. </documentation>
    </annotation>
    </enumeration>
    <enumeration value="COMPLETE">
    <annotation>
    <documentation> Corresponds to the {@code complete} tracking event. </documentation>
    </annotation>
    </enumeration>
    <enumeration value="MUTE">
    <annotation>
    <documentation> Corresponds to the {@code mute} tracking event. </documentation>
    </annotation>
    </enumeration>
    <enumeration value="UNMUTE">
    <annotation>
    <documentation> Corresponds to the {@code unmute} tracking event. </documentation>
    </annotation>
    </enumeration>
    <enumeration value="PAUSE">
    <annotation>
    <documentation> Corresponds to the {@code pause} tracking event. </documentation>
    </annotation>
    </enumeration>
    <enumeration value="REWIND">
    <annotation>
    <documentation> Corresponds to the {@code rewind} tracking event. </documentation>
    </annotation>
    </enumeration>
    <enumeration value="RESUME">
    <annotation>
    <documentation> Corresponds to the {@code resume} tracking event. </documentation>
    </annotation>
    </enumeration>
    <enumeration value="SKIPPED">
    <annotation>
    <documentation> An event that is fired when a video was skipped. This event does not correspond to any VAST element and is implemented using an extension. </documentation>
    </annotation>
    </enumeration>
    <enumeration value="FULLSCREEN">
    <annotation>
    <documentation> Corresponds to the {@code fullscreen} tracking event. </documentation>
    </annotation>
    </enumeration>
    <enumeration value="EXPAND">
    <annotation>
    <documentation> Corresponds to the {@code expand} tracking event. </documentation>
    </annotation>
    </enumeration>
    <enumeration value="COLLAPSE">
    <annotation>
    <documentation> Corresponds to the {@code collapse} tracking event. </documentation>
    </annotation>
    </enumeration>
    <enumeration value="ACCEPT_INVITATION">
    <annotation>
    <documentation> Corresponds to the {@code acceptInvitation} tracking event. </documentation>
    </annotation>
    </enumeration>
    <enumeration value="CLOSE">
    <annotation>
    <documentation> Corresponds to the {@code close} tracking event. </documentation>
    </annotation>
    </enumeration>
    <enumeration value="CLICK_TRACKING">
    <annotation>
    <documentation> Corresponds to the {@code Linear.VideoClicks.ClickTracking} node. </documentation>
    </annotation>
    </enumeration>
    <enumeration value="SURVEY">
    <annotation>
    <documentation> Corresponds to the {@code InLine.Survey} node. </documentation>
    </annotation>
    </enumeration>
    <enumeration value="CUSTOM_CLICK">
    <annotation>
    <documentation> Corresponds to the {@code Linear.VideoClicks.CustomClick} node. </documentation>
    </annotation>
    </enumeration>
    <enumeration value="MEASURABLE_IMPRESSION">
    <annotation>
    <documentation> Corresponds to the {@code measurableImpression} tracking event. </documentation>
    </annotation>
    </enumeration>
    <enumeration value="VIEWABLE_IMPRESSION">
    <annotation>
    <documentation> Corresponds to the {@code viewableImpression} tracking event. </documentation>
    </annotation>
    </enumeration>
    <enumeration value="VIDEO_ABANDON">
    <annotation>
    <documentation> Corresponds to the {@code abandon} tracking event. </documentation>
    </annotation>
    </enumeration>
    <enumeration value="FULLY_VIEWABLE_AUDIBLE_HALF_DURATION_IMPRESSION">
    <annotation>
    <documentation> Corresponds to the {@code fullyViewableAudibleHalfDurationImpression} tracking event. </documentation>
    </annotation>
    </enumeration>
    </restriction>
    </simpleType>
    """
    UNKNOWN = "UNKNOWN"
    CREATIVE_VIEW = "CREATIVE_VIEW"
    START = "START"
    SKIP_SHOWN = "SKIP_SHOWN"
    FIRST_QUARTILE = "FIRST_QUARTILE"
    MIDPOINT = "MIDPOINT"
    THIRD_QUARTILE = "THIRD_QUARTILE"
    ENGAGED_VIEW = "ENGAGED_VIEW"
    COMPLETE = "COMPLETE"
    MUTE = "MUTE"
    UNMUTE = "UNMUTE"
    PAUSE = "PAUSE"
    REWIND = "REWIND"
    RESUME = "RESUME"
    SKIPPED = "SKIPPED"
    FULLSCREEN = "FULLSCREEN"
    EXPAND = "EXPAND"
    COLLAPSE = "COLLAPSE"
    ACCEPT_INVITATION = "ACCEPT_INVITATION"
    CLOSE = "CLOSE"
    CLICK_TRACKING = "CLICK_TRACKING"
    SURVEY = "SURVEY"
    CUSTOM_CLICK = "CUSTOM_CLICK"
    MEASURABLE_IMPRESSION = "MEASURABLE_IMPRESSION"
    VIEWABLE_IMPRESSION = "VIEWABLE_IMPRESSION"
    VIDEO_ABANDON = "VIDEO_ABANDON"
    FULLY_VIEWABLE_AUDIBLE_HALF_DURATION_IMPRESSION = "FULLY_VIEWABLE_AUDIBLE_HALF_DURATION_IMPRESSION"


class TrackingUrls(GAMSOAPBaseModel):
    """
    <complexType name="TrackingUrls">
    <annotation>
    <documentation> A list of URLs that should be pinged for a conversion event. </documentation>
    </annotation>
    <sequence>
    <element maxOccurs="unbounded" minOccurs="0" name="urls" type="xsd:string">
    <annotation>
    <documentation> A list of all URLs that should be pinged. </documentation>
    </annotation>
    </element>
    </sequence>
    </complexType>
    """
    urls: Optional[List[str]] = Field(None, description="A list of all URLs that should be pinged.")


class ConversionEvent_TrackingUrlsMapEntry(GAMSOAPBaseModel):
    """
    <complexType name="ConversionEvent_TrackingUrlsMapEntry">
    <annotation>
    <documentation> This represents an entry in a map with a key of type ConversionEvent and value of type TrackingUrls. </documentation>
    </annotation>
    <sequence>
    <element maxOccurs="1" minOccurs="0" name="key" type="tns:ConversionEvent"/>
    <element maxOccurs="1" minOccurs="0" name="value" type="tns:TrackingUrls"/>
    </sequence>
    </complexType>
    """
    key: Optional[ConversionEvent] = Field(None)
    value: Optional[TrackingUrls] = Field(None)


class AdIdType(str, Enum):
    """
    <simpleType name="AdIdType">
    <annotation>
    <documentation> The registry that an ad ID belongs to. </documentation>
    </annotation>
    <restriction base="xsd:string">
    <enumeration value="UNKNOWN">
    <annotation>
    <documentation> The value returned if the actual value is not exposed by the requested API version. </documentation>
    </annotation>
    </enumeration>
    <enumeration value="AD_ID">
    <annotation>
    <documentation> The ad ID is registered with ad-id.org. </documentation>
    </annotation>
    </enumeration>
    <enumeration value="CLEARCAST">
    <annotation>
    <documentation> The ad ID is registered with clearcast.co.uk. </documentation>
    </annotation>
    </enumeration>
    <enumeration value="NONE">
    <annotation>
    <documentation> The creative does not have an ad ID outside of Ad Manager. </documentation>
    </annotation>
    </enumeration>
    <enumeration value="ARPP">
    <annotation>
    <documentation> The ad ID is registered with ARPP Pub-ID. </documentation>
    </annotation>
    </enumeration>
    <enumeration value="CUSV">
    <annotation>
    <documentation> The ad ID is registered with Auditel Spot ID. </documentation>
    </annotation>
    </enumeration>
    </restriction>
    </simpleType>
    """
    UNKNOWN = "UNKNOWN"
    AD_ID = "AD_ID"
    CLEARCAST = "CLEARCAST"
    NONE = "NONE"
    ARPP = "ARPP"
    CUSV = "CUSV"


class SkippableAdType(str, Enum):
    """
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
    """
    UNKNOWN = "UNKNOWN"
    DISABLED = "DISABLED"
    ENABLED = "ENABLED"
    INSTREAM_SELECT = "INSTREAM_SELECT"
    ANY = "ANY"


class BaseVideoCreative(HasDestinationUrlCreative):
    """
    complexType abstract="true" name="BaseVideoCreative">
    <annotation>
    <documentation> A base type for video creatives. </documentation>
    </annotation>
    <complexContent>
    <extension base="tns:HasDestinationUrlCreative">
    <sequence>
    <element maxOccurs="1" minOccurs="0" name="duration" type="xsd:int">
    <annotation>
    <documentation> The expected duration of this creative in milliseconds. </documentation>
    </annotation>
    </element>
    <element maxOccurs="1" minOccurs="0" name="allowDurationOverride" type="xsd:boolean">
    <annotation>
    <documentation> Allows the creative duration to differ from the actual asset durations. This attribute is optional. </documentation>
    </annotation>
    </element>
    <element maxOccurs="unbounded" minOccurs="0" name="trackingUrls" type="tns:ConversionEvent_TrackingUrlsMapEntry">
    <annotation>
    <documentation> A map from {@code ConversionEvent} to a list of URLs that will be pinged when the event happens. This attribute is optional. </documentation>
    </annotation>
    </element>
    <element maxOccurs="unbounded" minOccurs="0" name="companionCreativeIds" type="xsd:long">
    <annotation>
    <documentation> The IDs of the companion creatives that are associated with this creative. This attribute is optional. </documentation>
    </annotation>
    </element>
    <element maxOccurs="1" minOccurs="0" name="customParameters" type="xsd:string">
    <annotation>
    <documentation> A comma separated key=value list of parameters that will be supplied to the creative, written into the VAST {@code AdParameters} node. This attribute is optional. </documentation>
    </annotation>
    </element>
    <element maxOccurs="1" minOccurs="0" name="adId" type="xsd:string">
    <annotation>
    <documentation> The ad id associated with the video as defined by the {@code adIdType} registry. This field is required if {@code adIdType} is not {@link AdIdType#NONE}. </documentation>
    </annotation>
    </element>
    <element maxOccurs="1" minOccurs="0" name="adIdType" type="tns:AdIdType">
    <annotation>
    <documentation> The registry which the ad id of this creative belongs to. This field is optional and defaults to {@link AdIdType#NONE}. </documentation>
    </annotation>
    </element>
    <element maxOccurs="1" minOccurs="0" name="skippableAdType" type="tns:SkippableAdType">
    <annotation>
    <documentation> The type of skippable ad. </documentation>
    </annotation>
    </element>
    <element maxOccurs="1" minOccurs="0" name="vastPreviewUrl" type="xsd:string">
    <annotation>
    <documentation> An ad tag URL that will return a preview of the VAST XML response specific to this creative. This attribute is read-only. </documentation>
    </annotation>
    </element>
    <element maxOccurs="1" minOccurs="0" name="sslScanResult" type="tns:SslScanResult">
    <annotation>
    <documentation> The SSL compatibility scan result of this creative. <p>This attribute is read-only and determined by Google. </documentation>
    </annotation>
    </element>
    <element maxOccurs="1" minOccurs="0" name="sslManualOverride" type="tns:SslManualOverride">
    <annotation>
    <documentation> The manual override for the SSL compatibility of this creative. <p>This attribute is optional and defaults to {@link SslManualOverride#NO_OVERRIDE}. </documentation>
    </annotation>
    </element>
    </sequence>
    </extension>
    </complexContent>
    </complexType>
    """
    duration: Optional[int] = Field(None, description="The expected duration of this creative in milliseconds.")
    allowDurationOverride: Optional[bool] = Field(
        None, description="Allows the creative duration to differ from the actual asset durations. This attribute is optional."
    )
    trackingUrls: Optional[List[ConversionEvent_TrackingUrlsMapEntry]] = Field(
        None, description="A map from {@code ConversionEvent} to a list of URLs that will be pinged when the event happens."
    )
    companionCreativeIds: Optional[List[int]] = Field(
        None, description="The IDs of the companion creatives that are associated with this creative. This attribute is optional."
    )
    customParameters: Optional[str] = Field(
        None,
        description=(
            "A comma separated key=value list of parameters that will be supplied to the creative, "
            "written into the VAST {@code AdParameters} node. This attribute is optional."
        )
    )
    adId: Optional[str] = Field(
        None,
        description=(
            "The ad id associated with the video as defined by the {@code adIdType} registry. "
            "This field is required if {@code adIdType} is not {@link AdIdType#NONE}."
        )
    )
    adIdType: Optional[AdIdType] = Field(
        None,
        description=(
            "The registry which the ad id of this creative belongs to. "
            "This field is optional and defaults to {@link AdIdType#NONE}."
        )
    )
    skippableAdType: Optional[SkippableAdType] = Field(None, description="The type of skippable ad.")
    vastPreviewUrl: Optional[str] = Field(
        None, description="An ad tag URL that will return a preview of the VAST XML response specific to this creative."
    )
    sslScanResult: Optional[SslScanResult] = Field(
        None,
        description=(
            "The SSL compatibility scan result of this creative. "
            "<p>This attribute is read-only and determined by Google."
        )
    )
    sslManualOverride: Optional[SslManualOverride] = Field(
        None,
        description=(
            "The manual override for the SSL compatibility of this creative. "
            "<p>This attribute is optional and defaults to {@link SslManualOverride#NO_OVERRIDE}."
        )
    )


class VideoCreative(BaseVideoCreative):
    """
    <complexType name="VideoCreative">
    <annotation>
    <documentation> A {@code Creative} that contains Ad Manager hosted video ads and is served via VAST XML. </documentation>
    </annotation>
    <complexContent>
    <extension base="tns:BaseVideoCreative">
    <sequence>
    <element maxOccurs="1" minOccurs="0" name="videoSourceUrl" type="xsd:string">
    <annotation>
    <documentation> A URL that points to the source media that will be used for transcoding. </documentation>
    </annotation>
    </element>
    </sequence>
    </extension>
    </complexContent>
    </complexType>
    """
    videoSourceUrl: Optional[str] = Field(None, description="A URL that points to the source media that will be used for transcoding.")


class Asset(GAMSOAPBaseModel):
    """
    <complexType abstract="true" name="Asset">
    <annotation>
    <documentation> Base asset properties. </documentation>
    </annotation>
    <sequence/>
    </complexType>
    """


class RedirectAsset(Asset):
    """
    <complexType abstract="true" name="RedirectAsset">
    <annotation>
    <documentation> An externally hosted asset. </documentation>
    </annotation>
    <complexContent>
    <extension base="tns:Asset">
    <sequence>
    <element maxOccurs="1" minOccurs="0" name="redirectUrl" type="xsd:string">
    <annotation>
    <documentation> The URL where the asset is hosted. </documentation>
    </annotation>
    </element>
    </sequence>
    </extension>
    </complexContent>
    </complexType>
    """
    redirectUrl: Optional[str] = Field(None, description="The URL where the asset is hosted.")


class MimeType(str, Enum):
    """
    <simpleType name="MimeType">
    <annotation>
    <documentation> Enum of supported mime types </documentation>
    </annotation>
    <restriction base="xsd:string">
    <enumeration value="UNKNOWN">
    <annotation>
    <documentation> The value returned if the actual value is not exposed by the requested API version. </documentation>
    </annotation>
    </enumeration>
    <enumeration value="ASP">
    <annotation>
    <documentation> application/x-asp </documentation>
    </annotation>
    </enumeration>
    <enumeration value="AUDIO_AIFF">
    <annotation>
    <documentation> audio/aiff </documentation>
    </annotation>
    </enumeration>
    <enumeration value="AUDIO_BASIC">
    <annotation>
    <documentation> audio/basic </documentation>
    </annotation>
    </enumeration>
    <enumeration value="AUDIO_FLAC">
    <annotation>
    <documentation> audio/flac </documentation>
    </annotation>
    </enumeration>
    <enumeration value="AUDIO_MID">
    <annotation>
    <documentation> audio/mid </documentation>
    </annotation>
    </enumeration>
    <enumeration value="AUDIO_MP3">
    <annotation>
    <documentation> audio/mpeg </documentation>
    </annotation>
    </enumeration>
    <enumeration value="AUDIO_MP4">
    <annotation>
    <documentation> audio/mp4 </documentation>
    </annotation>
    </enumeration>
    <enumeration value="AUDIO_MPEG_URL">
    <annotation>
    <documentation> audio/x-mpegurl </documentation>
    </annotation>
    </enumeration>
    <enumeration value="AUDIO_MS_WMA">
    <annotation>
    <documentation> audio/x-ms-wma </documentation>
    </annotation>
    </enumeration>
    <enumeration value="AUDIO_OGG">
    <annotation>
    <documentation> audio/ogg </documentation>
    </annotation>
    </enumeration>
    <enumeration value="AUDIO_REAL_AUDIO_PLUGIN">
    <annotation>
    <documentation> audio/x-pn-realaudio-plugin </documentation>
    </annotation>
    </enumeration>
    <enumeration value="AUDIO_WAV">
    <annotation>
    <documentation> audio/x-wav </documentation>
    </annotation>
    </enumeration>
    <enumeration value="BINARY">
    <annotation>
    <documentation> application/binary </documentation>
    </annotation>
    </enumeration>
    <enumeration value="DASH">
    <annotation>
    <documentation> application/dash+xml </documentation>
    </annotation>
    </enumeration>
    <enumeration value="DIRECTOR">
    <annotation>
    <documentation> application/x-director </documentation>
    </annotation>
    </enumeration>
    <enumeration value="FLASH">
    <annotation>
    <documentation> application/x-shockwave-flash </documentation>
    </annotation>
    </enumeration>
    <enumeration value="GRAPHIC_CONVERTER">
    <annotation>
    <documentation> application/graphicconverter </documentation>
    </annotation>
    </enumeration>
    <enumeration value="JAVASCRIPT">
    <annotation>
    <documentation> application/x-javascript </documentation>
    </annotation>
    </enumeration>
    <enumeration value="JSON">
    <annotation>
    <documentation> application/json </documentation>
    </annotation>
    </enumeration>
    <enumeration value="IMAGE_BITMAP">
    <annotation>
    <documentation> image/x-win-bitmap </documentation>
    </annotation>
    </enumeration>
    <enumeration value="IMAGE_BMP">
    <annotation>
    <documentation> image/bmp </documentation>
    </annotation>
    </enumeration>
    <enumeration value="IMAGE_GIF">
    <annotation>
    <documentation> image/gif </documentation>
    </annotation>
    </enumeration>
    <enumeration value="IMAGE_JPEG">
    <annotation>
    <documentation> image/jpeg </documentation>
    </annotation>
    </enumeration>
    <enumeration value="IMAGE_PHOTOSHOP">
    <annotation>
    <documentation> image/photoshop </documentation>
    </annotation>
    </enumeration>
    <enumeration value="IMAGE_PNG">
    <annotation>
    <documentation> image/png </documentation>
    </annotation>
    </enumeration>
    <enumeration value="IMAGE_TIFF">
    <annotation>
    <documentation> image/tiff </documentation>
    </annotation>
    </enumeration>
    <enumeration value="IMAGE_WBMP">
    <annotation>
    <documentation> image/vnd.wap.wbmp </documentation>
    </annotation>
    </enumeration>
    <enumeration value="M3U8">
    <annotation>
    <documentation> application/x-mpegURL </documentation>
    </annotation>
    </enumeration>
    <enumeration value="MAC_BIN_HEX_40">
    <annotation>
    <documentation> application/mac-binhex40 </documentation>
    </annotation>
    </enumeration>
    <enumeration value="MS_EXCEL">
    <annotation>
    <documentation> application/vnd.ms-excel </documentation>
    </annotation>
    </enumeration>
    <enumeration value="MS_POWERPOINT">
    <annotation>
    <documentation> application/ms-powerpoint </documentation>
    </annotation>
    </enumeration>
    <enumeration value="MS_WORD">
    <annotation>
    <documentation> application/msword </documentation>
    </annotation>
    </enumeration>
    <enumeration value="OCTET_STREAM">
    <annotation>
    <documentation> application/octet-stream </documentation>
    </annotation>
    </enumeration>
    <enumeration value="PDF">
    <annotation>
    <documentation> application/pdf </documentation>
    </annotation>
    </enumeration>
    <enumeration value="POSTSCRIPT">
    <annotation>
    <documentation> application/postscript </documentation>
    </annotation>
    </enumeration>
    <enumeration value="RN_REAL_MEDIA">
    <annotation>
    <documentation> application/vnd.rn-realmedia </documentation>
    </annotation>
    </enumeration>
    <enumeration value="RFC_822">
    <annotation>
    <documentation> message/rfc822 </documentation>
    </annotation>
    </enumeration>
    <enumeration value="RTF">
    <annotation>
    <documentation> application/rtf </documentation>
    </annotation>
    </enumeration>
    <enumeration value="TEXT_CALENDAR">
    <annotation>
    <documentation> text/calendar </documentation>
    </annotation>
    </enumeration>
    <enumeration value="TEXT_CSS">
    <annotation>
    <documentation> text/css </documentation>
    </annotation>
    </enumeration>
    <enumeration value="TEXT_CSV">
    <annotation>
    <documentation> text/csv </documentation>
    </annotation>
    </enumeration>
    <enumeration value="TEXT_HTML">
    <annotation>
    <documentation> text/html </documentation>
    </annotation>
    </enumeration>
    <enumeration value="TEXT_JAVA">
    <annotation>
    <documentation> text/java </documentation>
    </annotation>
    </enumeration>
    <enumeration value="TEXT_PLAIN">
    <annotation>
    <documentation> text/plain </documentation>
    </annotation>
    </enumeration>
    <enumeration value="VIDEO_3GPP">
    <annotation>
    <documentation> video/3gpp </documentation>
    </annotation>
    </enumeration>
    <enumeration value="VIDEO_3GPP2">
    <annotation>
    <documentation> video/3gpp2 </documentation>
    </annotation>
    </enumeration>
    <enumeration value="VIDEO_AVI">
    <annotation>
    <documentation> video/avi </documentation>
    </annotation>
    </enumeration>
    <enumeration value="VIDEO_FLV">
    <annotation>
    <documentation> video/x-flv </documentation>
    </annotation>
    </enumeration>
    <enumeration value="VIDEO_MP4">
    <annotation>
    <documentation> video/mp4 </documentation>
    </annotation>
    </enumeration>
    <enumeration value="VIDEO_MP4V_ES">
    <annotation>
    <documentation> video/mp4v-es </documentation>
    </annotation>
    </enumeration>
    <enumeration value="VIDEO_MPEG">
    <annotation>
    <documentation> video/mpeg </documentation>
    </annotation>
    </enumeration>
    <enumeration value="VIDEO_MS_ASF">
    <annotation>
    <documentation> video/x-ms-asf </documentation>
    </annotation>
    </enumeration>
    <enumeration value="VIDEO_MS_WM">
    <annotation>
    <documentation> video/x-ms-wm </documentation>
    </annotation>
    </enumeration>
    <enumeration value="VIDEO_MS_WMV">
    <annotation>
    <documentation> video/x-ms-wmv </documentation>
    </annotation>
    </enumeration>
    <enumeration value="VIDEO_MS_WVX">
    <annotation>
    <documentation> video/x-ms-wvx </documentation>
    </annotation>
    </enumeration>
    <enumeration value="VIDEO_OGG">
    <annotation>
    <documentation> video/ogg </documentation>
    </annotation>
    </enumeration>
    <enumeration value="VIDEO_QUICKTIME">
    <annotation>
    <documentation> video/x-quicktime </documentation>
    </annotation>
    </enumeration>
    <enumeration value="VIDEO_WEBM">
    <annotation>
    <documentation> video/webm </documentation>
    </annotation>
    </enumeration>
    <enumeration value="XAML">
    <annotation>
    <documentation> application/xaml+xml </documentation>
    </annotation>
    </enumeration>
    <enumeration value="XHTML">
    <annotation>
    <documentation> application/xhtml+xml </documentation>
    </annotation>
    </enumeration>
    <enumeration value="XML">
    <annotation>
    <documentation> application/xml </documentation>
    </annotation>
    </enumeration>
    <enumeration value="ZIP">
    <annotation>
    <documentation> application/zip </documentation>
    </annotation>
    </enumeration>
    </restriction>
    </simpleType>
    """
    UNKNOWN = "UNKNOWN"
    ASP = "ASP"
    AUDIO_AIFF = "AUDIO_AIFF"
    AUDIO_BASIC = "AUDIO_BASIC"
    AUDIO_FLAC = "AUDIO_FLAC"
    AUDIO_MID = "AUDIO_MID"
    AUDIO_MP3 = "AUDIO_MP3"
    AUDIO_MP4 = "AUDIO_MP4"
    AUDIO_MPEG_URL = "AUDIO_MPEG_URL"
    AUDIO_MS_WMA = "AUDIO_MS_WMA"
    AUDIO_OGG = "AUDIO_OGG"
    AUDIO_REAL_AUDIO_PLUGIN = "AUDIO_REAL_AUDIO_PLUGIN"
    AUDIO_WAV = "AUDIO_WAV"
    BINARY = "BINARY"
    DASH = "DASH"
    DIRECTOR = "DIRECTOR"
    FLASH = "FLASH"
    GRAPHIC_CONVERTER = "GRAPHIC_CONVERTER"
    JAVASCRIPT = "JAVASCRIPT"
    JSON = "JSON"
    IMAGE_BITMAP = "IMAGE_BITMAP"
    IMAGE_BMP = "IMAGE_BMP"
    IMAGE_GIF = "IMAGE_GIF"
    IMAGE_JPEG = "IMAGE_JPEG"
    IMAGE_PHOTOSHOP = "IMAGE_PHOTOSHOP"
    IMAGE_PNG = "IMAGE_PNG"
    IMAGE_TIFF = "IMAGE_TIFF"
    IMAGE_WBMP = "IMAGE_WBMP"
    M3U8 = "M3U8"
    MAC_BIN_HEX_40 = "MAC_BIN_HEX_40"
    MS_EXCEL = "MS_EXCEL"
    MS_POWERPOINT = "MS_POWERPOINT"
    MS_WORD = "MS_WORD"
    OCTET_STREAM = "OCTET_STREAM"
    PDF = "PDF"
    POSTSCRIPT = "POSTSCRIPT"
    RN_REAL_MEDIA = "RN_REAL_MEDIA"
    RFC_822 = "RFC_822"
    RTF = "RTF"
    TEXT_CALENDAR = "TEXT_CALENDAR"
    TEXT_CSS = "TEXT_CSS"
    TEXT_CSV = "TEXT_CSV"
    TEXT_HTML = "TEXT_HTML"
    TEXT_JAVA = "TEXT_JAVA"
    TEXT_PLAIN = "TEXT_PLAIN"
    VIDEO_3GPP = "VIDEO_3GPP"
    VIDEO_3GPP2 = "VIDEO_3GPP2"
    VIDEO_AVI = "VIDEO_AVI"
    VIDEO_FLV = "VIDEO_FLV"
    VIDEO_MP4 = "VIDEO_MP4"
    VIDEO_MP4V_ES = "VIDEO_MP4V_ES"
    VIDEO_MPEG = "VIDEO_MPEG"
    VIDEO_MS_ASF = "VIDEO_MS_ASF"
    VIDEO_MS_WM = "VIDEO_MS_WM"
    VIDEO_MS_WMV = "VIDEO_MS_WMV"
    VIDEO_MS_WVX = "VIDEO_MS_WVX"
    VIDEO_OGG = "VIDEO_OGG"
    VIDEO_QUICKTIME = "VIDEO_QUICKTIME"
    VIDEO_WEBM = "VIDEO_WEBM"
    XAML = "XAML"
    XHTML = "XHTML"
    XML = "XML"
    ZIP = "ZIP"


class VideoDeliveryType(str, Enum):
    """
    <simpleType name="VideoDeliveryType">
    <annotation>
    <documentation> The video delivery type. </documentation>
    </annotation>
    <restriction base="xsd:string">
    <enumeration value="UNKNOWN">
    <annotation>
    <documentation> The value returned if the actual value is not exposed by the requested API version. </documentation>
    </annotation>
    </enumeration>
    <enumeration value="PROGRESSIVE">
    <annotation>
    <documentation> Video will be served through a progressive download. </documentation>
    </annotation>
    </enumeration>
    <enumeration value="STREAMING">
    <annotation>
    <documentation> Video will be served via a streaming protocol like HLS or DASH. </documentation>
    </annotation>
    </enumeration>
    </restriction>
    </simpleType>
    """
    UNKNOWN = "UNKNOWN"
    PROGRESSIVE = "PROGRESSIVE"
    STREAMING = "STREAMING"


class ScalableType(str, Enum):
    """
    <simpleType name="ScalableType">
    <annotation>
    <documentation> The different ways a video/flash can scale. </documentation>
    </annotation>
    <restriction base="xsd:string">
    <enumeration value="UNKNOWN">
    <annotation>
    <documentation> The value returned if the actual value is not exposed by the requested API version. </documentation>
    </annotation>
    </enumeration>
    <enumeration value="NOT_SCALABLE">
    <annotation>
    <documentation> The creative should not be scaled. </documentation>
    </annotation>
    </enumeration>
    <enumeration value="RATIO_SCALABLE">
    <annotation>
    <documentation> The creative can be scaled and its aspect-ratio must be maintained. </documentation>
    </annotation>
    </enumeration>
    <enumeration value="STRETCH_SCALABLE">
    <annotation>
    <documentation> The creative can be scaled and its aspect-ratio can be distorted. </documentation>
    </annotation>
    </enumeration>
    </restriction>
    </simpleType>
    """
    UNKNOWN = "UNKNOWN"
    NOT_SCALABLE = "NOT_SCALABLE"
    RATIO_SCALABLE = "RATIO_SCALABLE"
    STRETCH_SCALABLE = "STRETCH_SCALABLE"


class VideoMetadata(GAMSOAPBaseModel):
    """
    <complexType name="VideoMetadata">
    <annotation>
    <documentation> Metadata for a video asset. </documentation>
    </annotation>
    <sequence>
    <element maxOccurs="1" minOccurs="0" name="scalableType" type="tns:ScalableType">
    <annotation>
    <documentation> The scalable type of the asset. This attribute is required. </documentation>
    </annotation>
    </element>
    <element maxOccurs="1" minOccurs="0" name="duration" type="xsd:int">
    <annotation>
    <documentation> The duration of the asset in milliseconds. This attribute is required. </documentation>
    </annotation>
    </element>
    <element maxOccurs="1" minOccurs="0" name="bitRate" type="xsd:int">
    <annotation>
    <documentation> The bit rate of the asset in kbps. If the asset can play at a range of bit rates (such as an Http Live Streaming video), then set the bit rate to zero and populate the minimum and maximum bit rate instead. </documentation>
    </annotation>
    </element>
    <element maxOccurs="1" minOccurs="0" name="minimumBitRate" type="xsd:int">
    <annotation>
    <documentation> The minimum bitrate of the video in kbps. Only set this if the asset can play at a range of bit rates. </documentation>
    </annotation>
    </element>
    <element maxOccurs="1" minOccurs="0" name="maximumBitRate" type="xsd:int">
    <annotation>
    <documentation> The maximum bitrate of the video in kbps. Only set this if the asset can play at a range of bit rates. </documentation>
    </annotation>
    </element>
    <element maxOccurs="1" minOccurs="0" name="size" type="tns:Size">
    <annotation>
    <documentation> The size (width and height) of the asset. This attribute is required. </documentation>
    </annotation>
    </element>
    <element maxOccurs="1" minOccurs="0" name="mimeType" type="tns:MimeType">
    <annotation>
    <documentation> The mime type of the asset. This attribute is required. </documentation>
    </annotation>
    </element>
    <element maxOccurs="1" minOccurs="0" name="deliveryType" type="tns:VideoDeliveryType">
    <annotation>
    <documentation> The delivery type of the asset. This attribute is required. </documentation>
    </annotation>
    </element>
    <element maxOccurs="unbounded" minOccurs="0" name="codecs" type="xsd:string">
    <annotation>
    <documentation> The codecs of the asset. This attribute is optional and defaults to an empty list. </documentation>
    </annotation>
    </element>
    </sequence>
    </complexType>
    """
    scalableType: Optional[ScalableType] = Field(None, description="The scalable type of the asset.")
    duration: Optional[int] = Field(None, description="The duration of the asset in milliseconds.")
    bitRate: Optional[int] = Field(
        None,
        description=(
            "The bit rate of the asset in kbps. If the asset can play at a range of bit rates "
            "(such as an Http Live Streaming video), then set the bit rate to zero and "
            "populate the minimum and maximum bit rate instead."
        ),
    )
    minimumBitRate: Optional[int] = Field(
        None,
        description=(
            "The minimum bitrate of the video in kbps. Only set this if the asset can play at a range of bit rates."
        ),
    )
    maximumBitRate: Optional[int] = Field(
        None,
        description=(
            "The maximum bitrate of the video in kbps. Only set this if the asset can play at a range of bit rates."
        ),
    )
    size: Optional[Size] = Field(None, description="The size (width and height) of the asset.")
    mimeType: Optional[MimeType] = Field(None, description="The mime type of the asset.")
    deliveryType: Optional[VideoDeliveryType] = Field(None, description="The delivery type of the asset.")
    codecs: Optional[List[str | None]] = Field(
        None,
        description="The codecs of the asset. This attribute is optional and defaults to an empty list."
    )


class VideoRedirectAsset(RedirectAsset):
    """
    <complexType name="VideoRedirectAsset">
    <annotation>
    <documentation> An externally-hosted video asset. </documentation>
    </annotation>
    <complexContent>
    <extension base="tns:RedirectAsset">
    <sequence>
    <element maxOccurs="1" minOccurs="0" name="metadata" type="tns:VideoMetadata">
    <annotation>
    <documentation> Metadata related to the asset. This attribute is required. </documentation>
    </annotation>
    </element>
    </sequence>
    </extension>
    </complexContent>
    </complexType>
    """
    metadata: Optional[VideoMetadata] = Field(None, description="Metadata related to the asset.")


class VideoRedirectCreative(BaseVideoCreative):
    """
    <complexType name="VideoRedirectCreative">
    <annotation>
    <documentation> A {@code Creative} that contains externally hosted video ads and is served via VAST XML. </documentation>
    </annotation>
    <complexContent>
    <extension base="tns:BaseVideoCreative">
    <sequence>
    <element maxOccurs="unbounded" minOccurs="0" name="videoAssets" type="tns:VideoRedirectAsset">
    <annotation>
    <documentation> The video creative assets. </documentation>
    </annotation>
    </element>
    <element maxOccurs="1" minOccurs="0" name="mezzanineFile" type="tns:VideoRedirectAsset">
    <annotation>
    <documentation> The high quality mezzanine video asset. </documentation>
    </annotation>
    </element>
    </sequence>
    </extension>
    </complexContent>
    </complexType>
    """
    videoAssets: Optional[List[VideoRedirectAsset]] = Field(None, description="The video creative assets.")
    mezzanineFile: Optional[VideoRedirectAsset] = Field(None, description="The high quality mezzanine video asset.")


class VastRedirectType(str, Enum):
    """
    <simpleType name="VastRedirectType">
    <annotation>
    <documentation> The types of VAST ads that a {@link VastRedirectCreative} can point to. </documentation>
    </annotation>
    <restriction base="xsd:string">
    <enumeration value="LINEAR">
    <annotation>
    <documentation> The VAST XML contains only {@code linear} ads. </documentation>
    </annotation>
    </enumeration>
    <enumeration value="NON_LINEAR">
    <annotation>
    <documentation> The VAST XML contains only {@code nonlinear} ads. </documentation>
    </annotation>
    </enumeration>
    <enumeration value="LINEAR_AND_NON_LINEAR">
    <annotation>
    <documentation> The VAST XML contains both {@code linear} and {@code nonlinear} ads. </documentation>
    </annotation>
    </enumeration>
    </restriction>
    </simpleType>
    """
    LINEAR = "LINEAR"
    NON_LINEAR = "NON_LINEAR"
    LINEAR_AND_NON_LINEAR = "LINEAR_AND_NON_LINEAR"


class VastRedirectCreative(Creative):
    """
    <complexType name="VastRedirectCreative">
    <annotation>
    <documentation> A {@code Creative} that points to an externally hosted VAST ad and is served via VAST XML as a VAST Wrapper. </documentation>
    </annotation>
    <complexContent>
    <extension base="tns:Creative">
    <sequence>
    <element maxOccurs="1" minOccurs="0" name="vastXmlUrl" type="xsd:string">
    <annotation>
    <documentation> The URL where the 3rd party VAST XML is hosted. This attribute is required. </documentation>
    </annotation>
    </element>
    <element maxOccurs="1" minOccurs="0" name="vastRedirectType" type="tns:VastRedirectType">
    <annotation>
    <documentation> The type of VAST ad that this redirects to. This attribute is required. </documentation>
    </annotation>
    </element>
    <element maxOccurs="1" minOccurs="0" name="duration" type="xsd:int">
    <annotation>
    <documentation> The duration of the VAST ad in milliseconds. This attribute is required. </documentation>
    </annotation>
    </element>
    <element maxOccurs="unbounded" minOccurs="0" name="companionCreativeIds" type="xsd:long">
    <annotation>
    <documentation> The IDs of the companion creatives that are associated with this creative. This attribute is optional. </documentation>
    </annotation>
    </element>
    <element maxOccurs="unbounded" minOccurs="0" name="trackingUrls" type="tns:ConversionEvent_TrackingUrlsMapEntry">
    <annotation>
    <documentation> A map from {@code ConversionEvent} to a list of URLs that will be pinged when the event happens. This attribute is optional. </documentation>
    </annotation>
    </element>
    <element maxOccurs="1" minOccurs="0" name="vastPreviewUrl" type="xsd:string">
    <annotation>
    <documentation> An ad tag URL that will return a preview of the VAST XML response specific to this creative. This attribute is read-only. </documentation>
    </annotation>
    </element>
    <element maxOccurs="1" minOccurs="0" name="sslScanResult" type="tns:SslScanResult">
    <annotation>
    <documentation> The SSL compatibility scan result for this creative. <p>This attribute is read-only and determined by Google. </documentation>
    </annotation>
    </element>
    <element maxOccurs="1" minOccurs="0" name="sslManualOverride" type="tns:SslManualOverride">
    <annotation>
    <documentation> The manual override for the SSL compatibility of this creative. <p>This attribute is optional and defaults to {@link SslManualOverride#NO_OVERRIDE}. </documentation>
    </annotation>
    </element>
    <element maxOccurs="1" minOccurs="0" name="isAudio" type="xsd:boolean">
    <annotation>
    <documentation> Whether the 3rd party VAST XML points to an audio ad. When true, {@link VastRedirectCreative#size} will always be 1x1. </documentation>
    </annotation>
    </element>
    </sequence>
    </extension>
    </complexContent>
    </complexType>
    """
    vastXmlUrl: Optional[str] = Field(None, description="The URL where the 3rd party VAST XML is hosted.")
    vastRedirectType: Optional[VastRedirectType] = Field(None, description="The type of VAST ad that this redirects to.")
    duration: Optional[int] = Field(None, description="The duration of the VAST ad in milliseconds.")
    companionCreativeIds: Optional[List[int]] = Field(
        None, description="The IDs of the companion creatives that are associated with this creative."
    )
    trackingUrls: Optional[List[ConversionEvent_TrackingUrlsMapEntry]] = Field(
        None,
        description="A map from {@code ConversionEvent} to a list of URLs that will be pinged when the event happens.",
    )
    vastPreviewUrl: Optional[str] = Field(
        None, description="An ad tag URL that will return a preview of the VAST XML response specific to this creative."
    )
    sslScanResult: Optional[SslScanResult] = Field(
        None,
        description=(
            "The SSL compatibility scan result for this creative. "
            "<p>This attribute is read-only and determined by Google."
        ),
    )
    sslManualOverride: Optional[SslManualOverride] = Field(
        None,
        description=(
            "The manual override for the SSL compatibility of this creative. "
            "<p>This attribute is optional and defaults to {@link SslManualOverride#NO_OVERRIDE}."
        ),
    )
    isAudio: Optional[bool] = Field(
        None,
        description=(
            "Whether the 3rd party VAST XML points to an audio ad. "
            "When true, {@link VastRedirectCreative#size} will always be 1x1."
        ),
    )


class ThirdPartyCreative(Creative):
    """
    <complexType name="ThirdPartyCreative">
    <annotation>
    <documentation> A {@code Creative} that is served by a 3rd-party vendor. </documentation>
    </annotation>
    <complexContent>
    <extension base="tns:Creative">
    <sequence>
    <element maxOccurs="1" minOccurs="0" name="snippet" type="xsd:string">
    <annotation>
    <documentation> The HTML snippet that this creative delivers. This attribute is required. </documentation>
    </annotation>
    </element>
    <element maxOccurs="1" minOccurs="0" name="expandedSnippet" type="xsd:string">
    <annotation>
    <documentation> The HTML snippet that this creative delivers with macros expanded. This attribute is read-only and is set by Google. </documentation>
    </annotation>
    </element>
    <element maxOccurs="1" minOccurs="0" name="sslScanResult" type="tns:SslScanResult">
    <annotation>
    <documentation> The SSL compatibility scan result for this creative. <p>This attribute is read-only and determined by Google. </documentation>
    </annotation>
    </element>
    <element maxOccurs="1" minOccurs="0" name="sslManualOverride" type="tns:SslManualOverride">
    <annotation>
    <documentation> The manual override for the SSL compatibility of this creative. <p>This attribute is optional and defaults to {@link SslManualOverride#NO_OVERRIDE}. </documentation>
    </annotation>
    </element>
    <element maxOccurs="1" minOccurs="0" name="lockedOrientation" type="tns:LockedOrientation">
    <annotation>
    <documentation> A locked orientation for this creative to be displayed in. </documentation>
    </annotation>
    </element>
    <element maxOccurs="1" minOccurs="0" name="isSafeFrameCompatible" type="xsd:boolean">
    <annotation>
    <documentation> Whether the {@link Creative} is compatible for SafeFrame rendering. <p>This attribute is optional and defaults to {@code true}. </documentation>
    </annotation>
    </element>
    <element maxOccurs="unbounded" minOccurs="0" name="thirdPartyImpressionTrackingUrls" type="xsd:string">
    <annotation>
    <documentation> A list of impression tracking URLs to ping when this creative is displayed. This field is optional. </documentation>
    </annotation>
    </element>
    <element maxOccurs="1" minOccurs="0" name="ampRedirectUrl" type="xsd:string">
    <annotation>
    <documentation> The URL of the AMP creative. </documentation>
    </annotation>
    </element>
    </sequence>
    </extension>
    </complexContent>
    </complexType>
    """
    snippet: Optional[str] = Field(None, description="The HTML snippet that this creative delivers.")
    expandedSnippet: Optional[str] = Field(
        None, description="The HTML snippet that this creative delivers with macros expanded. This attribute is read-only and is set by Google."
    )
    sslScanResult: Optional[SslScanResult] = Field(
        None,
        description=(
            "The SSL compatibility scan result for this creative. "
            "<p>This attribute is read-only and determined by Google."
        ),
    )
    sslManualOverride: Optional[SslManualOverride] = Field(
        None,
        description=(
            "The manual override for the SSL compatibility of this creative. "
            "<p>This attribute is optional and defaults to {@link SslManualOverride#NO_OVERRIDE}."
        ),
    )
    lockedOrientation: Optional[LockedOrientation] = Field(None, description="A locked orientation for this creative to be displayed in.")
    isSafeFrameCompatible: Optional[bool] = Field(
        None,
        description=(
            "Whether the {@link Creative} is compatible for SafeFrame rendering. "
            "<p>This attribute is optional and defaults to {@code true}."
        ),
    )
    thirdPartyImpressionTrackingUrls: Optional[List[str]] = Field(
        None,
        description="A list of impression tracking URLs to ping when this creative is displayed."
    )
    ampRedirectUrl: Optional[str] = Field(None, description="The URL of the AMP creative.")
