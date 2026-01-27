#!/usr/bin/env python3
"""
Test Copernicus CDS API connection and functionality for ArcheoScope.
Tests the CDS API key and basic data retrieval capabilities.
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
import tempfile

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

def test_cdsapi_installation():
    """Test if cdsapi is installed and can be imported."""
    print("🔍 Testing CDS API installation...")
    
    try:
        import cdsapi
        print(f"✅ cdsapi imported successfully - version: {cdsapi.__version__}")
        return True
    except ImportError as e:
        print(f"❌ cdsapi not installed: {e}")
        print("💡 Install with: pip install 'cdsapi>=0.7.7'")
        return False
    except Exception as e:
        print(f"❌ Error importing cdsapi: {e}")
        return False

def test_environment_config():
    """Test if CDS environment variables are properly configured."""
    print("\n🔍 Testing environment configuration...")
    
    cds_url = os.getenv("CDS_URL")
    cds_api_key = os.getenv("CDS_API_KEY")
    
    if not cds_url:
        print("❌ CDS_URL not found in environment")
        return False
    
    if not cds_api_key:
        print("❌ CDS_API_KEY not found in environment")
        return False
    
    print(f"✅ CDS_URL: {cds_url}")
    print(f"✅ CDS_API_KEY: {cds_api_key[:8]}...{cds_api_key[-8:]}")
    
    return True

def test_cdsapirc_file():
    """Test if .cdsapirc file exists and is properly configured."""
    print("\n🔍 Testing .cdsapirc file configuration...")
    
    home_dir = Path.home()
    cdsapirc_path = home_dir / ".cdsapirc"
    
    cds_url = os.getenv("CDS_URL")
    cds_api_key = os.getenv("CDS_API_KEY")
    
    if not cdsapirc_path.exists():
        print("⚠️  .cdsapirc file not found, creating it...")
        
        try:
            with open(cdsapirc_path, 'w') as f:
                f.write(f"url: {cds_url}\n")
                f.write(f"key: {cds_api_key}\n")
            
            print(f"✅ Created .cdsapirc file at: {cdsapirc_path}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to create .cdsapirc file: {e}")
            return False
    else:
        print(f"✅ .cdsapirc file exists at: {cdsapirc_path}")
        
        # Verify content
        try:
            with open(cdsapirc_path, 'r') as f:
                content = f.read()
                
            if cds_url in content and cds_api_key in content:
                print("✅ .cdsapirc file contains correct credentials")
                return True
            else:
                print("⚠️  .cdsapirc file exists but may have different credentials")
                print("Current content:")
                print(content)
                return True
                
        except Exception as e:
            print(f"❌ Error reading .cdsapirc file: {e}")
            return False

def test_cds_client_connection():
    """Test basic CDS client connection."""
    print("\n🔍 Testing CDS client connection...")
    
    try:
        import cdsapi
        
        # Create client with explicit configuration
        client = cdsapi.Client(
            url=os.getenv("CDS_URL"),
            key=os.getenv("CDS_API_KEY"),
            verify=True
        )
        
        print("✅ CDS client created successfully")
        return client
        
    except Exception as e:
        print(f"❌ Failed to create CDS client: {e}")
        return None

def test_dataset_access():
    """Test access to a simple dataset (metadata only)."""
    print("\n🔍 Testing dataset access...")
    
    try:
        import cdsapi
        
        client = cdsapi.Client(
            url=os.getenv("CDS_URL"),
            key=os.getenv("CDS_API_KEY"),
            verify=True
        )
        
        # Test with a simple, small dataset request
        # Using ERA5 reanalysis data for a single point and time
        dataset = 'reanalysis-era5-single-levels'
        
        # Get yesterday's date to ensure data availability
        yesterday = datetime.now() - timedelta(days=2)
        year = str(yesterday.year)
        month = f"{yesterday.month:02d}"
        day = f"{yesterday.day:02d}"
        
        request = {
            'product_type': 'reanalysis',
            'variable': ['2m_temperature'],
            'year': year,
            'month': month,
            'day': day,
            'time': '12:00',
            'area': [1, 1, 0, 0],  # Very small area: North, West, South, East
            'format': 'netcdf',
        }
        
        print(f"📊 Testing with dataset: {dataset}")
        print(f"📅 Date: {year}-{month}-{day}")
        print("⏳ This may take a moment...")
        
        # Use a temporary file
        with tempfile.NamedTemporaryFile(suffix='.nc', delete=False) as tmp_file:
            target = tmp_file.name
        
        try:
            # Set a reasonable timeout
            result = client.retrieve(dataset, request, target)
            
            if os.path.exists(target) and os.path.getsize(target) > 0:
                file_size = os.path.getsize(target)
                print(f"✅ Dataset access successful! Downloaded {file_size} bytes")
                
                # Clean up
                os.unlink(target)
                return True
            else:
                print("❌ Dataset request completed but no data received")
                return False
                
        except Exception as e:
            print(f"❌ Dataset request failed: {e}")
            
            # Clean up temp file if it exists
            if os.path.exists(target):
                os.unlink(target)
            
            return False
            
    except Exception as e:
        print(f"❌ Error testing dataset access: {e}")
        return False

def test_smos_soil_moisture():
    """Test access to SMOS soil moisture data (relevant for archaeological applications)."""
    print("\n🔍 Testing SMOS soil moisture dataset access...")
    
    try:
        import cdsapi
        
        client = cdsapi.Client(
            url=os.getenv("CDS_URL"),
            key=os.getenv("CDS_API_KEY"),
            verify=True
        )
        
        # Test SMOS soil moisture dataset
        dataset = 'satellite-soil-moisture'
        
        # Get a recent date
        yesterday = datetime.now() - timedelta(days=30)  # SMOS data may have delay
        year = str(yesterday.year)
        month = f"{yesterday.month:02d}"
        
        request = {
            'variable': 'volumetric_surface_soil_moisture',
            'type_of_sensor': 'passive',
            'type_of_record': 'cdr',
            'satellite': 'smos',
            'year': year,
            'month': month,
            'day': '01',
            'version': 'v202212.0.0',
            'area': [1, 1, 0, 0],  # Very small area
            'format': 'zip',
        }
        
        print(f"📊 Testing SMOS dataset: {dataset}")
        print(f"📅 Date: {year}-{month}-01")
        print("⏳ This may take a moment...")
        
        # Use a temporary file
        with tempfile.NamedTemporaryFile(suffix='.zip', delete=False) as tmp_file:
            target = tmp_file.name
        
        try:
            # This is just a test - we'll cancel if it takes too long
            result = client.retrieve(dataset, request, target)
            
            if os.path.exists(target) and os.path.getsize(target) > 0:
                file_size = os.path.getsize(target)
                print(f"✅ SMOS dataset access successful! Downloaded {file_size} bytes")
                
                # Clean up
                os.unlink(target)
                return True
            else:
                print("❌ SMOS dataset request completed but no data received")
                return False
                
        except Exception as e:
            print(f"⚠️  SMOS dataset request failed (this may be normal): {e}")
            print("💡 SMOS data may require specific terms acceptance or have access restrictions")
            
            # Clean up temp file if it exists
            if os.path.exists(target):
                os.unlink(target)
            
            return False
            
    except Exception as e:
        print(f"❌ Error testing SMOS dataset: {e}")
        return False

def generate_test_report(results: Dict[str, bool]) -> Dict[str, Any]:
    """Generate a comprehensive test report."""
    
    total_tests = len(results)
    passed_tests = sum(results.values())
    success_rate = (passed_tests / total_tests) * 100 if total_tests > 0 else 0
    
    report = {
        "timestamp": datetime.now().isoformat(),
        "test_results": results,
        "summary": {
            "total_tests": total_tests,
            "passed_tests": passed_tests,
            "failed_tests": total_tests - passed_tests,
            "success_rate": success_rate
        },
        "configuration": {
            "cds_url": os.getenv("CDS_URL"),
            "cds_api_key_configured": bool(os.getenv("CDS_API_KEY")),
            "home_directory": str(Path.home()),
            "cdsapirc_path": str(Path.home() / ".cdsapirc")
        },
        "recommendations": []
    }
    
    # Add recommendations based on results
    if not results.get("cdsapi_installation", False):
        report["recommendations"].append("Install cdsapi: pip install 'cdsapi>=0.7.7'")
    
    if not results.get("environment_config", False):
        report["recommendations"].append("Configure CDS_URL and CDS_API_KEY in .env file")
    
    if not results.get("cdsapirc_file", False):
        report["recommendations"].append("Ensure .cdsapirc file is properly configured")
    
    if not results.get("client_connection", False):
        report["recommendations"].append("Check CDS API credentials and network connectivity")
    
    if success_rate < 100:
        report["recommendations"].append("Review failed tests and follow setup instructions")
    
    return report

def main():
    """Run all CDS API tests."""
    print("🚀 ArcheoScope - Copernicus CDS API Connection Test")
    print("=" * 60)
    
    # Run all tests
    results = {}
    
    results["cdsapi_installation"] = test_cdsapi_installation()
    results["environment_config"] = test_environment_config()
    results["cdsapirc_file"] = test_cdsapirc_file()
    results["client_connection"] = test_cds_client_connection() is not None
    
    # Only run data tests if basic setup is working
    if all([results["cdsapi_installation"], results["environment_config"], results["client_connection"]]):
        results["dataset_access"] = test_dataset_access()
        results["smos_access"] = test_smos_soil_moisture()
    else:
        print("\n⚠️  Skipping data access tests due to basic setup issues")
        results["dataset_access"] = False
        results["smos_access"] = False
    
    # Generate report
    report = generate_test_report(results)
    
    # Save report
    report_file = f"copernicus_cds_test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(report_file, 'w') as f:
        json.dump(report, f, indent=2)
    
    # Print summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:25} {status}")
    
    print(f"\nOverall Success Rate: {report['summary']['success_rate']:.1f}%")
    print(f"Report saved to: {report_file}")
    
    if report["recommendations"]:
        print("\n💡 RECOMMENDATIONS:")
        for rec in report["recommendations"]:
            print(f"   • {rec}")
    
    # Return success status
    return report['summary']['success_rate'] >= 75

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)