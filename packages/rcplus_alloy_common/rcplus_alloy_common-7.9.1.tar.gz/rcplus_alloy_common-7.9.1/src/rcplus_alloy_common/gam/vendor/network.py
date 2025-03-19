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
<complexType name="ExchangeSignupApiError">
<annotation>
<documentation> {@link ApiError} for exceptions thrown by ExchangeSignupService. </documentation>
</annotation>
<complexContent>
<extension base="tns:ApiError">
<sequence>
<element maxOccurs="1" minOccurs="0" name="reason" type="tns:ExchangeSignupApiError.Reason"/>
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
<complexType name="InventoryClientApiError">
<annotation>
<documentation> {@link ApiError} for common exceptions thrown when accessing AdSense InventoryClient. </documentation>
</annotation>
<complexContent>
<extension base="tns:ApiError">
<sequence>
<element maxOccurs="1" minOccurs="0" name="reason" type="tns:InventoryClientApiError.Reason"/>
</sequence>
</extension>
</complexContent>
</complexType>
<complexType name="LiveStreamEventSlateError">
<annotation>
<documentation> Lists all errors associated with {@link LiveStreamEvent} slate creative id. </documentation>
</annotation>
<complexContent>
<extension base="tns:ApiError">
<sequence>
<element maxOccurs="1" minOccurs="0" name="reason" type="tns:LiveStreamEventSlateError.Reason"/>
</sequence>
</extension>
</complexContent>
</complexType>
<complexType name="McmError">
<annotation>
<documentation> An error for multiple customer management. </documentation>
</annotation>
<complexContent>
<extension base="tns:ApiError">
<sequence>
<element maxOccurs="1" minOccurs="0" name="reason" type="tns:McmError.Reason"/>
</sequence>
</extension>
</complexContent>
</complexType>
<complexType name="Network">
<annotation>
<documentation> {@code Network} represents a network. </documentation>
</annotation>
<sequence>
<element maxOccurs="1" minOccurs="0" name="id" type="xsd:long">
<annotation>
<documentation> The unique ID of the {@code Network}. This value is readonly and is assigned by Google. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="displayName" type="xsd:string">
<annotation>
<documentation> The display name of the network. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="networkCode" type="xsd:string">
<annotation>
<documentation> The network code. If the current login has access to multiple networks, then the network code must be provided in the SOAP request headers for all requests. Otherwise, it is optional to provide the network code in the SOAP headers. This field is read-only. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="propertyCode" type="xsd:string">
<annotation>
<documentation> The property code. This field is read-only. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="timeZone" type="xsd:string">
<annotation>
<documentation> The time zone associated with the delivery of orders and reporting. This field is read-only. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="currencyCode" type="xsd:string">
<annotation>
<documentation> The primary currency code. This field is read-only. </documentation>
</annotation>
</element>
<element maxOccurs="unbounded" minOccurs="0" name="secondaryCurrencyCodes" type="xsd:string">
<annotation>
<documentation> Currencies that can be used as an alternative to the {@link Network#currencyCode} for trafficking {@link LineItem line items}. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="effectiveRootAdUnitId" type="xsd:string">
<annotation>
<documentation> The {@link AdUnit#id} of the top most ad unit to which descendant ad units can be added. Should be used for the {@link AdUnit#parentId} when first building inventory hierarchy. This field is read-only. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="isTest" type="xsd:boolean">
<annotation>
<documentation> Whether this is a test network. This field is read-only. </documentation>
</annotation>
</element>
</sequence>
</complexType>
<complexType name="NetworkError">
<annotation>
<documentation> An error for a network. </documentation>
</annotation>
<complexContent>
<extension base="tns:ApiError">
<sequence>
<element maxOccurs="1" minOccurs="0" name="reason" type="tns:NetworkError.Reason"/>
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
<complexType name="RequestError">
<annotation>
<documentation> Encapsulates the generic errors thrown when there's an error with user request. </documentation>
</annotation>
<complexContent>
<extension base="tns:ApiError">
<sequence>
<element maxOccurs="1" minOccurs="0" name="reason" type="tns:RequestError.Reason"/>
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
<complexType name="ThirdPartyDataDeclaration">
<annotation>
<documentation> Represents a set of declarations about what (if any) third party companies are associated with a given creative. <p>This can be set at the network level, as a default for all creatives, or overridden for a particular creative. </documentation>
</annotation>
<sequence>
<element maxOccurs="1" minOccurs="0" name="declarationType" type="tns:DeclarationType"/>
<element maxOccurs="unbounded" minOccurs="0" name="thirdPartyCompanyIds" type="xsd:long"/>
</sequence>
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
<complexType name="UrlError">
<annotation>
<documentation> Common errors for URLs. </documentation>
</annotation>
<complexContent>
<extension base="tns:ApiError">
<sequence>
<element maxOccurs="1" minOccurs="0" name="reason" type="tns:UrlError.Reason"/>
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
<simpleType name="ExchangeSignupApiError.Reason">
<annotation>
<documentation> Potential reasons for ExchangeSignupService errors </documentation>
</annotation>
<restriction base="xsd:string">
<enumeration value="ADSENSE_ACCOUNT_CREATION_ERROR"/>
<enumeration value="ADSENSE_ACCOUNT_ALREADY_HAS_EXCHANGE"/>
<enumeration value="FAILED_TO_ADD_WEBSITE_TO_PROPERTY"/>
<enumeration value="FAILED_TO_CREATE_LINK_FOR_NEW_ACCOUNT"/>
<enumeration value="CANNOT_CREATE_NEW_ACCOUNT_FOR_MAPPED_CUSTOMER"/>
<enumeration value="FAILED_TO_CREATE_EXCHANGE_SETTINGS"/>
<enumeration value="DUPLICATE_PRODUCT_TYPE"/>
<enumeration value="INVALID_SIGNUP_PRODUCT"/>
<enumeration value="UNKNOWN_PRODUCT"/>
<enumeration value="BAD_SITE_VERIFICATION_UPDATE_REQUEST"/>
<enumeration value="NO_EXCHANGE_ACCOUNT"/>
<enumeration value="SINGLE_SYNDICATION_PRODUCT"/>
<enumeration value="ACCOUNT_NOT_YET_READY"/>
<enumeration value="MULTIPLE_ADSENSE_ACCOUNTS_NOT_ALLOWED"/>
<enumeration value="MISSING_LEGAL_ENTITY_NAME"/>
<enumeration value="MISSING_ACTIVE_BILLING_PROFILE"/>
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
<simpleType name="InventoryClientApiError.Reason">
<annotation>
<documentation> Potential reasons for errors calling InventoryClient </documentation>
</annotation>
<restriction base="xsd:string">
<enumeration value="ACCESS_DENIED"/>
<enumeration value="ADSENSE_AUTH_ERROR"/>
<enumeration value="ADSENSE_RPC_ERROR"/>
<enumeration value="DOMAIN_NO_SCHEME"/>
<enumeration value="DOMAIN_INVALID_HOST"/>
<enumeration value="DOMAIN_INVALID_TLD"/>
<enumeration value="DOMAIN_ONE_STRING_AND_PUBLIC_SUFFIX"/>
<enumeration value="DOMAIN_INVALID_INPUT"/>
<enumeration value="DOMAIN_NO_PUBLIC_SUFFIX"/>
<enumeration value="UNKNOWN_ERROR"/>
</restriction>
</simpleType>
<simpleType name="LiveStreamEventSlateError.Reason">
<annotation>
<documentation> Describes reasons for {@code LiveStreamEventSlateError}. </documentation>
</annotation>
<restriction base="xsd:string">
<enumeration value="INVALID_SLATE_CREATIVE_ID">
<annotation>
<documentation> The slate creative ID does not correspond to a slate creative. </documentation>
</annotation>
</enumeration>
<enumeration value="LIVE_STREAM_EVENT_SLATE_CREATIVE_ID_REQUIRED">
<annotation>
<documentation> The required field live stream event slate is not set. <p>There must either be a slate creative ID assigned to the live stream event or a valid network level slate selected. </documentation>
</annotation>
</enumeration>
<enumeration value="MISSING_SOURCE_FOR_SLATE">
<annotation>
<documentation> The slate does not have a videoSourceUrl or assetSourcePath. </documentation>
</annotation>
</enumeration>
<enumeration value="INVALID_SLATE_TYPE">
<annotation>
<documentation> The slate is of an invalid type. </documentation>
</annotation>
</enumeration>
<enumeration value="CANNOT_CHANGE_SLATE_VIDEO_SOURCE_URL">
<annotation>
<documentation> The slate video source url cannot change. </documentation>
</annotation>
</enumeration>
<enumeration value="UNKNOWN">
<annotation>
<documentation> The value returned if the actual value is not exposed by the requested API version. </documentation>
</annotation>
</enumeration>
</restriction>
</simpleType>
<simpleType name="McmError.Reason">
<annotation>
<documentation> Possible reasons for {@link McmError} </documentation>
</annotation>
<restriction base="xsd:string">
<enumeration value="UNKNOWN">
<annotation>
<documentation> The value returned if the actual value is not exposed by the requested API version. </documentation>
</annotation>
</enumeration>
<enumeration value="REVENUE_SHARE_PERCENT_OUTSIDE_RANGE">
<annotation>
<documentation> An MCM parent revenue share must be between 0 to 100_000L in millis. </documentation>
</annotation>
</enumeration>
<enumeration value="RESELLER_PARENT_REVENUE_SHARE_IS_NOT_100_PERCENT">
<annotation>
<documentation> An MCM reseller parent revenue share must be 100_000L in millis. </documentation>
</annotation>
</enumeration>
<enumeration value="MI_PARENT_REVENUE_SHARE_IS_NOT_100_PERCENT">
<annotation>
<documentation> An MCM Manage Inventory parent revenue share must be 100_000L in millis. </documentation>
</annotation>
</enumeration>
<enumeration value="DUPLICATE_CHILD_PUBLISHER_NETWORK_CODE">
<annotation>
<documentation> The network code is used by another child publisher. </documentation>
</annotation>
</enumeration>
<enumeration value="DUPLICATE_CHILD_PUBLISHER_ACTIVE_EMAIL">
<annotation>
<documentation> The email is used by another active child publisher. </documentation>
</annotation>
</enumeration>
<enumeration value="CHILD_NETWORK_DISAPPROVED">
<annotation>
<documentation> The MCM child network has been disapproved by Google. </documentation>
</annotation>
</enumeration>
<enumeration value="MANAGE_INVENTORY_UNSUPPORTED_IN_RESELLER_NETWORK">
<annotation>
<documentation> Manage inventory is not supported in reseller network. </documentation>
</annotation>
</enumeration>
<enumeration value="CANNOT_SEND_INVITATION_TO_MCM_PARENT">
<annotation>
<documentation> Cannot send MCM invitation to a MCM parent. </documentation>
</annotation>
</enumeration>
<enumeration value="CANNOT_SEND_INVITATION_TO_NETWORK_WITH_RESELLER_PARENT">
<annotation>
<documentation> A non-reseller MCM parent cannot send invitation to child which has another reseller parent. </documentation>
</annotation>
</enumeration>
<enumeration value="CANNOT_SEND_INVITATION_TO_SELF">
<annotation>
<documentation> Cannot send MCM invitation to self. </documentation>
</annotation>
</enumeration>
<enumeration value="CANNOT_CLOSE_MCM_WITH_ACTIVE_CHILDREN">
<annotation>
<documentation> An MCM parent network cannot be disabled as parent with active children. </documentation>
</annotation>
</enumeration>
<enumeration value="CANNOT_TURN_CHILD_INTO_PARENT_WITH_ACTIVE_INVITATION">
<annotation>
<documentation> Cannot turn on MCM feature flag on a MCM Child network with active invitations. </documentation>
</annotation>
</enumeration>
<enumeration value="MISSING_NETWORK_EXCHANGE_ACCOUNT">
<annotation>
<documentation> An Ad Exchange account is required for an MCM parent network. </documentation>
</annotation>
</enumeration>
</restriction>
</simpleType>
<simpleType name="NetworkError.Reason">
<annotation>
<documentation> Possible reasons for {@link NetworkError} </documentation>
</annotation>
<restriction base="xsd:string">
<enumeration value="UNKNOWN">
<annotation>
<documentation> The value returned if the actual value is not exposed by the requested API version. </documentation>
</annotation>
</enumeration>
<enumeration value="MULTI_CURRENCY_NOT_SUPPORTED">
<annotation>
<documentation> Multi-currency support is not enabled for this network. This is an Ad Manager 360 feature. </documentation>
</annotation>
</enumeration>
<enumeration value="UNSUPPORTED_CURRENCY">
<annotation>
<documentation> Currency provided is not supported. </documentation>
</annotation>
</enumeration>
<enumeration value="NETWORK_CURRENCY_CANNOT_BE_SAME_AS_SECONDARY">
<annotation>
<documentation> The network currency cannot also be specified as a secondary currency. </documentation>
</annotation>
</enumeration>
<enumeration value="DEPRECATED_DATA_TRANSFER_CONFIG_EVENT_TYPE">
<annotation>
<documentation> The data transfer config cannot have a deprecated event type. </documentation>
</annotation>
</enumeration>
<enumeration value="DELEGATION_CHILD_NETWORK_CANNOT_BECOME_A_PARENT">
<annotation>
<documentation> An MCM child network cannot become a parent network. </documentation>
</annotation>
</enumeration>
<enumeration value="DELEGATION_PARENT_NETWORK_CANNOT_BECOME_A_CHILD">
<annotation>
<documentation> An MCM parent network cannot become a child of another network. </documentation>
</annotation>
</enumeration>
<enumeration value="CANNOT_ADD_SAME_NETWORK_AS_DELEGATION_CHILD">
<annotation>
<documentation> In MCM, a network cannot become a parent of itself. </documentation>
</annotation>
</enumeration>
<enumeration value="MAX_APPROVED_DELEGATION_CHILD_NETWORKS_EXCEEDED">
<annotation>
<documentation> The MCM parent network has exceeded the system limit of child networks. </documentation>
</annotation>
</enumeration>
<enumeration value="MAX_PENDING_DELEGATION_CHILD_NETWORKS_EXCEEDED">
<annotation>
<documentation> The MCM parent network has exceeded the system limit of child networks pending approval. </documentation>
</annotation>
</enumeration>
<enumeration value="CHILD_NETWORK_ALREADY_EXISTS">
<annotation>
<documentation> The network is already being managed by the parent network for MCM. </documentation>
</annotation>
</enumeration>
<enumeration value="CHILD_NETWORK_CANNOT_BE_DISAPPROVED">
<annotation>
<documentation> A child network must not be disapproved. </documentation>
</annotation>
</enumeration>
<enumeration value="IN_PARENT_DELEGATION_UNSUPPORTED_FOR_NETWORK">
<annotation>
<documentation> Only Ad Manager 360 networks are allowed to manage the inventory of other networks. </documentation>
</annotation>
</enumeration>
<enumeration value="ERROR_REENABLING_AD_EXCHANGE_ON_MCM_CHILD">
<annotation>
<documentation> When an MCM child network self-signsup for ad exchange but disconnects from the parent, then tries to re-enable again, this indicates that there was an error in re-enabling ad exchange. </documentation>
</annotation>
</enumeration>
<enumeration value="ERROR_SETTING_SITE_SERVING_MODE_ON_MCM_CHILD">
<annotation>
<documentation> The error shown when there is an issue setting the approved site serving field when re-enabling or disabling ad exchange on an MCM child. </documentation>
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
<simpleType name="RequestError.Reason">
<restriction base="xsd:string">
<enumeration value="UNKNOWN">
<annotation>
<documentation> Error reason is unknown. </documentation>
</annotation>
</enumeration>
<enumeration value="INVALID_INPUT">
<annotation>
<documentation> Invalid input. </documentation>
</annotation>
</enumeration>
<enumeration value="UNSUPPORTED_VERSION">
<annotation>
<documentation> The api version in the request has been discontinued. Please update to the new AdWords API version. </documentation>
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
<simpleType name="UrlError.Reason">
<annotation>
<documentation> Reasons for inventory url errors. </documentation>
</annotation>
<restriction base="xsd:string">
<enumeration value="CANNOT_USE_RESERVED_URL">
<annotation>
<documentation> The URL has been reserved, and not available for usage. </documentation>
</annotation>
</enumeration>
<enumeration value="CANNOT_USE_GOOGLE_URL">
<annotation>
<documentation> The URL belongs to Google, and not available for usage. </documentation>
</annotation>
</enumeration>
<enumeration value="INVALID_URL">
<annotation>
<documentation> The URL is invalid. </documentation>
</annotation>
</enumeration>
<enumeration value="UNKNOWN">
<annotation>
<documentation> The value returned if the actual value is not exposed by the requested API version. </documentation>
</annotation>
</enumeration>
</restriction>
</simpleType>
<element name="getAllNetworks">
<annotation>
<documentation> Returns the list of {@link Network} objects to which the current login has access. <p>Intended to be used without a network code in the SOAP header when the login may have more than one network associated with it. </documentation>
</annotation>
<complexType>
<sequence/>
</complexType>
</element>
<element name="getAllNetworksResponse">
<complexType>
<sequence>
<element maxOccurs="unbounded" minOccurs="0" name="rval" type="tns:Network"/>
</sequence>
</complexType>
</element>
<element name="ApiExceptionFault" type="tns:ApiException">
<annotation>
<documentation> A fault element of type ApiException. </documentation>
</annotation>
</element>
<element name="getCurrentNetwork">
<annotation>
<documentation> Returns the current network for which requests are being made. </documentation>
</annotation>
<complexType>
<sequence/>
</complexType>
</element>
<element name="getCurrentNetworkResponse">
<complexType>
<sequence>
<element maxOccurs="1" minOccurs="0" name="rval" type="tns:Network"/>
</sequence>
</complexType>
</element>
<element name="getDefaultThirdPartyDataDeclaration">
<annotation>
<documentation> Returns the default {@link ThirdPartyDataDeclaration} for this network. If this setting has never been updated on your network, then this API response will be empty. </documentation>
</annotation>
<complexType>
<sequence/>
</complexType>
</element>
<element name="getDefaultThirdPartyDataDeclarationResponse">
<complexType>
<sequence>
<element maxOccurs="1" minOccurs="0" name="rval" type="tns:ThirdPartyDataDeclaration"/>
</sequence>
</complexType>
</element>
<element name="makeTestNetwork">
<annotation>
<documentation> Creates a new blank network for testing purposes using the current login. <p>Each login(i.e. email address) can only have one test network. Data from any of your existing networks will not be transferred to the new test network. Once the test network is created, the test network can be used in the API by supplying the {@link Network#networkCode} in the SOAP header or by logging into the Ad Manager UI. <p>Test networks are limited in the following ways: <ul> <li>Test networks cannot serve ads. <li>Because test networks cannot serve ads, reports will always come back without data. <li>Since forecasting requires serving history, forecast service results will be faked. See {@link ForecastService} for more info. <li>Test networks are, by default, Ad Manager networks and don't have any features from Ad Manager 360. To have additional features turned on, please contact your account manager. <li>Test networks are limited to 10,000 objects per entity type. </ul> </documentation>
</annotation>
<complexType>
<sequence/>
</complexType>
</element>
<element name="makeTestNetworkResponse">
<complexType>
<sequence>
<element maxOccurs="1" minOccurs="0" name="rval" type="tns:Network"/>
</sequence>
</complexType>
</element>
<element name="updateNetwork">
<annotation>
<documentation> Updates the specified network. Currently, only the network display name can be updated. </documentation>
</annotation>
<complexType>
<sequence>
<element maxOccurs="1" minOccurs="0" name="network" type="tns:Network"/>
</sequence>
</complexType>
</element>
<element name="updateNetworkResponse">
<complexType>
<sequence>
<element maxOccurs="1" minOccurs="0" name="rval" type="tns:Network"/>
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
<wsdl:message name="getAllNetworksRequest">
<wsdl:part element="tns:getAllNetworks" name="parameters"/>
</wsdl:message>
<wsdl:message name="getAllNetworksResponse">
<wsdl:part element="tns:getAllNetworksResponse" name="parameters"/>
</wsdl:message>
<wsdl:message name="ApiException">
<wsdl:part element="tns:ApiExceptionFault" name="ApiException"/>
</wsdl:message>
<wsdl:message name="getCurrentNetworkRequest">
<wsdl:part element="tns:getCurrentNetwork" name="parameters"/>
</wsdl:message>
<wsdl:message name="getCurrentNetworkResponse">
<wsdl:part element="tns:getCurrentNetworkResponse" name="parameters"/>
</wsdl:message>
<wsdl:message name="getDefaultThirdPartyDataDeclarationRequest">
<wsdl:part element="tns:getDefaultThirdPartyDataDeclaration" name="parameters"/>
</wsdl:message>
<wsdl:message name="getDefaultThirdPartyDataDeclarationResponse">
<wsdl:part element="tns:getDefaultThirdPartyDataDeclarationResponse" name="parameters"/>
</wsdl:message>
<wsdl:message name="makeTestNetworkRequest">
<wsdl:part element="tns:makeTestNetwork" name="parameters"/>
</wsdl:message>
<wsdl:message name="makeTestNetworkResponse">
<wsdl:part element="tns:makeTestNetworkResponse" name="parameters"/>
</wsdl:message>
<wsdl:message name="updateNetworkRequest">
<wsdl:part element="tns:updateNetwork" name="parameters"/>
</wsdl:message>
<wsdl:message name="updateNetworkResponse">
<wsdl:part element="tns:updateNetworkResponse" name="parameters"/>
</wsdl:message>
<wsdl:portType name="NetworkServiceInterface">
<wsdl:documentation> Provides operations for retrieving information related to the publisher's networks. This service can be used to obtain the list of all networks that the current login has access to, or to obtain information about a specific network. </wsdl:documentation>
<wsdl:operation name="getAllNetworks">
<wsdl:documentation> Returns the list of {@link Network} objects to which the current login has access. <p>Intended to be used without a network code in the SOAP header when the login may have more than one network associated with it. </wsdl:documentation>
<wsdl:input message="tns:getAllNetworksRequest" name="getAllNetworksRequest"/>
<wsdl:output message="tns:getAllNetworksResponse" name="getAllNetworksResponse"/>
<wsdl:fault message="tns:ApiException" name="ApiException"/>
</wsdl:operation>
<wsdl:operation name="getCurrentNetwork">
<wsdl:documentation> Returns the current network for which requests are being made. </wsdl:documentation>
<wsdl:input message="tns:getCurrentNetworkRequest" name="getCurrentNetworkRequest"/>
<wsdl:output message="tns:getCurrentNetworkResponse" name="getCurrentNetworkResponse"/>
<wsdl:fault message="tns:ApiException" name="ApiException"/>
</wsdl:operation>
<wsdl:operation name="getDefaultThirdPartyDataDeclaration">
<wsdl:documentation> Returns the default {@link ThirdPartyDataDeclaration} for this network. If this setting has never been updated on your network, then this API response will be empty. </wsdl:documentation>
<wsdl:input message="tns:getDefaultThirdPartyDataDeclarationRequest" name="getDefaultThirdPartyDataDeclarationRequest"/>
<wsdl:output message="tns:getDefaultThirdPartyDataDeclarationResponse" name="getDefaultThirdPartyDataDeclarationResponse"/>
<wsdl:fault message="tns:ApiException" name="ApiException"/>
</wsdl:operation>
<wsdl:operation name="makeTestNetwork">
<wsdl:documentation> Creates a new blank network for testing purposes using the current login. <p>Each login(i.e. email address) can only have one test network. Data from any of your existing networks will not be transferred to the new test network. Once the test network is created, the test network can be used in the API by supplying the {@link Network#networkCode} in the SOAP header or by logging into the Ad Manager UI. <p>Test networks are limited in the following ways: <ul> <li>Test networks cannot serve ads. <li>Because test networks cannot serve ads, reports will always come back without data. <li>Since forecasting requires serving history, forecast service results will be faked. See {@link ForecastService} for more info. <li>Test networks are, by default, Ad Manager networks and don't have any features from Ad Manager 360. To have additional features turned on, please contact your account manager. <li>Test networks are limited to 10,000 objects per entity type. </ul> </wsdl:documentation>
<wsdl:input message="tns:makeTestNetworkRequest" name="makeTestNetworkRequest"/>
<wsdl:output message="tns:makeTestNetworkResponse" name="makeTestNetworkResponse"/>
<wsdl:fault message="tns:ApiException" name="ApiException"/>
</wsdl:operation>
<wsdl:operation name="updateNetwork">
<wsdl:documentation> Updates the specified network. Currently, only the network display name can be updated. </wsdl:documentation>
<wsdl:input message="tns:updateNetworkRequest" name="updateNetworkRequest"/>
<wsdl:output message="tns:updateNetworkResponse" name="updateNetworkResponse"/>
<wsdl:fault message="tns:ApiException" name="ApiException"/>
</wsdl:operation>
</wsdl:portType>
<wsdl:binding name="NetworkServiceSoapBinding" type="tns:NetworkServiceInterface">
<wsdlsoap:binding style="document" transport="http://schemas.xmlsoap.org/soap/http"/>
<wsdl:operation name="getAllNetworks">
<wsdlsoap:operation soapAction=""/>
<wsdl:input name="getAllNetworksRequest">
<wsdlsoap:header message="tns:RequestHeader" part="RequestHeader" use="literal"/>
<wsdlsoap:body use="literal"/>
</wsdl:input>
<wsdl:output name="getAllNetworksResponse">
<wsdlsoap:header message="tns:ResponseHeader" part="ResponseHeader" use="literal"/>
<wsdlsoap:body use="literal"/>
</wsdl:output>
<wsdl:fault name="ApiException">
<wsdlsoap:fault name="ApiException" use="literal"/>
</wsdl:fault>
</wsdl:operation>
<wsdl:operation name="getCurrentNetwork">
<wsdlsoap:operation soapAction=""/>
<wsdl:input name="getCurrentNetworkRequest">
<wsdlsoap:header message="tns:RequestHeader" part="RequestHeader" use="literal"/>
<wsdlsoap:body use="literal"/>
</wsdl:input>
<wsdl:output name="getCurrentNetworkResponse">
<wsdlsoap:header message="tns:ResponseHeader" part="ResponseHeader" use="literal"/>
<wsdlsoap:body use="literal"/>
</wsdl:output>
<wsdl:fault name="ApiException">
<wsdlsoap:fault name="ApiException" use="literal"/>
</wsdl:fault>
</wsdl:operation>
<wsdl:operation name="getDefaultThirdPartyDataDeclaration">
<wsdlsoap:operation soapAction=""/>
<wsdl:input name="getDefaultThirdPartyDataDeclarationRequest">
<wsdlsoap:header message="tns:RequestHeader" part="RequestHeader" use="literal"/>
<wsdlsoap:body use="literal"/>
</wsdl:input>
<wsdl:output name="getDefaultThirdPartyDataDeclarationResponse">
<wsdlsoap:header message="tns:ResponseHeader" part="ResponseHeader" use="literal"/>
<wsdlsoap:body use="literal"/>
</wsdl:output>
<wsdl:fault name="ApiException">
<wsdlsoap:fault name="ApiException" use="literal"/>
</wsdl:fault>
</wsdl:operation>
<wsdl:operation name="makeTestNetwork">
<wsdlsoap:operation soapAction=""/>
<wsdl:input name="makeTestNetworkRequest">
<wsdlsoap:header message="tns:RequestHeader" part="RequestHeader" use="literal"/>
<wsdlsoap:body use="literal"/>
</wsdl:input>
<wsdl:output name="makeTestNetworkResponse">
<wsdlsoap:header message="tns:ResponseHeader" part="ResponseHeader" use="literal"/>
<wsdlsoap:body use="literal"/>
</wsdl:output>
<wsdl:fault name="ApiException">
<wsdlsoap:fault name="ApiException" use="literal"/>
</wsdl:fault>
</wsdl:operation>
<wsdl:operation name="updateNetwork">
<wsdlsoap:operation soapAction=""/>
<wsdl:input name="updateNetworkRequest">
<wsdlsoap:header message="tns:RequestHeader" part="RequestHeader" use="literal"/>
<wsdlsoap:body use="literal"/>
</wsdl:input>
<wsdl:output name="updateNetworkResponse">
<wsdlsoap:header message="tns:ResponseHeader" part="ResponseHeader" use="literal"/>
<wsdlsoap:body use="literal"/>
</wsdl:output>
<wsdl:fault name="ApiException">
<wsdlsoap:fault name="ApiException" use="literal"/>
</wsdl:fault>
</wsdl:operation>
</wsdl:binding>
<wsdl:service name="NetworkService">
<wsdl:port binding="tns:NetworkServiceSoapBinding" name="NetworkServiceInterfacePort">
<wsdlsoap:address location="https://ads.google.com/apis/ads/publisher/v202408/NetworkService"/>
</wsdl:port>
</wsdl:service>
</wsdl:definitions>
"""

from __future__ import annotations
from typing import Optional, List

from pydantic import Field

from .common import (
    GAMSOAPBaseModel,
)


class Network(GAMSOAPBaseModel):
    """
    <complexType name="Network">
    <annotation>
    <documentation> {@code Network} represents a network. </documentation>
    </annotation>
    <sequence>
    <element maxOccurs="1" minOccurs="0" name="id" type="xsd:long">
    <annotation>
    <documentation> The unique ID of the {@code Network}. This value is readonly and is assigned by Google. </documentation>
    </annotation>
    </element>
    <element maxOccurs="1" minOccurs="0" name="displayName" type="xsd:string">
    <annotation>
    <documentation> The display name of the network. </documentation>
    </annotation>
    </element>
    <element maxOccurs="1" minOccurs="0" name="networkCode" type="xsd:string">
    <annotation>
    <documentation> The network code. If the current login has access to multiple networks, then the network code must be provided in the SOAP request headers for all requests. Otherwise, it is optional to provide the network code in the SOAP headers. This field is read-only. </documentation>
    </annotation>
    </element>
    <element maxOccurs="1" minOccurs="0" name="propertyCode" type="xsd:string">
    <annotation>
    <documentation> The property code. This field is read-only. </documentation>
    </annotation>
    </element>
    <element maxOccurs="1" minOccurs="0" name="timeZone" type="xsd:string">
    <annotation>
    <documentation> The time zone associated with the delivery of orders and reporting. This field is read-only. </documentation>
    </annotation>
    </element>
    <element maxOccurs="1" minOccurs="0" name="currencyCode" type="xsd:string">
    <annotation>
    <documentation> The primary currency code. This field is read-only. </documentation>
    </annotation>
    </element>
    <element maxOccurs="unbounded" minOccurs="0" name="secondaryCurrencyCodes" type="xsd:string">
    <annotation>
    <documentation> Currencies that can be used as an alternative to the {@link Network#currencyCode} for trafficking {@link LineItem line items}. </documentation>
    </annotation>
    </element>
    <element maxOccurs="1" minOccurs="0" name="effectiveRootAdUnitId" type="xsd:string">
    <annotation>
    <documentation> The {@link AdUnit#id} of the top most ad unit to which descendant ad units can be added. Should be used for the {@link AdUnit#parentId} when first building inventory hierarchy. This field is read-only. </documentation>
    </annotation>
    </element>
    <element maxOccurs="1" minOccurs="0" name="isTest" type="xsd:boolean">
    <annotation>
    <documentation> Whether this is a test network. This field is read-only. </documentation>
    </annotation>
    </element>
    </sequence>
    </complexType>
    """
    id: Optional[int] = Field(
        None, description="The unique ID of the Network. This value is readonly and is assigned by Google."
    )
    displayName: Optional[str] = Field(None, description="The display name of the network.")
    networkCode: Optional[str] = Field(
        None,
        description="The network code. If the current login has access to multiple networks, then the network code must be provided in the SOAP request headers for all requests. Otherwise, it is optional to provide the network code in the SOAP headers. This field is read-only.",
    )
    propertyCode: Optional[str] = Field(None, description="The property code. This field is read-only.")
    timeZone: Optional[str] = Field(None, description="The time zone associated with the delivery of orders and reporting. This field is read-only.")
    currencyCode: Optional[str] = Field(None, description="The primary currency code. This field is read-only.")
    secondaryCurrencyCodes: Optional[List[str]] = Field(
        None, description="Currencies that can be used as an alternative to the Network.currencyCode for trafficking LineItem line items."
    )
    effectiveRootAdUnitId: Optional[str] = Field(
        None,
        description="The AdUnit.id of the top most ad unit to which descendant ad units can be added. Should be used for the AdUnit.parentId when first building inventory hierarchy. This field is read-only.",
    )
    isTest: Optional[bool] = Field(None, description="Whether this is a test network. This field is read-only.")
