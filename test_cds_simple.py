#!/usr/bin/env python3
"""
Simple Copernicus CDS API connection test for ArcheoScope.
"""

import os
import sys
from datetime import datetime, timedelta
import tempfile
from dotenv import load_dotenv

load_dotenv()

def test_cds_connection():
    """Test basic CDS connection and data retrieval."""
    print("🚀 Testing Copernicus CDS API Connection")
    print("=" * 50)
    
    # Test 1: Import cdsapi
    print("🔍 Testing cdsapi import...")
    try:
        import cdsapi
        print("✅ cdsapi imported successfully")
    except ImportError as e:
        print(f"❌ cdsapi import failed: {e}")
        return False
    
    # Test 2: Check environment variables
    print("\n🔍 Testing environment configuration...")
    cds_url = os.getenv("CDS_URL")
    cds_api_key = os.getenv("CDS_API_KEY")
    
    if not cds_url or not cds_api_key:
        print("❌ CDS_URL or CDS_API_KEY not configured")
        return False
    
    print(f"✅ CDS_URL: {cds_url}")
    print(f"✅ CDS_API_KEY: {cds_api_key[:8]}...{cds_api_key[-8:]}")
    
    # Test 3: Create client
    print("\n🔍 Testing CDS client creation...")
    try:
        client = cdsapi.Client(
            url=cds_url,
            key=cds_api_key,
            verify=True
        )
        print("✅ CDS client created successfully")
    except Exception as e:
        print(f"❌ CDS client creation failed: {e}")
        return False
    
    # Test 4: Simple data request
    print("\n🔍 Testing simple data request...")
    print("⏳ Requesting small ERA5 dataset (this may take 30-60 seconds)...")
    
    try:
        # Get a date from a week ago to ensure data availability
        test_date = datetime.now() - timedelta(days=7)
        year = str(test_date.year)
        month = f"{test_date.month:02d}"
        day = f"{test_date.day:02d}"
        
        dataset = 'reanalysis-era5-single-levels'
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
        
        print(f"📅 Requesting data for: {year}-{month}-{day}")
        print(f"📊 Dataset: {dataset}")
        print(f"🌡️  Variable: 2m_temperature")
        print(f"📍 Area: 1°N, 1°E to 0°N, 0°E")
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(suffix='.nc', delete=False) as tmp_file:
            target = tmp_file.name
        
        try:
            # Make the request
            result = client.retrieve(dataset, request, target)
            
            # Check if file was created and has content
            if os.path.exists(target) and os.path.getsize(target) > 0:
                file_size = os.path.getsize(target)
                print(f"✅ Data request successful!")
                print(f"📁 Downloaded file size: {file_size:,} bytes")
                
                # Clean up
                os.unlink(target)
                return True
            else:
                print("❌ Data request completed but no data received")
                return False
                
        except Exception as e:
            print(f"❌ Data request failed: {e}")
            
            # Clean up temp file if it exists
            if os.path.exists(target):
                os.unlink(target)
            
            # Check if it's an authentication error
            if "authentication" in str(e).lower() or "unauthorized" in str(e).lower():
                print("💡 This appears to be an authentication issue.")
                print("💡 Please verify your CDS API key is correct and active.")
                print("💡 You may need to accept terms of use for the dataset at:")
                print("💡 https://cds.climate.copernicus.eu/datasets/reanalysis-era5-single-levels")
            
            return False
            
    except Exception as e:
        print(f"❌ Unexpected error during data request: {e}")
        return False

def main():
    """Run the CDS connection test."""
    try:
        success = test_cds_connection()
        
        print("\n" + "=" * 50)
        if success:
            print("🎉 CDS API CONNECTION TEST PASSED!")
            print("✅ ArcheoScope can now use Copernicus CDS data")
            print("\n💡 Next steps:")
            print("   • Accept terms of use for specific datasets you need")
            print("   • Integrate CDS data into ArcheoScope analysis")
            print("   • Consider SMOS soil moisture data for archaeological applications")
        else:
            print("❌ CDS API CONNECTION TEST FAILED")
            print("\n💡 Troubleshooting:")
            print("   • Verify your CDS API key is correct")
            print("   • Check your internet connection")
            print("   • Accept terms of use for datasets at CDS website")
            print("   • Visit: https://cds.climate.copernicus.eu/user/login")
        
        return success
        
    except KeyboardInterrupt:
        print("\n⚠️  Test interrupted by user")
        return False
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)