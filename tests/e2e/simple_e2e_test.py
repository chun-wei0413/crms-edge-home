#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
E2E Test Script for Edge Computing Home Microservices System
"""

import requests
import time
import os
import sys

class E2ETest:
    def __init__(self):
        self.base_url = "http://localhost"
        self.minio_url = "http://localhost:9000"
        self.cleaning_service_url = "http://localhost:5001"
        self.pose_service_url = "http://localhost:5000"
        self.web_frontend_url = "http://localhost:3000"
        self.test_video_path = "video/test1.mp4"
        
    def wait_for_service(self, url, service_name, timeout=30):
        """Wait for service to start"""
        print(f"Waiting for {service_name} service...")
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                response = requests.get(url, timeout=5)
                if response.status_code < 500:
                    print(f"Service {service_name} is ready")
                    return True
            except requests.exceptions.RequestException:
                pass
            time.sleep(2)
        
        print(f"Service {service_name} failed to start")
        return False
    
    def test_cleaning_robot_service(self):
        """Test Cleaning Robot Service"""
        print("Testing Cleaning Robot Service...")
        
        try:
            response = requests.get(f"{self.cleaning_service_url}/")
            if response.status_code == 200:
                print("Cleaning Robot Service: OK")
                return True
            else:
                print(f"Cleaning Robot Service returned status: {response.status_code}")
                return False
                    
        except requests.exceptions.RequestException as e:
            print(f"Cleaning Robot Service test failed: {e}")
            return False
    
    def test_pose_analysis_service(self):
        """Test Pose Analysis Service"""
        print("Testing Pose Analysis Service...")
        
        try:
            response = requests.get(f"{self.pose_service_url}/")
            if response.status_code == 200:
                print("Pose Analysis Service: OK")
                
                # Test video upload if test video exists
                if os.path.exists(self.test_video_path):
                    print("Uploading test video...")
                    with open(self.test_video_path, 'rb') as video_file:
                        files = {'file': video_file}
                        upload_response = requests.post(f"{self.pose_service_url}/upload", files=files)
                        
                        if upload_response.status_code == 200:
                            print("Video upload: OK")
                        else:
                            print(f"Video upload failed with status: {upload_response.status_code}")
                
                return True
            else:
                print(f"Pose Analysis Service returned status: {response.status_code}")
                return False
                    
        except requests.exceptions.RequestException as e:
            print(f"Pose Analysis Service test failed: {e}")
            return False
    
    def test_minio_service(self):
        """Test MinIO Service"""
        print("Testing MinIO Service...")
        
        try:
            response = requests.get(f"{self.minio_url}/minio/health/live")
            if response.status_code == 200:
                print("MinIO Service: OK")
                return True
            else:
                print(f"MinIO Service returned status: {response.status_code}")
                return False
                
        except requests.exceptions.RequestException as e:
            print(f"MinIO Service test failed: {e}")
            return False
    
    def test_web_frontend(self):
        """Test Web Frontend Service"""
        print("Testing Web Frontend Service...")
        
        try:
            response = requests.get(self.web_frontend_url)
            if response.status_code == 200:
                print("Web Frontend Service: OK")
                return True
            else:
                print(f"Web Frontend Service returned status: {response.status_code}")
                return False
                
        except requests.exceptions.RequestException as e:
            print(f"Web Frontend Service test failed: {e}")
            return False
    
    def run_all_tests(self):
        """Run all tests"""
        print("Starting E2E Tests...")
        print("=" * 50)
        
        # Wait for all services
        services = [
            (self.minio_url + "/minio/health/live", "MinIO"),
            (self.cleaning_service_url, "Cleaning Robot"),
            (self.pose_service_url, "Pose Analysis"),
            (self.web_frontend_url, "Web Frontend")
        ]
        
        all_services_ready = True
        for url, name in services:
            if not self.wait_for_service(url, name):
                all_services_ready = False
        
        if not all_services_ready:
            print("Some services failed to start, aborting tests")
            return False
        
        print("\nAll services started, running functional tests...")
        print("=" * 50)
        
        # Run tests
        test_results = []
        test_results.append(self.test_minio_service())
        test_results.append(self.test_cleaning_robot_service())
        test_results.append(self.test_pose_analysis_service())
        test_results.append(self.test_web_frontend())
        
        # Results
        passed = sum(test_results)
        total = len(test_results)
        
        print("\n" + "=" * 50)
        print("Test Results:")
        print(f"Passed: {passed}/{total}")
        print(f"Failed: {total - passed}/{total}")
        
        if passed == total:
            print("All tests passed! System is working correctly.")
            return True
        else:
            print("Some tests failed, please check service status")
            return False

if __name__ == "__main__":
    tester = E2ETest()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)