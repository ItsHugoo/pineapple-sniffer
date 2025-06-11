import logging
import subprocess
import typing
from dataclasses import dataclass
from enum import Enum, auto

class VPNProtocol(Enum):
    OPENVPN = auto()
    WIREGUARD = auto()
    IPSEC = auto()
    UNKNOWN = auto()

@dataclass
class VPNConnectionDetails:
    protocol: VPNProtocol
    interface: str
    is_active: bool
    local_ip: typing.Optional[str] = None
    remote_ip: typing.Optional[str] = None

class VPNConfigDetectionError(Exception):
    """Custom exception for VPN configuration detection errors."""
    pass

class VPNConfigDetector:
    def __init__(self, log_level: int = logging.INFO):
        """
        Initialize VPN Configuration Detector
        
        Args:
            log_level (int): Logging level, defaults to logging.INFO
        """
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(log_level)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(formatter)
        
        # Add handler if not already added
        if not self.logger.handlers:
            self.logger.addHandler(console_handler)

    def detect_vpn_connections(self) -> typing.List[VPNConnectionDetails]:
        """
        Detect active VPN connections across different protocols
        
        Returns:
            List of VPN connection details
        
        Raises:
            VPNConfigDetectionError: If detection fails
        """
        try:
            # Placeholder for multi-protocol detection
            # This would be expanded with actual system-specific detection logic
            openvpn_connections = self._detect_openvpn()
            wireguard_connections = self._detect_wireguard()
            
            return openvpn_connections + wireguard_connections
        
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Command execution failed: {e}")
            raise VPNConfigDetectionError(f"VPN detection failed: {e}")
        
        except Exception as e:
            self.logger.exception(f"Unexpected error during VPN detection: {e}")
            raise VPNConfigDetectionError(f"Unexpected VPN detection error: {e}")

    def _detect_openvpn(self) -> typing.List[VPNConnectionDetails]:
        """
        Detect OpenVPN connections
        
        Returns:
            List of OpenVPN connection details
        """
        try:
            # Simulated OpenVPN detection
            # In a real implementation, this would use system-specific commands
            return [
                VPNConnectionDetails(
                    protocol=VPNProtocol.OPENVPN,
                    interface='tun0',
                    is_active=True
                )
            ]
        except Exception as e:
            self.logger.warning(f"OpenVPN detection failed: {e}")
            return []

    def _detect_wireguard(self) -> typing.List[VPNConnectionDetails]:
        """
        Detect WireGuard connections
        
        Returns:
            List of WireGuard connection details
        """
        try:
            # Simulated WireGuard detection
            # In a real implementation, this would use system-specific commands
            return [
                VPNConnectionDetails(
                    protocol=VPNProtocol.WIREGUARD,
                    interface='wg0',
                    is_active=True
                )
            ]
        except Exception as e:
            self.logger.warning(f"WireGuard detection failed: {e}")
            return []

def configure_logging(log_file: typing.Optional[str] = None, log_level: int = logging.INFO):
    """
    Configure global logging settings
    
    Args:
        log_file (str, optional): Path to log file
        log_level (int): Logging level
    """
    # Get the root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)

    # Clear existing handlers
    root_logger.handlers.clear()
    
    # Formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    # Console Handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)
    
    # File Handler (if log_file is provided)
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(log_level)
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)
    
    # Set specific logger for this module to the specified level
    logging.getLogger('src.vpn_config_detector').setLevel(log_level)