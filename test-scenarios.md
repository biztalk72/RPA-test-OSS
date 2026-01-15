# RPA Benchmarking Test Scenarios

## Overview
Each test scenario will be executed 100 times per RPA solution to ensure statistical reliability and identify consistency issues.

## Test Scenario 1: Integrated Business Workflow (PRIMARY)

### Objective
Simulate a real-world business automation workflow that combines Excel data management, web data collection, and comparative analysis.

### Business Context
**Scenario**: Daily Product Price Monitoring System
- A company maintains a product catalog in Excel with target prices
- Need to scrape competitor prices from e-commerce websites daily
- Compare actual market prices against target prices
- Generate analysis report with price variance calculations
- Highlight products that need price adjustments

### Workflow Steps

#### Phase 1: Excel Initial Setup (Data Preparation)
1. Create Excel workbook with "Product Catalog" sheet
2. Add product data:
   - Column A: Product Name (5 products)
   - Column B: Target Price
   - Column C: Category
   - Column D: Last Updated Date
3. Write formulas for initial calculations
4. Save as `product_catalog.xlsx`

#### Phase 2: Web Data Collection
5. Navigate to test e-commerce site (quotes.toscrape.com as proxy)
6. Extract data for 5 items:
   - Item identifier
   - Current price/quote text
   - Author/Source
   - Tags/Categories
7. Store scraped data in structured format (list/array)
8. Log collection timestamp

#### Phase 3: Excel Data Integration & Analysis
9. Open existing `product_catalog.xlsx`
10. Create new sheet "Market Data"
11. Write scraped data to "Market Data" sheet:
    - Column A: Item Name
    - Column B: Market Price (use quote text length as proxy numeric value)
    - Column C: Source
    - Column D: Collection Date
12. Create "Analysis" sheet with comparison formulas:
    - Calculate price variance: `=Market_Price - Target_Price`
    - Calculate variance percentage: `=(Variance/Target_Price)*100`
    - Flag items: `=IF(Variance>10%, "REVIEW", "OK")`
13. Add summary statistics:
    - Average variance
    - Max/Min variance
    - Count of items needing review
14. Save updated workbook as `product_analysis.xlsx`

#### Phase 4: Verification & Validation
15. Re-open both Excel files
16. Verify all formulas calculated correctly
17. Confirm data integrity:
    - Original data unchanged in catalog
    - Market data properly imported
    - Analysis formulas working
18. Compare initial vs final state
19. Generate success/failure report
20. Cleanup test files

### Success Criteria
- All 3 phases complete without errors
- Excel formulas calculate correctly
- Web data successfully scraped (5 items minimum)
- Data properly integrated across sheets
- Analysis calculations accurate
- Files saved and verified
- Original data integrity maintained
- Cleanup successful

### Metrics to Collect
- Total workflow duration (ms)
- Phase 1 duration (Excel setup)
- Phase 2 duration (Web scraping)
- Phase 3 duration (Integration & Analysis)
- Phase 4 duration (Verification)
- Memory usage (peak MB)
- CPU usage (%)
- Success/failure status
- Number of retries (if any)
- Error types (if any)

### Evaluation Criteria
- **Correctness**: All data accurate and formulas working (40 points)
- **Performance**: Execution time < 15 seconds (20 points)
- **Reliability**: 95%+ success rate over 100 runs (20 points)
- **Resource Efficiency**: Memory < 100MB, CPU < 80% (10 points)
- **Error Handling**: Graceful failure recovery (10 points)
- **Total**: 100 points

---

## Test Scenario 2: Excel Native Application Automation (LEGACY)

### Objective
Test the ability to interact with native Excel application, manipulate cells, and verify formula calculations.

### Steps
1. Launch Excel application
2. Create new workbook
3. Write value `100` to cell A1
4. Write formula `=A1*2` to cell B1
5. Read and verify B1 equals `200`
6. Update A1 to `250`
7. Read and verify B1 equals `500`
8. Write formula `=SUM(A1:A5)` to cell C1
9. Write values 10, 20, 30, 40, 50 to cells A1:A5
10. Verify C1 equals `150`
11. Save workbook as `test_output.xlsx`
12. Close Excel

### Success Criteria
- All cell values match expected results
- Formula calculations are correct
- File saved successfully
- No crashes or hangs

### Metrics to Collect
- Total execution time (ms)
- Memory usage (MB)
- Success/failure status
- Error messages (if any)

## Test Scenario 2: Web Scraping

### Objective
Extract structured data from a public website with pagination.

### Steps
1. Navigate to https://quotes.toscrape.com
2. Extract all quotes from page 1 (text and author)
3. Navigate to next page
4. Extract all quotes from page 2
5. Continue for 5 pages total
6. Save results to JSON file
7. Verify extracted data structure

### Success Criteria
- All quotes extracted correctly
- Authors matched to quotes
- Pagination handled properly
- Data saved in valid JSON format

### Metrics to Collect
- Total execution time (ms)
- Number of quotes extracted
- Network latency
- Success rate

## Test Scenario 3: Form Automation

### Objective
Fill complex web forms with validation.

### Steps
1. Navigate to https://demoqa.com/automation-practice-form
2. Fill text inputs (name, email, mobile)
3. Select radio buttons (gender)
4. Select checkboxes (hobbies)
5. Upload a file
6. Select date from calendar
7. Fill address
8. Submit form
9. Verify submission success

### Success Criteria
- All fields filled correctly
- Form validation passed
- Submission confirmed
- No timeout errors

### Metrics to Collect
- Total execution time (ms)
- Element interaction time
- Success/failure status

## Test Scenario 4: File Operations

### Objective
Perform bulk file operations efficiently.

### Steps
1. Create 100 text files with sequential names
2. Write unique content to each file
3. Read content from 50 random files
4. Rename all files with timestamp prefix
5. Move files to organized folder structure (by date)
6. Delete files older than specific criteria
7. Verify final count and structure

### Success Criteria
- All files created successfully
- Content integrity maintained
- Rename operation accurate
- Folder structure correct

### Metrics to Collect
- Total execution time (ms)
- Files processed per second
- I/O errors count
- Disk usage

## Test Scenario 5: API Integration

### Objective
Test REST API interaction capabilities.

### Steps
1. GET request to https://jsonplaceholder.typicode.com/posts
2. Parse JSON response
3. Filter posts by userId = 1
4. POST new post with data
5. PUT update existing post
6. DELETE a post
7. Handle authentication headers
8. Verify response status codes

### Success Criteria
- All HTTP methods executed successfully
- JSON parsing correct
- Status codes verified
- Error handling works

### Metrics to Collect
- Total execution time (ms)
- Request latency per endpoint
- Success rate
- Error types

## Test Scenario 6: Stress Test - High Volume Data Processing

### Objective
Process large datasets to test stability and performance under load.

### Steps
1. Generate CSV with 1000 rows of data
2. Read entire CSV
3. Perform data transformation (calculations, string operations)
4. Filter rows based on criteria
5. Write results to new CSV
6. Verify data integrity
7. Process 10 such files sequentially

### Success Criteria
- All rows processed correctly
- No memory leaks
- Consistent performance across iterations
- Output data valid

### Metrics to Collect
- Total execution time (ms)
- Rows processed per second
- Memory usage (peak and average)
- CPU usage percentage

## Test Scenario 7: Error Recovery

### Objective
Test error handling and recovery mechanisms.

### Steps
1. Attempt to open non-existent file
2. Handle exception gracefully
3. Try to access invalid URL
4. Handle timeout
5. Attempt invalid Excel operation
6. Recover and continue execution
7. Log all errors appropriately

### Success Criteria
- Errors caught and logged
- Process continues after errors
- No unhandled exceptions
- Proper cleanup performed

### Metrics to Collect
- Recovery time per error (ms)
- Error logging completeness
- Process stability
- Final status

## Test Execution Plan

### Iteration Protocol
- Run each scenario 10 times consecutively
- Clean environment between runs
- Randomize test order to avoid bias
- Record all metrics in structured format

### Data Collection
- Timestamp each run
- Capture stdout/stderr
- Monitor system resources
- Store results in JSON format

### Result Format
```json
{
  "tool": "tagui",
  "scenario": "excel-automation",
  "iteration": 1,
  "timestamp": "2024-01-01T12:00:00Z",
  "duration_ms": 1234,
  "memory_mb": 56,
  "cpu_percent": 45,
  "status": "success",
  "errors": []
}
```

### Statistical Analysis
- Calculate mean, median, std deviation
- Identify outliers
- Compare consistency across tools
- Generate visualization charts
