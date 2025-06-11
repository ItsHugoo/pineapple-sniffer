"""
Test module for VPN configuration detection.
"""
import pytest
from unittest.mock import patch
from src.vpn_security import detect_vpn_connection, VPNConfigurationError

def test_detect_vpn_connection_import():
    """Verify the detect_vpn_connection function can be imported."""
    assert detect_vpn_connection is not None

@patch('platform.system', return_value='Unknown')
def test_unsupported_os(mock_system):
    """Test handling of unsupported operating systems."""
    result = detect_vpn_connection()
    assert result == {}

@patch('platform.system', return_value='Darwin')
@patch('subprocess.run')
def test_macos_vpn_detection_active(mock_run, mock_system):
    """Test VPN detection on macOS with an active connection."""
    mock_run.return_value.stdout = "Some VPN connection"
    result = detect_vpn_connection()
    assert result == {"platform": "macOS", "active": True}

@patch('platform.system', return_value='Darwin')
@patch('subprocess.run')
def test_macos_vpn_detection_inactive(mock_run, mock_system):
    """Test VPN detection on macOS with no active connection."""
    mock_run.return_value.stdout = ""
    result = detect_vpn_connection()
    assert result == {}

@patch('platform.system', return_value='Linux')
@patch('subprocess.run')
def test_linux_vpn_detection_active(mock_run, mock_system):
    """Test VPN detection on Linux with an active connection."""
    mock_run.return_value.stdout = "tun0: tap"
    result = detect_vpn_connection()
    assert result == {"platform": "Linux", "active": True}

@patch('platform.system', return_value='Linux')
@patch('subprocess.run')
def test_linux_vpn_detection_inactive(mock_run, mock_system):
    """Test VPN detection on Linux with no active connection."""
    mock_run.return_value.stdout = ""
    result = detect_vpn_connection()
    assert result == {}