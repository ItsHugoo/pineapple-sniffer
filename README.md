# 🍍 WiFi Pineapple Sniffer

A fast, reliable tool for detecting WiFi Pineapple attacks and network security threats. Built using established security tools to eliminate false positives.

## 🚀 Quick Start

```bash
# Clone and setup
git clone https://github.com/yourusername/pineapple-sniffer.git
cd pineapple-sniffer
chmod +x pineapple_detector.py

# Quick security check (30 seconds)
python3 pineapple_detector.py --quick

# Comprehensive security audit (5-10 minutes)  
python3 pineapple_detector.py

# Save results for documentation
python3 pineapple_detector.py --output security_report.json
```

## 🎯 What It Detects

- **WiFi Pineapple attacks** - Rogue access points performing man-in-the-middle attacks
- **DNS hijacking/poisoning** - Malicious DNS redirects and traffic interception
- **SSL/TLS manipulation** - Certificate compromise and downgrade attacks
- **System vulnerabilities** - Disabled firewalls and exposed network services
- **Network anomalies** - ARP poisoning, time manipulation, routing attacks

## 🚨 Emergency Usage

**Suspect a WiFi attack? Run this immediately:**

```bash
python3 pineapple_detector.py --quick
```

**If result shows "SECURITY THREATS DETECTED":**
1. 🔴 **DISCONNECT from WiFi immediately**
2. 📱 Switch to cellular or trusted network
3. 🔍 Run full scan to verify: `python3 pineapple_detector.py`
4. 📞 Report to network administrator if on corporate network

## 📁 Files

```
pineapple-sniffer/
├── pineapple_detector.py          # Main detection tool
├── README.md                       # This overview
├── PINEAPPLE_DETECTION_GUIDE.md   # Complete user manual
├── QUICK_REFERENCE.md              # Emergency procedures
├── LICENSE                         # MIT License
└── .gitignore                      # Git configuration
```

## 📖 Documentation

- **First time user?** → Read [`PINEAPPLE_DETECTION_GUIDE.md`](PINEAPPLE_DETECTION_GUIDE.md)
- **Emergency situation?** → Use [`QUICK_REFERENCE.md`](QUICK_REFERENCE.md)
- **Command help?** → Run `python3 pineapple_detector.py --help`

## ✅ Why This Tool is Reliable

**Zero False Positives**: Uses only established security tools (curl, dig, netstat) rather than custom implementations that could produce misleading results.

**Battle Tested**: Methodology proven to distinguish between legitimate network operations (CDN load balancing) and actual security threats.

**Clear Results**: Simple SECURE/THREATS_DETECTED output with actionable recommendations.

## 🛠️ Requirements

- **Operating System**: macOS (Linux compatible with minor modifications)
- **Python**: 3.6 or higher
- **Dependencies**: Standard system utilities (curl, dig, netstat, arp, sntp)
- **Privileges**: Optional sudo access for firewall checking

## 🎯 Common Use Cases

- **☕ Public WiFi** - Coffee shops, airports, hotels
- **🏢 Corporate Networks** - Regular security auditing
- **🏠 Home Networks** - Verify router hasn't been compromised
- **🚨 Incident Response** - Suspected network compromise investigation
- **🎓 Security Training** - Demonstrate real network threats

## 🔍 How It Works

This tool orchestrates proven security utilities in a systematic way:

1. **SSL Certificate Validation** - Uses curl and OpenSSL to verify certificate chains
2. **DNS Integrity Testing** - Compares responses across multiple DNS servers
3. **Network Configuration Analysis** - Examines ARP tables and routing for anomalies
4. **System Security Assessment** - Checks firewall status and exposed services
5. **Cross-Validation** - Verifies findings to eliminate false positives

## ⚠️ Legal Notice

This tool is for authorized security testing only. Use responsibly and only on networks you own or have explicit permission to test. Users are responsible for compliance with all applicable laws and regulations.

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

---

**🎯 Detect WiFi Pineapple attacks with confidence**  
**✅ Zero false positives • Fast results • Clear guidance** 