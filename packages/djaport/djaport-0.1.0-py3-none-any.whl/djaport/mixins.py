import time
import functools

class DjaportTestMixin:
    """
    Mixin to add Djaort capabilities to test cases.
    
    This mixin adds:
    - Test timing
    - Logging functionality
    - Request/response logging
    
    Usage:
    class MyTestCase(DjaportTestMixin, TestCase):
        def test_something(self):
            self.log("Starting test")
            # Test code
            self.log("Test completed")
    """
    
    def setUp(self):
        """Initialize test logs and timer"""
        self._test_logs = []
        self._timer_start = time.time()
        super().setUp()
        self.log("Test setup completed")
    
    def tearDown(self):
        """Record test duration"""
        self._timer = time.time() - self._timer_start
        self.log("Test teardown completed")
        super().tearDown()
    
    def log_success(self, message="Test passed successfully"):
        """Log a success message"""
        self.log(f"SUCCESS: {message}")
    
    def log(self, message):
        """Add a log message to the test report"""
        if not hasattr(self, '_test_logs'):
            self._test_logs = []
        self._test_logs.append(message)
    
    def log_request(self, method, url, data=None, headers=None, response=None):
        """
        Log an API request and response.
        
        Args:
            method: HTTP method (GET, POST, etc.)
            url: Request URL
            data: Request data/payload
            headers: Request headers
            response: Response object
        """
        log_message = f"REQUEST: {method} {url}\n"
        
        if headers:
            log_message += "Headers:\n"
            for key, value in headers.items():
                log_message += f"  {key}: {value}\n"
        
        if data:
            log_message += f"Data: {data}\n"
        
        if response:
            log_message += f"RESPONSE: Status {response.status_code}\n"
            try:
                log_message += f"Response Data: {response.json()}\n"
            except:
                log_message += f"Response Content: {response.content}\n"
        
        self.log(log_message)


def djaport_test(category=None, author=None, description=None):
    """
    Decorator to add metadata to test methods.
    
    Args:
        category: Test category (e.g., 'Authentication', 'API')
        author: Test author
        description: Test description
        
    Usage:
    @djaport_test(category='Authentication', author='DevTeam', 
                description='Verify login with valid credentials')
    def test_login_valid(self):
        # Test code
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            # Add metadata to the test instance
            if not hasattr(self, '_test_metadata'):
                self._test_metadata = {}
            
            self._test_metadata[func.__name__] = {
                'category': category,
                'author': author,
                'description': description
            }
            
            return func(self, *args, **kwargs)
        return wrapper
    return decorator
