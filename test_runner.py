#!/usr/bin/env python3
"""
RPA Benchmark Test Runner
Executes each test scenario 10 times and collects metrics
"""

import json
import time
import psutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any
import statistics

class BenchmarkRunner:
    def __init__(self, output_dir: str = "results"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.results: List[Dict[str, Any]] = []
        
    def measure_resources(self, process=None):
        """Measure current resource usage"""
        if process:
            try:
                proc = psutil.Process(process.pid)
                memory_mb = proc.memory_info().rss / 1024 / 1024
                cpu_percent = proc.cpu_percent(interval=0.1)
            except:
                memory_mb = 0
                cpu_percent = 0
        else:
            memory_mb = psutil.virtual_memory().used / 1024 / 1024
            cpu_percent = psutil.cpu_percent(interval=0.1)
            
        return {
            "memory_mb": round(memory_mb, 2),
            "cpu_percent": round(cpu_percent, 2)
        }
    
    def run_test(self, tool: str, scenario: str, test_command: List[str], 
                 iteration: int) -> Dict[str, Any]:
        """Run a single test iteration"""
        print(f"Running {tool} - {scenario} - Iteration {iteration}")
        
        result = {
            "tool": tool,
            "scenario": scenario,
            "iteration": iteration,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "duration_ms": 0,
            "memory_mb": 0,
            "cpu_percent": 0,
            "status": "failed",
            "errors": [],
            "stdout": "",
            "stderr": ""
        }
        
        start_time = time.time()
        start_resources = self.measure_resources()
        
        try:
            process = subprocess.Popen(
                test_command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Monitor resources during execution
            resource_samples = []
            while process.poll() is None:
                resource_samples.append(self.measure_resources(process))
                time.sleep(0.1)
            
            stdout, stderr = process.communicate()
            
            end_time = time.time()
            duration_ms = int((end_time - start_time) * 1000)
            
            # Calculate average resources
            if resource_samples:
                avg_memory = statistics.mean([r["memory_mb"] for r in resource_samples])
                avg_cpu = statistics.mean([r["cpu_percent"] for r in resource_samples])
            else:
                avg_memory = 0
                avg_cpu = 0
            
            result.update({
                "duration_ms": duration_ms,
                "memory_mb": round(avg_memory, 2),
                "cpu_percent": round(avg_cpu, 2),
                "status": "success" if process.returncode == 0 else "failed",
                "stdout": stdout,
                "stderr": stderr,
                "exit_code": process.returncode
            })
            
            if process.returncode != 0:
                result["errors"].append(f"Exit code: {process.returncode}")
                
        except Exception as e:
            end_time = time.time()
            result["duration_ms"] = int((end_time - start_time) * 1000)
            result["errors"].append(str(e))
            result["status"] = "error"
        
        return result
    
    def run_scenario_iterations(self, tool: str, scenario: str, 
                                test_command: List[str], iterations: int = 10):
        """Run a scenario multiple times"""
        print(f"\n{'='*60}")
        print(f"Starting: {tool} - {scenario}")
        print(f"Iterations: {iterations}")
        print(f"{'='*60}\n")
        
        scenario_results = []
        
        for i in range(1, iterations + 1):
            result = self.run_test(tool, scenario, test_command, i)
            scenario_results.append(result)
            self.results.append(result)
            
            # Save after each iteration
            self.save_results()
            
            # Brief pause between iterations
            time.sleep(1)
        
        # Print summary for this scenario
        self.print_scenario_summary(tool, scenario, scenario_results)
        
    def print_scenario_summary(self, tool: str, scenario: str, results: List[Dict]):
        """Print summary statistics for a scenario"""
        print(f"\n{'='*60}")
        print(f"Summary: {tool} - {scenario}")
        print(f"{'='*60}")
        
        successful = [r for r in results if r["status"] == "success"]
        failed = [r for r in results if r["status"] != "success"]
        
        print(f"Success Rate: {len(successful)}/{len(results)} "
              f"({len(successful)/len(results)*100:.1f}%)")
        
        if successful:
            durations = [r["duration_ms"] for r in successful]
            memory = [r["memory_mb"] for r in successful]
            cpu = [r["cpu_percent"] for r in successful]
            
            print(f"\nExecution Time (ms):")
            print(f"  Mean: {statistics.mean(durations):.2f}")
            print(f"  Median: {statistics.median(durations):.2f}")
            print(f"  Std Dev: {statistics.stdev(durations) if len(durations) > 1 else 0:.2f}")
            print(f"  Min: {min(durations)}")
            print(f"  Max: {max(durations)}")
            
            print(f"\nMemory Usage (MB):")
            print(f"  Mean: {statistics.mean(memory):.2f}")
            print(f"  Max: {max(memory):.2f}")
            
            print(f"\nCPU Usage (%):")
            print(f"  Mean: {statistics.mean(cpu):.2f}")
            print(f"  Max: {max(cpu):.2f}")
        
        if failed:
            print(f"\nFailed Runs: {len(failed)}")
            for r in failed:
                print(f"  Iteration {r['iteration']}: {r['errors']}")
        
        print(f"{'='*60}\n")
    
    def save_results(self):
        """Save results to JSON file"""
        output_file = self.output_dir / f"benchmark_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(output_file, 'w') as f:
            json.dump(self.results, f, indent=2)
    
    def generate_summary_report(self):
        """Generate overall summary report"""
        print(f"\n{'='*60}")
        print("OVERALL BENCHMARK SUMMARY")
        print(f"{'='*60}\n")
        
        # Group by tool and scenario
        by_tool_scenario = {}
        for result in self.results:
            key = (result["tool"], result["scenario"])
            if key not in by_tool_scenario:
                by_tool_scenario[key] = []
            by_tool_scenario[key].append(result)
        
        # Summary table
        print(f"{'Tool':<20} {'Scenario':<25} {'Success':<10} {'Avg Time (ms)':<15}")
        print("-" * 70)
        
        for (tool, scenario), results in sorted(by_tool_scenario.items()):
            successful = [r for r in results if r["status"] == "success"]
            success_rate = f"{len(successful)}/{len(results)}"
            avg_time = statistics.mean([r["duration_ms"] for r in successful]) if successful else 0
            
            print(f"{tool:<20} {scenario:<25} {success_rate:<10} {avg_time:<15.2f}")
        
        print(f"\n{'='*60}\n")
        
        # Save summary to file
        summary_file = self.output_dir / "summary_report.txt"
        with open(summary_file, 'w') as f:
            f.write("RPA Benchmark Summary Report\n")
            f.write("=" * 60 + "\n\n")
            for (tool, scenario), results in sorted(by_tool_scenario.items()):
                f.write(f"\n{tool} - {scenario}\n")
                f.write("-" * 40 + "\n")
                successful = [r for r in results if r["status"] == "success"]
                if successful:
                    durations = [r["duration_ms"] for r in successful]
                    f.write(f"Success Rate: {len(successful)}/{len(results)}\n")
                    f.write(f"Mean Duration: {statistics.mean(durations):.2f} ms\n")
                    f.write(f"Median Duration: {statistics.median(durations):.2f} ms\n")
                    f.write(f"Std Dev: {statistics.stdev(durations) if len(durations) > 1 else 0:.2f} ms\n")

def main():
    """Main execution"""
    runner = BenchmarkRunner()
    
    # Example test configuration
    # In practice, you'll add actual test commands for each tool/scenario
    
    test_configs = [
        {
            "tool": "rpa-python",
            "scenario": "business-workflow",
            "command": ["python3", "implementations/rpa-python/business_workflow_test.py"],
            "iterations": 100
        },
        {
            "tool": "rpa-python",
            "scenario": "excel-automation",
            "command": ["python3", "implementations/rpa-python/excel_test.py"],
            "iterations": 100
        },
        # {
        #     "tool": "robot-framework",
        #     "scenario": "business-workflow",
        #     "command": ["robot", "--outputdir", "results/robot-logs", "--log", "NONE", "--report", "NONE", "implementations/robot-framework/business_workflow_test.robot"],
        #     "iterations": 100
        # },
        # {
        #     "tool": "robot-framework",
        #     "scenario": "excel-automation",
        #     "command": ["robot", "--outputdir", "results/robot-logs", "--log", "NONE", "--report", "NONE", "implementations/robot-framework/excel_test.robot"],
        #     "iterations": 100
        # },
    ]
    
    if len(test_configs) == 0:
        print("No test configurations defined yet.")
        print("Please implement test scripts for each RPA tool and scenario.")
        print("\nExample structure:")
        print("  implementations/")
        print("    tagui/excel_test.tag")
        print("    robot-framework/excel_test.robot")
        print("    rpa-python/excel_test.py")
        print("    openrpa/excel_test.xaml")
        return 1
    
    # Run all tests
    for config in test_configs:
        iterations = config.get("iterations", 10)  # Default to 10 if not specified
        runner.run_scenario_iterations(
            tool=config["tool"],
            scenario=config["scenario"],
            test_command=config["command"],
            iterations=iterations
        )
    
    # Generate final report
    runner.generate_summary_report()
    
    print(f"\nResults saved to: {runner.output_dir}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
