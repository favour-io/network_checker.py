#!/usr/bin/env python3
"""
Interactive Network Connectivity Checker
Author: Eniola Favour
Description: Lets users test connectivity to any websites they choose.
"""

import subprocess
import time
import platform

def ping_host(hostname):
    """
    Pings a single host and returns True if successful, False if failed.
    """
    # For Windows, we use '-n 2' for 2 pings. For Mac/Linux, it's '-c 2'
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    
    # Build the command: e.g., ['ping', '-c', '2', 'google.com']
    command = ['ping', param, '2', hostname]
    
    # Run the command
    try:
        result = subprocess.run(command, 
                              stdout=subprocess.DEVNULL, 
                              stderr=subprocess.DEVNULL, 
                              timeout=5)
        return result.returncode == 0
    except:
        return False

def get_user_targets():
    """
    Ask the user which websites they want to test.
    """
    print("🔍 Interactive Network Checker")
    print("=" * 40)
    print("Enter the websites or IP addresses you want to test.")
    print("Separate multiple sites with commas.")
    print("Example: google.com, 8.8.8.8, microsoft.com\n")
    
    # Get input from user
    user_input = input("Which sites would you like to test? : ").strip()
    
    # Split the input by commas and clean up any extra spaces
    targets = [site.strip() for site in user_input.split(',')]
    
    # Remove any empty entries
    targets = [site for site in targets if site]
    
    return targets

def main():
    """Main function that runs the checks"""
    
    # Get the list of sites from the user
    targets = get_user_targets()
    
    # If user didn't enter anything, use default sites
    if not targets:
        print("No sites entered. Using default test sites...")
        targets = ["google.com", "8.8.8.8", "cloudflare.com"]
    
    print(f"\nTesting {len(targets)} site(s): {', '.join(targets)}")
    print("Starting connectivity tests...\n")
    
    successful_checks = 0
    total_checks = len(targets)
    
    # Test each website one by one
    for target in targets:
        print(f"Testing {target}...", end=" ")
        
        if ping_host(target):
            print("✅ SUCCESS")
            successful_checks += 1
        else:
            print("❌ FAILED")
        
        time.sleep(1)  # Wait 1 second between tests
    
    # Print final summary
    print(f"\n📊 Results: {successful_checks}/{total_checks} tests passed")
    
    if successful_checks == total_checks:
        print("🎉 All sites are reachable! Network connectivity is good.")
    elif successful_checks > 0:
        print("⚠️  Partial connectivity - some sites are unreachable.")
        print("   This could indicate DNS issues or site-specific problems.")
    else:
        print("💥 No sites are reachable - check your internet connection.")

if __name__ == "__main__":
    main()
