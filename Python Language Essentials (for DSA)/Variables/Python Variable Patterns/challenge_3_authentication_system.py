"""
SOLUTION: Challenge 3 - Authentication System
Difficulty: Advanced
Patterns Used: All 7 patterns combined!
"""

from datetime import datetime, timedelta

class AuthenticationSystem:
    def __init__(self):
        # Configuration (Pattern 4)
        self.config = {
            'max_login_attempts': 3,
            'session_timeout_minutes': 30,
            'lockout_duration_minutes': 15
        }
        
        # User database (simplified)
        self.users = {
            'user@email.com': {
                'password': 'SecurePass123',
                'username': 'john_doe',
                'phone': '+1234567890'
            },
            'admin@email.com': {
                'password': 'AdminPass456',
                'username': 'admin',
                'phone': '+0987654321'
            }
        }
        
        # State variables (Pattern 6)
        self.user_states = {}
        
        # Feature flags (Pattern 2)
        self.user_flags = {}
        
        # Dictionary dispatch for login methods (Pattern 3)
        self.login_methods = {
            'email': self._login_by_email,
            'username': self._login_by_username,
            'phone': self._login_by_phone
        }
    
    def _initialize_user_state(self, identifier):
        """Initialize state for new user"""
        if identifier not in self.user_states:
            self.user_states[identifier] = {
                'logged_in': False,
                'session_start': None,
                'failed_attempts': 0,
                'locked_until': None,
                'last_activity': None
            }
        
        if identifier not in self.user_flags:
            self.user_flags[identifier] = {
                '2fa_enabled': False,
                'password_reset_required': False,
                'account_locked': False
            }
    
    def _login_by_email(self, email, password):
        """Login using email"""
        if email in self.users:
            if self.users[email]['password'] == password:
                return email, True
        return email, False
    
    def _login_by_username(self, username, password):
        """Login using username"""
        for email, user_data in self.users.items():
            if user_data['username'] == username:
                if user_data['password'] == password:
                    return email, True
        return username, False
    
    def _login_by_phone(self, phone, password):
        """Login using phone"""
        for email, user_data in self.users.items():
            if user_data['phone'] == phone:
                if user_data['password'] == password:
                    return email, True
        return phone, False
    
    def login(self, method, identifier, password):
        """Main login function"""
        print(f"\n🔐 Login Attempt: {method} - {identifier}")
        
        # Validate method
        if method not in self.login_methods:
            print(f"❌ Invalid login method: {method}")
            return False
        
        # Initialize user
        self._initialize_user_state(identifier)
        
        state = self.user_states[identifier]
        flags = self.user_flags[identifier]
        
        # Check if locked
        if state['locked_until']:
            if datetime.now() < state['locked_until']:
                time_left = (state['locked_until'] - datetime.now()).seconds // 60
                print(f"🔒 Account locked. Try again in {time_left} minutes")
                return False
            else:
                # Unlock
                state['locked_until'] = None
                state['failed_attempts'] = 0
                flags['account_locked'] = False
        
        # Check password reset flag
        if flags['password_reset_required']:
            print("⚠️ Password reset required before login")
            return False
        
        # Attempt login
        user_id, success = self.login_methods[method](identifier, password)
        
        if success:
            # Success!
            state['logged_in'] = True
            state['session_start'] = datetime.now()
            state['last_activity'] = datetime.now()
            state['failed_attempts'] = 0
            
            print(f"✅ Login successful! Welcome back.")
            
            # 2FA check
            if flags['2fa_enabled']:
                print("📱 2FA code sent to your device")
            
            return True
        
        else:
            # Failed
            state['failed_attempts'] += 1
            attempts_left = self.config['max_login_attempts'] - state['failed_attempts']
            
            print(f"❌ Login failed. Attempts remaining: {attempts_left}")
            
            # Lock if max attempts reached
            if state['failed_attempts'] >= self.config['max_login_attempts']:
                lockout = timedelta(minutes=self.config['lockout_duration_minutes'])
                state['locked_until'] = datetime.now() + lockout
                flags['account_locked'] = True
                print(f"🔒 Account locked for {self.config['lockout_duration_minutes']} minutes")
            
            return False
    
    def check_session(self, identifier):
        """Validate active session"""
        if identifier not in self.user_states:
            print("❌ User not found")
            return False
        
        state = self.user_states[identifier]
        
        if not state['logged_in']:
            print("❌ Not logged in")
            return False
        
        # Check timeout
        if state['last_activity']:
            timeout = timedelta(minutes=self.config['session_timeout_minutes'])
            if datetime.now() - state['last_activity'] > timeout:
                state['logged_in'] = False
                print("⏰ Session expired. Please log in again.")
                return False
        
        # Update activity
        state['last_activity'] = datetime.now()
        print("✅ Session valid")
        return True
    
    def logout(self, identifier):
        """Logout user"""
        if identifier in self.user_states:
            self.user_states[identifier]['logged_in'] = False
            self.user_states[identifier]['session_start'] = None
            print("👋 Logged out successfully")
    
    def enable_2fa(self, identifier):
        """Enable 2FA"""
        if identifier in self.user_flags:
            self.user_flags[identifier]['2fa_enabled'] = True
            print("🔐 2FA enabled for account")
    
    def require_password_reset(self, identifier):
        """Flag for password reset"""
        if identifier in self.user_flags:
            self.user_flags[identifier]['password_reset_required'] = True
            print("⚠️ Password reset flagged for next login")
    
    def get_user_status(self, identifier):
        """Display user status"""
        if identifier not in self.user_states:
            print("User not found")
            return
        
        state = self.user_states[identifier]
        flags = self.user_flags[identifier]
        
        print(f"\n{'='*50}")
        print(f"👤 USER STATUS: {identifier}")
        print(f"{'='*50}")
        print(f"Logged In:            {state['logged_in']}")
        print(f"Failed Attempts:      {state['failed_attempts']}")
        print(f"Account Locked:       {flags['account_locked']}")
        print(f"2FA Enabled:          {flags['2fa_enabled']}")
        print(f"Password Reset Req:   {flags['password_reset_required']}")
        
        if state['last_activity']:
            print(f"Last Activity:        {state['last_activity'].strftime('%Y-%m-%d %H:%M:%S')}")
        
        print(f"{'='*50}")


# ============================================================================
# DEMO / TESTING
# ============================================================================

if __name__ == "__main__":
    print("🎯 CHALLENGE 3: AUTHENTICATION SYSTEM SOLUTION\n")
    
    auth = AuthenticationSystem()
    
    # Test 1: Successful login
    print("\n--- TEST 1: Successful Login ---")
    auth.login('email', 'user@email.com', 'SecurePass123')
    auth.check_session('user@email.com')
    
    # Test 2: Failed attempts leading to lockout
    print("\n--- TEST 2: Failed Login Attempts ---")
    auth.login('username', 'admin', 'wrongpass')
    auth.login('username', 'admin', 'wrongpass')
    auth.login('username', 'admin', 'wrongpass')
    auth.login('username', 'admin', 'wrongpass')  # Should be locked
    
    # Test 3: Enable 2FA
    print("\n--- TEST 3: Enable 2FA ---")
    auth.enable_2fa('user@email.com')
    auth.logout('user@email.com')
    auth.login('email', 'user@email.com', 'SecurePass123')
    
    # Test 4: Multiple login methods
    print("\n--- TEST 4: Multiple Login Methods ---")
    auth.login('username', 'john_doe', 'SecurePass123')
    auth.login('phone', '+1234567890', 'SecurePass123')
    
    # Test 5: Get status
    print("\n--- TEST 5: User Status ---")
    auth.get_user_status('user@email.com')
    auth.get_user_status('admin')