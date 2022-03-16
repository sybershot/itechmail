*** Settings ***
Documentation  Testing automated email messaging to multiple recipients
Default Tags  Smoke

Variables  config/constants.py
Library  project/steps/MailSteps.py
Resource  project/resource.robot

Suite Setup  Open Browser
Test Teardown  Run keyword if test failed  Fatal Error  Step failed


*** Test Cases ***

Send Emails
     ${initial_message} =  Load Message From JSON
     ${prepared_message} =  Prepare message  ${initial_message}
     Send Message  ${prepared_message}
     Set Suite Variable  ${initial_message}

Check Yopmail
    ${page_object} =  Open Yopmail  ${browser}
    Enter Inbox  ${page_object}
    ${from_yopmail} =  Fetch Email  ${page_object}
    Set Suite Variable  ${from_yopmail}
    Test Teardown

Check Mailto
    ${from_mailto} =  Request Email
    Set Suite Variable  ${from_mailto}

Compare Emails
    Compare Fetched Emails  ${initial_message}  ${from_yopmail}  ${from_mailto}