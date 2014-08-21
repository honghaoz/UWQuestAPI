UW Quest API
==========

This API provides full access to University of Waterloo Quest, the Waterloo's student information system.

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
  - method: POST/GET
  - Parameters

     Parameter  | Description
    ----------- | -------------
    sid         | Session id 
    
  - Response: no data


### Personal Information

- /personal_information/addresses
  - method: POST/GET
  - Parameters

     Parameter  | Description
    ----------- | -------------
    sid         | Session id 
    
  - Response

     Field        | Description
    -----------   | -------------
    address_type  | address type
    address       | address
    
- /personal_information/names
  - method: POST/GET
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
    
- /personal_information/phone_numbers
  - method: POST/GET
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

- /personal_information/email_addresses
  - method: POST/GET
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
    
    
- /personal_information/emergency_contacts
  - method: POST/GET
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
    
- /personal_information/demographic_information
  - method: POST/GET
  - Parameters

     Parameter  | Description
    ----------- | -------------
    sid         | Session id 
    
  - Response

     Field                  | Description
    -----------             | -------------
    demographic_information | "gender", "date_of_birth", "id", "marital_status"
    national_identification_number  | "country", "national_id_type", "national_id"
    citizenship_information | "country", "description"  
    visa_or_permit_data     | "country", "type" 
    note                    | note on demographic information 

- /personal_information/citizenship_immigration_documents
  - method: POST/GET
  - Parameters

     Parameter  | Description
    ----------- | -------------
    sid         | Session id 
    
  - Response

     Field                  | Description
    -----------             | -------------
    visa_type | visa type
    country  | visa issue country
    date_received | received date
    expiration_date     | expiration date

### My Academics

- /my_academics/my_program
  - method: POST/GET
  - Parameters

     Parameter  | Description
    ----------- | -------------
    sid         | Session id 
    
  - Response

     Field        | Description
    -----------   | -------------
    current_program  | current program
    campus       | campus
    approved_load | approved load

- /my_academics/grades_index
  - method: POST/GET
  - Parameters

     Parameter  | Description
    ----------- | -------------
    sid         | Session id 
    
  - Response

     Field        | Description
    -----------   | -------------
    index  | int, the index for this term, used as parameters for get grades
    term       | which term
    career | undergraduate or graduate
    institution | institution
    
- /my_academics/grades_term
  - method: POST/GET
  - Parameters

     Parameter  | Description
    ----------- | -------------
    sid         | Session id 
    term_index	| index number which is responsed from /my_academics/grades_index
    
  - Response

     Field        | Description
    -----------   | -------------
    term       | which term
    career | undergraduate or graduate
    class | class category and number, e.g. CS 136
    description | class name
    units | units
    grade | your grades
    grade_points | your grade points
