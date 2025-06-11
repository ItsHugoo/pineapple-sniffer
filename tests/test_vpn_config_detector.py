import logging
import pytest
from src.vpn_config_detector import (
    VPNConfigDetector, 
    VPNConfigDetectionError, 
    VPNConnectionDetails, 
    VPNProtocol,
    configure_logging
)

def test_vpn_config_detector_initialization():
    """Test VPNConfigDetector initialization"""
    detector = VPNConfigDetector()
    assert detector.logger is not None
    assert detector.logger.level == logging.INFO

def test_detect_vpn_connections():
    """Test VPN connection detection"""
    detector = VPNConfigDetector()
    connections = detector.detect_vpn_connections()
    
    assert isinstance(connections, list)
    
    for connection in connections:
        assert isinstance(connection, VPNConnectionDetails)
        assert connection.protocol in VPNProtocol
        assert isinstance(connection.is_active, bool)
        assert connection.interface is not None

def test_logging_configuration():
    """Test logging configuration"""
    log_file = 'test_vpn_detection.log'
    configure_logging(log_file, logging.DEBUG)
    
    logger = logging.getLogger('src.vpn_config_detector')
    assert logger.level == logging.DEBUG
    
    # Optional: Check if log file is created (implementation-specific)
    import os
    assert os.path.exists(log_file)
    os.remove(log_file)  # Clean up test log file

def test_error_handling():
    """Test error handling in VPN configuration detection"""
    # This would require mocking subprocess or creating specific test scenarios
    pass