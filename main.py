
 #!/usr/bin/env python3
"""
Professional Network Diagnostics Tool
Author: Eniola Favour
Description: Network Connectivity Checker, an IT support tool with menu system
"""

import subprocess
import platform
import socket
import re
import time
import os

def clear_screen():
    """Clear the terminal screen"""
    os.system('cls' if platform.system() == 'Windows' else 'clear')

def show_banner():
    """Display tool banner"""
    print("🛠️  Professional Network Diagnostics Tool")
    print("=" * 50)

def validate_hostname(hostname):
    """Validate if hostname format is reasonable"""
    if not hostname or len(hostname) > 255:
        return False
    if re.match(r'^[a-zA-Z0-9.-]+$', hostname):
        return True
    return False

def ping_host(hostname, count=4, timeout=5):
    """Professional ping with detailed results"""
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    command = ['ping', param, str(count), hostname]
    
    try:
        result = subprocess.run(command, capture_output=True, text=True, timeout=timeout)
        
        if result.returncode == 0:
            time_match = re.search(r'time=([0-9.]+)\s*ms', result.stdout)
            response_time = float(time_match.group(1)) if time_match else 0
            return True, response_time, 0
        else:
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

def run_quick_diagnosis():
    """Quick automated network health check"""
    print("\n🚀 Running Quick Network Diagnosis...")
    print("-" * 40)
    
    test_services = [
        ("Google DNS (8.8.8.8)", "8.8.8.8"),  # Bypass DNS
        ("Google.com", "google.com"),         # Test DNS + connectivity
        ("Cloudflare", "cloudflare.com")      # Another reliable service
    ]
    
    all_successful = True
    dns_working = True
    
    for service_name, address in test_services:
        print(f"Testing {service_name}...", end=" ")
        
        # For IP addresses, skip DNS check
        if re.match(r'^\d+\.\d+\.\d+\.\d+$', address):
            success, response_time, loss = ping_host(address)
            if success:
                print(f"✅ {response_time:.1f}ms")
            else:
                print("❌ FAILED")
                all_successful = False
        else:
            # For domains, check DNS first
            dns_ok, ip = dns_lookup(address)
            if dns_ok:
                success, response_time, loss = ping_host(address)
                if success:
                    print(f"✅ {response_time:.1f}ms (DNS: {ip})")
                else:
                    print("❌ PING FAILED")
                    all_successful = False
            else:
                print("❌ DNS FAILED")
                dns_working = False
                all_successful = False
    
    # Provide intelligent diagnosis
    print("\n" + "=" * 50)
    print("🔧 DIAGNOSIS RESULTS:")
    print("=" * 50)
    
    if all_successful:
        print("✅ NETWORK STATUS: Excellent")
        print("   All systems operational - no issues detected")
    elif not dns_working:
        print("⚠️  NETWORK STATUS: DNS Issues")
        print("   Internet connectivity is working but DNS is failing")
        print("   Try using Google DNS (8.8.8.8) or Cloudflare (1.1.1.1)")
    else:
        print("🔴 NETWORK STATUS: Connectivity Issues")
        print("   Check your router, cables, or contact your ISP")

def run_custom_test():
    """Test specific websites entered by user"""
    print("\n🎯 Custom Website Testing")
    print("-" * 40)
    
    while True:
        user_input = input("\nEnter website to test (or 'back' to return): ").strip()
        
        if user_input.lower() == 'back':
            break
            
        if not validate_hostname(user_input):
            print("❌ Invalid hostname format")
            continue
            
        print(f"\nTesting: {user_input}")
        print("-" * 25)
        
        # Check if it's an IP or domain
        if re.match(r'^\d+\.\d+\.\d+\.\d+$', user_input):
            print("Type: IP Address (DNS bypassed)")
            success, response_time, loss = ping_host(user_input)
            if success:
                print(f"Status: ✅ Reachable ({response_time:.1f}ms)")
            else:
                print(f"Status: ❌ Unreachable ({loss}% packet loss)")
        else:
            # Domain name - check DNS first
            dns_ok, ip = dns_lookup(user_input)
            if dns_ok:
                print(f"DNS: ✅ Resolved to {ip}")
                success, response_time, loss = ping_host(user_input)
                if success:
                    print(f"Ping: ✅ Reachable ({response_time:.1f}ms)")
                else:
                    print(f"Ping: ❌ Unreachable ({loss}% packet loss)")
            else:
                print("DNS: ❌ Resolution failed - probably an inactive or misspelled site")
                print("Ping: Skipped (DNS failure)")

def show_network_tips():
    """Display common troubleshooting tips"""
    print("\n💡 Network Troubleshooting Tips")
    print("=" * 50)
    print("1. Restart your router/modem")
    print("2. Check physical cables and Wi-Fi connection")
    print("3. Try using Google DNS: 8.8.8.8 and 8.8.4.4")
    print("4. Disable VPN or proxy temporarily")
    print("5. Check firewall settings")
    print("6. Update network drivers")
    print("7. Contact your ISP if issues persist")
    input("\nPress Enter to return to menu...")

def main_menu():
    """Main interactive menu system"""
    while True:
        clear_screen()
        show_banner()
        
        print("\n📋 Main Menu:")
        print("1. 🔄 Quick Network Diagnosis")
        print("2. 🎯 Test Specific Website")
        print("3. 💡 Troubleshooting Tips")
        print("4. ❌ Exit Tool")
        
        choice = input("\nSelect option (1-4): ").strip()
        
        if choice == '1':
            run_quick_diagnosis()
            input("\nPress Enter to continue...")
        elif choice == '2':
            run_custom_test()
        elif choice == '3':
            show_network_tips()
        elif choice == '4':
            print("\n👋 Thank you for using the Network Diagnostics Tool!")
            break
        else:
            print("❌ Invalid option. Please try again.")
            time.sleep(1)

if __name__ == "__main__":
    main_menu()
