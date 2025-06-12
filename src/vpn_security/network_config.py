import subprocess
import re
import sys
from typing import Dict, List, Optional

class VPNConfigDetector:
    """
    A class to detect and analyze VPN network configurations.
    
    This class provides methods to inspect network interfaces,
    routing tables, and detect active VPN connections.
    """
    
    @staticmethod
    def get_network_interfaces() -> Dict[str, str]:
        """
        Retrieve network interface details.
        
        Returns:
            Dict of network interface names and their IP addresses.
        """
        try:
            # Use platform-independent command for network interfaces
            result = subprocess.run(['ip', 'addr'], 
                                    capture_output=True, 
                                    text=True, 
                                    check=True)
            
            # Updated regex to handle more diverse network interface outputs
            pattern = re.compile(
                r'^(\d+):\s*(\w+):\s*<.*>\n'      # Interface index and name
                r'(?:.*\n)*'                      # Optional intermediate lines
                r'\s*inet\s+(\d+\.\d+\.\d+\.\d+)(?:/\d+)?',  # Capture IP with optional CIDR
                re.MULTILINE
            )
            
            interfaces = {}
            for match in pattern.finditer(result.stdout):
                interface_name = match.group(2)
                ip_address = match.group(3)
                interfaces[interface_name] = ip_address
            
            print(f"DEBUG: Full output: {result.stdout}", file=sys.stderr)
            print(f"DEBUG: Detected interfaces: {interfaces}", file=sys.stderr)
            return interfaces
        
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            print(f"DEBUG: Error in get_network_interfaces: {e}", file=sys.stderr)
            # Fallback for systems without 'ip' command
            return {}
    
    # ... rest of the class remains the same