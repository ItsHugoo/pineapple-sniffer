import subprocess
import pytest
from unittest.mock import patch
from src.vpn_security.config_parser import VPNConfigParser

class TestVPNConfigParser:
    @patch('subprocess.run')
    def test_run_command_success(self, mock_run):
        """Test successful command execution."""
        mock_run.return_value.stdout = "test output\n"
        mock_run.return_value.stderr = ""
        
        result = VPNConfigParser.run_command(["ls", "-l"])
        assert result == "test output"
    
    @patch('subprocess.run')
    def test_run_command_failure(self, mock_run):
        """Test command execution failure."""
        mock_run.side_effect = subprocess.CalledProcessError(1, "cmd")
        
        result = VPNConfigParser.run_command(["invalid_command"])
        assert result == ""
    
    @patch('platform.system')
    @patch('subprocess.run')
    def test_detect_active_vpn_interfaces_darwin(self, mock_run, mock_system):
        """Test VPN interface detection on macOS."""
        mock_system.return_value = "Darwin"
        mock_run.return_value.stdout = """
en0: flags=8863<UP,BROADCAST,SMART,RUNNING,SIMPLEX,MULTICAST> mtu 1500
tun0: flags=8851<UP,POINTOPOINT,RUNNING,NOARP,MULTICAST> mtu 1380
        """
        
        interfaces = VPNConfigParser.detect_active_vpn_interfaces()
        assert "tun0" in interfaces
    
    @patch('platform.system')
    @patch('subprocess.run')
    def test_detect_active_vpn_interfaces_linux(self, mock_run, mock_system):
        """Test VPN interface detection on Linux."""
        mock_system.return_value = "Linux"
        mock_run.return_value.stdout = """
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN mode DEFAULT group default qlen 1000
2: ens33: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP mode DEFAULT group default qlen 1000
3: tun0: <POINTOPOINT,MULTICAST,NOARP,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UNKNOWN mode DEFAULT group default qlen 500
        """
        
        interfaces = VPNConfigParser.detect_active_vpn_interfaces()
        assert "tun0" in interfaces
    
    @patch('platform.system')
    @patch('subprocess.run')
    def test_get_vpn_connection_details_darwin(self, mock_run, mock_system):
        """Test VPN connection details retrieval on macOS."""
        mock_system.return_value = "Darwin"
        mock_run.return_value.stdout = """
tun0: flags=8851<UP,POINTOPOINT,RUNNING,NOARP,MULTICAST> mtu 1380
    inet 10.0.0.1 netmask 0xffffff00 destination 10.0.0.2
        """
        
        details = VPNConfigParser.get_vpn_connection_details("tun0")
        assert details['interface'] == "tun0"
        assert details['ip_address'] == "10.0.0.1"
        assert details['subnet_mask'] == "255.255.255.0"
        assert details['protocol'] == "OpenVPN"
    
    @patch('platform.system')
    @patch('subprocess.run')
    def test_get_vpn_connection_details_linux(self, mock_run, mock_system):
        """Test VPN connection details retrieval on Linux."""
        mock_system.return_value = "Linux"
        mock_run.return_value.stdout = """
3: tun0: <POINTOPOINT,MULTICAST,NOARP,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UNKNOWN mode DEFAULT group default qlen 500
    link/none 
    inet 10.8.0.5/24 scope global tun0
       valid_lft forever preferred_lft forever
        """
        
        details = VPNConfigParser.get_vpn_connection_details("tun0")
        assert details['interface'] == "tun0"
        assert details['ip_address'] == "10.8.0.5"
        assert details['subnet_mask'] == "24"
        assert details['protocol'] == "OpenVPN"