UWQuestAPI
==========

University of Waterloo Quest API.
This API provides full access to Quest.

## Accessing the API

## Endpoints

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
    status      | "success" or "failure"
    sid         | New session id, used for subsequent operations
    reason      | If failure happens, this filed will contain reasons
    

- /account/logout
  - method: POST
  - Parameters

     Parameter  | Description
    ----------- | -------------
    sid         | Session id 
    
  - Response

     Field  | Description
    ----------- | -------------
    status      | "success" or "failure"
    reason      | If failure happens, this filed will contain reasons


### Food Services

- **[/personalinformation/menu](v2/foodservices/menu.md)**
- **[/personalinformation/addresses](v2/foodservices/menu.md)**
