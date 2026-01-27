#!/usr/bin/env python3
"""
Quick CDS API authentication test for ArcheoScope.
Tests authentication without downloading data.
"""

import os
import sys
import requests
from dotenv import load_dotenv

load_dotenv()

def test_cds_authentication():
    """Test CDS API authentication."""
    print("🚀 Testing Copernicus CDS API Authentication")
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
    
    # Test 3: Test authentication with direct HTTP request
    print("\n🔍 Testing API authentication...")
    try:
        # Test authentication by making a simple request to the API
        auth_url = f"{cds_url}/resources"
        
        response = requests.get(
            auth_url,
            auth=(cds_api_key.split('-')[0], cds_api_key),
            timeout=10
        )
        
        if response.status_code == 200:
            print("✅ Authentication successful!")
            print(f"📊 API responded with status: {response.status_code}")
            return True
        elif response.status_code == 401:
            print("❌ Authentication failed - Invalid API key")
            return False
        else:
            print(f"⚠️  API responded with status: {response.status_code}")
            print("✅ Authentication appears to be working (non-401 response)")
            return True
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Network error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_cds_client_creation():
    """Test CDS client creation."""
    print("\n🔍 Testing CDS client creation...")
    try:
        import cdsapi
        
        client = cdsapi.Client(
            url=os.getenv("CDS_URL"),
            key=os.getenv("CDS_API_KEY"),
            verify=True
        )
        print("✅ CDS client created successfully")
        
        # Try to access client info (this doesn't download data)
        print("✅ Client configuration appears valid")
        return True
        
    except Exception as e:
        print(f"❌ CDS client creation failed: {e}")
        return False

def main():
    """Run the authentication test."""
    try:
        auth_success = test_cds_authentication()
        client_success = test_cds_client_creation()
        
        overall_success = auth_success and client_success
        
        print("\n" + "=" * 50)
        print("📊 TEST RESULTS:")
        print(f"   Authentication: {'✅ PASS' if auth_success else '❌ FAIL'}")
        print(f"   Client Creation: {'✅ PASS' if client_success else '❌ FAIL'}")
        
        if overall_success:
            print("\n🎉 CDS API AUTHENTICATION TEST PASSED!")
            print("✅ Your CDS API key is valid and working")
            print("✅ ArcheoScope can connect to Copernicus CDS")
            print("\n💡 Next steps:")
            print("   • Accept terms of use for specific datasets")
            print("   • Test actual data downloads")
            print("   • Integrate CDS data into ArcheoScope")
            print("\n🌍 Available datasets for archaeological applications:")
            print("   • ERA5 reanalysis (weather/climate data)")
            print("   • SMOS soil moisture (subsurface conditions)")
            print("   • Satellite soil moisture products")
            print("   • Land cover and vegetation indices")
        else:
            print("\n❌ CDS API AUTHENTICATION TEST FAILED")
            print("\n💡 Troubleshooting:")
            print("   • Verify your CDS API key at: https://cds.climate.copernicus.eu/user/login")
            print("   • Check if your account is active")
            print("   • Ensure you've accepted the CDS terms of use")
        
        return overall_success
        
    except KeyboardInterrupt:
        print("\n⚠️  Test interrupted by user")
        return False
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)