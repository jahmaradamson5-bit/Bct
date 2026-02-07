import requests
import json
import time
import asyncio
import websockets
import sys
from datetime import datetime

class TradingBotAPITester:
    def __init__(self, base_url="https://btc-signal-engine-1.preview.emergentagent.com"):
        self.base_url = base_url
        self.api = f"{base_url}/api"
        self.tests_run = 0
        self.tests_passed = 0
        self.created_wallet_id = None
        
    def run_test(self, name, method, endpoint, expected_status, data=None, headers=None):
        """Run a single API test"""
        url = f"{self.api}/{endpoint}"
        default_headers = {'Content-Type': 'application/json'}
        if headers:
            default_headers.update(headers)
            
        self.tests_run += 1
        print(f"\n🔍 Testing {name}...")
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=default_headers, timeout=10)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=default_headers, timeout=15)
            elif method == 'DELETE':
                response = requests.delete(url, headers=default_headers, timeout=10)
            
            success = response.status_code == expected_status
            if success:
                self.tests_passed += 1
                print(f"✅ PASSED - Status: {response.status_code}")
                if response.content:
                    try:
                        result = response.json()
                        print(f"   Response preview: {str(result)[:200]}...")
                        return True, result
                    except:
                        return True, {}
            else:
                print(f"❌ FAILED - Expected {expected_status}, got {response.status_code}")
                if response.content:
                    try:
                        error_detail = response.json()
                        print(f"   Error: {error_detail}")
                    except:
                        print(f"   Raw response: {response.text[:200]}...")
                return False, {}
                
        except Exception as e:
            print(f"❌ FAILED - Error: {str(e)}")
            return False, {}

    def test_health_check(self):
        """Test health endpoint"""
        success, response = self.run_test("Health Check", "GET", "", 200)
        return success
    
    def test_api_health(self):
        """Test API health endpoint"""
        success, response = self.run_test("API Health Check", "GET", "health", 200)
        if success:
            print(f"   Services initialized: {response.get('services_initialized', 'Unknown')}")
            print(f"   Binance connected: {response.get('binance_connected', 'Unknown')}")
        return success
    
    def test_current_prices(self):
        """Test current prices endpoint"""
        success, response = self.run_test("Current Prices", "GET", "prices/current", 200)
        if success:
            print(f"   Binance Price: ${response.get('binance_price', 'N/A')}")
            print(f"   Polymarket Price: {response.get('polymarket_price', 'N/A')}")
            print(f"   Price Delta: {response.get('price_delta', 'N/A')}")
        return success
    
    def test_add_wallet(self):
        """Test adding a wallet"""
        wallet_data = {
            "address": "0x123456789abcdef0123456789abcdef012345678",
            "label": "Test Wallet #1"
        }
        success, response = self.run_test("Add Wallet", "POST", "wallets", 200, wallet_data)
        if success and 'id' in response:
            self.created_wallet_id = response['id']
            print(f"   Created wallet ID: {self.created_wallet_id}")
        return success
    
    def test_get_wallets(self):
        """Test getting wallets list"""
        success, response = self.run_test("Get Wallets", "GET", "wallets", 200)
        if success:
            print(f"   Found {len(response)} wallets")
        return success
    
    def test_generate_signal(self):
        """Test generating AI signal (may take longer due to GPT-5.2)"""
        print(f"🧠 Testing AI Signal Generation (GPT-5.2) - This may take 10-15 seconds...")
        success, response = self.run_test("Generate Signal", "POST", "signals/generate", 200)
        if success:
            print(f"   Signal Type: {response.get('signal_type', 'N/A')}")
            print(f"   Confidence: {response.get('confidence', 'N/A')}")
            print(f"   Reason: {response.get('reason', 'N/A')[:100]}...")
        return success
    
    def test_get_signals(self):
        """Test getting signals list"""
        success, response = self.run_test("Get Signals", "GET", "signals", 200)
        if success:
            print(f"   Found {len(response)} signals")
        return success
    
    def test_wallet_positions(self):
        """Test wallet positions (uses mock data)"""
        if not self.created_wallet_id:
            print("⚠️  Skipping wallet positions test - no wallet created")
            return False
            
        address = "0x123456789abcdef0123456789abcdef012345678"
        success, response = self.run_test("Wallet Positions", "GET", f"wallets/{address}/positions", 200)
        if success:
            print(f"   Total Value: ${response.get('total_value', 'N/A')}")
            print(f"   Total PNL: {response.get('total_pnl', 'N/A')}")
        return success
    
    def test_wallet_activity(self):
        """Test wallet activity (uses mock data)"""
        if not self.created_wallet_id:
            print("⚠️  Skipping wallet activity test - no wallet created")
            return False
            
        address = "0x123456789abcdef0123456789abcdef012345678"
        success, response = self.run_test("Wallet Activity", "GET", f"wallets/{address}/activity", 200)
        if success:
            print(f"   Found {len(response)} activity records")
        return success
    
    def test_delete_wallet(self):
        """Test deleting a wallet"""
        if not self.created_wallet_id:
            print("⚠️  Skipping wallet deletion test - no wallet to delete")
            return False
            
        success, response = self.run_test("Delete Wallet", "DELETE", f"wallets/{self.created_wallet_id}", 200)
        return success
    
    async def test_socket_connection(self):
        """Test Socket.IO connectivity"""
        print(f"\n🔌 Testing Socket.IO Connection...")
        socket_url = f"{self.base_url.replace('https://', 'wss://').replace('http://', 'ws://')}/api/socket.io/?transport=websocket"
        
        try:
            # Simple websocket connection test
            async with websockets.connect(socket_url, timeout=10) as websocket:
                print("✅ Socket.IO connection established")
                return True
        except Exception as e:
            print(f"❌ Socket.IO connection failed: {e}")
            return False

def main():
    print("🚀 Starting Polymarket Trading Bot API Tests")
    print("=" * 60)
    
    tester = TradingBotAPITester()
    
    # Run synchronous tests
    tests = [
        ("Basic Health Check", tester.test_health_check),
        ("API Health Status", tester.test_api_health),
        ("Current Prices", tester.test_current_prices),
        ("Add Wallet", tester.test_add_wallet),
        ("Get Wallets", tester.test_get_wallets),
        ("Generate AI Signal", tester.test_generate_signal),
        ("Get Signals", tester.test_get_signals),
        ("Wallet Positions", tester.test_wallet_positions),
        ("Wallet Activity", tester.test_wallet_activity),
        ("Delete Wallet", tester.test_delete_wallet),
    ]
    
    for test_name, test_func in tests:
        try:
            test_func()
        except Exception as e:
            print(f"❌ CRITICAL ERROR in {test_name}: {e}")
    
    # Test Socket.IO connection
    try:
        asyncio.run(tester.test_socket_connection())
    except Exception as e:
        print(f"❌ Socket.IO test error: {e}")
    
    # Print final results
    print("\n" + "=" * 60)
    print(f"📊 FINAL RESULTS")
    print(f"Tests Run: {tester.tests_run}")
    print(f"Tests Passed: {tester.tests_passed}")
    print(f"Success Rate: {(tester.tests_passed/tester.tests_run)*100:.1f}%" if tester.tests_run > 0 else "0%")
    
    if tester.tests_passed == tester.tests_run:
        print("🎉 ALL TESTS PASSED!")
        return 0
    else:
        print(f"⚠️  {tester.tests_run - tester.tests_passed} tests failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())