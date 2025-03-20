import os
import subprocess
import logging
import shlex  # Add this import
from datetime import datetime
import shutil
from pathlib import Path
from .database import log_run
from .config_parser import (
    load_config,
    get_test_config,
    get_base_command,
    get_test_names,
    process_params,
    process_environment
)
import concurrent.futures

# Base logs directory
BASE_LOG_DIR = "test_runs"
os.makedirs(BASE_LOG_DIR, exist_ok=True)

def create_run_directory():
    """Create a timestamped directory for this test run"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    run_dir = os.path.join(BASE_LOG_DIR, f"run_{timestamp}")
    os.makedirs(run_dir, exist_ok=True)
    return run_dir

def run_single_test(config_path, test_name, run_dir):
    """
    Run a single test from a configuration file.
    """
    # Load and parse the configuration
    config = load_config(config_path)
    test_config = get_test_config(config, test_name)
    
    # Get base command - test-specific base_command overrides global base_command
    base_command = get_base_command(config, test_config)
    
    # If there's no test config or it's invalid, return an error
    if not test_config or not isinstance(test_config, dict):
        return {
            "config": test_name,
            "success": False,
            "error_trace": ["Test configuration not found or invalid"],
            "log_file": None
        }
    
    start_time = datetime.utcnow()
    start_time_formatted = start_time.strftime("%Y%m%d_%H%M%S")
    
    try:
        # Process environment variables
        env = os.environ.copy()
        env_vars = process_environment(test_config)
        env.update(env_vars)
        
        # Process parameters
        params = process_params(test_config, False)
        
        # Special handling for different command types
        if base_command == 'python' and len(params) >= 2 and params[0] == '-c':
            # For Python -c commands, combine the script into a single properly quoted argument
            python_script = params[1]
            # Properly escape the Python code for shell execution
            escaped_script = python_script.replace('"', '\\"')
            cmd_to_run = f"{base_command} {params[0]} \"{escaped_script}\""
            
        elif base_command in ['/bin/bash', '/bin/sh', 'bash', 'sh'] and len(params) >= 2 and params[0] == '-c':
            # For shell -c commands, use double quotes and escape any single or double quotes within
            shell_command = params[1]
            # Replace single quotes with the shell's way of handling embedded quotes
            escaped_cmd = shell_command.replace("'", "'\\''")
            cmd_to_run = f"{base_command} {params[0]} '{escaped_cmd}'"
            
        else:
            # For all other commands, join with proper quoting
            cmd_components = [base_command]
            cmd_components.extend(params)
            cmd_to_run = " ".join(shlex.quote(comp) if ' ' in comp or "'" in comp or '"' in comp else comp 
                                for comp in cmd_components)
        
        # Run the command with shell=True to support command chaining (&&, ||, etc.)
        result = subprocess.run(
            cmd_to_run, 
            capture_output=True, 
            text=True, 
            env=env, 
            shell=True  # Using shell=True to support command chaining
        )
        
        stdout = result.stdout
        stderr = result.stderr
        returncode = result.returncode
        
        # Determine success/failure
        success = returncode == 0
        status_str = "PASS" if success else "FAIL"
        
        # Create a descriptive log filename
        log_filename = f"{start_time_formatted}_{test_name}_{status_str}.log"
        log_file = os.path.join(run_dir, log_filename)
        
        with open(log_file, "w") as log:
            log.write(f"Test: {test_name}\n")
            log.write(f"Status: {'SUCCESS' if success else 'FAILURE'}\n")
            
            # Write the actual command that was run
            if isinstance(cmd_to_run, list):
                log.write(f"Command: {' '.join(cmd_to_run)}\n")
            else:
                log.write(f"Command: {cmd_to_run}\n")
            
            # Include environment variables in the log
            if env_vars:
                log.write("Environment:\n")
                for key, value in env_vars.items():
                    log.write(f"  {key}={value}\n")
            
            log.write(f"Return code: {returncode}\n")
            log.write(f"Start time: {start_time}\n")
            log.write(f"End time: {datetime.utcnow()}\n\n")
            log.write(f"--- STDOUT ---\n")
            log.write(stdout)
            if stderr:
                log.write("\n\n--- STDERR ---\n")
                log.write(stderr)
        
        error_message = f"Command failed with return code {returncode}" if not success else None
        error_trace = stderr.split("\n")[-3:] if stderr and not success else None
        if not error_trace and not success:
            error_trace = [error_message]
        failure = stderr if stderr and not success else error_message if not success else None
        
    except Exception as e:
        success = False
        error_trace = str(e).split("\n")
        failure = str(e)
        
        # Create error log for exceptions
        log_filename = f"{start_time_formatted}_{test_name}_EXCEPTION.log"
        log_file = os.path.join(run_dir, log_filename)
        
        with open(log_file, "w") as log:
            log.write(f"Test: {test_name}\n")
            log.write(f"Status: EXCEPTION\n")
            log.write(f"Start time: {start_time}\n")
            log.write(f"End time: {datetime.utcnow()}\n\n")
            log.write(f"--- ERROR ---\n")
            log.write(str(e))
    
    end_time = datetime.utcnow()
    
    # Convert cmd_to_run to string for database logging if it's a list
    cmd_str = cmd_to_run if isinstance(cmd_to_run, str) else " ".join(cmd_to_run)
    log_run(test_name, test_name, cmd_str, success, start_time, end_time, log_file, error_trace, failure)
    
    result_info = {
        "config": test_name, 
        "success": success, 
        "log_file": log_file, 
        "error_trace": error_trace if not success else None
    }
    
    return result_info

def run_tests(config_path, run_dir, max_workers=4):
    """
    Run multiple tests in parallel using ThreadPoolExecutor.
    """
    # Load and parse the configuration
    config = load_config(config_path)
    test_names = get_test_names(config)
    results = []
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all test jobs to the thread pool
        future_to_test = {
            executor.submit(run_single_test, config_path, test_name, run_dir): test_name 
            for test_name in test_names
        }
        
        # Process results as they complete
        for future in concurrent.futures.as_completed(future_to_test):
            test_name = future_to_test[future]
            try:
                result = future.result()
                results.append(result)
                status = "Succeeded" if result["success"] else "Failed"
                print(f"Test '{test_name}' {status}")
            except Exception as e:
                print(f"Error running test '{test_name}': {e}")
                results.append({
                    "config": test_name,
                    "success": False,
                    "error_trace": [str(e)],
                    "log_file": None
                })
    
    return results

def run_test_from_cli(config_path, output_path=None, max_workers=4):
    """
    Run tests from CLI using thread pool for parallelism.
    """
    # Create a unique directory for this test run
    run_dir = create_run_directory()
    print(f"Launching tests from {config_path}")
    print(f"Test run directory: {run_dir}")
    
    # Copy the config file to the run directory for reference
    config_filename = os.path.basename(config_path)
    shutil.copy2(config_path, os.path.join(run_dir, config_filename))
    
    # Run the tests
    results = run_tests(config_path, run_dir, max_workers=max_workers)
    
    # Generate summary
    print("\n=== TEST SUMMARY ===")
    successful = sum(1 for r in results if r["success"])
    total = len(results)
    if total > 0:
        success_percent = (successful / total) * 100
    else:
        success_percent = 0
    print(f"Tests passed: {successful}/{total} ({success_percent:.1f}%)")
    
    # Print details of failing tests
    failing_tests = [r for r in results if not r["success"]]
    if failing_tests:
        print("\nFailing tests:")
        for test in failing_tests:
            print(f"- {test['config']}")
            if test.get("error_trace"):
                error = test["error_trace"] if isinstance(test["error_trace"], list) else [test["error_trace"]]
                for line in error:
                    if line:
                        print(f"  {line}")
    
    # If output_path is not specified, create one in the run directory
    if not output_path:
        output_path = os.path.join(run_dir, "test_report.txt")
    else:
        # If output_path is specified but doesn't have a directory component,
        # put it in the run directory
        if os.path.dirname(output_path) == '':
            output_path = os.path.join(run_dir, output_path)
        
        # Also create a copy in the run directory if the specified path is elsewhere
        if os.path.dirname(output_path) != run_dir:
            run_dir_report = os.path.join(run_dir, "test_report.txt")
    
    # Save summary to output file
    with open(output_path, "w") as f:
        f.write(f"Test Summary\n")
        f.write(f"============\n")
        f.write(f"Tests passed: {successful}/{total} ({success_percent:.1f}%)\n\n")
        
        f.write("Test Results:\n")
        for result in results:
            status = "PASS" if result["success"] else "FAIL"
            f.write(f"{result['config']}: {status}\n")
            if not result["success"] and result.get("error_trace"):
                error = result["error_trace"] if isinstance(result["error_trace"], list) else [result["error_trace"]]
                for line in error:
                    if line:
                        f.write(f"  Error: {line}\n")
        
        f.write("\nLog Files:\n")
        for result in results:
            if result.get("log_file"):
                # Get the base filename only
                log_filename = os.path.basename(result["log_file"])
                f.write(f"{result['config']}: {log_filename}\n")
                
    print(f"Report written to {output_path}")
    
    # Create a symlink to the latest run for convenience
    latest_link = os.path.join(BASE_LOG_DIR, "latest")
    if os.path.exists(latest_link):
        if os.path.islink(latest_link):
            os.unlink(latest_link)
        else:
            shutil.rmtree(latest_link)
    
    try:
        # Create relative symlink on UNIX systems
        os.symlink(os.path.basename(run_dir), latest_link)
    except (OSError, AttributeError):
        # On Windows or if symlinks aren't supported, create a directory with copies
        os.makedirs(latest_link, exist_ok=True)
        for file in os.listdir(run_dir):
            src = os.path.join(run_dir, file)
            dst = os.path.join(latest_link, file)
            if os.path.isfile(src):
                shutil.copy2(src, dst)
    
    return results, run_dir

