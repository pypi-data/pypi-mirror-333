# ruff: noqa: E501
"""
<!--  Generated file, do not edit  -->
<!--  Copyright 2024 Google Inc. All Rights Reserved  -->
<wsdl:definitions xmlns:tns="https://www.google.com/apis/ads/publisher/v202408" xmlns:wsdl="http://schemas.xmlsoap.org/wsdl/" xmlns:wsdlsoap="http://schemas.xmlsoap.org/wsdl/soap/" xmlns:xsd="http://www.w3.org/2001/XMLSchema" targetNamespace="https://www.google.com/apis/ads/publisher/v202408">
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
<complexType name="ActivateCustomTargetingKeys">
<annotation>
<documentation> The action used for activating inactive (i.e. deleted) {@link CustomTargetingKey} objects. </documentation>
</annotation>
<complexContent>
<extension base="tns:CustomTargetingKeyAction">
<sequence/>
</extension>
</complexContent>
</complexType>
<complexType name="ActivateCustomTargetingValues">
<annotation>
<documentation> The action used for activating inactive (i.e. deleted) {@link CustomTargetingValue} objects. </documentation>
</annotation>
<complexContent>
<extension base="tns:CustomTargetingValueAction">
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
<complexType abstract="true" name="CustomTargetingKeyAction">
<annotation>
<documentation> Represents the actions that can be performed on {@link CustomTargetingKey} objects. </documentation>
</annotation>
<sequence/>
</complexType>
<complexType name="CustomTargetingKey">
<annotation>
<documentation> {@code CustomTargetingKey} represents a key used for custom targeting. </documentation>
</annotation>
<sequence>
<element maxOccurs="1" minOccurs="0" name="id" type="xsd:long">
<annotation>
<documentation> The ID of the {@code CustomTargetingKey}. This value is readonly and is populated by Google. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="name" type="xsd:string">
<annotation>
<documentation> Name of the key. Keys can contain up to 10 characters each. You can use alphanumeric characters and symbols other than the following: ", ', =, !, +, #, *, ~, ;, ^, (, ), <, >, [, ], the white space character. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="displayName" type="xsd:string">
<annotation>
<documentation> Descriptive name for the key. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="type" type="tns:CustomTargetingKey.Type">
<annotation>
<documentation> Indicates whether users will select from predefined values or create new targeting values, while specifying targeting criteria for a line item. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="status" type="tns:CustomTargetingKey.Status">
<annotation>
<documentation> Status of the {@code CustomTargetingKey}. This field is read-only. A key can be activated and deactivated by calling {@link CustomTargetingService#performCustomTargetingKeyAction}. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="reportableType" type="tns:ReportableType">
<annotation>
<documentation> Reportable state of a {@CustomTargetingKey} as defined in {@link ReportableType}. </documentation>
</annotation>
</element>
</sequence>
</complexType>
<complexType name="CustomTargetingKeyPage">
<annotation>
<documentation> Captures a page of {@link CustomTargetingKey} objects. </documentation>
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
<element maxOccurs="unbounded" minOccurs="0" name="results" type="tns:CustomTargetingKey">
<annotation>
<documentation> The collection of custom targeting keys contained within this page. </documentation>
</annotation>
</element>
</sequence>
</complexType>
<complexType abstract="true" name="CustomTargetingValueAction">
<annotation>
<documentation> Represents the actions that can be performed on {@link CustomTargetingValue} objects. </documentation>
</annotation>
<sequence/>
</complexType>
<complexType name="CustomTargetingValue">
<annotation>
<documentation> {@code CustomTargetingValue} represents a value used for custom targeting. </documentation>
</annotation>
<sequence>
<element maxOccurs="1" minOccurs="0" name="customTargetingKeyId" type="xsd:long">
<annotation>
<documentation> The ID of the {@code CustomTargetingKey} for which this is the value. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="id" type="xsd:long">
<annotation>
<documentation> The ID of the {@code CustomTargetingValue}. This value is readonly and is populated by Google. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="name" type="xsd:string">
<annotation>
<documentation> Name of the value. Values can contain up to 40 characters each. You can use alphanumeric characters and symbols other than the following: ", ', =, !, +, #, *, ~, ;, ^, (, ), <, >, [, ]. Values are not data-specific; all values are treated as string. For example, instead of using "age>=18 AND <=34", try "18-34" </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="displayName" type="xsd:string">
<annotation>
<documentation> Descriptive name for the value. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="matchType" type="tns:CustomTargetingValue.MatchType">
<annotation>
<documentation> The way in which the {@link CustomTargetingValue#name} strings will be matched. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="status" type="tns:CustomTargetingValue.Status">
<annotation>
<documentation> Status of the {@code CustomTargetingValue}. This field is read-only. A value can be activated and deactivated by calling {@link CustomTargetingService#performCustomTargetingValueAction}. </documentation>
</annotation>
</element>
</sequence>
</complexType>
<complexType name="CustomTargetingValuePage">
<annotation>
<documentation> Captures a page of {@link CustomTargetingValue} objects. </documentation>
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
<element maxOccurs="unbounded" minOccurs="0" name="results" type="tns:CustomTargetingValue">
<annotation>
<documentation> The collection of custom targeting keys contained within this page. </documentation>
</annotation>
</element>
</sequence>
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
<complexType name="DeleteCustomTargetingKeys">
<annotation>
<documentation> Represents the delete action that can be performed on {@link CustomTargetingKey} objects. Deleting a key will not delete the {@link CustomTargetingValue} objects associated with it. Also, if a custom targeting key that has been deleted is recreated, any previous custom targeting values associated with it that were not deleted will continue to exist. </documentation>
</annotation>
<complexContent>
<extension base="tns:CustomTargetingKeyAction">
<sequence/>
</extension>
</complexContent>
</complexType>
<complexType name="DeleteCustomTargetingValues">
<annotation>
<documentation> Represents the delete action that can be performed on {@link CustomTargetingValue} objects. </documentation>
</annotation>
<complexContent>
<extension base="tns:CustomTargetingValueAction">
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
<simpleType name="CustomTargetingKey.Status">
<annotation>
<documentation> Describes the statuses for {@code CustomTargetingKey} objects. </documentation>
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
<enumeration value="UNKNOWN">
<annotation>
<documentation> The value returned if the actual value is not exposed by the requested API version. </documentation>
</annotation>
</enumeration>
</restriction>
</simpleType>
<simpleType name="CustomTargetingKey.Type">
<annotation>
<documentation> Specifies the types for {@code CustomTargetingKey} objects. </documentation>
</annotation>
<restriction base="xsd:string">
<enumeration value="PREDEFINED">
<annotation>
<documentation> Target audiences by criteria values that are defined in advance. </documentation>
</annotation>
</enumeration>
<enumeration value="FREEFORM">
<annotation>
<documentation> Target audiences by adding criteria values when creating line items. </documentation>
</annotation>
</enumeration>
</restriction>
</simpleType>
<simpleType name="CustomTargetingValue.MatchType">
<annotation>
<documentation> Represents the ways in which {@link CustomTargetingValue#name} strings will be matched with ad requests. </documentation>
</annotation>
<restriction base="xsd:string">
<enumeration value="EXACT">
<annotation>
<documentation> Used for exact matching. For example, the targeting value {@code car=honda} will only match to the ad request {@code car=honda}. </documentation>
</annotation>
</enumeration>
<enumeration value="BROAD">
<annotation>
<documentation> Used for lenient matching when at least one of the words in the ad request matches the targeted value. The targeting value {@code car=honda} will match to ad requests containing the word {@code honda}. So ad requests {@code car=honda} or {@code car=honda civic} or {@code car=buy honda} or {@code car=how much does a honda cost} will all have the line item delivered. <p>This match type can not be used within an audience segment rule. </documentation>
</annotation>
</enumeration>
<enumeration value="PREFIX">
<annotation>
<documentation> Used for 'starts with' matching when the first few characters in the ad request match all of the characters in the targeted value. The targeting value {@code car=honda} will match to ad requests {@code car=honda} or {@code car=hondas for sale} but not to {@code car=I want a honda}. </documentation>
</annotation>
</enumeration>
<enumeration value="BROAD_PREFIX">
<annotation>
<documentation> This is a combination of {@code MatchType#BROAD} and {@code MatchType#PREFIX} matching. The targeting value {@code car=honda} will match to ad requests that contain words that start with the characters in the targeted value, for example with {@code car=civic hondas}. <p>This match type can not be used within an audience segment rule. </documentation>
</annotation>
</enumeration>
<enumeration value="SUFFIX">
<annotation>
<documentation> Used for 'ends with' matching when the last characters in the ad request match all of the characters in the targeted value. The targeting value {@code car=honda} will match with ad requests {@code car=honda} or {@code car=I want a honda} but not to {@code car=hondas for sale}. <p>This match type can not be used within line item targeting. </documentation>
</annotation>
</enumeration>
<enumeration value="CONTAINS">
<annotation>
<documentation> Used for 'within' matching when the string in the ad request contains the string in the targeted value. The targeting value {@code car=honda} will match with ad requests {@code car=honda}, {@code car=I want a honda}, and also with {@code car=hondas for sale}, but not with {@code car=misspelled hond a}. <p>This match type can not be used within line item targeting. </documentation>
</annotation>
</enumeration>
<enumeration value="UNKNOWN">
<annotation>
<documentation> The value returned if the actual value is not exposed by the requested API version. </documentation>
</annotation>
</enumeration>
</restriction>
</simpleType>
<simpleType name="CustomTargetingValue.Status">
<annotation>
<documentation> Describes the statuses for {@code CustomTargetingValue} objects. </documentation>
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
<simpleType name="ReportableType">
<annotation>
<documentation> Represents the reportable state of a custom key. </documentation>
</annotation>
<restriction base="xsd:string">
<enumeration value="UNKNOWN">
<annotation>
<documentation> The value returned if the actual value is not exposed by the requested API version. </documentation>
</annotation>
</enumeration>
<enumeration value="ON">
<annotation>
<documentation> Available for reporting in the Ad Manager query tool. </documentation>
</annotation>
</enumeration>
<enumeration value="OFF">
<annotation>
<documentation> Not available for reporting in the Ad Manager query tool. </documentation>
</annotation>
</enumeration>
<enumeration value="CUSTOM_DIMENSION">
<annotation>
<documentation> Custom dimension available for reporting in the AdManager query tool. </documentation>
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
<element name="createCustomTargetingKeys">
<annotation>
<documentation> Creates new {@link CustomTargetingKey} objects. <p>The following fields are required: <ul> <li>{@link CustomTargetingKey#name} <li>{@link CustomTargetingKey#type} </ul> </documentation>
</annotation>
<complexType>
<sequence>
<element maxOccurs="unbounded" minOccurs="0" name="keys" type="tns:CustomTargetingKey"/>
</sequence>
</complexType>
</element>
<element name="createCustomTargetingKeysResponse">
<complexType>
<sequence>
<element maxOccurs="unbounded" minOccurs="0" name="rval" type="tns:CustomTargetingKey"/>
</sequence>
</complexType>
</element>
<element name="ApiExceptionFault" type="tns:ApiException">
<annotation>
<documentation> A fault element of type ApiException. </documentation>
</annotation>
</element>
<element name="createCustomTargetingValues">
<annotation>
<documentation> Creates new {@link CustomTargetingValue} objects. <p>The following fields are required: <ul> <li>{@link CustomTargetingValue#customTargetingKeyId} <li>{@link CustomTargetingValue#name} </ul> </documentation>
</annotation>
<complexType>
<sequence>
<element maxOccurs="unbounded" minOccurs="0" name="values" type="tns:CustomTargetingValue"/>
</sequence>
</complexType>
</element>
<element name="createCustomTargetingValuesResponse">
<complexType>
<sequence>
<element maxOccurs="unbounded" minOccurs="0" name="rval" type="tns:CustomTargetingValue"/>
</sequence>
</complexType>
</element>
<element name="getCustomTargetingKeysByStatement">
<annotation>
<documentation> Gets a {@link CustomTargetingKeyPage} of {@link CustomTargetingKey} objects that satisfy the given {@link Statement#query}. The following fields are supported for filtering: <table> <tr> <th scope="col">PQL Property</th> <th scope="col">Object Property</th> </tr> <tr> <tr> <td>{@code id}</td> <td>{@link CustomTargetingKey#id}</td> </tr> <tr> <td>{@code name}</td> <td>{@link CustomTargetingKey#name}</td> </tr> <tr> <td>{@code displayName}</td> <td>{@link CustomTargetingKey#displayName}</td> </tr> <tr> <td>{@code type}</td> <td>{@link CustomTargetingKey#type}</td> </tr> </table> </documentation>
</annotation>
<complexType>
<sequence>
<element maxOccurs="1" minOccurs="0" name="filterStatement" type="tns:Statement"/>
</sequence>
</complexType>
</element>
<element name="getCustomTargetingKeysByStatementResponse">
<complexType>
<sequence>
<element maxOccurs="1" minOccurs="0" name="rval" type="tns:CustomTargetingKeyPage"/>
</sequence>
</complexType>
</element>
<element name="getCustomTargetingValuesByStatement">
<annotation>
<documentation> Gets a {@link CustomTargetingValuePage} of {@link CustomTargetingValue} objects that satisfy the given {@link Statement#query}. <p>The {@code WHERE} clause in the {@link Statement#query} must always contain {@link CustomTargetingValue#customTargetingKeyId} as one of its columns in a way that it is AND'ed with the rest of the query. So, if you want to retrieve values for a known set of key ids, valid {@link Statement#query} would look like: <ol> <li>"WHERE customTargetingKeyId IN ('17','18','19')" retrieves all values that are associated with keys having ids 17, 18, 19. <li>"WHERE customTargetingKeyId = '17' AND name = 'red'" retrieves values that are associated with keys having id 17 and value name is 'red'. </ol> <p>The following fields are supported for filtering: <table> <tr> <th scope="col">PQL Property</th> <th scope="col">Object Property</th> </tr> <tr> <td>{@code id}</td> <td>{@link CustomTargetingValue#id}</td> </tr> <tr> <td>{@code customTargetingKeyId}</td> <td>{@link CustomTargetingValue#customTargetingKeyId}</td> </tr> <tr> <td>{@code name}</td> <td>{@link CustomTargetingValue#name}</td> </tr> <tr> <td>{@code displayName}</td> <td>{@link CustomTargetingValue#displayName}</td> </tr> <tr> <td>{@code matchType}</td> <td>{@link CustomTargetingValue#matchType}</td> </tr> </table> </documentation>
</annotation>
<complexType>
<sequence>
<element maxOccurs="1" minOccurs="0" name="filterStatement" type="tns:Statement"/>
</sequence>
</complexType>
</element>
<element name="getCustomTargetingValuesByStatementResponse">
<complexType>
<sequence>
<element maxOccurs="1" minOccurs="0" name="rval" type="tns:CustomTargetingValuePage"/>
</sequence>
</complexType>
</element>
<element name="performCustomTargetingKeyAction">
<annotation>
<documentation> Performs actions on {@link CustomTargetingKey} objects that match the given {@link Statement#query}. </documentation>
</annotation>
<complexType>
<sequence>
<element maxOccurs="1" minOccurs="0" name="customTargetingKeyAction" type="tns:CustomTargetingKeyAction"/>
<element maxOccurs="1" minOccurs="0" name="filterStatement" type="tns:Statement"/>
</sequence>
</complexType>
</element>
<element name="performCustomTargetingKeyActionResponse">
<complexType>
<sequence>
<element maxOccurs="1" minOccurs="0" name="rval" type="tns:UpdateResult"/>
</sequence>
</complexType>
</element>
<element name="performCustomTargetingValueAction">
<annotation>
<documentation> Performs actions on {@link CustomTargetingValue} objects that match the given {@link Statement#query}. </documentation>
</annotation>
<complexType>
<sequence>
<element maxOccurs="1" minOccurs="0" name="customTargetingValueAction" type="tns:CustomTargetingValueAction"/>
<element maxOccurs="1" minOccurs="0" name="filterStatement" type="tns:Statement"/>
</sequence>
</complexType>
</element>
<element name="performCustomTargetingValueActionResponse">
<complexType>
<sequence>
<element maxOccurs="1" minOccurs="0" name="rval" type="tns:UpdateResult"/>
</sequence>
</complexType>
</element>
<element name="updateCustomTargetingKeys">
<annotation>
<documentation> Updates the specified {@link CustomTargetingKey} objects. </documentation>
</annotation>
<complexType>
<sequence>
<element maxOccurs="unbounded" minOccurs="0" name="keys" type="tns:CustomTargetingKey"/>
</sequence>
</complexType>
</element>
<element name="updateCustomTargetingKeysResponse">
<complexType>
<sequence>
<element maxOccurs="unbounded" minOccurs="0" name="rval" type="tns:CustomTargetingKey"/>
</sequence>
</complexType>
</element>
<element name="updateCustomTargetingValues">
<annotation>
<documentation> Updates the specified {@link CustomTargetingValue} objects. </documentation>
</annotation>
<complexType>
<sequence>
<element maxOccurs="unbounded" minOccurs="0" name="values" type="tns:CustomTargetingValue"/>
</sequence>
</complexType>
</element>
<element name="updateCustomTargetingValuesResponse">
<complexType>
<sequence>
<element maxOccurs="unbounded" minOccurs="0" name="rval" type="tns:CustomTargetingValue"/>
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
<wsdl:message name="createCustomTargetingKeysRequest">
<wsdl:part element="tns:createCustomTargetingKeys" name="parameters"/>
</wsdl:message>
<wsdl:message name="createCustomTargetingKeysResponse">
<wsdl:part element="tns:createCustomTargetingKeysResponse" name="parameters"/>
</wsdl:message>
<wsdl:message name="ApiException">
<wsdl:part element="tns:ApiExceptionFault" name="ApiException"/>
</wsdl:message>
<wsdl:message name="createCustomTargetingValuesRequest">
<wsdl:part element="tns:createCustomTargetingValues" name="parameters"/>
</wsdl:message>
<wsdl:message name="createCustomTargetingValuesResponse">
<wsdl:part element="tns:createCustomTargetingValuesResponse" name="parameters"/>
</wsdl:message>
<wsdl:message name="getCustomTargetingKeysByStatementRequest">
<wsdl:part element="tns:getCustomTargetingKeysByStatement" name="parameters"/>
</wsdl:message>
<wsdl:message name="getCustomTargetingKeysByStatementResponse">
<wsdl:part element="tns:getCustomTargetingKeysByStatementResponse" name="parameters"/>
</wsdl:message>
<wsdl:message name="getCustomTargetingValuesByStatementRequest">
<wsdl:part element="tns:getCustomTargetingValuesByStatement" name="parameters"/>
</wsdl:message>
<wsdl:message name="getCustomTargetingValuesByStatementResponse">
<wsdl:part element="tns:getCustomTargetingValuesByStatementResponse" name="parameters"/>
</wsdl:message>
<wsdl:message name="performCustomTargetingKeyActionRequest">
<wsdl:part element="tns:performCustomTargetingKeyAction" name="parameters"/>
</wsdl:message>
<wsdl:message name="performCustomTargetingKeyActionResponse">
<wsdl:part element="tns:performCustomTargetingKeyActionResponse" name="parameters"/>
</wsdl:message>
<wsdl:message name="performCustomTargetingValueActionRequest">
<wsdl:part element="tns:performCustomTargetingValueAction" name="parameters"/>
</wsdl:message>
<wsdl:message name="performCustomTargetingValueActionResponse">
<wsdl:part element="tns:performCustomTargetingValueActionResponse" name="parameters"/>
</wsdl:message>
<wsdl:message name="updateCustomTargetingKeysRequest">
<wsdl:part element="tns:updateCustomTargetingKeys" name="parameters"/>
</wsdl:message>
<wsdl:message name="updateCustomTargetingKeysResponse">
<wsdl:part element="tns:updateCustomTargetingKeysResponse" name="parameters"/>
</wsdl:message>
<wsdl:message name="updateCustomTargetingValuesRequest">
<wsdl:part element="tns:updateCustomTargetingValues" name="parameters"/>
</wsdl:message>
<wsdl:message name="updateCustomTargetingValuesResponse">
<wsdl:part element="tns:updateCustomTargetingValuesResponse" name="parameters"/>
</wsdl:message>
<wsdl:portType name="CustomTargetingServiceInterface">
<wsdl:documentation> Provides operations for creating, updating and retrieving {@link CustomTargetingKey} and {@link CustomTargetingValue} objects. </wsdl:documentation>
<wsdl:operation name="createCustomTargetingKeys">
<wsdl:documentation> Creates new {@link CustomTargetingKey} objects. <p>The following fields are required: <ul> <li>{@link CustomTargetingKey#name} <li>{@link CustomTargetingKey#type} </ul> </wsdl:documentation>
<wsdl:input message="tns:createCustomTargetingKeysRequest" name="createCustomTargetingKeysRequest"/>
<wsdl:output message="tns:createCustomTargetingKeysResponse" name="createCustomTargetingKeysResponse"/>
<wsdl:fault message="tns:ApiException" name="ApiException"/>
</wsdl:operation>
<wsdl:operation name="createCustomTargetingValues">
<wsdl:documentation> Creates new {@link CustomTargetingValue} objects. <p>The following fields are required: <ul> <li>{@link CustomTargetingValue#customTargetingKeyId} <li>{@link CustomTargetingValue#name} </ul> </wsdl:documentation>
<wsdl:input message="tns:createCustomTargetingValuesRequest" name="createCustomTargetingValuesRequest"/>
<wsdl:output message="tns:createCustomTargetingValuesResponse" name="createCustomTargetingValuesResponse"/>
<wsdl:fault message="tns:ApiException" name="ApiException"/>
</wsdl:operation>
<wsdl:operation name="getCustomTargetingKeysByStatement">
<wsdl:documentation> Gets a {@link CustomTargetingKeyPage} of {@link CustomTargetingKey} objects that satisfy the given {@link Statement#query}. The following fields are supported for filtering: <table> <tr> <th scope="col">PQL Property</th> <th scope="col">Object Property</th> </tr> <tr> <tr> <td>{@code id}</td> <td>{@link CustomTargetingKey#id}</td> </tr> <tr> <td>{@code name}</td> <td>{@link CustomTargetingKey#name}</td> </tr> <tr> <td>{@code displayName}</td> <td>{@link CustomTargetingKey#displayName}</td> </tr> <tr> <td>{@code type}</td> <td>{@link CustomTargetingKey#type}</td> </tr> </table> </wsdl:documentation>
<wsdl:input message="tns:getCustomTargetingKeysByStatementRequest" name="getCustomTargetingKeysByStatementRequest"/>
<wsdl:output message="tns:getCustomTargetingKeysByStatementResponse" name="getCustomTargetingKeysByStatementResponse"/>
<wsdl:fault message="tns:ApiException" name="ApiException"/>
</wsdl:operation>
<wsdl:operation name="getCustomTargetingValuesByStatement">
<wsdl:documentation> Gets a {@link CustomTargetingValuePage} of {@link CustomTargetingValue} objects that satisfy the given {@link Statement#query}. <p>The {@code WHERE} clause in the {@link Statement#query} must always contain {@link CustomTargetingValue#customTargetingKeyId} as one of its columns in a way that it is AND'ed with the rest of the query. So, if you want to retrieve values for a known set of key ids, valid {@link Statement#query} would look like: <ol> <li>"WHERE customTargetingKeyId IN ('17','18','19')" retrieves all values that are associated with keys having ids 17, 18, 19. <li>"WHERE customTargetingKeyId = '17' AND name = 'red'" retrieves values that are associated with keys having id 17 and value name is 'red'. </ol> <p>The following fields are supported for filtering: <table> <tr> <th scope="col">PQL Property</th> <th scope="col">Object Property</th> </tr> <tr> <td>{@code id}</td> <td>{@link CustomTargetingValue#id}</td> </tr> <tr> <td>{@code customTargetingKeyId}</td> <td>{@link CustomTargetingValue#customTargetingKeyId}</td> </tr> <tr> <td>{@code name}</td> <td>{@link CustomTargetingValue#name}</td> </tr> <tr> <td>{@code displayName}</td> <td>{@link CustomTargetingValue#displayName}</td> </tr> <tr> <td>{@code matchType}</td> <td>{@link CustomTargetingValue#matchType}</td> </tr> </table> </wsdl:documentation>
<wsdl:input message="tns:getCustomTargetingValuesByStatementRequest" name="getCustomTargetingValuesByStatementRequest"/>
<wsdl:output message="tns:getCustomTargetingValuesByStatementResponse" name="getCustomTargetingValuesByStatementResponse"/>
<wsdl:fault message="tns:ApiException" name="ApiException"/>
</wsdl:operation>
<wsdl:operation name="performCustomTargetingKeyAction">
<wsdl:documentation> Performs actions on {@link CustomTargetingKey} objects that match the given {@link Statement#query}. </wsdl:documentation>
<wsdl:input message="tns:performCustomTargetingKeyActionRequest" name="performCustomTargetingKeyActionRequest"/>
<wsdl:output message="tns:performCustomTargetingKeyActionResponse" name="performCustomTargetingKeyActionResponse"/>
<wsdl:fault message="tns:ApiException" name="ApiException"/>
</wsdl:operation>
<wsdl:operation name="performCustomTargetingValueAction">
<wsdl:documentation> Performs actions on {@link CustomTargetingValue} objects that match the given {@link Statement#query}. </wsdl:documentation>
<wsdl:input message="tns:performCustomTargetingValueActionRequest" name="performCustomTargetingValueActionRequest"/>
<wsdl:output message="tns:performCustomTargetingValueActionResponse" name="performCustomTargetingValueActionResponse"/>
<wsdl:fault message="tns:ApiException" name="ApiException"/>
</wsdl:operation>
<wsdl:operation name="updateCustomTargetingKeys">
<wsdl:documentation> Updates the specified {@link CustomTargetingKey} objects. </wsdl:documentation>
<wsdl:input message="tns:updateCustomTargetingKeysRequest" name="updateCustomTargetingKeysRequest"/>
<wsdl:output message="tns:updateCustomTargetingKeysResponse" name="updateCustomTargetingKeysResponse"/>
<wsdl:fault message="tns:ApiException" name="ApiException"/>
</wsdl:operation>
<wsdl:operation name="updateCustomTargetingValues">
<wsdl:documentation> Updates the specified {@link CustomTargetingValue} objects. </wsdl:documentation>
<wsdl:input message="tns:updateCustomTargetingValuesRequest" name="updateCustomTargetingValuesRequest"/>
<wsdl:output message="tns:updateCustomTargetingValuesResponse" name="updateCustomTargetingValuesResponse"/>
<wsdl:fault message="tns:ApiException" name="ApiException"/>
</wsdl:operation>
</wsdl:portType>
<wsdl:binding name="CustomTargetingServiceSoapBinding" type="tns:CustomTargetingServiceInterface">
<wsdlsoap:binding style="document" transport="http://schemas.xmlsoap.org/soap/http"/>
<wsdl:operation name="createCustomTargetingKeys">
<wsdlsoap:operation soapAction=""/>
<wsdl:input name="createCustomTargetingKeysRequest">
<wsdlsoap:header message="tns:RequestHeader" part="RequestHeader" use="literal"/>
<wsdlsoap:body use="literal"/>
</wsdl:input>
<wsdl:output name="createCustomTargetingKeysResponse">
<wsdlsoap:header message="tns:ResponseHeader" part="ResponseHeader" use="literal"/>
<wsdlsoap:body use="literal"/>
</wsdl:output>
<wsdl:fault name="ApiException">
<wsdlsoap:fault name="ApiException" use="literal"/>
</wsdl:fault>
</wsdl:operation>
<wsdl:operation name="createCustomTargetingValues">
<wsdlsoap:operation soapAction=""/>
<wsdl:input name="createCustomTargetingValuesRequest">
<wsdlsoap:header message="tns:RequestHeader" part="RequestHeader" use="literal"/>
<wsdlsoap:body use="literal"/>
</wsdl:input>
<wsdl:output name="createCustomTargetingValuesResponse">
<wsdlsoap:header message="tns:ResponseHeader" part="ResponseHeader" use="literal"/>
<wsdlsoap:body use="literal"/>
</wsdl:output>
<wsdl:fault name="ApiException">
<wsdlsoap:fault name="ApiException" use="literal"/>
</wsdl:fault>
</wsdl:operation>
<wsdl:operation name="getCustomTargetingKeysByStatement">
<wsdlsoap:operation soapAction=""/>
<wsdl:input name="getCustomTargetingKeysByStatementRequest">
<wsdlsoap:header message="tns:RequestHeader" part="RequestHeader" use="literal"/>
<wsdlsoap:body use="literal"/>
</wsdl:input>
<wsdl:output name="getCustomTargetingKeysByStatementResponse">
<wsdlsoap:header message="tns:ResponseHeader" part="ResponseHeader" use="literal"/>
<wsdlsoap:body use="literal"/>
</wsdl:output>
<wsdl:fault name="ApiException">
<wsdlsoap:fault name="ApiException" use="literal"/>
</wsdl:fault>
</wsdl:operation>
<wsdl:operation name="getCustomTargetingValuesByStatement">
<wsdlsoap:operation soapAction=""/>
<wsdl:input name="getCustomTargetingValuesByStatementRequest">
<wsdlsoap:header message="tns:RequestHeader" part="RequestHeader" use="literal"/>
<wsdlsoap:body use="literal"/>
</wsdl:input>
<wsdl:output name="getCustomTargetingValuesByStatementResponse">
<wsdlsoap:header message="tns:ResponseHeader" part="ResponseHeader" use="literal"/>
<wsdlsoap:body use="literal"/>
</wsdl:output>
<wsdl:fault name="ApiException">
<wsdlsoap:fault name="ApiException" use="literal"/>
</wsdl:fault>
</wsdl:operation>
<wsdl:operation name="performCustomTargetingKeyAction">
<wsdlsoap:operation soapAction=""/>
<wsdl:input name="performCustomTargetingKeyActionRequest">
<wsdlsoap:header message="tns:RequestHeader" part="RequestHeader" use="literal"/>
<wsdlsoap:body use="literal"/>
</wsdl:input>
<wsdl:output name="performCustomTargetingKeyActionResponse">
<wsdlsoap:header message="tns:ResponseHeader" part="ResponseHeader" use="literal"/>
<wsdlsoap:body use="literal"/>
</wsdl:output>
<wsdl:fault name="ApiException">
<wsdlsoap:fault name="ApiException" use="literal"/>
</wsdl:fault>
</wsdl:operation>
<wsdl:operation name="performCustomTargetingValueAction">
<wsdlsoap:operation soapAction=""/>
<wsdl:input name="performCustomTargetingValueActionRequest">
<wsdlsoap:header message="tns:RequestHeader" part="RequestHeader" use="literal"/>
<wsdlsoap:body use="literal"/>
</wsdl:input>
<wsdl:output name="performCustomTargetingValueActionResponse">
<wsdlsoap:header message="tns:ResponseHeader" part="ResponseHeader" use="literal"/>
<wsdlsoap:body use="literal"/>
</wsdl:output>
<wsdl:fault name="ApiException">
<wsdlsoap:fault name="ApiException" use="literal"/>
</wsdl:fault>
</wsdl:operation>
<wsdl:operation name="updateCustomTargetingKeys">
<wsdlsoap:operation soapAction=""/>
<wsdl:input name="updateCustomTargetingKeysRequest">
<wsdlsoap:header message="tns:RequestHeader" part="RequestHeader" use="literal"/>
<wsdlsoap:body use="literal"/>
</wsdl:input>
<wsdl:output name="updateCustomTargetingKeysResponse">
<wsdlsoap:header message="tns:ResponseHeader" part="ResponseHeader" use="literal"/>
<wsdlsoap:body use="literal"/>
</wsdl:output>
<wsdl:fault name="ApiException">
<wsdlsoap:fault name="ApiException" use="literal"/>
</wsdl:fault>
</wsdl:operation>
<wsdl:operation name="updateCustomTargetingValues">
<wsdlsoap:operation soapAction=""/>
<wsdl:input name="updateCustomTargetingValuesRequest">
<wsdlsoap:header message="tns:RequestHeader" part="RequestHeader" use="literal"/>
<wsdlsoap:body use="literal"/>
</wsdl:input>
<wsdl:output name="updateCustomTargetingValuesResponse">
<wsdlsoap:header message="tns:ResponseHeader" part="ResponseHeader" use="literal"/>
<wsdlsoap:body use="literal"/>
</wsdl:output>
<wsdl:fault name="ApiException">
<wsdlsoap:fault name="ApiException" use="literal"/>
</wsdl:fault>
</wsdl:operation>
</wsdl:binding>
<wsdl:service name="CustomTargetingService">
<wsdl:port binding="tns:CustomTargetingServiceSoapBinding" name="CustomTargetingServiceInterfacePort">
<wsdlsoap:address location="https://ads.google.com/apis/ads/publisher/v202408/CustomTargetingService"/>
</wsdl:port>
</wsdl:service>
</wsdl:definitions>
"""

from __future__ import annotations
from typing import Optional
from enum import Enum

from pydantic import Field

from rcplus_alloy_common.gam.vendor.common import (
    GAMSOAPBaseModel,
)


class CustomTargetingKeyType(str, Enum):
    """
    <simpleType name="CustomTargetingKey.Type">
    <annotation>
    <documentation> Specifies the types for {@code CustomTargetingKey} objects. </documentation>
    </annotation>
    <restriction base="xsd:string">
    <enumeration value="PREDEFINED">
    <annotation>
    <documentation> Target audiences by criteria values that are defined in advance. </documentation>
    </annotation>
    </enumeration>
    <enumeration value="FREEFORM">
    <annotation>
    <documentation> Target audiences by adding criteria values when creating line items. </documentation>
    </annotation>
    </enumeration>
    </restriction>
    </simpleType>
    """
    PREDEFINED = "PREDEFINED"
    FREEFORM = "FREEFORM"


class CustomTargetingKeyStatus(str, Enum):
    """
    <simpleType name="CustomTargetingKey.Status">
    <annotation>
    <documentation> Describes the statuses for {@code CustomTargetingKey} objects. </documentation>
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
    <enumeration value="UNKNOWN">
    <annotation>
    <documentation> The value returned if the actual value is not exposed by the requested API version. </documentation>
    </annotation>
    </enumeration>
    </restriction>
    </simpleType>
    """
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    UNKNOWN = "UNKNOWN"


class ReportableType(str, Enum):
    """
    <simpleType name="ReportableType">
    <annotation>
    <documentation> Represents the reportable state of a custom key. </documentation>
    </annotation>
    <restriction base="xsd:string">
    <enumeration value="UNKNOWN">
    <annotation>
    <documentation> The value returned if the actual value is not exposed by the requested API version. </documentation>
    </annotation>
    </enumeration>
    <enumeration value="ON">
    <annotation>
    <documentation> Available for reporting in the Ad Manager query tool. </documentation>
    </annotation>
    </enumeration>
    <enumeration value="OFF">
    <annotation>
    <documentation> Not available for reporting in the Ad Manager query tool. </documentation>
    </annotation>
    </enumeration>
    <enumeration value="CUSTOM_DIMENSION">
    <annotation>
    <documentation> Custom dimension available for reporting in the AdManager query tool. </documentation>
    </annotation>
    </enumeration>
    </restriction>
    </simpleType>
    """
    UNKNOWN = "UNKNOWN"
    ON = "ON"
    OFF = "OFF"
    CUSTOM_DIMENSION = "CUSTOM_DIMENSION"


class CustomTargetingKey(GAMSOAPBaseModel):
    """
    <complexType name="CustomTargetingKey">
    <annotation>
    <documentation> {@code CustomTargetingKey} represents a key used for custom targeting. </documentation>
    </annotation>
    <sequence>
    <element maxOccurs="1" minOccurs="0" name="id" type="xsd:long">
    <annotation>
    <documentation> The ID of the {@code CustomTargetingKey}. This value is readonly and is populated by Google. </documentation>
    </annotation>
    </element>
    <element maxOccurs="1" minOccurs="0" name="name" type="xsd:string">
    <annotation>
    <documentation> Name of the key. Keys can contain up to 10 characters each. You can use alphanumeric characters and symbols other than the following: ", ', =, !, +, #, *, ~, ;, ^, (, ), <, >, [, ], the white space character. </documentation>
    </annotation>
    </element>
    <element maxOccurs="1" minOccurs="0" name="displayName" type="xsd:string">
    <annotation>
    <documentation> Descriptive name for the key. </documentation>
    </annotation>
    </element>
    <element maxOccurs="1" minOccurs="0" name="type" type="tns:CustomTargetingKey.Type">
    <annotation>
    <documentation> Indicates whether users will select from predefined values or create new targeting values, while specifying targeting criteria for a line item. </documentation>
    </annotation>
    </element>
    <element maxOccurs="1" minOccurs="0" name="status" type="tns:CustomTargetingKey.Status">
    <annotation>
    <documentation> Status of the {@code CustomTargetingKey}. This field is read-only. A key can be activated and deactivated by calling {@link CustomTargetingService#performCustomTargetingKeyAction}. </documentation>
    </annotation>
    </element>
    <element maxOccurs="1" minOccurs="0" name="reportableType" type="tns:ReportableType">
    <annotation>
    <documentation> Reportable state of a {@CustomTargetingKey} as defined in {@link ReportableType}. </documentation>
    </annotation>
    </element>
    </sequence>
    </complexType>
    """
    id: Optional[int] = Field(
        None,
        description="The ID of the CustomTargetingKey. This value is readonly and is populated by Google.",
    )
    name: Optional[str] = Field(
        None,
        description="Name of the key. Keys can contain up to 10 characters each. You can use alphanumeric characters and symbols other than the following: ', =, !, +, #, *, ~, ;, ^, (, ), <, >, [, ], the white space character.",
    )
    displayName: Optional[str] = Field(
        None, description="Descriptive name for the key."
    )
    type: Optional[CustomTargetingKeyType] = Field(
        None,
        description="Indicates whether users will select from predefined values or create new targeting values, while specifying targeting criteria for a line item.",
    )
    status: Optional[CustomTargetingKeyStatus] = Field(
        None,
        description="Status of the CustomTargetingKey. This field is read-only. A key can be activated and deactivated by calling CustomTargetingService#performCustomTargetingKeyAction.",
    )
    reportableType: Optional[ReportableType] = Field(
        None, description="Reportable state of a CustomTargetingKey as defined in ReportableType."
    )


class CustomTargetingValueMatchType(str, Enum):
    """
    <simpleType name="CustomTargetingValue.MatchType">
    <annotation>
    <documentation> Represents the ways in which {@link CustomTargetingValue#name} strings will be matched with ad requests. </documentation>
    </annotation>
    <restriction base="xsd:string">
    <enumeration value="EXACT">
    <annotation>
    <documentation> Used for exact matching. For example, the targeting value {@code car=honda} will only match to the ad request {@code car=honda}. </documentation>
    </annotation>
    </enumeration>
    <enumeration value="BROAD">
    <annotation>
    <documentation> Used for lenient matching when at least one of the words in the ad request matches the targeted value. The targeting value {@code car=honda} will match to ad requests containing the word {@code honda}. So ad requests {@code car=honda} or {@code car=honda civic} or {@code car=buy honda} or {@code car=how much does a honda cost} will all have the line item delivered. <p>This match type can not be used within an audience segment rule. </documentation>
    </annotation>
    </enumeration>
    <enumeration value="PREFIX">
    <annotation>
    <documentation> Used for 'starts with' matching when the first few characters in the ad request match all of the characters in the targeted value. The targeting value {@code car=honda} will match to ad requests {@code car=honda} or {@code car=hondas for sale} but not to {@code car=I want a honda}. </documentation>
    </annotation>
    </enumeration>
    <enumeration value="BROAD_PREFIX">
    <annotation>
    <documentation> This is a combination of {@code MatchType#BROAD} and {@code MatchType#PREFIX} matching. The targeting value {@code car=honda} will match to ad requests that contain words that start with the characters in the targeted value, for example with {@code car=civic hondas}. <p>This match type can not be used within an audience segment rule. </documentation>
    </annotation>
    </enumeration>
    <enumeration value="SUFFIX">
    <annotation>
    <documentation> Used for 'ends with' matching when the last characters in the ad request match all of the characters in the targeted value. The targeting value {@code car=honda} will match with ad requests {@code car=honda} or {@code car=I want a honda} but not to {@code car=hondas for sale}. <p>This match type can not be used within line item targeting. </documentation>
    </annotation>
    </enumeration>
    <enumeration value="CONTAINS">
    <annotation>
    <documentation> Used for 'within' matching when the string in the ad request contains the string in the targeted value. The targeting value {@code car=honda} will match with ad requests {@code car=honda}, {@code car=I want a honda}, and also with {@code car=hondas for sale}, but not with {@code car=misspelled hond a}. <p>This match type can not be used within line item targeting. </documentation>
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
    EXACT = "EXACT"
    BROAD = "BROAD"
    PREFIX = "PREFIX"
    BROAD_PREFIX = "BROAD_PREFIX"
    SUFFIX = "SUFFIX"
    CONTAINS = "CONTAINS"
    UNKNOWN = "UNKNOWN"


class CustomTargetingValueStatus(str, Enum):
    """
    <simpleType name="CustomTargetingValue.Status">
    <annotation>
    <documentation> Describes the statuses for {@code CustomTargetingValue} objects. </documentation>
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
    <enumeration value="UNKNOWN">
    <annotation>
    <documentation> The value returned if the actual value is not exposed by the requested API version. </documentation>
    </annotation>
    </enumeration>
    </restriction>
    </simpleType>
    """
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    UNKNOWN = "UNKNOWN"


class CustomTargetingValue(GAMSOAPBaseModel):
    """
    <complexType name="CustomTargetingValue">
    <annotation>
    <documentation> {@code CustomTargetingValue} represents a value used for custom targeting. </documentation>
    </annotation>
    <sequence>
    <element maxOccurs="1" minOccurs="0" name="customTargetingKeyId" type="xsd:long">
    <annotation>
    <documentation> The ID of the {@code CustomTargetingKey} for which this is the value. </documentation>
    </annotation>
    </element>
    <element maxOccurs="1" minOccurs="0" name="id" type="xsd:long">
    <annotation>
    <documentation> The ID of the {@code CustomTargetingValue}. This value is readonly and is populated by Google. </documentation>
    </annotation>
    </element>
    <element maxOccurs="1" minOccurs="0" name="name" type="xsd:string">
    <annotation>
    <documentation> Name of the value. Values can contain up to 40 characters each. You can use alphanumeric characters and symbols other than the following: ", ', =, !, +, #, *, ~, ;, ^, (, ), <, >, [, ]. Values are not data-specific; all values are treated as string. For example, instead of using "age>=18 AND <=34", try "18-34" </documentation>
    </annotation>
    </element>
    <element maxOccurs="1" minOccurs="0" name="displayName" type="xsd:string">
    <annotation>
    <documentation> Descriptive name for the value. </documentation>
    </annotation>
    </element>
    <element maxOccurs="1" minOccurs="0" name="matchType" type="tns:CustomTargetingValue.MatchType">
    <annotation>
    <documentation> The way in which the {@link CustomTargetingValue#name} strings will be matched. </documentation>
    </annotation>
    </element>
    <element maxOccurs="1" minOccurs="0" name="status" type="tns:CustomTargetingValue.Status">
    <annotation>
    <documentation> Status of the {@code CustomTargetingValue}. This field is read-only. A value can be activated and deactivated by calling {@link CustomTargetingService#performCustomTargetingValueAction}. </documentation>
    </annotation>
    </element>
    </sequence>
    </complexType>
    """
    customTargetingKeyId: Optional[int] = Field(
        None, description="The ID of the CustomTargetingKey for which this is the value."
    )
    id: Optional[int] = Field(
        None,
        description="The ID of the CustomTargetingValue. This value is readonly and is populated by Google.",
    )
    name: Optional[str] = Field(
        None,
        description="Name of the value. Values can contain up to 40 characters each. You can use alphanumeric characters and symbols other than the following: ', =, !, +, #, *, ~, ;, ^, (, ), <, >, [. Values are not data-specific; all values are treated as string. For example, instead of using age>=18 AND <=34, try 18-34",
    )
    displayName: Optional[str] = Field(
        None, description="Descriptive name for the value."
    )
    matchType: Optional[CustomTargetingValueMatchType] = Field(
        None,
        description="The way in which the CustomTargetingValue#name strings will be matched.",
    )
    status: Optional[CustomTargetingValueStatus] = Field(
        None,
        description="Status of the CustomTargetingValue. This field is read-only. A value can be activated and deactivated by calling CustomTargetingService#performCustomTargetingValueAction.",
    )
