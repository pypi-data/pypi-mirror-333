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
<complexType name="ActivateAudienceSegments">
<annotation>
<documentation> Action that can be performed on {@link FirstPartyAudienceSegment} objects to activate them. </documentation>
</annotation>
<complexContent>
<extension base="tns:AudienceSegmentAction">
<sequence/>
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
<complexType name="ApproveAudienceSegments">
<annotation>
<documentation> Action that can be performed on {@link ThirdPartyAudienceSegment} objects to approve them. </documentation>
</annotation>
<complexContent>
<extension base="tns:AudienceSegmentAction">
<sequence/>
</extension>
</complexContent>
</complexType>
<complexType name="AudienceSegmentDataProvider">
<annotation>
<documentation> Data provider that owns this segment. For a {@link FirstPartyAudienceSegment}, it would be the publisher network. For a {@link SharedAudienceSegment} or a {@link ThirdPartyAudienceSegment}, it would be the entity that provides that {@link AudienceSegment}. </documentation>
</annotation>
<sequence>
<element maxOccurs="1" minOccurs="0" name="name" type="xsd:string">
<annotation>
<documentation> Name of the data provider. This attribute is readonly and is assigned by Google. </documentation>
</annotation>
</element>
</sequence>
</complexType>
<complexType name="AudienceSegmentPage">
<annotation>
<documentation> Represents a page of {@link AudienceSegment} objects. </documentation>
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
<element maxOccurs="unbounded" minOccurs="0" name="results" type="tns:AudienceSegment">
<annotation>
<documentation> The collection of audience segments contained within this page. </documentation>
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
<complexType abstract="true" name="FirstPartyAudienceSegment">
<annotation>
<documentation> A {@link FirstPartyAudienceSegment} is an {@link AudienceSegment} owned by the publisher network. </documentation>
</annotation>
<complexContent>
<extension base="tns:AudienceSegment">
<sequence/>
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
<complexType name="DeactivateAudienceSegments">
<annotation>
<documentation> Action that can be performed on {@link FirstPartyAudienceSegment} objects to deactivate them. </documentation>
</annotation>
<complexContent>
<extension base="tns:AudienceSegmentAction">
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
<complexType name="ThirdPartyAudienceSegment">
<annotation>
<documentation> A {@link ThirdPartyAudienceSegment} is an {@link AudienceSegment} owned by a data provider and licensed to the Ad Manager publisher. </documentation>
</annotation>
<complexContent>
<extension base="tns:AudienceSegment">
<sequence>
<element maxOccurs="1" minOccurs="0" name="approvalStatus" type="tns:AudienceSegmentApprovalStatus">
<annotation>
<documentation> Specifies if the publisher has approved or rejected the segment. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="cost" type="tns:Money">
<annotation>
<documentation> Specifies CPM cost for the given segment. This attribute is readonly and is assigned by the data provider. <p>The CPM cost comes from the active pricing, if there is one; otherwise it comes from the latest pricing. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="licenseType" type="tns:LicenseType">
<annotation>
<documentation> Specifies the license type of the external segment. This attribute is read-only. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="startDateTime" type="tns:DateTime">
<annotation>
<documentation> Specifies the date and time at which this segment becomes available for use. This attribute is readonly and is assigned by the data provider. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="endDateTime" type="tns:DateTime">
<annotation>
<documentation> Specifies the date and time at which this segment ceases to be available for use. This attribute is readonly and is assigned by the data provider. </documentation>
</annotation>
</element>
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
<complexType name="NonRuleBasedFirstPartyAudienceSegment">
<annotation>
<documentation> A {@link NonRuleBasedFirstPartyAudienceSegment} is a {@link FirstPartyAudienceSegment} owned by the publisher network. It doesn't contain a rule. Cookies are usually added to this segment via cookie upload. </documentation>
</annotation>
<complexContent>
<extension base="tns:FirstPartyAudienceSegment">
<sequence>
<element maxOccurs="1" minOccurs="0" name="membershipExpirationDays" type="xsd:int">
<annotation>
<documentation> Specifies the number of days after which a user's cookie will be removed from the audience segment due to inactivity. This attribute is required and can be between 1 and 540. </documentation>
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
<complexType name="PopulateAudienceSegments">
<annotation>
<documentation> Action that can be performed on {@link FirstPartyAudienceSegment} objects to populate them based on last 30 days of traffic. </documentation>
</annotation>
<complexContent>
<extension base="tns:AudienceSegmentAction">
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
<complexType name="FirstPartyAudienceSegmentRule">
<annotation>
<documentation> Rule of a {@link FirstPartyAudienceSegment} that defines user's eligibility criteria to be part of a segment. </documentation>
</annotation>
<sequence>
<element maxOccurs="1" minOccurs="0" name="inventoryRule" type="tns:InventoryTargeting">
<annotation>
<documentation> Specifies the inventory (i.e. ad units and placements) that are part of the rule of a {@link FirstPartyAudienceSegment}. This attribute is required. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="customCriteriaRule" type="tns:CustomCriteriaSet">
<annotation>
<documentation> Specifies the collection of custom criteria that are part of the rule of a {@link FirstPartyAudienceSegment}. <p>Once the {@link FirstPartyAudienceSegment} is updated or modified with custom criteria, the server may return a normalized, but equivalent representation of the custom criteria rule. <ul> {@code customCriteriaRule} will have up to three levels including itself. <li>The top level {@link CustomCriteriaSet} i.e. the {@code customTargeting} object can only contain a {@link CustomCriteriaSet.LogicalOperator#OR} of all its children. <li>The second level of {@link CustomCriteriaSet} objects can only contain {@link CustomCriteriaSet.LogicalOperator#AND} of all their children. If a {@link CustomCriteria} is placed on this level, the server will wrap it in a {@link CustomCriteriaSet}. <li>The third level can only comprise of {@link CustomCriteria} objects. </ul> <p>The resulting custom criteria rule would be of the form: <br> <img src="https://chart.apis.google.com/chart?cht=gv&chl=digraph{customTargeting_LogicalOperator_OR-%3ECustomCriteriaSet_LogicalOperator_AND_1-%3ECustomCriteria_1;CustomCriteriaSet_LogicalOperator_AND_1-%3Eellipsis1;customTargeting_LogicalOperator_OR-%3Eellipsis2;ellipsis1[label=%22...%22,shape=none,fontsize=32];ellipsis2[label=%22...%22,shape=none,fontsize=32]}&chs=450x200"/> </documentation>
</annotation>
</element>
</sequence>
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
<complexType name="RejectAudienceSegments">
<annotation>
<documentation> Action that can be performed on {@link ThirdPartyAudienceSegment} objects to reject them. </documentation>
</annotation>
<complexContent>
<extension base="tns:AudienceSegmentAction">
<sequence/>
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
<complexType name="RuleBasedFirstPartyAudienceSegment">
<annotation>
<documentation> A {@link RuleBasedFirstPartyAudienceSegment} is a {@link FirstPartyAudienceSegment} owned by the publisher network. It contains a rule. </documentation>
</annotation>
<complexContent>
<extension base="tns:RuleBasedFirstPartyAudienceSegmentSummary">
<sequence>
<element maxOccurs="1" minOccurs="0" name="rule" type="tns:FirstPartyAudienceSegmentRule">
<annotation>
<documentation> Specifies the rule of the segment which determines user's eligibility criteria to be part of the segment. This attribute is required. </documentation>
</annotation>
</element>
</sequence>
</extension>
</complexContent>
</complexType>
<complexType name="RuleBasedFirstPartyAudienceSegmentSummary">
<annotation>
<documentation> A {@link RuleBasedFirstPartyAudienceSegmentSummary} is a {@link FirstPartyAudienceSegment} owned by the publisher network. </documentation>
</annotation>
<complexContent>
<extension base="tns:FirstPartyAudienceSegment">
<sequence>
<element maxOccurs="1" minOccurs="0" name="pageViews" type="xsd:int">
<annotation>
<documentation> Specifies the number of times a user's cookie must match the segment rule before it's associated with the audience segment. This is used in combination with {@link FirstPartyAudienceSegment#recencyDays} to determine eligibility of the association. This attribute is required and can be between 1 and 12. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="recencyDays" type="xsd:int">
<annotation>
<documentation> Specifies the number of days within which a user's cookie must match the segment rule before it's associated with the audience segment. This is used in combination with {@link FirstPartyAudienceSegment#pageViews} to determine eligibility of the association. This attribute is required only if {@link FirstPartyAudienceSegment#pageViews} is greater than 1. When required, it can be between 1 and 90. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="membershipExpirationDays" type="xsd:int">
<annotation>
<documentation> Specifies the number of days after which a user's cookie will be removed from the audience segment due to inactivity. This attribute is required and can be between 1 and 540. </documentation>
</annotation>
</element>
</sequence>
</extension>
</complexContent>
</complexType>
<complexType abstract="true" name="AudienceSegmentAction">
<annotation>
<documentation> Action that can be performed on {@link AudienceSegment} objects. </documentation>
</annotation>
<sequence/>
</complexType>
<complexType name="AudienceSegment">
<annotation>
<documentation> An {@link AudienceSegment} represents audience segment object. </documentation>
</annotation>
<sequence>
<element maxOccurs="1" minOccurs="0" name="id" type="xsd:long">
<annotation>
<documentation> Id of the {@link AudienceSegment}. This attribute is readonly and is populated by Google. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="name" type="xsd:string">
<annotation>
<documentation> Name of the {@link AudienceSegment}. This attribute is required and has a maximum length of 255 characters. </documentation>
</annotation>
</element>
<element maxOccurs="unbounded" minOccurs="0" name="categoryIds" type="xsd:long">
<annotation>
<documentation> The ids of the categories this segment belongs to. This field is optional, it may be empty. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="description" type="xsd:string">
<annotation>
<documentation> Description of the {@link AudienceSegment}. This attribute is optional and has a maximum length of 8192 characters. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="status" type="tns:AudienceSegment.Status">
<annotation>
<documentation> Status of the {@link AudienceSegment}. This controls whether the given segment is available for targeting or not. During creation this attribute is optional and defaults to {@code ACTIVE}. This attribute is readonly for updates. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="size" type="xsd:long">
<annotation>
<documentation> Number of unique identifiers in the {@link AudienceSegment}. This attribute is readonly and is populated by Google. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="mobileWebSize" type="xsd:long">
<annotation>
<documentation> Number of unique identifiers in the {@link AudienceSegment} for mobile web. This attribute is read-only. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="idfaSize" type="xsd:long">
<annotation>
<documentation> Number of unique IDFA identifiers in the {@link AudienceSegment}. This attribute is read-only. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="adIdSize" type="xsd:long">
<annotation>
<documentation> Number of unique AdID identifiers in the {@link AudienceSegment}. This attribute is read-only. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="ppidSize" type="xsd:long">
<annotation>
<documentation> Number of unique PPID (publisher provided identifiers) in the {@link AudienceSegment}. This attribute is read-only. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="dataProvider" type="tns:AudienceSegmentDataProvider">
<annotation>
<documentation> Owner data provider of this segment. This attribute is readonly and is assigned by Google. </documentation>
</annotation>
</element>
<element maxOccurs="1" minOccurs="0" name="type" type="tns:AudienceSegment.Type">
<annotation>
<documentation> Type of the segment. This attribute is readonly and is assigned by Google. </documentation>
</annotation>
</element>
</sequence>
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
<complexType name="SharedAudienceSegment">
<annotation>
<documentation> A {@link SharedAudienceSegment} is an {@link AudienceSegment} owned by another entity and shared with the publisher network. </documentation>
</annotation>
<complexContent>
<extension base="tns:AudienceSegment">
<sequence/>
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
<simpleType name="AudienceSegmentApprovalStatus">
<annotation>
<documentation> Approval status values for {@link ThirdPartyAudienceSegment} objects. </documentation>
</annotation>
<restriction base="xsd:string">
<enumeration value="UNAPPROVED">
<annotation>
<documentation> Specifies that this segment is waiting to be approved or rejected. It cannot be targeted. </documentation>
</annotation>
</enumeration>
<enumeration value="APPROVED">
<annotation>
<documentation> Specifies that this segment is approved and can be targeted. </documentation>
</annotation>
</enumeration>
<enumeration value="REJECTED">
<annotation>
<documentation> Specifies that this segment is rejected and cannot be targeted. </documentation>
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
<simpleType name="LicenseType">
<annotation>
<documentation> Specifies the license type of a {@link ThirdPartyAudienceSegment}. </documentation>
</annotation>
<restriction base="xsd:string">
<enumeration value="DIRECT_LICENSE">
<annotation>
<documentation> A direct license is the result of a direct contract between the data provider and the publisher. </documentation>
</annotation>
</enumeration>
<enumeration value="GLOBAL_LICENSE">
<annotation>
<documentation> A global license is the result of an agreement between Google and the data provider, which agrees to license their audience segments to all the publishers and/or advertisers of the Google ecosystem. </documentation>
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
<simpleType name="AudienceSegment.Type">
<annotation>
<documentation> Specifies types for {@link AudienceSegment} objects. </documentation>
</annotation>
<restriction base="xsd:string">
<enumeration value="FIRST_PARTY">
<annotation>
<documentation> First party segments created and owned by the publisher. </documentation>
</annotation>
</enumeration>
<enumeration value="SHARED">
<annotation>
<documentation> First party segments shared by other clients. </documentation>
</annotation>
</enumeration>
<enumeration value="THIRD_PARTY">
<annotation>
<documentation> Third party segments licensed by the publisher from data providers. This doesn't include Google-provided licensed segments. </documentation>
</annotation>
</enumeration>
<enumeration value="UNKNOWN">
<annotation>
<documentation> The value returned if the actual value is not exposed by the requested API version. </documentation>
</annotation>
</enumeration>
</restriction>
</simpleType>
<simpleType name="AudienceSegment.Status">
<annotation>
<documentation> Specifies the statuses for {@link AudienceSegment} objects. </documentation>
</annotation>
<restriction base="xsd:string">
<enumeration value="UNKNOWN">
<annotation>
<documentation> The value returned if the actual value is not exposed by the requested API version. </documentation>
</annotation>
</enumeration>
<enumeration value="ACTIVE">
<annotation>
<documentation> Active status means this audience segment is available for targeting. </documentation>
</annotation>
</enumeration>
<enumeration value="INACTIVE">
<annotation>
<documentation> Inactive status means this audience segment is not available for targeting. </documentation>
</annotation>
</enumeration>
<enumeration value="UNUSED">
<annotation>
<documentation> Unused status means this audience segment was deactivated by Google because it is unused. </documentation>
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
<element name="createAudienceSegments">
<annotation>
<documentation> Creates new {@link FirstPartyAudienceSegment} objects. </documentation>
</annotation>
<complexType>
<sequence>
<element maxOccurs="unbounded" minOccurs="0" name="segments" type="tns:FirstPartyAudienceSegment"/>
</sequence>
</complexType>
</element>
<element name="createAudienceSegmentsResponse">
<complexType>
<sequence>
<element maxOccurs="unbounded" minOccurs="0" name="rval" type="tns:FirstPartyAudienceSegment"/>
</sequence>
</complexType>
</element>
<element name="ApiExceptionFault" type="tns:ApiException">
<annotation>
<documentation> A fault element of type ApiException. </documentation>
</annotation>
</element>
<element name="getAudienceSegmentsByStatement">
<annotation>
<documentation> Gets an {@link AudienceSegmentPage} of {@link AudienceSegment} objects that satisfy the given {@link Statement#query}. The following fields are supported for filtering: <table> <tr> <th scope="col">PQL Property</th> <th scope="col">Object Property</th> </tr> <tr> <td>{@code id}</td> <td>{@link AudienceSegment#id}</td> </tr> <tr> <td>{@code name}</td> <td>{@link AudienceSegment#name}</td> </tr> <tr> <td>{@code status}</td> <td>{@link AudienceSegment#status}</td> </tr> <tr> <td>{@code type}</td> <td>{@link AudienceSegment#type}</td> </tr> <tr> <td>{@code size}</td> <td>{@link AudienceSegment#size}</td> </tr> <tr> <td>{@code dataProviderName}</td> <td>{@link AudienceSegmentDataProvider#name}</td> </tr> <tr> <td>{@code segmentType}</td> <td>{@link AudienceSegment#type}</td> </tr> <tr> <td>{@code approvalStatus}</td> <td>{@link ThirdPartyAudienceSegment#approvalStatus}</td> </tr> <tr> <td>{@code cost}</td> <td>{@link ThirdPartyAudienceSegment#cost}</td> </tr> <tr> <td>{@code startDateTime}</td> <td>{@link ThirdPartyAudienceSegment#startDateTime}</td> </tr> <tr> <td>{@code endDateTime}</td> <td>{@link ThirdPartyAudienceSegment#endDateTime}</td> </tr> </table> </documentation>
</annotation>
<complexType>
<sequence>
<element maxOccurs="1" minOccurs="0" name="filterStatement" type="tns:Statement"/>
</sequence>
</complexType>
</element>
<element name="getAudienceSegmentsByStatementResponse">
<complexType>
<sequence>
<element maxOccurs="1" minOccurs="0" name="rval" type="tns:AudienceSegmentPage"/>
</sequence>
</complexType>
</element>
<element name="performAudienceSegmentAction">
<annotation>
<documentation> Performs the given {@link AudienceSegmentAction} on the set of segments identified by the given statement. </documentation>
</annotation>
<complexType>
<sequence>
<element maxOccurs="1" minOccurs="0" name="action" type="tns:AudienceSegmentAction"/>
<element maxOccurs="1" minOccurs="0" name="filterStatement" type="tns:Statement"/>
</sequence>
</complexType>
</element>
<element name="performAudienceSegmentActionResponse">
<complexType>
<sequence>
<element maxOccurs="1" minOccurs="0" name="rval" type="tns:UpdateResult"/>
</sequence>
</complexType>
</element>
<element name="updateAudienceSegments">
<annotation>
<documentation> Updates the given {@link FirstPartyAudienceSegment} objects. </documentation>
</annotation>
<complexType>
<sequence>
<element maxOccurs="unbounded" minOccurs="0" name="segments" type="tns:FirstPartyAudienceSegment"/>
</sequence>
</complexType>
</element>
<element name="updateAudienceSegmentsResponse">
<complexType>
<sequence>
<element maxOccurs="unbounded" minOccurs="0" name="rval" type="tns:FirstPartyAudienceSegment"/>
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
<wsdl:message name="createAudienceSegmentsRequest">
<wsdl:part element="tns:createAudienceSegments" name="parameters"/>
</wsdl:message>
<wsdl:message name="createAudienceSegmentsResponse">
<wsdl:part element="tns:createAudienceSegmentsResponse" name="parameters"/>
</wsdl:message>
<wsdl:message name="ApiException">
<wsdl:part element="tns:ApiExceptionFault" name="ApiException"/>
</wsdl:message>
<wsdl:message name="getAudienceSegmentsByStatementRequest">
<wsdl:part element="tns:getAudienceSegmentsByStatement" name="parameters"/>
</wsdl:message>
<wsdl:message name="getAudienceSegmentsByStatementResponse">
<wsdl:part element="tns:getAudienceSegmentsByStatementResponse" name="parameters"/>
</wsdl:message>
<wsdl:message name="performAudienceSegmentActionRequest">
<wsdl:part element="tns:performAudienceSegmentAction" name="parameters"/>
</wsdl:message>
<wsdl:message name="performAudienceSegmentActionResponse">
<wsdl:part element="tns:performAudienceSegmentActionResponse" name="parameters"/>
</wsdl:message>
<wsdl:message name="updateAudienceSegmentsRequest">
<wsdl:part element="tns:updateAudienceSegments" name="parameters"/>
</wsdl:message>
<wsdl:message name="updateAudienceSegmentsResponse">
<wsdl:part element="tns:updateAudienceSegmentsResponse" name="parameters"/>
</wsdl:message>
<wsdl:portType name="AudienceSegmentServiceInterface">
<wsdl:documentation> Provides operations for creating, updating and retrieving {@link AudienceSegment} objects. </wsdl:documentation>
<wsdl:operation name="createAudienceSegments">
<wsdl:documentation> Creates new {@link FirstPartyAudienceSegment} objects. </wsdl:documentation>
<wsdl:input message="tns:createAudienceSegmentsRequest" name="createAudienceSegmentsRequest"/>
<wsdl:output message="tns:createAudienceSegmentsResponse" name="createAudienceSegmentsResponse"/>
<wsdl:fault message="tns:ApiException" name="ApiException"/>
</wsdl:operation>
<wsdl:operation name="getAudienceSegmentsByStatement">
<wsdl:documentation> Gets an {@link AudienceSegmentPage} of {@link AudienceSegment} objects that satisfy the given {@link Statement#query}. The following fields are supported for filtering: <table> <tr> <th scope="col">PQL Property</th> <th scope="col">Object Property</th> </tr> <tr> <td>{@code id}</td> <td>{@link AudienceSegment#id}</td> </tr> <tr> <td>{@code name}</td> <td>{@link AudienceSegment#name}</td> </tr> <tr> <td>{@code status}</td> <td>{@link AudienceSegment#status}</td> </tr> <tr> <td>{@code type}</td> <td>{@link AudienceSegment#type}</td> </tr> <tr> <td>{@code size}</td> <td>{@link AudienceSegment#size}</td> </tr> <tr> <td>{@code dataProviderName}</td> <td>{@link AudienceSegmentDataProvider#name}</td> </tr> <tr> <td>{@code segmentType}</td> <td>{@link AudienceSegment#type}</td> </tr> <tr> <td>{@code approvalStatus}</td> <td>{@link ThirdPartyAudienceSegment#approvalStatus}</td> </tr> <tr> <td>{@code cost}</td> <td>{@link ThirdPartyAudienceSegment#cost}</td> </tr> <tr> <td>{@code startDateTime}</td> <td>{@link ThirdPartyAudienceSegment#startDateTime}</td> </tr> <tr> <td>{@code endDateTime}</td> <td>{@link ThirdPartyAudienceSegment#endDateTime}</td> </tr> </table> </wsdl:documentation>
<wsdl:input message="tns:getAudienceSegmentsByStatementRequest" name="getAudienceSegmentsByStatementRequest"/>
<wsdl:output message="tns:getAudienceSegmentsByStatementResponse" name="getAudienceSegmentsByStatementResponse"/>
<wsdl:fault message="tns:ApiException" name="ApiException"/>
</wsdl:operation>
<wsdl:operation name="performAudienceSegmentAction">
<wsdl:documentation> Performs the given {@link AudienceSegmentAction} on the set of segments identified by the given statement. </wsdl:documentation>
<wsdl:input message="tns:performAudienceSegmentActionRequest" name="performAudienceSegmentActionRequest"/>
<wsdl:output message="tns:performAudienceSegmentActionResponse" name="performAudienceSegmentActionResponse"/>
<wsdl:fault message="tns:ApiException" name="ApiException"/>
</wsdl:operation>
<wsdl:operation name="updateAudienceSegments">
<wsdl:documentation> Updates the given {@link FirstPartyAudienceSegment} objects. </wsdl:documentation>
<wsdl:input message="tns:updateAudienceSegmentsRequest" name="updateAudienceSegmentsRequest"/>
<wsdl:output message="tns:updateAudienceSegmentsResponse" name="updateAudienceSegmentsResponse"/>
<wsdl:fault message="tns:ApiException" name="ApiException"/>
</wsdl:operation>
</wsdl:portType>
<wsdl:binding name="AudienceSegmentServiceSoapBinding" type="tns:AudienceSegmentServiceInterface">
<wsdlsoap:binding style="document" transport="http://schemas.xmlsoap.org/soap/http"/>
<wsdl:operation name="createAudienceSegments">
<wsdlsoap:operation soapAction=""/>
<wsdl:input name="createAudienceSegmentsRequest">
<wsdlsoap:header message="tns:RequestHeader" part="RequestHeader" use="literal"/>
<wsdlsoap:body use="literal"/>
</wsdl:input>
<wsdl:output name="createAudienceSegmentsResponse">
<wsdlsoap:header message="tns:ResponseHeader" part="ResponseHeader" use="literal"/>
<wsdlsoap:body use="literal"/>
</wsdl:output>
<wsdl:fault name="ApiException">
<wsdlsoap:fault name="ApiException" use="literal"/>
</wsdl:fault>
</wsdl:operation>
<wsdl:operation name="getAudienceSegmentsByStatement">
<wsdlsoap:operation soapAction=""/>
<wsdl:input name="getAudienceSegmentsByStatementRequest">
<wsdlsoap:header message="tns:RequestHeader" part="RequestHeader" use="literal"/>
<wsdlsoap:body use="literal"/>
</wsdl:input>
<wsdl:output name="getAudienceSegmentsByStatementResponse">
<wsdlsoap:header message="tns:ResponseHeader" part="ResponseHeader" use="literal"/>
<wsdlsoap:body use="literal"/>
</wsdl:output>
<wsdl:fault name="ApiException">
<wsdlsoap:fault name="ApiException" use="literal"/>
</wsdl:fault>
</wsdl:operation>
<wsdl:operation name="performAudienceSegmentAction">
<wsdlsoap:operation soapAction=""/>
<wsdl:input name="performAudienceSegmentActionRequest">
<wsdlsoap:header message="tns:RequestHeader" part="RequestHeader" use="literal"/>
<wsdlsoap:body use="literal"/>
</wsdl:input>
<wsdl:output name="performAudienceSegmentActionResponse">
<wsdlsoap:header message="tns:ResponseHeader" part="ResponseHeader" use="literal"/>
<wsdlsoap:body use="literal"/>
</wsdl:output>
<wsdl:fault name="ApiException">
<wsdlsoap:fault name="ApiException" use="literal"/>
</wsdl:fault>
</wsdl:operation>
<wsdl:operation name="updateAudienceSegments">
<wsdlsoap:operation soapAction=""/>
<wsdl:input name="updateAudienceSegmentsRequest">
<wsdlsoap:header message="tns:RequestHeader" part="RequestHeader" use="literal"/>
<wsdlsoap:body use="literal"/>
</wsdl:input>
<wsdl:output name="updateAudienceSegmentsResponse">
<wsdlsoap:header message="tns:ResponseHeader" part="ResponseHeader" use="literal"/>
<wsdlsoap:body use="literal"/>
</wsdl:output>
<wsdl:fault name="ApiException">
<wsdlsoap:fault name="ApiException" use="literal"/>
</wsdl:fault>
</wsdl:operation>
</wsdl:binding>
<wsdl:service name="AudienceSegmentService">
<wsdl:port binding="tns:AudienceSegmentServiceSoapBinding" name="AudienceSegmentServiceInterfacePort">
<wsdlsoap:address location="https://ads.google.com/apis/ads/publisher/v202408/AudienceSegmentService"/>
</wsdl:port>
</wsdl:service>
</wsdl:definitions>
"""


from __future__ import annotations
from typing import List, Optional
from enum import Enum

from pydantic import Field

from rcplus_alloy_common.gam.vendor.common import GAMSOAPBaseModel


class AudienceSegmentType(str, Enum):
    """
    <simpleType name="AudienceSegment.Type">
    <annotation>
    <documentation> Specifies types for {@link AudienceSegment} objects. </documentation>
    </annotation>
    <restriction base="xsd:string">
    <enumeration value="FIRST_PARTY">
    <annotation>
    <documentation> First party segments created and owned by the publisher. </documentation>
    </annotation>
    </enumeration>
    <enumeration value="SHARED">
    <annotation>
    <documentation> First party segments shared by other clients. </documentation>
    </annotation>
    </enumeration>
    <enumeration value="THIRD_PARTY">
    <annotation>
    <documentation> Third party segments licensed by the publisher from data providers. This doesn't include Google-provided licensed segments. </documentation>
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
    FIRST_PARTY = "FIRST_PARTY"
    SHARED = "SHARED"
    THIRD_PARTY = "THIRD_PARTY"
    UNKNOWN = "UNKNOWN"


class AudienceSegmentDataProvider(GAMSOAPBaseModel):
    """
    <complexType name="AudienceSegmentDataProvider">
    <annotation>
    <documentation> Data provider that owns this segment. For a {@link FirstPartyAudienceSegment}, it would be the publisher network. For a {@link SharedAudienceSegment} or a {@link ThirdPartyAudienceSegment}, it would be the entity that provides that {@link AudienceSegment}. </documentation>
    </annotation>
    <sequence>
    <element maxOccurs="1" minOccurs="0" name="name" type="xsd:string">
    <annotation>
    <documentation> Name of the data provider. This attribute is readonly and is assigned by Google. </documentation>
    </annotation>
    </element>
    </sequence>
    </complexType>
    """
    name: Optional[str] = Field(
        None,
        description="Name of the data provider. This attribute is readonly and is assigned by Google."
    )


class AudienceSegmentStatus(str, Enum):
    """
    <simpleType name="AudienceSegment.Status">
    <annotation>
    <documentation> Specifies the statuses for {@link AudienceSegment} objects. </documentation>
    </annotation>
    <restriction base="xsd:string">
    <enumeration value="UNKNOWN">
    <annotation>
    <documentation> The value returned if the actual value is not exposed by the requested API version. </documentation>
    </annotation>
    </enumeration>
    <enumeration value="ACTIVE">
    <annotation>
    <documentation> Active status means this audience segment is available for targeting. </documentation>
    </annotation>
    </enumeration>
    <enumeration value="INACTIVE">
    <annotation>
    <documentation> Inactive status means this audience segment is not available for targeting. </documentation>
    </annotation>
    </enumeration>
    <enumeration value="UNUSED">
    <annotation>
    <documentation> Unused status means this audience segment was deactivated by Google because it is unused. </documentation>
    </annotation>
    </enumeration>
    </restriction>
    </simpleType>
    """
    UNKNOWN = "UNKNOWN"
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    UNUSED = "UNUSED"


class AudienceSegment(GAMSOAPBaseModel):
    """
    <complexType name="AudienceSegment">
    <annotation>
    <documentation> An {@link AudienceSegment} represents audience segment object. </documentation>
    </annotation>
    <sequence>
    <element maxOccurs="1" minOccurs="0" name="id" type="xsd:long">
    <annotation>
    <documentation> Id of the {@link AudienceSegment}. This attribute is readonly and is populated by Google. </documentation>
    </annotation>
    </element>
    <element maxOccurs="1" minOccurs="0" name="name" type="xsd:string">
    <annotation>
    <documentation> Name of the {@link AudienceSegment}. This attribute is required and has a maximum length of 255 characters. </documentation>
    </annotation>
    </element>
    <element maxOccurs="unbounded" minOccurs="0" name="categoryIds" type="xsd:long">
    <annotation>
    <documentation> The ids of the categories this segment belongs to. This field is optional, it may be empty. </documentation>
    </annotation>
    </element>
    <element maxOccurs="1" minOccurs="0" name="description" type="xsd:string">
    <annotation>
    <documentation> Description of the {@link AudienceSegment}. This attribute is optional and has a maximum length of 8192 characters. </documentation>
    </annotation>
    </element>
    <element maxOccurs="1" minOccurs="0" name="status" type="tns:AudienceSegment.Status">
    <annotation>
    <documentation> Status of the {@link AudienceSegment}. This controls whether the given segment is available for targeting or not. During creation this attribute is optional and defaults to {@code ACTIVE}. This attribute is readonly for updates. </documentation>
    </annotation>
    </element>
    <element maxOccurs="1" minOccurs="0" name="size" type="xsd:long">
    <annotation>
    <documentation> Number of unique identifiers in the {@link AudienceSegment}. This attribute is readonly and is populated by Google. </documentation>
    </annotation>
    </element>
    <element maxOccurs="1" minOccurs="0" name="mobileWebSize" type="xsd:long">
    <annotation>
    <documentation> Number of unique identifiers in the {@link AudienceSegment} for mobile web. This attribute is read-only. </documentation>
    </annotation>
    </element>
    <element maxOccurs="1" minOccurs="0" name="idfaSize" type="xsd:long">
    <annotation>
    <documentation> Number of unique IDFA identifiers in the {@link AudienceSegment}. This attribute is read-only. </documentation>
    </annotation>
    </element>
    <element maxOccurs="1" minOccurs="0" name="adIdSize" type="xsd:long">
    <annotation>
    <documentation> Number of unique AdID identifiers in the {@link AudienceSegment}. This attribute is read-only. </documentation>
    </annotation>
    </element>
    <element maxOccurs="1" minOccurs="0" name="ppidSize" type="xsd:long">
    <annotation>
    <documentation> Number of unique PPID (publisher provided identifiers) in the {@link AudienceSegment}. This attribute is read-only. </documentation>
    </annotation>
    </element>
    <element maxOccurs="1" minOccurs="0" name="dataProvider" type="tns:AudienceSegmentDataProvider">
    <annotation>
    <documentation> Owner data provider of this segment. This attribute is readonly and is assigned by Google. </documentation>
    </annotation>
    </element>
    <element maxOccurs="1" minOccurs="0" name="type" type="tns:AudienceSegment.Type">
    <annotation>
    <documentation> Type of the segment. This attribute is readonly and is assigned by Google. </documentation>
    </annotation>
    </element>
    </sequence>
    </complexType>
    """
    id: Optional[int] = Field(
        None,
        description="Id of the {@link AudienceSegment}. This attribute is readonly and is populated by Google."
    )
    name: Optional[str] = Field(
        None,
        description="Name of the {@link AudienceSegment}. This attribute is required and has a maximum length of 255 characters."
    )
    categoryIds: Optional[List[int]] = Field(
        None,
        description="The ids of the categories this segment belongs to. This field is optional, it may be empty."
    )
    description: Optional[str] = Field(
        None,
        description="Description of the {@link AudienceSegment}. This attribute is optional and has a maximum length of 8192 characters."
    )
    status: Optional[AudienceSegmentStatus] = Field(
        None,
        description="Status of the {@link AudienceSegment}. This controls whether the given segment is available for targeting or not. During creation this attribute is optional and defaults to {@code ACTIVE}. This attribute is readonly for updates."
    )
    size: Optional[int] = Field(
        None,
        description="Number of unique identifiers in the {@link AudienceSegment}. This attribute is readonly and is populated by Google."
    )
    mobileWebSize: Optional[int] = Field(
        None,
        description="Number of unique identifiers in the {@link AudienceSegment} for mobile web. This attribute is read-only."
    )
    idfaSize: Optional[int] = Field(
        None,
        description="Number of unique IDFA identifiers in the {@link AudienceSegment}. This attribute is read-only."
    )
    adIdSize: Optional[int] = Field(
        None,
        description="Number of unique AdID identifiers in the {@link AudienceSegment}. This attribute is read-only."
    )
    ppidSize: Optional[int] = Field(
        None,
        description="Number of unique PPID (publisher provided identifiers) in the {@link AudienceSegment}. This attribute is read-only."
    )
    dataProvider: Optional[AudienceSegmentDataProvider] = Field(
        None,
        description="Owner data provider of this segment. This attribute is readonly and is assigned by Google."
    )
    type: Optional[AudienceSegmentType] = Field(
        None,
        description="Type of the segment. This attribute is readonly and is assigned by Google."
    )


class FirstPartyAudienceSegment(AudienceSegment):
    """
    <complexType abstract="true" name="FirstPartyAudienceSegment">
    <annotation>
    <documentation> A {@link FirstPartyAudienceSegment} is an {@link AudienceSegment} owned by the publisher network. </documentation>
    </annotation>
    <complexContent>
    <extension base="tns:AudienceSegment">
    <sequence/>
    </extension>
    </complexContent>
    </complexType>
    """


class NonRuleBasedFirstPartyAudienceSegment(FirstPartyAudienceSegment):
    """
    <complexType name="NonRuleBasedFirstPartyAudienceSegment">
    <annotation>
    <documentation> A {@link NonRuleBasedFirstPartyAudienceSegment} is a {@link FirstPartyAudienceSegment} owned by the publisher network. It doesn't contain a rule. Cookies are usually added to this segment via cookie upload. </documentation>
    </annotation>
    <complexContent>
    <extension base="tns:FirstPartyAudienceSegment">
    <sequence>
    <element maxOccurs="1" minOccurs="0" name="membershipExpirationDays" type="xsd:int">
    <annotation>
    <documentation> Specifies the number of days after which a user's cookie will be removed from the audience segment due to inactivity. This attribute is required and can be between 1 and 540. </documentation>
    </annotation>
    </element>
    </sequence>
    </extension>
    </complexContent>
    </complexType>
    """
    membershipExpirationDays: Optional[int] = Field(
        None,
        description="Specifies the number of days after which a user's cookie will be removed from the audience segment due to inactivity. This attribute is required and can be between 1 and 540."
    )


class RuleBasedFirstPartyAudienceSegment(FirstPartyAudienceSegment):
    """
    <complexType name="RuleBasedFirstPartyAudienceSegmentSummary">
    <annotation>
    <documentation> A {@link RuleBasedFirstPartyAudienceSegmentSummary} is a {@link FirstPartyAudienceSegment} owned by the publisher network. </documentation>
    </annotation>
    <complexContent>
    <extension base="tns:FirstPartyAudienceSegment">
    <sequence>
    <element maxOccurs="1" minOccurs="0" name="pageViews" type="xsd:int">
    <annotation>
    <documentation> Specifies the number of times a user's cookie must match the segment rule before it's associated with the audience segment. This is used in combination with {@link FirstPartyAudienceSegment#recencyDays} to determine eligibility of the association. This attribute is required and can be between 1 and 12. </documentation>
    </annotation>
    </element>
    <element maxOccurs="1" minOccurs="0" name="recencyDays" type="xsd:int">
    <annotation>
    <documentation> Specifies the number of days within which a user's cookie must match the segment rule before it's associated with the audience segment. This is used in combination with {@link FirstPartyAudienceSegment#pageViews} to determine eligibility of the association. This attribute is required only if {@link FirstPartyAudienceSegment#pageViews} is greater than 1. When required, it can be between 1 and 90. </documentation>
    </annotation>
    </element>
    <element maxOccurs="1" minOccurs="0" name="membershipExpirationDays" type="xsd:int">
    <annotation>
    <documentation> Specifies the number of days after which a user's cookie will be removed from the audience segment due to inactivity. This attribute is required and can be between 1 and 540. </documentation>
    </annotation>
    </element>
    </sequence>
    </extension>
    </complexContent>
    </complexType>
    """
    pageViews: Optional[int] = Field(
        None,
        description="Specifies the number of times a user's cookie must match the segment rule before it's associated with the audience segment. This is used in combination with {@link FirstPartyAudienceSegment#recencyDays} to determine eligibility of the association. This attribute is required and can be between 1 and 12."
    )
    recencyDays: Optional[int] = Field(
        None,
        description="Specifies the number of days within which a user's cookie must match the segment rule before it's associated with the audience segment. This is used in combination with {@link FirstPartyAudienceSegment#pageViews} to determine eligibility of the association. This attribute is required only if {@link FirstPartyAudienceSegment#pageViews} is greater than 1. When required, it can be between 1 and 90."
    )
    membershipExpirationDays: Optional[int] = Field(
        None,
        description="Specifies the number of days after which a user's cookie will be removed from the audience segment due to inactivity. This attribute is required and can be between 1 and 540."
    )
