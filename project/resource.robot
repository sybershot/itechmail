*** Settings ***
Variables  config/constants.py
Library  utils/browser_manager/BrowserManager.py


*** Keywords ***
Open Browser
    ${browser} =  Get Browser  ${BROWSER_TYPE}
    Set Suite Variable  ${browser}  ${browser}

Test Teardown
    Close Browser  ${browser}