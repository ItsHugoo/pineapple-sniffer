import unittest
from unittest.mock import patch
import sys
from src.vpn_detector import VPNConfigDetector

class TestVPNConfigDetector(unittest.TestCase):
    def setUp(self):
        # Reset platform-specific behavior
        self.original_platform = sys.platform

    def tearDown(self):
        # Restore original platform
        sys.platform = self.original_platform

    @patch('subprocess.run')
    def test_detect_vpn_interfaces_darwin(self, mock_run):
        # Simulate macOS interface detection
        sys.platform = 'darwin'
        mock_run.return_value.stdout = """
lo0: flags=8049<UP,LOOPBACK,RUNNING,MULTICAST> mtu 16384
en0: flags=8863<UP,BROADCAST,SMART,RUNNING,SIMPLEX,MULTICAST> mtu 1500
utun0: flags=8051<UP,POINTOPOINT,RUNNING,MULTICAST> mtu 1380
utun1: flags=8051<UP,POINTOPOINT,RUNNING,MULTICAST> mtu 1380
        """
        mock_run.return_value.returncode = 0

        interfaces = VPNConfigDetector.detect_vpn_interfaces()
        self.assertIn('utun0', interfaces)
        self.assertIn('utun1', interfaces)

    @patch('subprocess.run')
    def test_detect_vpn_interfaces_linux(self, mock_run):
        # Simulate Linux interface detection
        sys.platform = 'linux'
        mock_run.return_value.stdout = """
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN mode DEFAULT group default qlen 1000
2: eth0@if3: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP mode DEFAULT group default 
3: tun0@if4: <POINTOPOINT,MULTICAST,NOARP,UP,LOWER_UP> mtu 1500 qdisc noqueue state UNKNOWN mode DEFAULT group default 
        """
        mock_run.return_value.returncode = 0

        interfaces = VPNConfigDetector.detect_vpn_interfaces()
        self.assertIn('tun0', interfaces)

    @patch('subprocess.run')
    def test_get_routing_info_darwin(self, mock_run):
        # Simulate macOS routing info
        sys.platform = 'darwin'
        mock_run.return_value.stdout = """
Routing tables


Internet:
Destination        Gateway            Flags        Refs      Use   Netif Expire
default            192.168.1.1        UGScg          49        0     en0
192.168.1/24       link#5             UCS            0        0     en0
        """
        mock_run.return_value.returncode = 0

        routing_info = VPNConfigDetector.get_routing_info()
        self.assertEqual(routing_info.get('default'), 'en0')

    @patch('subprocess.run')
    def test_get_routing_info_linux(self, mock_run):
        # Simulate Linux routing info
        sys.platform = 'linux'
        mock_run.return_value.stdout = """
default via 192.168.1.1 dev eth0 proto static 
192.168.1.0/24 dev eth0 proto kernel scope link src 192.168.1.100 
        """
        mock_run.return_value.returncode = 0

        routing_info = VPNConfigDetector.get_routing_info()
        self.assertEqual(routing_info.get('default'), 'eth0')

    def test_unsupported_platform(self):
        # Test an unsupported platform returns empty lists/dicts
        sys.platform = 'unsupported_os'
        
        interfaces = VPNConfigDetector.detect_vpn_interfaces()
        self.assertEqual(interfaces, [])

        routing_info = VPNConfigDetector.get_routing_info()
        self.assertEqual(routing_info, {})

if __name__ == '__main__':
    unittest.main()