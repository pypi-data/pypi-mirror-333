*** Settings ***
Documentation  doc
Test Tags      sometag


*** Test Cases ***
Test
    [Documentation]  doc
    [Tags]  sometag
    Pass
    Keyword
    One More

Test
    [Documentation]  doc
    [Tags]  othertag  sometag
    Pass
    Keyword
    One More

*** Keywords ***
Keyword
    [Documentation]  this is doc
    No Operation
    Pass
    No Operation
    Fail
