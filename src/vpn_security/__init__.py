"""
VPN Security Detection Module

This module provides functionality for detecting and analyzing VPN configurations.
"""
from typing import Dict, Optional, Any
import logging
import subprocess
import platform

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='vpn_security.log'
)
logger = logging.getLogger(__name__)

class VPNConfigurationError(Exception):
    """Custom exception for VPN configuration errors."""
    pass

def detect_vpn_connection() -> Dict[str, Any]:
    """
    Detect active VPN connections across different platforms.

    Returns:
        Dict[str, Any]: Dictionary containing VPN connection details or empty if no connection.

    Raises:
        VPNConfigurationError: If there's an error during VPN detection.
    """
    try:
        os_name = platform.system().lower()
        
        if os_name == 'darwin':  # macOS
            return _detect_macos_vpn()
        elif os_name == 'linux':
            return _detect_linux_vpn()
        else:
            logger.warning(f"Unsupported operating system: {os_name}")
            return {}
    except subprocess.CalledProcessError as e:
        logger.error(f"Command execution error: {e}")
        raise VPNConfigurationError(f"Failed to detect VPN connection: {e}")
    except Exception as e:
        logger.error(f"Unexpected error in VPN detection: {e}")
        raise VPNConfigurationError(f"Unexpected VPN detection error: {e}")

def _detect_macos_vpn() -> Dict[str, Any]:
    """Detect VPN connections on macOS."""
    try:
        result = subprocess.run(
            ['scutil', '--nc', 'list'], 
            capture_output=True, 
            text=True, 
            check=True
        )
        
        if result.stdout.strip():
            logger.info("VPN connection detected on macOS")
            return {"platform": "macOS", "active": True}
        
        logger.info("No VPN connection found on macOS")
        return {}
    except subprocess.CalledProcessError as e:
        logger.error(f"macOS VPN detection failed: {e}")
        raise

def _detect_linux_vpn() -> Dict[str, Any]:
    """Detect VPN connections on Linux."""
    try:
        # Check for typical VPN interfaces like tun0, ppp0
        result = subprocess.run(
            ['ip', 'tuntap'], 
            capture_output=True, 
            text=True, 
            check=True
        )
        
        if result.stdout.strip():
            logger.info("VPN connection detected on Linux")
            return {"platform": "Linux", "active": True}
        
        logger.info("No VPN connection found on Linux")
        return {}
    except subprocess.CalledProcessError as e:
        logger.error(f"Linux VPN detection failed: {e}")
        raise