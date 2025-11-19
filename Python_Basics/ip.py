import subprocess
import platform
import concurrent.futures

def check_ip_reachability(ip):
    """
    Pings a single IP address to check for reachability.
    Returns the IP if reachable, None otherwise.
    """
    # Determine the correct ping command based on the OS
    system = platform.system().lower()
    
    # -n 1 (Windows) or -c 1 (Linux/macOS): Send only 1 packet
    # -w 1000 (Windows) or -W 1 (Linux/macOS): Set a 1-second (1000ms) timeout
    if system == "windows":
        command = ["ping", "-n", "1", "-w", "1000", ip]
    else:
        command = ["ping", "-c", "1", "-W", "1", ip]

    try:
        # Run the command, suppressing all output
        result = subprocess.run(
            command,
            stdout=subprocess.DEVNULL, 
            stderr=subprocess.DEVNULL
        )
        
        # A return code of 0 means the ping was successful
        if result.returncode == 0:
            return ip
    except Exception:
        # Handle any unexpected errors (e.g., if ping isn't installed)
        pass
    
    return None

def filter_reachable_ips(ip_list):
    """
    Accepts a list of IP addresses and returns a list
    of only those that are reachable (respond to a ping).
    """
    reachable_ips = []
    
    # Use ThreadPoolExecutor to check IPs in parallel
    # We set max_workers to 50 as a reasonable limit
    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        # map() runs the function for each item and returns results in order
        results = executor.map(check_ip_reachability, ip_list)
        
        # Filter out the None results (unreachable IPs)
        for ip in results:
            if ip:
                reachable_ips.append(ip)
                
    return reachable_ips


# A list of public DNS servers and some unreachable IPs
ips_to_check = [
    "8.8.8.8",        
    "1.1.1.1",        
    "192.0.2.1",      
    "9.9.9.9",        
    "198.51.100.1",   
    "208.67.222.222"  
]

print(f"Checking {len(ips_to_check)} IPs...")

reachable = filter_reachable_ips(ips_to_check)

print("\n--- Reachable IPs ---")
for ip in reachable:
    print(ip)