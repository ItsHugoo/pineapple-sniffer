import subprocess
import re
from typing import Dict, Optional, List, Union

class VPNConfigParser:
    """
    A class to parse VPN configuration details from system commands.
    
    Supports parsing VPN configurations across different platforms and protocols.
    """
    
    @staticmethod
    def run_command(command: Union[str, List[str]]) -> str:
        """
        Run a system command and return its output.
        
        Args:
            command (str or List[str]): Command to execute
        
        Returns:
            str: Command output
        
        Raises:
            subprocess.CalledProcessError: If command execution fails
        """
        try:
            if isinstance(command, str):
                command = command.split()
            
            result = subprocess.run(
                command, 
                capture_output=True, 
                text=True, 
                check=True
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            # Log the error and return an empty string
            print(f"Command execution failed: {e}")
            return ""
    
    @classmethod
    def detect_active_vpn_interfaces(cls) -> List[str]:
        """
        Detect active VPN network interfaces.
        
        Returns:
            List[str]: List of active VPN interface names
        """
        # Platform-specific interface detection commands
        interface_commands = {
            'darwin': ["ifconfig"],   # macOS
            'linux': ["ip", "link", "show", "type", "tun"]  # Linux
        }
        
        import platform
        os_name = platform.system().lower()
        
        if os_name not in interface_commands:
            return []
        
        try:
            output = cls.run_command(interface_commands[os_name])
            
            # Extract interface names for VPN-like interfaces
            if os_name == 'darwin':
                interfaces = re.findall(r'^(\w+\d+):', output, re.MULTILINE)
            else:  # linux
                interfaces = re.findall(r'\d+: (\w+):', output)
            
            return [iface for iface in interfaces if re.search(r'(tun|vpn)', iface, re.IGNORECASE)]
        
        except Exception as e:
            print(f"Error detecting VPN interfaces: {e}")
            return []
    
    @classmethod
    def get_vpn_connection_details(cls, interface: str) -> Dict[str, Optional[str]]:
        """
        Retrieve VPN connection details for a specific interface.
        
        Args:
            interface (str): Network interface name
        
        Returns:
            Dict[str, Optional[str]]: VPN connection details
        """
        details = {
            'interface': interface,
            'ip_address': None,
            'subnet_mask': None,
            'protocol': None
        }
        
        # Platform-specific IP configuration commands
        ip_commands = {
            'darwin': ["ifconfig", interface],  # macOS
            'linux': ["ip", "addr", "show", interface]  # Linux
        }
        
        import platform
        os_name = platform.system().lower()
        
        if os_name not in ip_commands:
            return details
        
        try:
            output = cls.run_command(ip_commands[os_name])
            
            # IP address extraction logic
            ip_match = re.search(r'inet\s+(\d+\.\d+\.\d+\.\d+)', output)
            if ip_match:
                details['ip_address'] = ip_match.group(1)
            
            # Subnet mask extraction (platform-specific)
            if os_name == 'darwin':
                subnet_match = re.search(r'netmask\s+(0x[0-9a-fA-F]+)', output)
                if subnet_match:
                    # Convert hex netmask to decimal
                    subnet_hex = int(subnet_match.group(1), 16)
                    details['subnet_mask'] = '.'.join(str((subnet_hex >> (8 * i)) & 255) for i in range(3, -1, -1))
            else:  # linux
                subnet_match = re.search(r'inet\s+\d+\.\d+\.\d+\.\d+/(\d+)', output)
                if subnet_match:
                    details['subnet_mask'] = subnet_match.group(1)
            
            # Detect protocol based on interface name
            details['protocol'] = 'OpenVPN' if 'tun' in interface else 'Unknown'
            
            return details
        
        except Exception as e:
            print(f"Error retrieving VPN connection details: {e}")
            return details