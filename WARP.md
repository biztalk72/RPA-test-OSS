# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project Overview

RPA-test-OSS is an RPA (Robotic Process Automation) benchmarking framework that compares different open-source RPA solutions through standardized test scenarios. The project focuses on measuring performance, stability, and resource efficiency across multiple RPA tools including TagUI, Robot Framework, OpenRPA, and RPA for Python.

## Essential Commands

### Setup
```bash
# Install Python dependencies
pip install -r requirements.txt

# Create directory structure
./setup_structure.sh
```

### Running Tests

```bash
# Run full benchmark suite (10 iterations each test)
python3 test_runner.py

# Test individual implementation
python3 implementations/rpa-python/excel_test.py
python3 implementations/rpa-python/business_workflow_test.py

# Run Robot Framework tests
robot --outputdir results/robot-logs --log NONE --report NONE implementations/robot-framework/excel_test.robot
```

### Development

```bash
# Run single test iteration for debugging
python3 implementations/<tool>/<test_file>.py

# Clean test artifacts
rm -rf test-data/*/
rm -rf results/
```

## Architecture

### Core Components

**test_runner.py**: Central benchmark orchestration system
- Executes test scenarios multiple times (configurable iterations, default 10)
- Collects metrics: execution time (ms), memory usage (MB), CPU utilization (%)
- Generates statistical analysis: mean, median, std deviation, min/max
- Outputs results to `results/` directory as JSON and summary reports
- Uses psutil for resource monitoring during test execution

**Test Configuration Structure**:
```python
test_configs = [
    {
        "tool": "<rpa-tool-name>",
        "scenario": "<scenario-name>",
        "command": ["python3", "path/to/test.py"],
        "iterations": 100  # Number of test runs
    }
]
```

### Test Scenarios

The project uses two primary test scenarios defined in `test-scenarios.md`:

1. **Integrated Business Workflow** (PRIMARY): Multi-phase workflow simulating real-world RPA use case
   - Phase 1: Excel data preparation with product catalog
   - Phase 2: Web scraping from quotes.toscrape.com
   - Phase 3: Data integration and analysis across multiple Excel sheets
   - Phase 4: Verification and cleanup
   - Success criteria: 100% accuracy, <15s execution, 95%+ success rate

2. **Excel Automation** (LEGACY): Native Excel file manipulation
   - Cell read/write operations
   - Formula creation and validation
   - Multi-sheet operations

### Implementation Directory Structure

```
implementations/
├── rpa-python/           # Python-based RPA tests using openpyxl, requests, BeautifulSoup
│   ├── excel_test.py              # Excel automation test (formula verification)
│   ├── business_workflow_test.py  # Multi-phase integrated workflow
│   └── integrated_test.py
├── robot-framework/      # Robot Framework tests
│   └── excel_test.robot
├── tagui/               # TagUI tests (planned)
└── openrpa/             # OpenRPA tests (planned, Windows only)
```

### Test Data Management

- Test artifacts stored in `test-data/` (automatically created)
- Each test creates isolated subdirectories: `test-data/excel/`, `test-data/workflow/`
- Tests perform cleanup after execution to prevent data accumulation
- Output files use predictable naming: `test_output.xlsx`, `product_catalog.xlsx`, `product_analysis.xlsx`

### Results and Reporting

The benchmark runner produces:
- `results/benchmark_results_YYYYMMDD_HHMMSS.json` - Raw metrics for all test iterations
- `results/summary_report.txt` - Statistical summary with success rates and timing analysis
- Detailed BMT results documented in `docs/bmt-detailed-results.md`

## Key Implementation Patterns

### Resource Monitoring
The test_runner.py monitors test processes using psutil:
- Samples resource usage every 100ms during test execution
- Calculates average memory and CPU from all samples
- Tracks process-specific metrics when available, falls back to system-wide metrics

### Test Isolation
Each test implementation should:
- Create its own test data in `test-data/<scenario>/`
- Clean up artifacts in `finally` blocks
- Return exit code 0 for success, 1 for failure
- Print structured output for test_runner.py to capture

### Adding New Test Implementations

1. Create test file in `implementations/<tool>/`
2. Implement test logic following existing patterns:
   - Use try/except/finally for robust error handling
   - Print progress messages for each test step
   - Verify results with assertions
   - Clean up test artifacts
3. Update test_configs list in test_runner.py:
   ```python
   {
       "tool": "new-tool",
       "scenario": "scenario-name",
       "command": ["command", "to", "run"],
       "iterations": 10
   }
   ```

### Statistical Analysis Methodology
- Each scenario runs 10 times by default (configurable to 100 for harsh benchmarking)
- Metrics collected: duration_ms, memory_mb, cpu_percent, status, errors
- Statistics calculated only on successful runs
- Standard deviation measures consistency/stability
- Success rate tracks reliability (target: 95%+)

## Python Dependencies

Key libraries used (from requirements.txt):
- **openpyxl**: Excel file manipulation without requiring Excel installation
- **psutil**: System resource monitoring (memory, CPU)
- **requests + beautifulsoup4**: Web scraping capabilities
- **robotframework + rpaframework**: Robot Framework test execution
- **selenium**: Browser automation (for future tests)
- **pandas + matplotlib**: Data analysis and visualization (for future reporting)

## Testing Philosophy

This project emphasizes "harsh benchmarking":
- Multiple iterations to identify consistency issues and outliers
- Clean system state between runs
- Resource monitoring to detect memory leaks
- Verification of result accuracy, not just execution speed
- Real-world scenarios over synthetic benchmarks
