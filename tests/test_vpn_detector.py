import sys
import pytest
from src.vpn_detector import VPNConfigurationDetector

def test_vpn_configuration_detector_instantiation():
    """Test that VPNConfigurationDetector can be instantiated."""
    detector = VPNConfigurationDetector()
    assert detector is not None

def test_detect_vpn_interfaces():
    """Test VPN interface detection method."""
    detector = VPNConfigurationDetector()
    interfaces = detector.detect_vpn_interfaces()
    
    # We don't assert specific interfaces due to environment differences
    assert isinstance(interfaces, dict)

def test_get_vpn_routing_info():
    """Test VPN routing information retrieval."""
    detector = VPNConfigurationDetector()
    routing_info = detector.get_vpn_routing_info()
    
    # Validate routing info structure
    assert isinstance(routing_info, dict)
    
    # Optional: Additional validation for route keys
    for key in routing_info:
        assert isinstance(routing_info[key], str)

def test_platform_specific_detection_methods():
    """Test platform-specific VPN detection methods."""
    detector = VPNConfigurationDetector()
    
    # Validate method exists for the current platform
    if sys.platform.lower().startswith('linux'):
        assert hasattr(detector, '_detect_linux_vpn_interfaces')
        linux_interfaces = detector._detect_linux_vpn_interfaces()
        assert isinstance(linux_interfaces, dict)
    
    elif sys.platform.lower().startswith('darwin'):
        assert hasattr(detector, '_detect_macos_vpn_interfaces')
        macos_interfaces = detector._detect_macos_vpn_interfaces()
        assert isinstance(macos_interfaces, dict)

def test_run_command_failure_handling():
    """Test command execution failure handling."""
    detector = VPNConfigurationDetector()
    
    with pytest.raises(RuntimeError):
        detector._run_command(['nonexistent_command'])