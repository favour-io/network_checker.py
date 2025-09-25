#!/usr/bin/env python
"""
Professional Network Diagnostics Tool
Author: Eniola Favour
Description: Network troubleshooting for IT support
"""

import subprocess
import platform
import socket
import re
from datetime import datetime

def validate_hostname(hostname):
    """Validate if hostname format is reasonable"""
    if not hostname or len(hostname) > 255:
        return False
    # Basic format check for domains and IPs
    if re.match(r'^[a-zA-Z0-9.-]+$', hostname):
        return True
    return False

def ping_host(hostname, count=4, timeout=5):
    """
    Professional ping with detailed results
    Returns: (success, response_time, packet_loss)
    """
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    command = ['ping', param, str(count), hostname]
    
    try:
        result = subprocess.run(command, capture_output=True, text=True, timeout=timeout)
        
        if result.returncode == 0:
            # Extract response time from ping output
            time_match = re.search(r'time=([0-9.]+)\s*ms', result.stdout)
            response_time = float(time_match.group(1)) if time_match else 0
            return True, response_time, 0
        else:
            # Calculate packet loss
            loss_match = re.search(r'([0-9.]+)%\s+packet\s+loss', result.stdout)
            packet_loss = float(loss_match.group(1)) if loss_match else 100
            return False, 0, packet_loss
            
    except subprocess.TimeoutExpired:
        return False, 0, 100
    except Exception as e:
        return False, 0, 100

def dns_lookup(hostname):
    """Check DNS resolution"""
    try:
        ip = socket.gethostbyname(hostname)
        return True, ip
    except socket.gaierror:
        return False, "DNS resolution failed"

def check_common_services():
    """Check essential internet services to determine actual connectivity"""
    critical_services = [
        "google.com",  # Most reliable
        "cloudflare.com",  # DNS service
        "8.8.8.8",  # Google DNS (IP, so no DNS dependency)
    ]
    return critical_services

def diagnose_connectivity(results):
    """
    Professional diagnosis based on pattern analysis
    """
    successful_checks = sum(1 for success, _, _ in results.values() if success)
    total_checks = len(results)
    
    print("\n" + "="*60)
    print("🔧 NETWORK DIAGNOSIS REPORT")
    print("="*60)
    
    # Analyze patterns for professional diagnosis
    dns_failures = sum(1 for host, (success, _, _) in results.items() 
                      if not success and "DNS resolution" in str(host))
    
    ip_success = any(success for host, (success, _, _) in results.items() 
                    if re.match(r'^\d+\.\d+\.\d+\.\d+$', host))
    domain_failures = sum(1 for host, (success, _, _) in results.items() 
                         if not success and not re.match(r'^\d+\.\d+\.\d+\.\d+$', host))
    
    if successful_checks == total_checks:
        print("✅ NETWORK STATUS: Excellent - All systems operational")
        print("   Your internet connection is working perfectly.")
        
    elif ip_success and domain_failures > 0:
        print("⚠️  NETWORK STATUS: DNS Issues Detected")
        print("   • Internet connectivity: WORKING")
        print("   • DNS resolution: FAILING")
        print("   • Action: Check DNS settings or try using 8.8.8.8/1.1.1.1")
        
    elif successful_checks > 0:
        print("⚠️  NETWORK STATUS: Partial Connectivity")
        print("   • Some services are reachable, others are not")
        print("   • Possible issues: Firewall, specific service outages")
        print("   • Action: Check if the problem is site-specific")
        
    else:
        # Critical analysis when everything fails
        print("🔴 NETWORK STATUS: No Connectivity")
        print("   • Check physical connections (Ethernet/Wi-Fi)")
        print("   • Restart router/modem")
        print("   • Contact ISP if problem persists")
    
    print("="*60)

def main():
    print("🛠️  Professional Network Diagnostics Tool")
    print("="*50)
    
    # Always test critical services first for baseline
    print("Phase 1: Testing critical internet services...")
    critical_services = check_common_services()
    
    results = {}
    
    for service in critical_services:
        if not validate_hostname(service):
            continue
            
        print(f"\nTesting: {service}")
        
        # DNS check first
        dns_success, dns_info = dns_lookup(service)
        if dns_success:
            print(f"  DNS: ✅ Resolved to {dns_info}")
        else:
            print(f"  DNS: ❌ Failed")
            results[service] = (False, 0, "DNS resolution failed")
            continue
        
        # Ping check
        success, response_time, packet_loss = ping_host(service)
        results[service] = (success, response_time, packet_loss)
        
        if success:
            print(f"  Ping: ✅ {response_time:.1f}ms (0% packet loss)")
        else:
            print(f"  Ping: ❌ Failed ({packet_loss}% packet loss)")
    
    # Now test user-specific sites
    print("\n" + "-"*50)
    print("Phase 2: Testing your specific sites...")
    
    user_input = input("Enter websites to test (comma-separated, or press Enter to skip): ").strip()
    
    if user_input:
        user_sites = [site.strip() for site in user_input.split(',') if site.strip()]
        
        for site in user_sites:
            if not validate_hostname(site):
                print(f"  {site}: ⚠️ Invalid format - skipping")
                continue
                
            dns_success, dns_info = dns_lookup(site)
            success, response_time, packet_loss = ping_host(site)
            results[site] = (success, response_time, packet_loss)
            
            status = "✅" if success else "❌"
            dns_status = "Resolved" if dns_success else "Failed"
            print(f"  {site}: {status} Ping: {response_time:.1f}ms, DNS: {dns_status}")
    
    # Professional diagnosis
    diagnose_connectivity(results)
    
    # Summary table
    print("\n📊 DETAILED RESULTS:")
    print("-"*60)
    print(f"{'Host':<20} {'Status':<10} {'Response Time':<15} {'DNS'}") 
    print("-"*60)
    
    for host, (success, response_time, packet_loss) in results.items():
        status = "✅ UP" if success else "❌ DOWN"
        time_str = f"{response_time:.1f}ms" if success else "N/A"
        dns_success, dns_info = dns_lookup(host)
        dns_str = "✅" if dns_success else "❌"
        
        print(f"{host:<20} {status:<10} {time_str:<15} {dns_str}")

if __name__ == "__main__":
    main()
