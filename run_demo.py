#!/usr/bin/env python3
"""
Demo script for PyFlink ETL Pipeline
This script demonstrates the complete ETL workflow and validates the results.
"""

import os
import sys
import subprocess
import logging
from pathlib import Path

# Add current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import ETLConfig

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def check_java_installation():
    """Check if Java is installed and accessible"""
    try:
        result = subprocess.run(['java', '-version'], capture_output=True, text=True)
        if result.returncode == 0:
            logger.info("Java installation found")
            return True
        else:
            logger.error("Java is not installed or not accessible")
            return False
    except FileNotFoundError:
        logger.error("Java is not installed or not in PATH")
        return False

def setup_environment():
    """Set up the environment for running the ETL pipeline"""
    logger.info("Setting up environment...")
    
    # Validate paths
    ETLConfig.validate_paths()
    
    # Check Java installation
    if not check_java_installation():
        logger.warning("Java not found. PyFlink requires Java 8 or 11.")
        logger.info("To install Java on Ubuntu/Debian: sudo apt-get install openjdk-11-jdk")
        logger.info("To install Java on CentOS/RHEL: sudo yum install java-11-openjdk-devel")
        return False
    
    # Check if input data exists
    if not os.path.exists(ETLConfig.SOURCE_FILE):
        logger.error(f"Input file not found: {ETLConfig.SOURCE_FILE}")
        return False
    
    logger.info("Environment setup completed successfully")
    return True

def validate_output():
    """Validate the ETL pipeline output"""
    output_file = ETLConfig.SINK_FILE
    
    if not os.path.exists(output_file):
        logger.error(f"Output file not found: {output_file}")
        return False
    
    # Read and validate output
    try:
        with open(output_file, 'r') as f:
            lines = f.readlines()
            
        if len(lines) < 2:  # Header + at least one data row
            logger.error("Output file appears to be empty or invalid")
            return False
        
        logger.info(f"Output validation successful. Found {len(lines)-1} processed records.")
        logger.info(f"Output file: {output_file}")
        
        # Show sample output
        logger.info("Sample output:")
        for i, line in enumerate(lines[:5]):  # Show first 5 lines
            logger.info(f"  {line.strip()}")
        
        return True
        
    except Exception as e:
        logger.error(f"Error validating output: {str(e)}")
        return False

def run_demo():
    """Run the complete demo workflow"""
    logger.info("Starting PyFlink ETL Demo...")
    
    # Setup environment
    if not setup_environment():
        logger.error("Environment setup failed. Exiting.")
        return False
    
    # Clean previous output
    if os.path.exists(ETLConfig.SINK_FILE):
        os.remove(ETLConfig.SINK_FILE)
        logger.info("Cleaned previous output files")
    
    # Run ETL pipeline
    try:
        logger.info("Running ETL pipeline...")
        from etl_pipeline import run_etl_pipeline
        run_etl_pipeline()
        
    except Exception as e:
        logger.error(f"ETL pipeline failed: {str(e)}")
        return False
    
    # Validate output
    if validate_output():
        logger.info("Demo completed successfully!")
        return True
    else:
        logger.error("Demo failed during output validation")
        return False

if __name__ == "__main__":
    success = run_demo()
    sys.exit(0 if success else 1)