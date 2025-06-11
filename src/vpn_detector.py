import subprocess
import re
from typing import Dict, List, Optional, Any
import platform
import logging

class VPNConfigDetector:
    """
    A utility class for detecting VPN configurations across different platforms.
    """

    @staticmethod
    def _run_command(cmd: List[str]) -> str:
        """
        Run a shell command and return its output.
        
        Args:
            cmd (List[str]): The command to run as a list of strings.
        
        Returns:
            str: The command output.
        
        Raises:
            subprocess.CalledProcessError: If the command fails.
        """
        try:
            result = subprocess.run(
                cmd, 
                capture_output=True, 
                text=True, 
                check=True
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            logging.error(f"Command {' '.join(cmd)} failed: {e}")
            return ""

    @classmethod
    def detect_vpn_interfaces(cls) -> List[str]:
        """
        Detect VPN network interfaces across different platforms.
        
        Returns:
            List[str]: A list of detected VPN interface names.
        """
        system = platform.system().lower()
        vpn_interfaces = []

        try:
            if system == 'darwin':  # macOS
                interfaces = cls._run_command(['ifconfig', '-a'])
                vpn_interfaces = re.findall(r'^(utun\d+|ppp\d+)', interfaces, re.MULTILINE)
            
            elif system == 'linux':
                interfaces = cls._run_command(['ip', 'link', 'show'])
                vpn_interfaces = re.findall(r'^\d+: (tun\d+|ppp\d+|wg\d+)', interfaces, re.MULTILINE)
            
            elif system == 'windows':
                # Windows command to list network adapters
                interfaces = cls._run_command(['ipconfig', '/all'])
                vpn_interfaces = re.findall(r'Tunnel adapter (.*?):', interfaces)
        
        except Exception as e:
            logging.error(f"Error detecting VPN interfaces: {e}")
        
        return vpn_interfaces

    @classmethod
    def get_vpn_routing_info(cls) -> Dict[str, str]:
        """
        Retrieve VPN routing information.
        
        Returns:
            Dict[str, str]: A dictionary containing VPN routing details.
        """
        system = platform.system().lower()
        routing_info = {}

        try:
            if system == 'darwin':  # macOS
                route_output = cls._run_command(['netstat', '-nr'])
                vpn_routes = re.findall(r'(tun\d+|ppp\d+)\s+(\S+)', route_output)
                routing_info = dict(vpn_routes)
            
            elif system == 'linux':
                route_output = cls._run_command(['ip', 'route', 'show', 'table', 'all'])
                vpn_routes = re.findall(r'(tun\d+|ppp\d+|wg\d+)\s+(\S+)', route_output)
                routing_info = dict(vpn_routes)
            
            elif system == 'windows':
                # Windows route print command
                route_output = cls._run_command(['route', 'print'])
                vpn_routes = re.findall(r'Tunnel\s+(\S+)\s+(\S+)', route_output)
                routing_info = dict(vpn_routes)
        
        except Exception as e:
            logging.error(f"Error retrieving VPN routing information: {e}")
        
        return routing_info

    def detect_vpn_configuration(self) -> Dict[str, Any]:
        """
        Detect and compile comprehensive VPN configuration information.
        
        Returns:
            Dict[str, Any]: A dictionary containing VPN configuration details.
        """
        vpn_config = {
            'interfaces': self.detect_vpn_interfaces(),
            'routing': self.get_vpn_routing_info(),
            'is_vpn_active': bool(self.detect_vpn_interfaces())
        }
        
        return vpn_config