#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simple system test for Edge Computing Home Microservices System
"""

import requests
import time
import os
import sys

def test_service(name, url, timeout=5):
    """Generic service test"""
    try:
        response = requests.get(url, timeout=timeout)
        if response.status_code == 200:
            print(f"[OK] {name} is working")
            return True
        else:
            print(f"[FAIL] {name} returned status {response.status_code}")
            return False
    except Exception as e:
        print(f"[FAIL] {name} error: {e}")
        return False

def test_cleaning_robot():
    """Test cleaning robot with actual commands"""
    print("Testing Cleaning Robot Service...")
    
    try:
        # Test state
        state_response = requests.get("http://localhost:5001/state")
        if state_response.status_code == 200:
            state = state_response.json()
            print(f"[OK] Robot state - Power: {state['is_on']}, Battery: {state['battery']}%")
            
            # Turn on robot
            on_response = requests.post("http://localhost:5001/on")
            if on_response.status_code == 200:
                print("[OK] Robot turned ON")
                time.sleep(2)
                
                # Check state after turning on
                new_state = requests.get("http://localhost:5001/state").json()
                print(f"[INFO] Robot is now: {new_state['is_on']}")
                
                # Turn off robot
                time.sleep(1)
                off_response = requests.post("http://localhost:5001/off")
                if off_response.status_code == 200:
                    print("[OK] Robot turned OFF")
                    return True
        
        return False
    except Exception as e:
        print(f"[FAIL] Cleaning robot test error: {e}")
        return False

def main():
    """Run system tests"""
    print("Edge Computing Home Microservices - System Test")
    print("=" * 50)
    
    results = []
    
    # Test all services
    results.append(test_service("MinIO", "http://localhost:9000/minio/health/live"))
    results.append(test_service("Web Frontend", "http://localhost:3000"))
    results.append(test_cleaning_robot())
    
    # Test pose analysis on both possible ports
    pose_working = False
    for port in [5000, 5001]:
        if test_service(f"Pose Analysis (port {port})", f"http://localhost:{port}"):
            pose_working = True
            break
    results.append(pose_working)
    
    # Check test video
    video_path = "video/test1.mp4"
    if os.path.exists(video_path):
        size = os.path.getsize(video_path)
        print(f"[OK] Test video found: {size:,} bytes")
        results.append(True)
    else:
        print("[FAIL] Test video not found")
        results.append(False)
    
    # Summary
    passed = sum(results)
    total = len(results)
    
    print("\n" + "=" * 50)
    print(f"RESULTS: {passed}/{total} tests passed")
    print(f"Success rate: {(passed/total)*100:.1f}%")
    
    if passed >= 4:
        print("System is working well!")
    elif passed >= 3:
        print("System is mostly working.")
    else:
        print("System needs attention.")
    
    return passed >= 3

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)