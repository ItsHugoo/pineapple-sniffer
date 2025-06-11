import pytest
from src.security.vpn_detector import PineappleDetector

class TestVPNConfiguration:
    def test_vpn_configuration_detection(self):
        detector = PineappleDetector()
        vpn_config = detector.detect_vpn_configuration()
        
        assert vpn_config is not None, "VPN configuration detection should return a result"
        assert isinstance(vpn_config, dict), "VPN configuration should be a dictionary"
        
        # Check for expected keys in VPN configuration
        expected_keys = ['status', 'protocol', 'connection_type']
        for key in expected_keys:
            assert key in vpn_config, f"Missing {key} in VPN configuration"
    
    def test_vpn_status_parsing(self):
        detector = PineappleDetector()
        vpn_status = detector.detect_vpn_configuration()
        
        assert 'status' in vpn_status, "VPN status should be included"
        assert vpn_status['status'] in ['connected', 'disconnected', 'unknown'], "Invalid VPN status"