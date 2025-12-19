# Quick Start Guide - RPA Benchmarking

## Setup

### 1. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 2. Test Individual Implementation (Optional)
Before running the full benchmark, you can test a single implementation:

```bash
# Test RPA Python Excel automation
python3 implementations/rpa-python/excel_test.py
```

### 3. Run Full Benchmark Suite (10 iterations each)
```bash
python3 test_runner.py
```

This will:
- Run each test scenario 10 times consecutively
- Collect metrics (execution time, memory, CPU usage)
- Calculate statistics (mean, median, std deviation)
- Generate detailed reports in `results/` directory

## What Gets Tested

### Current Tests
- **Excel Automation** (rpa-python): Native Excel file manipulation with formulas

### Planned Tests
- Robot Framework implementation
- TagUI implementation  
- OpenRPA implementation (Windows only)
- Web scraping scenarios
- API integration tests
- File operations tests
- Stress tests

## Understanding Results

### During Execution
You'll see real-time output:
```
Running rpa-python - excel-automation - Iteration 1
Step 1: Creating new workbook
Step 2: Writing 100 to A1
...
✓ All Excel automation tests passed!
```

### After Completion
Results are saved to:
- `results/benchmark_results_TIMESTAMP.json` - Raw data for all runs
- `results/summary_report.txt` - Statistical summary

### Metrics Collected
- **Duration**: Execution time in milliseconds
- **Memory**: Average memory usage in MB
- **CPU**: Average CPU utilization percentage
- **Status**: success/failed/error
- **Errors**: Error messages if any

### Statistical Analysis
For each test scenario:
- Mean execution time
- Median execution time
- Standard deviation (measures consistency)
- Min/Max values
- Success rate

## Adding New Tests

### 1. Create Test Script
Add your test implementation in the appropriate directory:
```
implementations/
  ├── rpa-python/
  │   └── your_test.py
  ├── robot-framework/
  │   └── your_test.robot
  └── tagui/
      └── your_test.tag
```

### 2. Update test_runner.py
Add configuration to `test_configs` list:
```python
{
    "tool": "your-tool",
    "scenario": "your-scenario",
    "command": ["command", "to", "run", "test"]
}
```

### 3. Run Benchmark
```bash
python3 test_runner.py
```

## Troubleshooting

### Missing Dependencies
```bash
pip install --upgrade -r requirements.txt
```

### Permission Issues
```bash
chmod +x test_runner.py
chmod +x implementations/*/.*test.*
```

### Excel Not Found (macOS)
The current implementation uses openpyxl which works with Excel files directly without requiring Microsoft Excel to be installed.

For native Excel application testing, you would need:
- Microsoft Excel installed
- Additional libraries like `pywin32` (Windows) or `appscript` (macOS)

## Next Steps

1. **Review test scenarios**: Check `test-scenarios.md` for detailed test plans
2. **Implement remaining tests**: Add implementations for other RPA tools
3. **Run benchmarks**: Execute 10 iterations of each test
4. **Analyze results**: Compare performance across tools
5. **Document findings**: Update `docs/` with your analysis

## Tips for Harsh Benchmarking

- Clean system state between runs (close other apps)
- Run tests during low system activity
- Use consistent test data
- Monitor for memory leaks over iterations
- Test edge cases and error conditions
- Verify results accuracy, not just speed
