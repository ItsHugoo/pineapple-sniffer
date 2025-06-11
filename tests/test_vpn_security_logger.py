import os
import json
import pytest
import tempfile
from src.vpn_security_logger import VPNSecurityLogger

@pytest.fixture
def vpn_logger():
    """Create a VPN logger with a temporary log directory."""
    with tempfile.TemporaryDirectory() as temp_dir:
        logger = VPNSecurityLogger(log_dir=temp_dir)
        yield logger

def test_vpn_security_logger_initialization(vpn_logger):
    """Test VPN security logger initialization."""
    assert os.path.exists(vpn_logger.log_dir)
    assert isinstance(vpn_logger.security_log, object)

def test_log_vpn_connection(vpn_logger, caplog):
    """Test logging VPN connection details."""
    connection_details = {
        'protocol': 'OpenVPN',
        'server': 'us-west.example.com',
        'password': 'secret_password',
        'ip': '192.168.1.100'
    }
    
    vpn_logger.log_vpn_connection(connection_details)
    
    # Check if log contains sanitized details
    assert 'secret_password' not in caplog.text
    assert '********' in caplog.text
    assert 'us-west.example.com' in caplog.text

def test_sanitize_connection_details(vpn_logger):
    """Test sanitization of connection details."""
    details = {
        'username': 'test_user',
        'password': 'super_secret',
        'server': 'vpn.example.com'
    }
    
    sanitized = vpn_logger._sanitize_connection_details(details)
    
    assert sanitized['username'] == 'test_user'
    assert sanitized['password'] == '********'
    assert sanitized['server'] == 'vpn.example.com'

def test_generate_security_report(vpn_logger):
    """Test generating a security report."""
    report = vpn_logger.generate_security_report()
    
    assert report is not None
    assert 'timestamp' in report
    assert 'log_directory' in report
    assert 'log_files' in report

def test_log_directory_creation(tmpdir):
    """Test log directory creation."""
    custom_log_dir = os.path.join(tmpdir, 'custom_logs')
    logger = VPNSecurityLogger(log_dir=custom_log_dir)
    
    assert os.path.exists(custom_log_dir)
    assert os.path.isdir(custom_log_dir)