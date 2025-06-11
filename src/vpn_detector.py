import subprocess
import sys
import re
from typing import Dict, List, Optional

class VPNConfigurationDetector:
    """
    A class to detect and analyze VPN network configurations.
    
    Supports multiple platforms and provides insights into VPN network interfaces
    and routing configurations.
    """

    @staticmethod
    def _run_command(command: List[str]) -> str:
        """
        Run a shell command and return its output.
        
        Args:
            command (List[str]): Command to execute as a list of strings.
        
        Returns:
            str: Command output
        
        Raises:
            RuntimeError: If command execution fails
        """
        try:
            result = subprocess.run(
                command, 
                capture_output=True, 
                text=True, 
                check=True
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Command execution failed: {e}")

    def detect_vpn_interfaces(self) -> Dict[str, str]:
        """
        Detect VPN network interfaces across different platforms.
        
        Returns:
            Dict[str, str]: Dictionary of VPN interface names and their details
        """
        try:
            platform = sys.platform.lower()
            
            if platform.startswith('linux'):
                return self._detect_linux_vpn_interfaces()
            elif platform.startswith('darwin'):
                return self._detect_macos_vpn_interfaces()
            elif platform.startswith('win'):
                return self._detect_windows_vpn_interfaces()
            else:
                raise NotImplementedError(f"Unsupported platform: {platform}")
        
        except Exception as e:
            return {"error": str(e)}

    def _detect_linux_vpn_interfaces(self) -> Dict[str, str]:
        """
        Detect VPN interfaces on Linux systems.
        
        Returns:
            Dict[str, str]: VPN network interfaces
        """
        try:
            interfaces_raw = self._run_command(['ip', 'tuntap', 'show'])
            tun_interfaces = re.findall(r'tun\d+', interfaces_raw)
            
            # Add WireGuard support
            wireguard_interfaces = self._run_command(['wg', 'show', 'interfaces']).split()
            
            combined_interfaces = {
                **{iface: 'tun' for iface in tun_interfaces},
                **{iface: 'wireguard' for iface in wireguard_interfaces}
            }
            
            return combined_interfaces
        except Exception:
            return {}

    def _detect_macos_vpn_interfaces(self) -> Dict[str, str]:
        """
        Detect VPN interfaces on macOS systems.
        
        Returns:
            Dict[str, str]: VPN network interfaces
        """
        try:
            interfaces_raw = self._run_command(['ifconfig'])
            
            # Match various VPN-related interface patterns
            vpn_patterns = [
                r'(utun\d+)',      # macOS VPN interfaces
                r'(ppp\d+)',       # Point-to-Point Protocol
                r'(ipsec\d+)'      # IPSec interfaces
            ]
            
            interfaces = {}
            for pattern in vpn_patterns:
                found_interfaces = re.findall(pattern, interfaces_raw)
                interfaces.update({iface: 'vpn' for iface in found_interfaces})
            
            return interfaces
        except Exception:
            return {}

    def _detect_windows_vpn_interfaces(self) -> Dict[str, str]:
        """
        Detect VPN interfaces on Windows systems.
        
        Returns:
            Dict[str, str]: VPN network interfaces
        """
        try:
            # Future implementation for Windows VPN detection
            return {}
        except Exception:
            return {}

    def get_vpn_routing_info(self) -> Dict[str, str]:
        """
        Get VPN routing information.
        
        Returns:
            Dict[str, str]: VPN routing details
        """
        try:
            platform = sys.platform.lower()
            
            if platform.startswith('linux'):
                return self._get_linux_routing()
            elif platform.startswith('darwin'):
                return self._get_macos_routing()
            else:
                return {}
        
        except Exception as e:
            return {"error": str(e)}

    def _get_linux_routing(self) -> Dict[str, str]:
        """
        Get routing information for Linux.
        
        Returns:
            Dict[str, str]: Routing details
        """
        try:
            routes = self._run_command(['ip', 'route', 'show'])
            default_route = re.search(r'default via (\S+) dev (\S+)', routes)
            
            if default_route:
                return {
                    "gateway": default_route.group(1),
                    "interface": default_route.group(2)
                }
            return {}
        except Exception:
            return {}

    def _get_macos_routing(self) -> Dict[str, str]:
        """
        Get routing information for macOS.
        
        Returns:
            Dict[str, str]: Routing details
        """
        try:
            routes = self._run_command(['netstat', '-nr'])
            default_route = re.search(r'default\s+(\S+)\s+(\S+)', routes)
            
            if default_route:
                return {
                    "gateway": default_route.group(1),
                    "interface": default_route.group(2)
                }
            return {}
        except Exception:
            return {}