#!/usr/bin/env python3
"""
Test script to upload video to cleaning robot service using test1.mp4
"""

import requests
import os
import sys

def test_video_upload():
    """Test uploading video/test1.mp4 to the cleaning robot service"""
    
    # Service URL
    cleaning_service_url = "http://localhost:5001"
    test_video_path = "video/test1.mp4"
    
    # Check if test video exists
    if not os.path.exists(test_video_path):
        print(f"Test video not found: {test_video_path}")
        return False
    
    print(f"Found test video: {test_video_path}")
    print(f"Video size: {os.path.getsize(test_video_path)} bytes")
    
    # Test basic connection
    try:
        print("Testing basic connection to cleaning robot service...")
        response = requests.get(f"{cleaning_service_url}/")
        if response.status_code != 200:
            print(f"Service not responding correctly: {response.status_code}")
            return False
        print("Cleaning robot service is responding")
        
        # Check available endpoints
        print("Testing robot status endpoint...")
        status_response = requests.get(f"{cleaning_service_url}/status")
        if status_response.status_code == 200:
            print("Status endpoint working:")
            print(status_response.json())
        else:
            print(f"Status endpoint returned: {status_response.status_code}")
            
        # Test robot control endpoints
        print("Testing robot control commands...")
        
        # Start cleaning
        start_response = requests.post(f"{cleaning_service_url}/start_cleaning")
        if start_response.status_code == 200:
            print("Start cleaning command successful")
            print(start_response.json())
        else:
            print(f"Start cleaning failed: {start_response.status_code}")
            
        # Stop cleaning
        stop_response = requests.post(f"{cleaning_service_url}/stop_cleaning")
        if stop_response.status_code == 200:
            print("Stop cleaning command successful")
            print(stop_response.json())
        else:
            print(f"Stop cleaning failed: {stop_response.status_code}")
            
        # Get robot map/position if available
        map_response = requests.get(f"{cleaning_service_url}/map")
        if map_response.status_code == 200:
            print("Map endpoint working")
        else:
            print(f"Map endpoint returned: {map_response.status_code}")
            
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to cleaning robot service: {e}")
        return False

if __name__ == "__main__":
    print("Testing Cleaning Robot Service with test video...")
    print("=" * 60)
    
    success = test_video_upload()
    
    if success:
        print("\n" + "=" * 60)
        print("Cleaning robot service test completed successfully!")
    else:
        print("\n" + "=" * 60)
        print("Cleaning robot service test failed!")
    
    sys.exit(0 if success else 1)