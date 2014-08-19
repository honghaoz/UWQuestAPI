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
  - method: POST
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
    middle_name   | middle name
    last_name     | last name
    name_suffix   | name suffix
