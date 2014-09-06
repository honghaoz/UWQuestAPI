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
    current_sub_plan | sub plan
    campus       | campus
    approved_load | approved load

- /my_academics/grades
  - There are two kinds of response. 
  	- If only sid is provided, response will be terms that can be queried
  	- If sid and term index are provided, response will be grades for queried term
  
  - 1) method: POST/GET
  - 1) Parameters

     Parameter  | Description
    ----------- | -------------
    sid         | Session id 
    
  - 1) Response

     Field        | Description
    -----------   | -------------
    term_index  | int, the index for this term, used as parameters for get grades
    term       | which term
    career | undergraduate or graduate
    institution | institution


  - 2) method: POST/GET
  - 2) Parameters

     Parameter  | Description
    ----------- | -------------
    sid         | Session id 
    term_index	| index number which is responsed from /my_academics/grades
    
  - 2) Response

     Field        | Description
    -----------   | -------------
    term       | which term
    career | undergraduate or graduate
    message | message like "Grades for the term will be available on Dec 20, 2014."
    institution | institution
    class | class category and number, e.g. CS 136
    description | class name
    units | units
    grade | your grades
    grade_points | your grade points
    
- /my_academics/unofficial_transcript
  - There are two kinds of response. 
  	- If only sid is provided, response will be options that can be queried
  	- If sid, academic_institution and report_type are provided, response will be unofficial transcript queried

  - 1) method: POST/GET
  - 1) Parameters

     Parameter  | Description
    ----------- | -------------
    sid         | Session id 
    
  - 1) Response

     Field        | Description
    -----------   | -------------
    academic_institution | institution issues transcript
    report_type | type
    value | option values, e.g. 'UNGRD', 'UNUG', 'UWATR'
    description | description for option value
    selected    | whether is selected by default "Y" or "N"
    

  - 2) method: POST/GET
  - 2) Parameters

     Parameter  | Description
    ----------- | -------------
    sid         | Session id 
    academic_institution | value get from /my_academics/unofficial_transcript
    report_type | value get from /my_academics/unofficial_transcript
    
  - 2) Response

     Field        | Description
    -----------   | -------------
    data | html source code for transcript
    
- /my_academics/my_advisors
  - method: POST/GET
  - Parameters

     Parameter  | Description
    ----------- | -------------
    sid         | Session id 
    
  - Response

     Field        | Description
    -----------   | -------------
    academic_program | 
    (program plan name) | e.g. master_of_engineering
    advisor_name | a list of advisors' name

### Enroll

- /enroll/my_class_schedule
  - There are two kinds of response. 
  	- If only sid is provided, response will be terms that can be queried
  	- If sid and term index are provided, response will be class schedule for queried term
  	
  - 1) method: POST/GET
  - 1) Parameters

     Parameter  | Description
    ----------- | -------------
    sid         | Session id 
    
  - 1) Response

     Field        | Description
    -----------   | -------------
    term_index  | int, the index for this term, used as parameters for get class schedule
    term       | which term
    career | undergraduate or graduate
    institution | institution
  	

  - 2) method: POST/GET
  - 2) Parameters

     Parameter  | Description
    ----------- | -------------
    sid         | Session id 
    term_index	| index number which is responsed from /my_academics/my_class_schedule
    
    
  - 2) Response

     Field        | Description
    -----------   | -------------
    term       | which term
    career | undergraduate or graduate
    institution | institution
    classes | list contains classes
    status | enrolled or not
    subject | e.g. CS, ECE
    category_number | 136
    description | class name
    grading | grading method
    units | units
    grade | your grades
    components | list contains class components
    class_nbr | class number
    section | section
    component | LEC TUT TST
    days_&_times | days and times
    room | class room number
    instructor | instructor name
    start/end_date | start/end date
    
- /enroll/add

  - method: POST/GET
  - Parameters

     Parameter  | Description
    ----------- | -------------
    sid         | Session id 
    
  - Response

     Field        | Description
    -----------   | -------------
      |
    
- /enroll/drop


- /enroll/component_swap

- /enroll/search_for_classes

	- There are two kinds of response. 
  		- If only sid is provided, response will be search criteria and option values that can be queried
  		- If sid and at least two criterias are provided, response will be results for this search
  	
  - 1) method: POST/GET
  - 1) Parameters

     Parameter  | Description
    ----------- | -------------
    sid         | Session id 
    
  - 1) Response

     Field        | Description
    -----------   | -------------
    institution   | which institution
    term		   | which term
    course_subject| eg. "CS", "ECE"
    course_number | 
    course_number_relations | contians, equal...
    course_career | undergraduate or graduate
    show_open_classes_only | "Y" or "N"

  - 2) method: POST/GET
  - 2) Parameters

     Parameter  | Description
    ----------- | -------------
    sid         | Session id 
    institution   | which institution
    term		   | which term
    course_subject| eg. "CS", "ECE"
    course_number | 
    course_number_relations | contians, equal...
    course_career | "UG" or "GRD"
    show_open_classes_only | "Y" or "N"
    
    
  - 2) Response

     Field        | Description
    -----------   | -------------
    course_subject       | 
    course_number |
    course_name |
    sections |
    	sections_number |
    	class_number |
    	status | Open or Close
    	session | Regular
    	section_info_request_value | value used for get detail info for this section
    	schedules | section schedules
    	days_&_times | 
    	meeting_dates  |
    	instructor | 
    	room |
    	
    	
    	
    	

    
    
