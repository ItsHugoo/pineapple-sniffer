import pytest
import sys
from unittest.mock import patch, MagicMock
import logging

from src.vpn_security.vpn_detector import VPNConfigurationDetector, VPNDetectionError

class TestVPNConfigurationDetector:
    def setup_method(self):
        """Set up a new VPNConfigurationDetector for each test."""
        self.detector = VPNConfigurationDetector(log_level=logging.DEBUG)
    
    def test_initialization(self):
        """Test that the detector initializes correctly."""
        assert isinstance(self.detector, VPNConfigurationDetector)
        assert self.detector.logger is not None
    
    @patch('subprocess.run')
    def test_run_command_success(self, mock_run):
        """Test successful command execution."""
        mock_run.return_value = MagicMock(stdout='test output', stderr='')
        result = self.detector._run_command(['echo', 'test'])
        assert result == 'test output'
    
    @patch('subprocess.run')
    def test_run_command_failure(self, mock_run):
        """Test command execution failure."""
        mock_run.side_effect = subprocess.CalledProcessError(
            returncode=1, 
            cmd=['invalid_command'], 
            stderr='Command not found'
        )
        with pytest.raises(VPNDetectionError):
            self.detector._run_command(['invalid_command'])
    
    @patch('sys.platform', 'darwin')
    @patch.object(VPNConfigurationDetector, '_run_command')
    def test_detect_vpn_interfaces_macos(self, mock_run_command):
        """Test VPN interface detection on macOS."""
        mock_run_command.return_value = """
        (Hardware Port: VPN (utun1), Device: utun1
        (Hardware Port: Wi-Fi, Device: en0
        """
        interfaces = self.detector.detect_vpn_interfaces()
        assert 'utun1' in interfaces
    
    @patch('sys.platform', 'linux')
    @patch.object(VPNConfigurationDetector, '_run_command')
    def test_detect_vpn_interfaces_linux(self, mock_run_command):
        """Test VPN interface detection on Linux."""
        mock_run_command.return_value = """
        4: tun0: <POINTOPOINT,MULTICAST,NOARP> mtu 1500 qdisc pfifo_fast state UNKNOWN mode DEFAULT group default qlen 100
        """
        interfaces = self.detector.detect_vpn_interfaces()
        assert 'tun0' in interfaces
    
    def test_get_vpn_connection_details(self):
        """Test retrieving VPN connection details."""
        with patch.object(VPNConfigurationDetector, 'detect_vpn_interfaces', return_value=['utun1']):
            details = self.detector.get_vpn_connection_details()
            assert details is not None
            assert details['active'] is True
            assert 'utun1' in details['interfaces']
    
    def test_unsupported_platform(self):
        """Test behavior on an unsupported platform."""
        with patch('sys.platform', 'unsupported_os'):
            interfaces = self.detector.detect_vpn_interfaces()
            assert interfaces == []