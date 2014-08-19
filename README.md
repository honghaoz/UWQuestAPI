UW Quest API
==========

This API provides full access to UW Quest.

## Accessing the API

## Endpoints

All responses contain two keys: "meta" and "data", "meta" contains informations about requests, and "data" contains data needed, this value maybe empty.

- "meta":

  Field       | Description
  ----------- | -------------
  status      | either "success" or "failure"
  message     | when status is "success", this is empty, when status is "failure", this will contain error reasons
  requests    | request operation sequence number
  version     | API version
  
- "data": See below

### Accout

- /account/login
  - method: POST/GET
  - Parameters

     Parameter  | Description
    ----------- | -------------
    userid      | Your UW Quest user id 
    password    | Your UW Quest password
    
  - Response

     Field  | Description
    ----------- | -------------
      sid       | New session id, used for subsequent operations

- /account/logout
  - method: POST
  - Parameters

     Parameter  | Description
    ----------- | -------------
    sid         | Session id 
    
  - Response: no data


### Personal Information

- /personalinformation/addresses
  - method: GET
  - Parameters

     Parameter  | Description
    ----------- | -------------
    sid         | Session id 
    
  - Response

     Field        | Description
    -----------   | -------------
    address_type  | address type
    address       | address
    
- /personalinformation/names
  - method: GET
  - Parameters

     Parameter  | Description
    ----------- | -------------
    sid         | Session id 
    
  - Response

     Field        | Description
    -----------   | -------------
    name_type     | name type
    name_prefix   | name prefix
    first_name    | first name
    middle_name   | middle name, if not exists, return "-"
    last_name     | last name
    name_suffix   | name suffix
    
- /personalinformation/phone_numbers
  - method: GET
  - Parameters

     Parameter  | Description
    ----------- | -------------
    sid         | Session id 
    
  - Response

     Field        | Description
    -----------   | -------------
    phone_type    | phone type
    telephone     | phone number
    ext           | extension
    country       | country code
    preferred     | is preferred, either "Y" or  "N"

- /personalinformation/email_addresses
  - method: GET
  - Parameters

     Parameter  | Description
    ----------- | -------------
    sid         | Session id 
    
  - Response

     Field                | Description
    -----------           | -------------
    description           | descriptipn for different email
    campus_email_address  | campus email address section
    campus_email          | campus email address
    delivered_to          | email server be delivered to
    alternate_email_address | alternate email address section
    email_type            | type of alternate email address
    email_address         | alternate email address
    
    
- /personalinformation/emergency_contacts
  - method: GET
  - Parameters

     Parameter  | Description
    ----------- | -------------
    sid         | Session id 
    
  - Response

     Field          | Description
    -----------     | -------------
    primary_contact | descriptipn for different email
    contact_name    | campus email address section
    relationship    | campus email address
    phone           | email server be delivered to
    extension       | alternate email address section
    country         | type of alternate email address
