import pytest
from src.vpn_detector import VPNConfigDetector

class TestVPNConfigDetector:
    @pytest.fixture
    def vpn_detector(self):
        return VPNConfigDetector()

    def test_detect_vpn_interfaces_type(self, vpn_detector):
        """Test that detect_vpn_interfaces returns a list."""
        interfaces = vpn_detector.detect_vpn_interfaces()
        assert isinstance(interfaces, list)

    def test_get_vpn_routing_info_type(self, vpn_detector):
        """Test that get_vpn_routing_info returns a dictionary."""
        routing_info = vpn_detector.get_vpn_routing_info()
        assert isinstance(routing_info, dict)

    def test_detect_vpn_configuration_structure(self, vpn_detector):
        """Test the structure of detect_vpn_configuration return value."""
        config = vpn_detector.detect_vpn_configuration()
        
        assert 'interfaces' in config
        assert 'routing' in config
        assert 'is_vpn_active' in config
        
        assert isinstance(config['interfaces'], list)
        assert isinstance(config['routing'], dict)
        assert isinstance(config['is_vpn_active'], bool)

    def test_run_command_error_handling(self, vpn_detector):
        """Test that _run_command handles errors gracefully."""
        with pytest.raises(TypeError):
            # Should raise TypeError for invalid input
            vpn_detector._run_command(None)  # type: ignore