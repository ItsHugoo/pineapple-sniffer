import logging
import subprocess
import sys
from typing import Dict, Optional, List, Union

class VPNDetectionError(Exception):
    """Custom exception for VPN detection errors."""
    pass

class VPNConfigurationDetector:
    """
    A class to detect and analyze VPN configurations with robust error handling.
    
    Attributes:
        logger (logging.Logger): Logger for tracking VPN detection activities
    """
    
    def __init__(self, log_level: int = logging.INFO):
        """
        Initialize the VPN configuration detector.
        
        Args:
            log_level (int): Logging level. Defaults to logging.INFO.
        """
        # Configure logging
        logging.basicConfig(
            level=log_level, 
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler(sys.stdout),
                logging.FileHandler('vpn_detection.log', mode='a')
            ]
        )
        self.logger = logging.getLogger(self.__class__.__name__)
    
    def _run_command(self, command: List[str]) -> str:
        """
        Run a system command with error handling.
        
        Args:
            command (List[str]): Command to execute
        
        Returns:
            str: Command output
        
        Raises:
            VPNDetectionError: If command execution fails
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
            error_msg = f"Command {' '.join(command)} failed: {e.stderr}"
            self.logger.error(error_msg)
            raise VPNDetectionError(error_msg) from e
        except FileNotFoundError as e:
            error_msg = f"Command not found: {' '.join(command)}"
            self.logger.error(error_msg)
            raise VPNDetectionError(error_msg) from e
    
    def detect_vpn_interfaces(self) -> List[str]:
        """
        Detect VPN network interfaces.
        
        Returns:
            List[str]: List of detected VPN interfaces
        """
        try:
            # Check network interfaces that might indicate VPN
            if sys.platform.startswith('darwin'):  # macOS
                command = ['networksetup', '-listnetworkserviceorder']
            elif sys.platform.startswith('linux'):
                command = ['ip', 'link', 'show', 'type', 'tun']
            else:
                self.logger.warning(f"Unsupported platform: {sys.platform}")
                return []
            
            output = self._run_command(command)
            
            # Parse and filter VPN-related interfaces
            vpn_interfaces = self._parse_vpn_interfaces(output)
            
            self.logger.info(f"Detected VPN interfaces: {vpn_interfaces}")
            return vpn_interfaces
        
        except VPNDetectionError as e:
            self.logger.error(f"VPN interface detection failed: {e}")
            return []
    
    def _parse_vpn_interfaces(self, output: str) -> List[str]:
        """
        Parse system output to extract VPN interfaces.
        
        Args:
            output (str): Raw command output
        
        Returns:
            List[str]: List of VPN interface names
        """
        # This is a simplified implementation
        vpn_keywords = ['tun', 'tap', 'ppp', 'vpn', 'utun']
        return [
            line.split()[-1] 
            for line in output.splitlines() 
            if any(keyword in line.lower() for keyword in vpn_keywords)
        ]
    
    def get_vpn_connection_details(self) -> Optional[Dict[str, Union[str, bool]]]:
        """
        Retrieve detailed VPN connection information.
        
        Returns:
            Optional[Dict[str, Union[str, bool]]]: VPN connection details or None
        """
        try:
            interfaces = self.detect_vpn_interfaces()
            
            if not interfaces:
                self.logger.info("No VPN interfaces detected")
                return None
            
            # Placeholder for platform-specific detailed checks
            details = {
                'active': bool(interfaces),
                'interfaces': interfaces,
                'platform': sys.platform
            }
            
            self.logger.info(f"VPN Connection Details: {details}")
            return details
        
        except Exception as e:
            self.logger.error(f"Error retrieving VPN connection details: {e}")
            return None