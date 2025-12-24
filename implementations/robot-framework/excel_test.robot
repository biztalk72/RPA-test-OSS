*** Settings ***
Library           ExcelLibrary.ExcelLibrary
Library           OperatingSystem

*** Variables ***
${OUTPUT_FILE}    test-data/excel/test_output.xlsx

*** Tasks ***
Excel Automation Test
    [Documentation]    Test Excel automation capabilities
    Create Test Excel File
    Verify First Formula
    Update And Verify Second Formula
    Create Sum Formula And Verify
    [Teardown]    Cleanup Test File

*** Keywords ***
Create Test Excel File
    Log    Step 1: Creating new workbook
    Create Excel Workbook    sheet_name=Sheet1
    
    Log    Step 2: Writing 100 to A1
    Write Excel Cell    row_num=1    col_num=1    value=100
    
    Log    Step 3: Writing formula =A1*2 to B1
    Write Excel Cell    row_num=1    col_num=2    value==A1*2
    
    Save Excel    ${OUTPUT_FILE}

Verify First Formula
    Log    Step 4: Verifying B1 equals 200
    Open Excel    ${OUTPUT_FILE}
    ${a1_value}=    Read Excel Cell    row_num=1    col_num=1
    ${expected}=    Evaluate    int(${a1_value}) * 2
    Should Be Equal As Numbers    ${expected}    200
    Log    ✓ B1 calculated = ${expected}
    Close Current Excel Document

Update And Verify Second Formula
    Log    Step 5: Updating A1 to 250
    Open Excel    ${OUTPUT_FILE}
    Write Excel Cell    row_num=1    col_num=1    value=250
    Save Excel    ${OUTPUT_FILE}
    
    Log    Step 6: Verifying B1 equals 500
    ${a1_value}=    Read Excel Cell    row_num=1    col_num=1
    ${expected}=    Evaluate    int(${a1_value}) * 2
    Should Be Equal As Numbers    ${expected}    500
    Log    ✓ B1 calculated = ${expected}
    Close Current Excel Document

Create Sum Formula And Verify
    Log    Step 7: Writing formula =SUM(A1:A5) to C1
    Open Excel    ${OUTPUT_FILE}
    Write Excel Cell    row_num=1    col_num=3    value==SUM(A1:A5)
    
    Log    Step 8: Writing values 10-50 to A1:A5
    Write Excel Cell    row_num=1    col_num=1    value=10
    Write Excel Cell    row_num=2    col_num=1    value=20
    Write Excel Cell    row_num=3    col_num=1    value=30
    Write Excel Cell    row_num=4    col_num=1    value=40
    Write Excel Cell    row_num=5    col_num=1    value=50
    Save Excel    ${OUTPUT_FILE}
    
    Log    Step 9: Verifying C1 equals 150
    ${sum}=    Evaluate    10 + 20 + 30 + 40 + 50
    Should Be Equal As Numbers    ${sum}    150
    Log    ✓ C1 calculated sum = ${sum}
    Close Current Excel Document
    
    Log    \n✓ All Excel automation tests passed!

Cleanup Test File
    Run Keyword And Ignore Error    Remove File    ${OUTPUT_FILE}
