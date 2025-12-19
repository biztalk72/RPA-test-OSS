#!/usr/bin/env python3
"""
Excel Automation Test for RPA Python
Tests Excel native application automation capabilities
"""

import sys
from pathlib import Path
import openpyxl
from openpyxl import Workbook

def test_excel_automation():
    """
    Excel automation test scenario:
    1. Create new workbook
    2. Write value 100 to cell A1
    3. Write formula =A1*2 to cell B1
    4. Verify B1 equals 200
    5. Update A1 to 250
    6. Verify B1 equals 500
    7. Write formula =SUM(A1:A5) to cell C1
    8. Write values 10, 20, 30, 40, 50 to cells A1:A5
    9. Verify C1 equals 150
    10. Save and close
    """
    
    output_file = Path("test-data/excel/test_output.xlsx")
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        # Step 1: Create new workbook
        print("Step 1: Creating new workbook")
        wb = Workbook()
        ws = wb.active
        
        # Step 2: Write value 100 to A1
        print("Step 2: Writing 100 to A1")
        ws['A1'] = 100
        
        # Step 3: Write formula =A1*2 to B1
        print("Step 3: Writing formula =A1*2 to B1")
        ws['B1'] = '=A1*2'
        
        # Save to calculate formulas
        wb.save(output_file)
        wb.close()
        
        # Reopen to get calculated values
        wb = openpyxl.load_workbook(output_file, data_only=True)
        ws = wb.active
        
        # Step 4: Verify B1 equals 200
        print("Step 4: Verifying B1 equals 200")
        b1_value = ws['B1'].value
        assert b1_value == 200, f"Expected B1=200, got {b1_value}"
        print(f"✓ B1 = {b1_value}")
        
        wb.close()
        
        # Step 5: Update A1 to 250
        print("Step 5: Updating A1 to 250")
        wb = openpyxl.load_workbook(output_file)
        ws = wb.active
        ws['A1'] = 250
        wb.save(output_file)
        wb.close()
        
        # Step 6: Verify B1 equals 500
        print("Step 6: Verifying B1 equals 500")
        wb = openpyxl.load_workbook(output_file, data_only=True)
        ws = wb.active
        b1_value = ws['B1'].value
        assert b1_value == 500, f"Expected B1=500, got {b1_value}"
        print(f"✓ B1 = {b1_value}")
        
        wb.close()
        
        # Step 7: Write formula =SUM(A1:A5) to C1
        print("Step 7: Writing formula =SUM(A1:A5) to C1")
        wb = openpyxl.load_workbook(output_file)
        ws = wb.active
        ws['C1'] = '=SUM(A1:A5)'
        
        # Step 8: Write values 10, 20, 30, 40, 50 to A1:A5
        print("Step 8: Writing values 10-50 to A1:A5")
        values = [10, 20, 30, 40, 50]
        for idx, val in enumerate(values, start=1):
            ws[f'A{idx}'] = val
        
        wb.save(output_file)
        wb.close()
        
        # Step 9: Verify C1 equals 150
        print("Step 9: Verifying C1 equals 150")
        wb = openpyxl.load_workbook(output_file, data_only=True)
        ws = wb.active
        c1_value = ws['C1'].value
        assert c1_value == 150, f"Expected C1=150, got {c1_value}"
        print(f"✓ C1 = {c1_value}")
        
        # Verify individual values
        for idx, expected in enumerate(values, start=1):
            actual = ws[f'A{idx}'].value
            assert actual == expected, f"Expected A{idx}={expected}, got {actual}"
        
        wb.close()
        
        print("\n✓ All Excel automation tests passed!")
        return 0
        
    except AssertionError as e:
        print(f"\n✗ Test failed: {e}")
        return 1
    except Exception as e:
        print(f"\n✗ Error during test: {e}")
        import traceback
        traceback.print_exc()
        return 1
    finally:
        # Cleanup
        if output_file.exists():
            output_file.unlink()

if __name__ == "__main__":
    sys.exit(test_excel_automation())
