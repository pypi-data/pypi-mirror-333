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
<complexType name="ChildPublisher">
<annotation>
<documentation> A {@code ChildPublisher} represents a network being managed as part of Multiple Customer Management. </documentation>
</annotation>
<sequence>
<element maxOccurs="1" minOccurs="0" name="approvedDelegationType" type="tns:DelegationType">
<annotation>
<documentation> Type of delegation the parent has been approved to have over the child. This field is read-only, and set to the proposed delegation type value {@code proposedDelegationType} upon approval by the child network. The value remains null if the parent network has not been approved. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="proposedDelegationType" type="tns:DelegationType">
<annotation>
<documentation> Type of delegation the parent has proposed to have over the child, pending approval of the child network. Set the value of this field to the delegation type you intend this network to have over the child network. Upon approval by the child network, its value is copied to {@code approvedDelegationType}, and {@code proposedDelegationType} is set to null. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="status" type="tns:DelegationStatus">
<annotation>
<documentation> Status of the delegation relationship between parent and child. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="accountStatus" type="tns:AccountStatus">
<annotation>
<documentation> Status of the child publisher's Ad Manager account based on {@code ChildPublisher#status} as well as Google's policy verification results. This field is read-only. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="childNetworkCode" type="xsd:string">
<annotation>
<documentation> Network code of child network. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="sellerId" type="xsd:string">
<annotation>
<documentation> The child publisher's seller ID, as specified in the parent publisher's sellers.json file. <p>This field is only relevant for Manage Inventory child publishers. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="proposedRevenueShareMillipercent" type="xsd:long">
<annotation>
<documentation> The proposed revenue share that the parent publisher will receive in millipercentage (values 0 to 100000) for Manage Account proposals. For example, 15% is 15000 millipercent. <p>For updates, this field is read-only. Use company actions to propose new revenue share agreements for existing MCM children. This field is ignored for Manage Inventory proposals. </documentation>
</annotation>
</element>
<element maxOccurs="unbounded" minOccurs="0" name="onboardingTasks" type="tns:OnboardingTask">
<annotation>
<documentation> The child publisher's pending onboarding tasks. <p>This will only be populated if the child publisher's {@code AccountStatus} is {@code PENDING_GOOGLE_APPROVAL}. This attribute is read-only. </documentation>
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
<complexType abstract="true" name="CompanyAction">
<annotation>
<documentation> Represents the actions that can be performed on {@code Company} objects. </documentation>
</annotation>
<sequence/>
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
<complexType name="Company">
<annotation>
<documentation> A {@code Company} represents an agency, a single advertiser or an entire advertising network. </documentation>
</annotation>
<sequence>
<element maxOccurs="1" minOccurs="0" name="id" type="xsd:long">
<annotation>
<documentation> Uniquely identifies the {@code Company}. This value is read-only and is assigned by Google when the company is created. This attribute is required for updates. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="name" type="xsd:string">
<annotation>
<documentation> The full name of the company. This attribute is required and has a maximum length of 127 characters. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="type" type="tns:Company.Type">
<annotation>
<documentation> Specifies what kind of company this is. This attribute is required. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="address" type="xsd:string">
<annotation>
<documentation> Specifies the address of the company. This attribute is optional and has a maximum length of 1024 characters. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="email" type="xsd:string">
<annotation>
<documentation> Specifies the email of the company. This attribute is optional and has a maximum length of 128 characters. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="faxPhone" type="xsd:string">
<annotation>
<documentation> Specifies the fax phone number of the company. This attribute is optional and has a maximum length of 63 characters. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="primaryPhone" type="xsd:string">
<annotation>
<documentation> Specifies the primary phone number of the company. This attribute is optional and has a maximum length of 63 characters. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="externalId" type="xsd:string">
<annotation>
<documentation> Specifies the external ID of the company. This attribute is optional and has a maximum length of 255 characters. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="comment" type="xsd:string">
<annotation>
<documentation> Specifies the comment of the company. This attribute is optional and has a maximum length of 1024 characters. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="creditStatus" type="tns:Company.CreditStatus">
<annotation>
<documentation> Specifies the company's credit status. This attribute is optional and defaults to {@link CreditStatus#ACTIVE} when basic credit status settings are enabled, and {@link CreditStatus#ON_HOLD} when advanced credit status settings are enabled. </documentation>
</annotation>
</element>
<element maxOccurs="unbounded" minOccurs="0" name="appliedLabels" type="tns:AppliedLabel">
<annotation>
<documentation> The set of labels applied to this company. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="primaryContactId" type="xsd:long">
<annotation>
<documentation> The ID of the {@link Contact} who is acting as the primary contact for this company. This attribute is optional. </documentation>
</annotation>
</element>
<element maxOccurs="unbounded" minOccurs="0" name="appliedTeamIds" type="xsd:long">
<annotation>
<documentation> The IDs of all teams that this company is on directly. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="thirdPartyCompanyId" type="xsd:int">
<annotation>
<documentation> Specifies the ID of the Google-recognized canonicalized form of this company. This attribute is optional. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="lastModifiedDateTime" type="tns:DateTime">
<annotation>
<documentation> The date and time this company was last modified. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="childPublisher" type="tns:ChildPublisher">
<annotation>
<documentation> Info required for when Company Type is CHILD_PUBLISHER. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="viewabilityProvider" type="tns:ViewabilityProvider">
<annotation>
<documentation> Info required for when Company Type is VIEWABILITY_PROVIDER. </documentation>
</annotation>
</element>
</sequence>
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
<complexType name="CompanyPage">
<annotation>
<documentation> Captures a page of {@link Company} objects. </documentation>
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
<element maxOccurs="unbounded" minOccurs="0" name="results" type="tns:Company">
<annotation>
<documentation> The collection of companies contained within this page. </documentation>
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
<complexType name="ReInviteAction">
<annotation>
<documentation> The action used by the parent network to send a new invitation with a potentially updated proposal to a rejected or withdrawn child publisher. </documentation>
</annotation>
<complexContent>
<extension base="tns:CompanyAction">
<sequence>
<element maxOccurs="1" minOccurs="0" name="proposedDelegationType" type="tns:DelegationType">
<annotation>
<documentation> The type of delegation the parent has proposed to have over the child, pending approval of the child publisher. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="proposedRevenueShareMillipercent" type="xsd:long">
<annotation>
<documentation> The proposed revenue share that the parent publisher will receive in millipercentage (values 0 to 100000) for Manage Account proposals. For example, 15% is 15000 millipercent. <p>This field is ignored for Manage Inventory proposals. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="proposedEmail" type="xsd:string">
<annotation>
<documentation> The updated email of the child publisher. <p>This field is optional. If set, the scoping statement many not evaluate to more than one rejected or withdrawn child publisher. </documentation>
</annotation>
</element>
</sequence>
</extension>
</complexContent>
</complexType>
<complexType name="EndAgreementAction">
<annotation>
<documentation> The action used by the parent network to withdraw from being the MCM parent for a child. </documentation>
</annotation>
<complexContent>
<extension base="tns:CompanyAction">
<sequence/>
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
<complexType name="ResendInvitationAction">
<annotation>
<documentation> The action used by the parent network to resend an invitation email with the same proposal to an expired child publisher. </documentation>
</annotation>
<complexContent>
<extension base="tns:CompanyAction">
<sequence/>
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
<complexType name="SiteError">
<annotation>
<documentation> Errors associated with the {@code Site}. </documentation>
</annotation>
<complexContent>
<extension base="tns:ApiError">
<sequence>
<element maxOccurs="1" minOccurs="0" name="reason" type="tns:SiteError.Reason"/>
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
<complexType name="ViewabilityProvider">
<annotation>
<documentation> Information required for {@link Company} of Type VIEWABILITY_PROVIDER. It contains all of the data needed to capture viewability metrics. </documentation>
</annotation>
<sequence>
<element maxOccurs="1" minOccurs="0" name="vendorKey" type="xsd:string">
<annotation>
<documentation> The key for this ad verification vendor. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="verificationScriptUrl" type="xsd:string">
<annotation>
<documentation> The URL that hosts the verification script for this vendor. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="verificationParameters" type="xsd:string">
<annotation>
<documentation> The parameters that will be passed to the verification script. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="verificationRejectionTrackerUrl" type="xsd:string">
<annotation>
<documentation> The URL that should be pinged if the verification script cannot be run. </documentation>
</annotation>
</element>
</sequence>
</complexType>
<simpleType name="DelegationStatus">
<annotation>
<documentation> Status of the association between networks. When a parent network requests access, it is marked as pending. Once the child network approves, it is marked as approved. </documentation>
</annotation>
<restriction base="xsd:string">
<enumeration value="UNKNOWN">
<annotation>
<documentation> The value returned if the actual value is not exposed by the requested API version. </documentation>
</annotation>
</enumeration>
<enumeration value="APPROVED">
<annotation>
<documentation> The association request from the parent network is approved by the child network. </documentation>
</annotation>
</enumeration>
<enumeration value="PENDING">
<annotation>
<documentation> The association request from the parent network is pending child network approval or rejection. </documentation>
</annotation>
</enumeration>
<enumeration value="REJECTED">
<annotation>
<documentation> The association request from the parent network is rejected or revoked by the child network. </documentation>
</annotation>
</enumeration>
<enumeration value="WITHDRAWN">
<annotation>
<documentation> The association request from the parent network is withdrawn by the parent network. </documentation>
</annotation>
</enumeration>
</restriction>
</simpleType>
<simpleType name="DelegationType">
<annotation>
<documentation> The type of delegation of the child network to the parent network in MCM. </documentation>
</annotation>
<restriction base="xsd:string">
<enumeration value="UNKNOWN">
<annotation>
<documentation> The value returned if the actual value is not exposed by the requested API version. </documentation>
</annotation>
</enumeration>
<enumeration value="MANAGE_ACCOUNT">
<annotation>
<documentation> The parent network gets complete access to the child network's account </documentation>
</annotation>
</enumeration>
<enumeration value="MANAGE_INVENTORY">
<annotation>
<documentation> A subset of the ad requests from the child are delegated to the parent, determined by the tag on the child network's web pages. The parent network does not have access to the child network, as a subset of the inventory could be owned and operated by the child network. </documentation>
</annotation>
</enumeration>
</restriction>
</simpleType>
<simpleType name="AccountStatus">
<annotation>
<documentation> Status of the MCM child publisher's Ad Manager account with respect to delegated serving. In order for the child network to be served ads for MCM, it must have accepted the invite from the parent network, and must have passed Google's policy compliance verifications. </documentation>
</annotation>
<restriction base="xsd:string">
<enumeration value="UNKNOWN">
<annotation>
<documentation> The value returned if the actual value is not exposed by the requested API version. </documentation>
</annotation>
</enumeration>
<enumeration value="INVITED">
<annotation>
<documentation> The child publisher has not acted on the invite from the parent. </documentation>
</annotation>
</enumeration>
<enumeration value="DECLINED">
<annotation>
<documentation> The child publisher has declined the invite. </documentation>
</annotation>
</enumeration>
<enumeration value="PENDING_GOOGLE_APPROVAL">
<annotation>
<documentation> The child publisher has accepted the invite, and is awaiting Google's policy compliance verifications. </documentation>
</annotation>
</enumeration>
<enumeration value="APPROVED">
<annotation>
<documentation> The child publisher accepted the invite, and Google found it to be compliant with its policies, i.e. no policy violations were found, and the child publisher can be served ads. </documentation>
</annotation>
</enumeration>
<enumeration value="CLOSED_POLICY_VIOLATION">
<annotation>
<documentation> The child publisher accepted the invite, but was disapproved by Google for violating its policies. </documentation>
</annotation>
</enumeration>
<enumeration value="CLOSED_INVALID_ACTIVITY">
<annotation>
<documentation> The child publisher accepted the invite, but was disapproved by Google for invalid activity. </documentation>
</annotation>
</enumeration>
<enumeration value="CLOSED_BY_PUBLISHER">
<annotation>
<documentation> The child publisher has closed their own account. </documentation>
</annotation>
</enumeration>
<enumeration value="DISAPPROVED_INELIGIBLE">
<annotation>
<documentation> The child publisher accepted the invite, but was disapproved as ineligible by Google. </documentation>
</annotation>
</enumeration>
<enumeration value="DISAPPROVED_DUPLICATE_ACCOUNT">
<annotation>
<documentation> The child publisher accepted the invite, but was disapproved by Google for being a duplicate of another account. </documentation>
</annotation>
</enumeration>
<enumeration value="EXPIRED">
<annotation>
<documentation> The invite was sent to the child publisher more than 90 days ago, due to which it has been deactivated. </documentation>
</annotation>
</enumeration>
<enumeration value="INACTIVE">
<annotation>
<documentation> Either the child publisher disconnected from the parent network, or the parent network withdrew the invite. </documentation>
</annotation>
</enumeration>
<enumeration value="DEACTIVATED_BY_AD_MANAGER">
<annotation>
<documentation> The association between the parent and child publishers was deactivated by Google Ad Manager. </documentation>
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
<simpleType name="Company.CreditStatus">
<annotation>
<documentation> Specifies the credit-worthiness of the company for which the publisher runs an order. By doing so, the publisher can control the running of campaigns for the company. A publisher can choose between Basic and Advanced Credit Status settings. This feature needs to be enabled in the Ad Manager web site. Also the kind of setting you need - Basic or Advanced must be configured. If Basic is enabled then, the values allowed are {@code ACTIVE} and {@code INACTIVE}. If Advanced is chosen, then all values are allowed. Choosing an Advanced setting when only the Basic feature has been enabled, or using the Basic setting without turning the feature on will result in an error. </documentation>
</annotation>
<restriction base="xsd:string">
<enumeration value="ACTIVE">
<annotation>
<documentation> When the credit status is active, all line items in all orders belonging to the company will be served. This is a Basic as well as an Advanced Credit Status setting. </documentation>
</annotation>
</enumeration>
<enumeration value="ON_HOLD">
<annotation>
<documentation> When the credit status is on hold, the publisher cannot activate new line items of the company. However, line items that were activated before the credit status change will remain active. You can still create orders and line items for the company. This is an Advanced Credit Status setting. </documentation>
</annotation>
</enumeration>
<enumeration value="CREDIT_STOP">
<annotation>
<documentation> When the credit status is credit stop, the publisher cannot activate new line items of the company. However, line items that were activated before the credit status change will remain active. You cannot create any new orders or line items for the company. This is an Advanced Credit Status setting. </documentation>
</annotation>
</enumeration>
<enumeration value="INACTIVE">
<annotation>
<documentation> When the credit status is inactive, the publisher cannot activate new line items of the company. However, line items that were activated before the credit status change will remain active. You cannot create any new orders or line items for the company. It is used to mark companies with which business is to be discontinued. Such companies are not listed in Ad Manager web site. This is a Basic as well as an Advanced Credit Status setting. </documentation>
</annotation>
</enumeration>
<enumeration value="BLOCKED">
<annotation>
<documentation> When the credit status of a company is marked blocked, then all active line items belonging to the company will stop serving with immediate effect. You cannot active new line items of the company nor can you create any new orders or line items belonging to the company. This is an Advanced Credit Status setting. </documentation>
</annotation>
</enumeration>
</restriction>
</simpleType>
<simpleType name="Company.Type">
<annotation>
<documentation> The type of the company. Once a company is created, it is not possible to change its type. </documentation>
</annotation>
<restriction base="xsd:string">
<enumeration value="HOUSE_ADVERTISER">
<annotation>
<documentation> The publisher's own advertiser. When no outside advertiser buys its inventory, the publisher may run its own advertising campaigns. </documentation>
</annotation>
</enumeration>
<enumeration value="HOUSE_AGENCY">
<annotation>
<documentation> The publisher's own agency. </documentation>
</annotation>
</enumeration>
<enumeration value="ADVERTISER">
<annotation>
<documentation> A business entity that buys publisher inventory to run advertising campaigns. An advertiser is optionally associated with one or more agencies. </documentation>
</annotation>
</enumeration>
<enumeration value="AGENCY">
<annotation>
<documentation> A business entity that offers services, such as advertising creation, placement, and management, to advertisers. </documentation>
</annotation>
</enumeration>
<enumeration value="AD_NETWORK">
<annotation>
<documentation> A company representing multiple advertisers and agencies. </documentation>
</annotation>
</enumeration>
<enumeration value="PARTNER">
<annotation>
<documentation> A company representing a partner. </documentation>
</annotation>
</enumeration>
<enumeration value="CHILD_PUBLISHER">
<annotation>
<documentation> A company representing a child network. </documentation>
</annotation>
</enumeration>
<enumeration value="VIEWABILITY_PROVIDER">
<annotation>
<documentation> A company representing a viewability provider. </documentation>
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
<simpleType name="OnboardingTask">
<annotation>
<documentation> Pending onboarding tasks for the child publishers that must completed before Google's policy compliance is verified. </documentation>
</annotation>
<restriction base="xsd:string">
<enumeration value="UNKNOWN"/>
<enumeration value="BILLING_PROFILE_CREATION">
<annotation>
<documentation> Creation of the child publisher's payments billing profile. </documentation>
</annotation>
</enumeration>
<enumeration value="PHONE_PIN_VERIFICATION">
<annotation>
<documentation> Verification of the child publisher's phone number. </documentation>
</annotation>
</enumeration>
<enumeration value="AD_MANAGER_ACCOUNT_SETUP">
<annotation>
<documentation> Setup of the child publisher's Ad Manager account. </documentation>
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
<simpleType name="SiteError.Reason">
<annotation>
<documentation> The reasons for the target error. </documentation>
</annotation>
<restriction base="xsd:string">
<enumeration value="INVALID_CHILD_NETWORK_CODE">
<annotation>
<documentation> The network code must belong to an MCM child network. </documentation>
</annotation>
</enumeration>
<enumeration value="CANNOT_ARCHIVE_SITE_WITH_SUBSITES">
<annotation>
<documentation> Archive all subsites before archiving the site. </documentation>
</annotation>
</enumeration>
<enumeration value="INVALID_URL_FOR_SITE">
<annotation>
<documentation> The URL is invalid for a top-level site. </documentation>
</annotation>
</enumeration>
<enumeration value="MULTIPLE_UPDATES_FOR_SAME_SITE">
<annotation>
<documentation> The batch of sites could not be updated because the same site was updated multiple times in the batch. </documentation>
</annotation>
</enumeration>
<enumeration value="TOO_MANY_SITES_PER_REVIEW_REQUEST">
<annotation>
<documentation> Too many sites in the request to submit them for review. </documentation>
</annotation>
</enumeration>
<enumeration value="TOO_MANY_REVIEW_REQUESTS_FOR_SITE">
<annotation>
<documentation> The site has been submitted for review too many times. </documentation>
</annotation>
</enumeration>
<enumeration value="INVALID_APPROVAL_STATUS_FOR_REVIEW">
<annotation>
<documentation> Only sites with approval status {@link ApprovalStatus#DRAFT}, {@link ApprovalStatus#DISAPPROVED} and {@link ApprovalStatus#REQUIRES_REVIEW} can be submitted for review. </documentation>
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
<element name="createCompanies">
<annotation>
<documentation> Creates new {@link Company} objects. </documentation>
</annotation>
<complexType>
<sequence>
<element maxOccurs="unbounded" minOccurs="0" name="companies" type="tns:Company"/>
</sequence>
</complexType>
</element>
<element name="createCompaniesResponse">
<complexType>
<sequence>
<element maxOccurs="unbounded" minOccurs="0" name="rval" type="tns:Company"/>
</sequence>
</complexType>
</element>
<element name="ApiExceptionFault" type="tns:ApiException">
<annotation>
<documentation> A fault element of type ApiException. </documentation>
</annotation>
</element>
<element name="getCompaniesByStatement">
<annotation>
<documentation> Gets a {@link CompanyPage} of {@link Company} objects that satisfy the given {@link Statement#query}. The following fields are supported for filtering: <table> <tr> <th scope="col">PQL Property</th> <th scope="col">Object Property</th> </tr> <tr> <td>{@code id}</td> <td>{@link Company#id}</td> </tr> <tr> <td>{@code name}</td> <td>{@link Company#name}</td> </tr> <tr> <td>{@code type}</td> <td>{@link Company#type}</td> </tr> <tr> <td>{@code lastModifiedDateTime}</td> <td>{@link Company#lastModifiedDateTime}</td> </tr> </table> </documentation>
</annotation>
<complexType>
<sequence>
<element maxOccurs="1" minOccurs="0" name="filterStatement" type="tns:Statement"/>
</sequence>
</complexType>
</element>
<element name="getCompaniesByStatementResponse">
<complexType>
<sequence>
<element maxOccurs="1" minOccurs="0" name="rval" type="tns:CompanyPage"/>
</sequence>
</complexType>
</element>
<element name="performCompanyAction">
<annotation>
<documentation> Performs actions on {@link Company} objects that match the given {@code Statement}. </documentation>
</annotation>
<complexType>
<sequence>
<element maxOccurs="1" minOccurs="0" name="companyAction" type="tns:CompanyAction"/>
<element maxOccurs="1" minOccurs="0" name="statement" type="tns:Statement"/>
</sequence>
</complexType>
</element>
<element name="performCompanyActionResponse">
<complexType>
<sequence>
<element maxOccurs="1" minOccurs="0" name="rval" type="tns:UpdateResult"/>
</sequence>
</complexType>
</element>
<element name="updateCompanies">
<annotation>
<documentation> Updates the specified {@link Company} objects. </documentation>
</annotation>
<complexType>
<sequence>
<element maxOccurs="unbounded" minOccurs="0" name="companies" type="tns:Company"/>
</sequence>
</complexType>
</element>
<element name="updateCompaniesResponse">
<complexType>
<sequence>
<element maxOccurs="unbounded" minOccurs="0" name="rval" type="tns:Company"/>
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
<wsdl:message name="createCompaniesRequest">
<wsdl:part element="tns:createCompanies" name="parameters"/>
</wsdl:message>
<wsdl:message name="createCompaniesResponse">
<wsdl:part element="tns:createCompaniesResponse" name="parameters"/>
</wsdl:message>
<wsdl:message name="ApiException">
<wsdl:part element="tns:ApiExceptionFault" name="ApiException"/>
</wsdl:message>
<wsdl:message name="getCompaniesByStatementRequest">
<wsdl:part element="tns:getCompaniesByStatement" name="parameters"/>
</wsdl:message>
<wsdl:message name="getCompaniesByStatementResponse">
<wsdl:part element="tns:getCompaniesByStatementResponse" name="parameters"/>
</wsdl:message>
<wsdl:message name="performCompanyActionRequest">
<wsdl:part element="tns:performCompanyAction" name="parameters"/>
</wsdl:message>
<wsdl:message name="performCompanyActionResponse">
<wsdl:part element="tns:performCompanyActionResponse" name="parameters"/>
</wsdl:message>
<wsdl:message name="updateCompaniesRequest">
<wsdl:part element="tns:updateCompanies" name="parameters"/>
</wsdl:message>
<wsdl:message name="updateCompaniesResponse">
<wsdl:part element="tns:updateCompaniesResponse" name="parameters"/>
</wsdl:message>
<wsdl:portType name="CompanyServiceInterface">
<wsdl:documentation> Provides operations for creating, updating and retrieving {@link Company} objects. </wsdl:documentation>
<wsdl:operation name="createCompanies">
<wsdl:documentation> Creates new {@link Company} objects. </wsdl:documentation>
<wsdl:input message="tns:createCompaniesRequest" name="createCompaniesRequest"/>
<wsdl:output message="tns:createCompaniesResponse" name="createCompaniesResponse"/>
<wsdl:fault message="tns:ApiException" name="ApiException"/>
</wsdl:operation>
<wsdl:operation name="getCompaniesByStatement">
<wsdl:documentation> Gets a {@link CompanyPage} of {@link Company} objects that satisfy the given {@link Statement#query}. The following fields are supported for filtering: <table> <tr> <th scope="col">PQL Property</th> <th scope="col">Object Property</th> </tr> <tr> <td>{@code id}</td> <td>{@link Company#id}</td> </tr> <tr> <td>{@code name}</td> <td>{@link Company#name}</td> </tr> <tr> <td>{@code type}</td> <td>{@link Company#type}</td> </tr> <tr> <td>{@code lastModifiedDateTime}</td> <td>{@link Company#lastModifiedDateTime}</td> </tr> </table> </wsdl:documentation>
<wsdl:input message="tns:getCompaniesByStatementRequest" name="getCompaniesByStatementRequest"/>
<wsdl:output message="tns:getCompaniesByStatementResponse" name="getCompaniesByStatementResponse"/>
<wsdl:fault message="tns:ApiException" name="ApiException"/>
</wsdl:operation>
<wsdl:operation name="performCompanyAction">
<wsdl:documentation> Performs actions on {@link Company} objects that match the given {@code Statement}. </wsdl:documentation>
<wsdl:input message="tns:performCompanyActionRequest" name="performCompanyActionRequest"/>
<wsdl:output message="tns:performCompanyActionResponse" name="performCompanyActionResponse"/>
<wsdl:fault message="tns:ApiException" name="ApiException"/>
</wsdl:operation>
<wsdl:operation name="updateCompanies">
<wsdl:documentation> Updates the specified {@link Company} objects. </wsdl:documentation>
<wsdl:input message="tns:updateCompaniesRequest" name="updateCompaniesRequest"/>
<wsdl:output message="tns:updateCompaniesResponse" name="updateCompaniesResponse"/>
<wsdl:fault message="tns:ApiException" name="ApiException"/>
</wsdl:operation>
</wsdl:portType>
<wsdl:binding name="CompanyServiceSoapBinding" type="tns:CompanyServiceInterface">
<wsdlsoap:binding style="document" transport="http://schemas.xmlsoap.org/soap/http"/>
<wsdl:operation name="createCompanies">
<wsdlsoap:operation soapAction=""/>
<wsdl:input name="createCompaniesRequest">
<wsdlsoap:header message="tns:RequestHeader" part="RequestHeader" use="literal"/>
<wsdlsoap:body use="literal"/>
</wsdl:input>
<wsdl:output name="createCompaniesResponse">
<wsdlsoap:header message="tns:ResponseHeader" part="ResponseHeader" use="literal"/>
<wsdlsoap:body use="literal"/>
</wsdl:output>
<wsdl:fault name="ApiException">
<wsdlsoap:fault name="ApiException" use="literal"/>
</wsdl:fault>
</wsdl:operation>
<wsdl:operation name="getCompaniesByStatement">
<wsdlsoap:operation soapAction=""/>
<wsdl:input name="getCompaniesByStatementRequest">
<wsdlsoap:header message="tns:RequestHeader" part="RequestHeader" use="literal"/>
<wsdlsoap:body use="literal"/>
</wsdl:input>
<wsdl:output name="getCompaniesByStatementResponse">
<wsdlsoap:header message="tns:ResponseHeader" part="ResponseHeader" use="literal"/>
<wsdlsoap:body use="literal"/>
</wsdl:output>
<wsdl:fault name="ApiException">
<wsdlsoap:fault name="ApiException" use="literal"/>
</wsdl:fault>
</wsdl:operation>
<wsdl:operation name="performCompanyAction">
<wsdlsoap:operation soapAction=""/>
<wsdl:input name="performCompanyActionRequest">
<wsdlsoap:header message="tns:RequestHeader" part="RequestHeader" use="literal"/>
<wsdlsoap:body use="literal"/>
</wsdl:input>
<wsdl:output name="performCompanyActionResponse">
<wsdlsoap:header message="tns:ResponseHeader" part="ResponseHeader" use="literal"/>
<wsdlsoap:body use="literal"/>
</wsdl:output>
<wsdl:fault name="ApiException">
<wsdlsoap:fault name="ApiException" use="literal"/>
</wsdl:fault>
</wsdl:operation>
<wsdl:operation name="updateCompanies">
<wsdlsoap:operation soapAction=""/>
<wsdl:input name="updateCompaniesRequest">
<wsdlsoap:header message="tns:RequestHeader" part="RequestHeader" use="literal"/>
<wsdlsoap:body use="literal"/>
</wsdl:input>
<wsdl:output name="updateCompaniesResponse">
<wsdlsoap:header message="tns:ResponseHeader" part="ResponseHeader" use="literal"/>
<wsdlsoap:body use="literal"/>
</wsdl:output>
<wsdl:fault name="ApiException">
<wsdlsoap:fault name="ApiException" use="literal"/>
</wsdl:fault>
</wsdl:operation>
</wsdl:binding>
<wsdl:service name="CompanyService">
<wsdl:port binding="tns:CompanyServiceSoapBinding" name="CompanyServiceInterfacePort">
<wsdlsoap:address location="https://ads.google.com/apis/ads/publisher/v202408/CompanyService"/>
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
    AppliedLabel,
)


class CompanyType(str, Enum):
    """
    <simpleType name="Company.Type">
    <annotation>
    <documentation> The type of the company. Once a company is created, it is not possible to change its type. </documentation>
    </annotation>
    <restriction base="xsd:string">
    <enumeration value="HOUSE_ADVERTISER">
    <annotation>
    <documentation> The publisher's own advertiser. When no outside advertiser buys its inventory, the publisher may run its own advertising campaigns. </documentation>
    </annotation>
    </enumeration>
    <enumeration value="HOUSE_AGENCY">
    <annotation>
    <documentation> The publisher's own agency. </documentation>
    </annotation>
    </enumeration>
    <enumeration value="ADVERTISER">
    <annotation>
    <documentation> A business entity that buys publisher inventory to run advertising campaigns. An advertiser is optionally associated with one or more agencies. </documentation>
    </annotation>
    </enumeration>
    <enumeration value="AGENCY">
    <annotation>
    <documentation> A business entity that offers services, such as advertising creation, placement, and management, to advertisers. </documentation>
    </annotation>
    </enumeration>
    <enumeration value="AD_NETWORK">
    <annotation>
    <documentation> A company representing multiple advertisers and agencies. </documentation>
    </annotation>
    </enumeration>
    <enumeration value="PARTNER">
    <annotation>
    <documentation> A company representing a partner. </documentation>
    </annotation>
    </enumeration>
    <enumeration value="CHILD_PUBLISHER">
    <annotation>
    <documentation> A company representing a child network. </documentation>
    </annotation>
    </enumeration>
    <enumeration value="VIEWABILITY_PROVIDER">
    <annotation>
    <documentation> A company representing a viewability provider. </documentation>
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
    HOUSE_ADVERTISER = "HOUSE_ADVERTISER"
    HOUSE_AGENCY = "HOUSE_AGENCY"
    ADVERTISER = "ADVERTISER"
    AGENCY = "AGENCY"
    AD_NETWORK = "AD_NETWORK"
    PARTNER = "PARTNER"
    CHILD_PUBLISHER = "CHILD_PUBLISHER"
    VIEWABILITY_PROVIDER = "VIEWABILITY_PROVIDER"
    UNKNOWN = "UNKNOWN"


class CompanyCreditStatus(str, Enum):
    """
    <simpleType name="Company.CreditStatus">
    <annotation>
    <documentation> Specifies the credit-worthiness of the company for which the publisher runs an order. By doing so, the publisher can control the running of campaigns for the company. A publisher can choose between Basic and Advanced Credit Status settings. This feature needs to be enabled in the Ad Manager web site. Also the kind of setting you need - Basic or Advanced must be configured. If Basic is enabled then, the values allowed are {@code ACTIVE} and {@code INACTIVE}. If Advanced is chosen, then all values are allowed. Choosing an Advanced setting when only the Basic feature has been enabled, or using the Basic setting without turning the feature on will result in an error. </documentation>
    </annotation>
    <restriction base="xsd:string">
    <enumeration value="ACTIVE">
    <annotation>
    <documentation> When the credit status is active, all line items in all orders belonging to the company will be served. This is a Basic as well as an Advanced Credit Status setting. </documentation>
    </annotation>
    </enumeration>
    <enumeration value="ON_HOLD">
    <annotation>
    <documentation> When the credit status is on hold, the publisher cannot activate new line items of the company. However, line items that were activated before the credit status change will remain active. You can still create orders and line items for the company. This is an Advanced Credit Status setting. </documentation>
    </annotation>
    </enumeration>
    <enumeration value="CREDIT_STOP">
    <annotation>
    <documentation> When the credit status is credit stop, the publisher cannot activate new line items of the company. However, line items that were activated before the credit status change will remain active. You cannot create any new orders or line items for the company. This is an Advanced Credit Status setting. </documentation>
    </annotation>
    </enumeration>
    <enumeration value="INACTIVE">
    <annotation>
    <documentation> When the credit status is inactive, the publisher cannot activate new line items of the company. However, line items that were activated before the credit status change will remain active. You cannot create any new orders or line items for the company. It is used to mark companies with which business is to be discontinued. Such companies are not listed in Ad Manager web site. This is a Basic as well as an Advanced Credit Status setting. </documentation>
    </annotation>
    </enumeration>
    <enumeration value="BLOCKED">
    <annotation>
    <documentation> When the credit status of a company is marked blocked, then all active line items belonging to the company will stop serving with immediate effect. You cannot active new line items of the company nor can you create any new orders or line items belonging to the company. This is an Advanced Credit Status setting. </documentation>
    </annotation>
    </enumeration>
    </restriction>
    </simpleType>
    """
    ACTIVE = "ACTIVE"
    ON_HOLD = "ON_HOLD"
    CREDIT_STOP = "CREDIT_STOP"
    INACTIVE = "INACTIVE"
    BLOCKED = "BLOCKED"


class Company(GAMSOAPBaseModel):
    """
    <complexType name="Company">
    <annotation>
    <documentation> A {@code Company} represents an agency, a single advertiser or an entire advertising network. </documentation>
    </annotation>
    <sequence>
    <element maxOccurs="1" minOccurs="0" name="id" type="xsd:long">
    <annotation>
    <documentation> Uniquely identifies the {@code Company}. This value is read-only and is assigned by Google when the company is created. This attribute is required for updates. </documentation>
    </annotation>
    </element>
    <element maxOccurs="1" minOccurs="0" name="name" type="xsd:string">
    <annotation>
    <documentation> The full name of the company. This attribute is required and has a maximum length of 127 characters. </documentation>
    </annotation>
    </element>
    <element maxOccurs="1" minOccurs="0" name="type" type="tns:Company.Type">
    <annotation>
    <documentation> Specifies what kind of company this is. This attribute is required. </documentation>
    </annotation>
    </element>
    <element maxOccurs="1" minOccurs="0" name="address" type="xsd:string">
    <annotation>
    <documentation> Specifies the address of the company. This attribute is optional and has a maximum length of 1024 characters. </documentation>
    </annotation>
    </element>
    <element maxOccurs="1" minOccurs="0" name="email" type="xsd:string">
    <annotation>
    <documentation> Specifies the email of the company. This attribute is optional and has a maximum length of 128 characters. </documentation>
    </annotation>
    </element>
    <element maxOccurs="1" minOccurs="0" name="faxPhone" type="xsd:string">
    <annotation>
    <documentation> Specifies the fax phone number of the company. This attribute is optional and has a maximum length of 63 characters. </documentation>
    </annotation>
    </element>
    <element maxOccurs="1" minOccurs="0" name="primaryPhone" type="xsd:string">
    <annotation>
    <documentation> Specifies the primary phone number of the company. This attribute is optional and has a maximum length of 63 characters. </documentation>
    </annotation>
    </element>
    <element maxOccurs="1" minOccurs="0" name="externalId" type="xsd:string">
    <annotation>
    <documentation> Specifies the external ID of the company. This attribute is optional and has a maximum length of 255 characters. </documentation>
    </annotation>
    </element>
    <element maxOccurs="1" minOccurs="0" name="comment" type="xsd:string">
    <annotation>
    <documentation> Specifies the comment of the company. This attribute is optional and has a maximum length of 1024 characters. </documentation>
    </annotation>
    </element>
    <element maxOccurs="1" minOccurs="0" name="creditStatus" type="tns:Company.CreditStatus">
    <annotation>
    <documentation> Specifies the company's credit status. This attribute is optional and defaults to {@link CreditStatus#ACTIVE} when basic credit status settings are enabled, and {@link CreditStatus#ON_HOLD} when advanced credit status settings are enabled. </documentation>
    </annotation>
    </element>
    <element maxOccurs="unbounded" minOccurs="0" name="appliedLabels" type="tns:AppliedLabel">
    <annotation>
    <documentation> The set of labels applied to this company. </documentation>
    </annotation>
    </element>
    <element maxOccurs="1" minOccurs="0" name="primaryContactId" type="xsd:long">
    <annotation>
    <documentation> The ID of the {@link Contact} who is acting as the primary contact for this company. This attribute is optional. </documentation>
    </annotation>
    </element>
    <element maxOccurs="unbounded" minOccurs="0" name="appliedTeamIds" type="xsd:long">
    <annotation>
    <documentation> The IDs of all teams that this company is on directly. </documentation>
    </annotation>
    </element>
    <element maxOccurs="1" minOccurs="0" name="thirdPartyCompanyId" type="xsd:int">
    <annotation>
    <documentation> Specifies the ID of the Google-recognized canonicalized form of this company. This attribute is optional. </documentation>
    </annotation>
    </element>
    <element maxOccurs="1" minOccurs="0" name="lastModifiedDateTime" type="tns:DateTime">
    <annotation>
    <documentation> The date and time this company was last modified. </documentation>
    </annotation>
    </element>
    <element maxOccurs="1" minOccurs="0" name="childPublisher" type="tns:ChildPublisher">
    <annotation>
    <documentation> Info required for when Company Type is CHILD_PUBLISHER. </documentation>
    </annotation>
    </element>
    <element maxOccurs="1" minOccurs="0" name="viewabilityProvider" type="tns:ViewabilityProvider">
    <annotation>
    <documentation> Info required for when Company Type is VIEWABILITY_PROVIDER. </documentation>
    </annotation>
    </element>
    </sequence>
    </complexType>
    """
    id: Optional[int] = Field(None, description="Uniquely identifies the {@code Company}. This value is read-only and is assigned by Google when the company is created. This attribute is required for updates.")
    name: Optional[str] = Field(None, description="The full name of the company. This attribute is required and has a maximum length of 127 characters.")
    type: Optional[CompanyType] = Field(None, description="Specifies what kind of company this is. This attribute is required.")
    address: Optional[str] = Field(None, description="Specifies the address of the company. This attribute is optional and has a maximum length of 1024 characters.")
    email: Optional[str] = Field(None, description="Specifies the email of the company. This attribute is optional and has a maximum length of 128 characters.")
    faxPhone: Optional[str] = Field(None, description="Specifies the fax phone number of the company. This attribute is optional and has a maximum length of 63 characters.")
    primaryPhone: Optional[str] = Field(None, description="Specifies the primary phone number of the company. This attribute is optional and has a maximum length of 63 characters.")
    externalId: Optional[str] = Field(None, description="Specifies the external ID of the company. This attribute is optional and has a maximum length of 255 characters.")
    comment: Optional[str] = Field(None, description="Specifies the comment of the company. This attribute is optional and has a maximum length of 1024 characters.")
    creditStatus: Optional[CompanyCreditStatus] = Field(None, description="Specifies the company's credit status. This attribute is optional and defaults to {@link CreditStatus#ACTIVE} when basic credit status settings are enabled, and {@link CreditStatus#ON_HOLD} when advanced credit status settings are enabled.")
    appliedLabels: Optional[List[AppliedLabel]] = Field(None, description="The set of labels applied to this company.")
    primaryContactId: Optional[int] = Field(None, description="The ID of the {@link Contact} who is acting as the primary contact for this company. This attribute is optional.")
    appliedTeamIds: Optional[List[int]] = Field(None, description="The IDs of all teams that this company is on directly.")
    thirdPartyCompanyId: Optional[int] = Field(None, description="Specifies the ID of the Google-recognized canonicalized form of this company. This attribute is optional.")
    lastModifiedDateTime: Optional[DateTime] = Field(None, description="The date and time this company was last modified.")
    # TODO: Add ChildPublisher and ViewabilityProvider classes
    childPublisher: Optional[Any] = Field(None, description="Info required for when Company Type is CHILD_PUBLISHER.")
    viewabilityProvider: Optional[Any] = Field(None, description="Info required for when Company Type is VIEWABILITY_PROVIDER.")
