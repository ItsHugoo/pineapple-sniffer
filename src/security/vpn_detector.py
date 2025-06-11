import subprocess
import json
import platform
from typing import Dict, Optional

class PineappleDetector:
    def __init__(self):
        self.os_type = platform.system().lower()
    
    def detect_vpn_configuration(self) -> Dict[str, str]:
        """
        Detect VPN configuration across different operating systems.
        
        Returns:
            Dict[str, str]: A dictionary containing VPN configuration details.
        """
        try:
            if self.os_type == 'darwin':  # macOS
                return self._detect_vpn_macos()
            elif self.os_type == 'linux':
                return self._detect_vpn_linux()
            else:
                return {'status': 'unknown', 'protocol': 'unsupported', 'connection_type': 'unknown'}
        
        except Exception as e:
            return {
                'status': 'error',
                'error_message': str(e),
                'protocol': 'unknown',
                'connection_type': 'unknown'
            }
    
    def _detect_vpn_macos(self) -> Dict[str, str]:
        """Detect VPN configuration on macOS."""
        try:
            result = subprocess.run(['scutil', '--nc', 'list'], capture_output=True, text=True)
            if 'Connected' in result.stdout:
                return {
                    'status': 'connected',
                    'protocol': 'native_macos',
                    'connection_type': 'system_vpn'
                }
            return {
                'status': 'disconnected',
                'protocol': 'native_macos',
                'connection_type': 'system_vpn'
            }
        except Exception:
            return {
                'status': 'unknown',
                'protocol': 'native_macos',
                'connection_type': 'system_vpn'
            }
    
    def _detect_vpn_linux(self) -> Dict[str, str]:
        """Detect VPN configuration on Linux."""
        try:
            result = subprocess.run(['ip', 'tuntap'], capture_output=True, text=True)
            if result.stdout.strip():
                return {
                    'status': 'connected',
                    'protocol': 'linux_tun',
                    'connection_type': 'network_interface'
                }
            return {
                'status': 'disconnected',
                'protocol': 'linux_tun',
                'connection_type': 'network_interface'
            }
        except Exception:
            return {
                'status': 'unknown',
                'protocol': 'linux_tun',
                'connection_type': 'network_interface'
            }