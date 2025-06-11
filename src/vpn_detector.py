import subprocess
import sys
import re
from typing import Dict, List, Optional

class VPNConfigDetector:
    """
    A utility class for detecting VPN configurations across different platforms.
    """

    @staticmethod
    def _run_command(command: List[str]) -> str:
        """
        Run a shell command and return its output.

        Args:
            command (List[str]): The command to run as a list of strings.

        Returns:
            str: The output of the command.

        Raises:
            subprocess.CalledProcessError: If the command fails.
        """
        try:
            result = subprocess.run(
                command, 
                capture_output=True, 
                text=True, 
                check=True
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError:
            return ""

    @classmethod
    def detect_vpn_interfaces(cls) -> List[str]:
        """
        Detect VPN network interfaces across different platforms.

        Returns:
            List[str]: A list of detected VPN interface names.
        """
        try:
            # Platform-specific interface detection
            if sys.platform.startswith('darwin'):  # macOS
                return cls._detect_vpn_interfaces_darwin()
            elif sys.platform.startswith('linux'):  # Linux
                return cls._detect_vpn_interfaces_linux()
            else:
                return []
        except Exception:
            return []

    @classmethod
    def _detect_vpn_interfaces_darwin(cls) -> List[str]:
        """
        Detect VPN interfaces on macOS.

        Returns:
            List[str]: Detected VPN interface names.
        """
        try:
            # Check network interfaces that might indicate VPN
            output = cls._run_command(['ifconfig', '-a'])
            vpn_keywords = ['utun', 'ppp', 'ipsec', 'wireguard', 'tun']
            return [
                line.split(':')[0] 
                for line in output.split('\n') 
                if any(keyword in line.lower() for keyword in vpn_keywords)
            ]
        except Exception:
            return []

    @classmethod
    def _detect_vpn_interfaces_linux(cls) -> List[str]:
        """
        Detect VPN interfaces on Linux.

        Returns:
            List[str]: Detected VPN interface names.
        """
        try:
            # Check network interfaces that might indicate VPN
            output = cls._run_command(['ip', 'link', 'show'])
            vpn_keywords = ['tun', 'tap', 'wireguard', 'ppp', 'ipsec']
            return [
                line.split(':')[1].strip().split('@')[0] 
                for line in output.split('\n') 
                if any(keyword in line.lower() for keyword in vpn_keywords)
            ]
        except Exception:
            return []

    @classmethod
    def get_routing_info(cls) -> Dict[str, str]:
        """
        Get current routing information.

        Returns:
            Dict[str, str]: Routing information with interface and destination.
        """
        try:
            if sys.platform.startswith('darwin'):  # macOS
                return cls._get_routing_info_darwin()
            elif sys.platform.startswith('linux'):  # Linux
                return cls._get_routing_info_linux()
            else:
                return {}
        except Exception:
            return {}

    @classmethod
    def _get_routing_info_darwin(cls) -> Dict[str, str]:
        """
        Get routing information on macOS.

        Returns:
            Dict[str, str]: Routing details.
        """
        try:
            output = cls._run_command(['netstat', '-nr'])
            routes = {}
            for line in output.split('\n')[4:]:  # Skip header lines
                parts = line.split()
                if len(parts) >= 8:
                    # Explicitly look for 'default' route
                    if parts[0] == 'default':
                        routes['default'] = parts[5]
                    elif '/' in parts[0]:
                        # Optional: handle other network routes if needed
                        routes[parts[0]] = parts[5]
            return routes
        except Exception:
            return {}

    @classmethod
    def _get_routing_info_linux(cls) -> Dict[str, str]:
        """
        Get routing information on Linux.

        Returns:
            Dict[str, str]: Routing details.
        """
        try:
            output = cls._run_command(['ip', 'route'])
            routes = {}
            for line in output.split('\n'):
                parts = line.split()
                if parts and len(parts) >= 3:
                    # If route contains 'dev', extract the interface
                    dev_index = parts.index('dev') + 1 if 'dev' in parts else None
                    routes[parts[0]] = parts[dev_index] if dev_index is not None else parts[2]
            return routes
        except Exception:
            return {}