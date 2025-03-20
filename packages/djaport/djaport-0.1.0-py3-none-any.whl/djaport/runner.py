from django.test.runner import DiscoverRunner
import datetime
import os
import json
import traceback
import time
import unittest
from unittest.runner import TextTestResult

class DjaportTestResult(TextTestResult):
    """
    A custom test result class that keeps track of all tests that were run,
    including successful ones.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.successes = []  # Track successful tests
    
    def addSuccess(self, test):
        """Called when a test succeeds"""
        super().addSuccess(test)
        self.successes.append(test)

class CustomTestRunner(DiscoverRunner):
    """
    Custom test runner that extends Django's DiscoverRunner to generate
    ExtentReports-like HTML reports for test execution.
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.report_dir = os.path.join(os.getcwd(), 'target/reports')
        os.makedirs(self.report_dir, exist_ok=True)
        
        self.start_time = time.time()
        self.test_results = {
            'start_time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'tests': [],
            'summary': {
                'total': 0,
                'passed': 0,
                'failed': 0,
                'skipped': 0,
                'errors': 0
            },
            'environment': self._get_environment_info()
        }
    
    def get_resultclass(self):
        """Return the custom result class to use"""
        return DjaportTestResult
    
    def _get_environment_info(self):
        """Collect environment information for the report"""
        import platform
        import django
        
        return {
            'python_version': platform.python_version(),
            'platform': platform.platform(),
            'django_version': django.__version__,
            'timestamp': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    
    def run_suite(self, suite, **kwargs):
        """Run the test suite and process results"""
        # Run the test suite with our custom result class
        result = super().run_suite(suite, **kwargs)
        
        # Store the test suite in the result for later access
        result.test_suite = suite
        
        # Process the results
        self._process_test_results(result)
        
        # Generate the report
        self._generate_report()
        
        return result
    
    def _extract_assertion_html(self, error_msg):
        """Extract assertion details from error message and format as HTML"""
        if not error_msg:
            return None
            
        # Clean up the error message for HTML display
        error_msg = error_msg.replace('<', '&lt;').replace('>', '&gt;')
        
        # Print the full error message for debugging
        print("\nFull error message:")
        print(error_msg)
        
        # Extract the main parts of the assertion error
        assertion_html = []
        in_diff_section = False
        in_traceback = True  # Assume we start in traceback
        assertion_found = False
        
        lines = error_msg.split('\n')
        for i, line in enumerate(lines):
            line_stripped = line.strip()
            
            # Skip initial traceback lines until we find AssertionError
            if in_traceback:
                if 'AssertionError' in line:
                    in_traceback = False
                    assertion_found = True
                    
                    # Extract the assertion message
                    assertion_part = line.split('AssertionError:')[-1].strip()
                    if assertion_part:
                        assertion_html.append(f"<strong class='fail'>AssertionError:</strong> {assertion_part}")
                    else:
                        assertion_html.append(f"<strong class='fail'>AssertionError</strong>")
                        
                        # Look ahead for the assertion message on the next line
                        if i + 1 < len(lines) and lines[i + 1].strip() and not lines[i + 1].strip().startswith('File "'):
                            assertion_html.append(lines[i + 1].strip())
                continue
            
            # Process expected/actual lines
            if line_stripped.startswith('Expected:') or line_stripped.startswith('expected:'):
                assertion_html.append(f"<strong>Expected:</strong> {line.split(':')[-1].strip()}")
            elif line_stripped.startswith('Actual:') or line_stripped.startswith('actual:'):
                assertion_html.append(f"<strong>Actual:</strong> {line.split(':')[-1].strip()}")
            elif line_stripped.startswith('Got:') or line_stripped.startswith('got:'):
                assertion_html.append(f"<strong>Got:</strong> {line.split(':')[-1].strip()}")
            
            # Process diff lines
            elif line_stripped == '- expected' or line_stripped == '+ actual' or line_stripped == '? ^':
                in_diff_section = True
                assertion_html.append(f"<span style='color: {'#e74c3c' if '-' in line_stripped else '#27ae60'}'>{line_stripped}</span>")
            elif in_diff_section and (line_stripped.startswith('-') or line_stripped.startswith('+') or line_stripped.startswith('?')):
                assertion_html.append(f"<span style='color: {'#e74c3c' if line_stripped.startswith('-') else '#27ae60'}'>{line_stripped}</span>")
            
            # Process other relevant lines
            elif line_stripped and not line_stripped.startswith('Traceback') and not line_stripped.startswith('File "'):
                assertion_html.append(line_stripped)
        
        # If we didn't find an assertion error, try to extract any useful information
        if not assertion_found and 'AssertionError' in error_msg:
            # Find the line with AssertionError
            for line in lines:
                if 'AssertionError' in line:
                    assertion_part = line.split('AssertionError:')[-1].strip()
                    if assertion_part:
                        assertion_html.append(f"<strong class='fail'>AssertionError:</strong> {assertion_part}")
                    else:
                        assertion_html.append(f"<strong class='fail'>AssertionError</strong>")
                    break
        
        # If we still don't have any assertion details, include the whole error message
        if not assertion_html:
            assertion_html = [f"<pre>{error_msg}</pre>"]
                
        return "<br>".join(assertion_html) if assertion_html else None
    
    def _process_test_results(self, result):
        """Process test results and collect data for the report"""
        # Get all tests from the result
        all_tests = self._get_all_tests(result)
        print(f"\nFound {len(all_tests)} total tests in the test suite")
        
        # Create sets for tracking processed tests
        processed_test_ids = set()
        failed_test_ids = set()
        error_test_ids = set()
        skipped_test_ids = set()
        
        # Process failures
        for test_case, error_msg in result.failures:
            test_id = test_case.id()
            failed_test_ids.add(test_id)
            processed_test_ids.add(test_id)
            
            # Extract assertion details
            assertion_html = self._extract_assertion_html(error_msg)
            
            # Debug: Print the error message to see what's in it
            print(f"\nProcessing failure for {test_id}")
            print(f"Error message: {error_msg[:200]}...")  # Print first 200 chars
            
            self.test_results['tests'].append({
                'name': test_id,
                'class': test_case.__class__.__name__,
                'method': test_case._testMethodName,
                'status': 'FAIL',
                'duration': getattr(test_case, '_timer', 0),
                'error_message': error_msg,
                'assertion_html': assertion_html,
                'traceback': error_msg,
                'logs': getattr(test_case, '_test_logs', []),
                'metadata': getattr(test_case, '_test_metadata', {}).get(test_case._testMethodName, {})
            })
        
        # Process errors
        for test_case, error_msg in result.errors:
            test_id = test_case.id()
            error_test_ids.add(test_id)
            processed_test_ids.add(test_id)
            
            # Extract assertion details
            assertion_html = self._extract_assertion_html(error_msg)
            
            # Debug: Print the error message to see what's in it
            print(f"\nProcessing error for {test_id}")
            print(f"Error message: {error_msg[:200]}...")  # Print first 200 chars
            
            self.test_results['tests'].append({
                'name': test_id,
                'class': test_case.__class__.__name__,
                'method': test_case._testMethodName,
                'status': 'ERROR',
                'duration': getattr(test_case, '_timer', 0),
                'error_message': error_msg,
                'assertion_html': assertion_html,
                'traceback': error_msg,
                'logs': getattr(test_case, '_test_logs', []),
                'metadata': getattr(test_case, '_test_metadata', {}).get(test_case._testMethodName, {})
            })
        
        # Process skipped tests
        for test_case, reason in result.skipped:
            test_id = test_case.id()
            skipped_test_ids.add(test_id)
            processed_test_ids.add(test_id)
            
            print(f"\nProcessing skipped test for {test_id}")
            print(f"Skip reason: {reason}")
            
            self.test_results['tests'].append({
                'name': test_id,
                'class': test_case.__class__.__name__,
                'method': test_case._testMethodName,
                'status': 'SKIP',
                'duration': getattr(test_case, '_timer', 0),
                'skip_reason': reason,
                'logs': getattr(test_case, '_test_logs', []),
                'metadata': getattr(test_case, '_test_metadata', {}).get(test_case._testMethodName, {})
            })
        
        # Process successful tests
        if hasattr(result, 'successes'):
            for test_case in result.successes:
                test_id = test_case.id()
                
                if test_id not in processed_test_ids:
                    print(f"\nProcessing successful test for {test_id}")
                    
                    self.test_results['tests'].append({
                        'name': test_id,
                        'class': test_case.__class__.__name__,
                        'method': test_case._testMethodName,
                        'status': 'PASS',
                        'duration': getattr(test_case, '_timer', 0),
                        'logs': getattr(test_case, '_test_logs', []),
                        'metadata': getattr(test_case, '_test_metadata', {}).get(test_case._testMethodName, {}),
                        'success_message': 'Test passed successfully'
                    })
                    processed_test_ids.add(test_id)
        
        # Process any remaining tests
        for test_case in all_tests:
            test_id = test_case.id()
            
            if test_id not in processed_test_ids:
                print(f"\nProcessing remaining test for {test_id}")
                
                self.test_results['tests'].append({
                    'name': test_id,
                    'class': test_case.__class__.__name__,
                    'method': test_case._testMethodName,
                    'status': 'PASS',
                    'duration': getattr(test_case, '_timer', 0),
                    'logs': getattr(test_case, '_test_logs', []),
                    'metadata': getattr(test_case, '_test_metadata', {}).get(test_case._testMethodName, {}),
                    'success_message': 'Test passed successfully'
                })
        
        # Update summary counts
        self.test_results['summary']['total'] = len(self.test_results['tests'])
        self.test_results['summary']['failed'] = len(failed_test_ids)
        self.test_results['summary']['errors'] = len(error_test_ids)
        self.test_results['summary']['skipped'] = len(skipped_test_ids)
        self.test_results['summary']['passed'] = (
            self.test_results['summary']['total'] - 
            self.test_results['summary']['failed'] - 
            self.test_results['summary']['errors'] - 
            self.test_results['summary']['skipped']
        )
        
        # Debug: Print the number of tests in the report
        print(f"\nTotal tests in report: {self.test_results['summary']['total']}")
        print(f"Passed tests in report: {self.test_results['summary']['passed']}")
        print(f"Failed tests in report: {self.test_results['summary']['failed']}")
        print(f"Error tests in report: {self.test_results['summary']['errors']}")
        print(f"Skipped tests in report: {self.test_results['summary']['skipped']}")
        
        # Add end time and duration
        self.test_results['end_time'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.test_results['duration'] = time.time() - self.start_time
    
    def _collect_all_test_methods(self):
        """Collect all test methods from test classes in the project and instantiate test cases"""
        import unittest
        import inspect
        import sys
        
        all_test_cases = []
        
        # Create a copy of sys.modules to avoid "dictionary changed size during iteration" error
        modules = list(sys.modules.items())
        
        # Get all modules in the project
        for module_name, module in modules:
            if 'test' in module_name and not module_name.startswith('_'):
                try:
                    # Find all test classes in the module
                    for name, obj in inspect.getmembers(module):
                        try:
                            if (inspect.isclass(obj) and 
                                issubclass(obj, unittest.TestCase) and 
                                obj.__module__ == module.__name__):
                                
                                # Find all test methods in the class
                                for method_name in dir(obj):
                                    if method_name.startswith('test'):
                                        # Create a test case instance
                                        try:
                                            test_case = obj(method_name)
                                            all_test_cases.append(test_case)
                                        except Exception as e:
                                            print(f"Error creating test case for {obj.__name__}.{method_name}: {e}")
                        except (TypeError, AttributeError):
                            # Skip if there's an issue with this class
                            continue
                except (ImportError, AttributeError):
                    # Skip if there's an issue with this module
                    continue
        
        return all_test_cases
    
    def _get_all_tests(self, result):
        """Extract all test cases from the result and collect all test methods"""
        all_tests = []
        
        # Get tests from the result
        for test_case, _ in result.failures + result.errors + result.skipped:
            if test_case not in all_tests:
                all_tests.append(test_case)
        
        # Get successful tests if available
        if hasattr(result, 'successes'):
            for test_case in result.successes:
                if test_case not in all_tests:
                    all_tests.append(test_case)
        
        # Try to get all tests from the result
        if hasattr(result, 'test_suite'):
            self._extract_tests_from_suite(result.test_suite, all_tests)
        elif hasattr(result, '_tests'):
            self._extract_tests_from_suite(result._tests, all_tests)
            
        # If we still don't have enough tests, collect all test methods
        if len(all_tests) < result.testsRun:
            print(f"\nCollecting all test methods to find missing tests...")
            collected_tests = self._collect_all_test_methods()
            
            # Add only the tests that aren't already in all_tests
            for test_case in collected_tests:
                if test_case not in all_tests:
                    # Check if this test was actually run
                    test_id = test_case.id()
                    test_name = test_case._testMethodName
                    
                    # Add the test case
                    all_tests.append(test_case)
                    print(f"Added test case: {test_id}")
        
        # Debug: Print the number of tests found vs tests run
        print(f"\nFound {len(all_tests)} total tests (testsRun: {result.testsRun})")
        
        return all_tests
    
    def _extract_tests_from_suite(self, test_suite, all_tests):
        """Recursively extract all test cases from a test suite"""
        if hasattr(test_suite, 'countTestCases') and test_suite.countTestCases() == 0:
            return
            
        if isinstance(test_suite, list):
            for test in test_suite:
                self._extract_tests_from_suite(test, all_tests)
        elif hasattr(test_suite, '_tests'):  # TestSuite
            for subtest in test_suite._tests:
                self._extract_tests_from_suite(subtest, all_tests)
        elif hasattr(test_suite, '_testMethodName'):  # TestCase
            if test_suite not in all_tests:
                all_tests.append(test_suite)
        elif hasattr(test_suite, '__iter__'):  # Iterable test suite
            for test in test_suite:
                self._extract_tests_from_suite(test, all_tests)
    
    def _generate_report(self):
        """Generate JSON data file and HTML report"""
        # Generate JSON data file
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        json_path = os.path.join(self.report_dir, f'test_results.json')
        
        with open(json_path, 'w') as f:
            json.dump(self.test_results, f, indent=2)
        
        # Generate HTML report
        html_path = os.path.join(self.report_dir, f'test_report.html')
        self._generate_html_report(html_path)
        
        print(f"\nTest report generated at: {html_path}")
        print(f"Test data saved at: {json_path}")
    
    def _generate_html_report(self, output_path):
        """Generate HTML report using template"""
        # Read the template file directly instead of using Django's template system
        template_path = os.path.join(os.path.dirname(__file__), 'templates', 'report.html')
        
        if not os.path.exists(template_path):
            print(f"Template file not found at: {template_path}")
            return
        
        with open(template_path, 'r') as f:
            template_content = f.read()
        
        # Simple template variable replacement
        # Replace summary values
        template_content = template_content.replace('{{ results.start_time }}', self.test_results['start_time'])
        template_content = template_content.replace('{{ results.end_time }}', self.test_results['end_time'])
        template_content = template_content.replace('{{ results.duration|floatformat:2 }}', f"{self.test_results['duration']:.2f}")
        
        # Replace summary counts
        template_content = template_content.replace('{{ results.summary.total }}', str(self.test_results['summary']['total']))
        template_content = template_content.replace('{{ results.summary.passed }}', str(self.test_results['summary']['passed']))
        template_content = template_content.replace('{{ results.summary.failed }}', str(self.test_results['summary']['failed']))
        template_content = template_content.replace('{{ results.summary.skipped }}', str(self.test_results['summary']['skipped']))
        template_content = template_content.replace('{{ results.summary.errors }}', str(self.test_results['summary']['errors']))
        
        # Generate test items HTML
        test_items_html = ""
        
        # Debug: Print test statuses before generating HTML
        print("\nTest statuses before generating HTML:")
        for test in self.test_results['tests']:
            print(f"{test['name']}: {test['status']}")
        
        # Sort tests by status (PASS, FAIL, ERROR, SKIP)
        sorted_tests = sorted(self.test_results['tests'], 
                             key=lambda t: {'PASS': 0, 'FAIL': 1, 'ERROR': 2, 'SKIP': 3}.get(t['status'], 4))
        
        for i, test in enumerate(sorted_tests, 1):
            status_class = test['status'].lower()
            
            # Test header
            test_item = f"""
            <div class="test-item">
                <div class="test-header" onclick="toggleDetails('test-{i}')">
                    <div class="test-name">{test['class']}.{test['method']}</div>
                    <div class="test-status status-{status_class}">{test['status']}</div>
                </div>
                <div id="test-{i}" class="test-details">
                    <div><strong>Duration:</strong> {test.get('duration', 0):.2f}s</div>
            """
            
            # Metadata
            if test.get('metadata'):
                metadata = test['metadata']
                test_item += '<div class="metadata">'
                if metadata.get('category'):
                    test_item += f'<div class="metadata-item"><span class="metadata-key">Category:</span><span>{metadata["category"]}</span></div>'
                if metadata.get('author'):
                    test_item += f'<div class="metadata-item"><span class="metadata-key">Author:</span><span>{metadata["author"]}</span></div>'
                if metadata.get('description'):
                    test_item += f'<div class="metadata-item"><span class="metadata-key">Description:</span><span>{metadata["description"]}</span></div>'
                test_item += '</div>'
            
            # Assertion HTML
            if test.get('assertion_html'):
                test_item += f'<div><strong>Assertion Failed:</strong><div class="test-logs assertion-error">{test["assertion_html"]}</div></div>'
            
            # Success message
            if test.get('success_message') and test['status'] == 'PASS':
                test_item += f'<div><strong class="pass">Success:</strong><div class="test-logs success-message">{test["success_message"]}</div></div>'
            
            # Error message and traceback
            if test.get('error_message'):
                # Clean up the error message for HTML display
                error_msg = test['error_message'].replace('<', '&lt;').replace('>', '&gt;')
                
                # Add the full error message
                test_item += f'<div><strong>Error Details:</strong><div class="test-logs">{error_msg}</div></div>'
                
                # Add traceback if available
                if test.get('traceback'):
                    traceback_html = test['traceback'].replace('<', '&lt;').replace('>', '&gt;')
                    test_item += f'<div><strong>Traceback:</strong><div class="test-logs traceback">{traceback_html}</div></div>'
            
            # Skip reason
            if test.get('skip_reason'):
                test_item += f'<div><strong>Skip Reason:</strong> {test["skip_reason"]}</div>'
            
            # Logs
            if test.get('logs'):
                test_item += '<div><strong>Logs:</strong><div class="test-logs">'
                for log in test['logs']:
                    test_item += f'{log}<br>'
                test_item += '</div></div>'
            
            # Close test item
            test_item += '</div></div>'
            test_items_html += test_item
        
        # Replace test items placeholder
        test_items_start = template_content.find('{% for test in results.tests %}')
        test_items_end = template_content.find('{% endfor %}', test_items_start) + len('{% endfor %}')
        if test_items_start != -1 and test_items_end != -1:
            template_content = template_content[:test_items_start] + test_items_html + template_content[test_items_end:]
        
        # Environment info
        env_items_html = ""
        for key, value in self.test_results['environment'].items():
            env_items_html += f"""
            <div class="environment-item">
                <div class="environment-key">{key.title()}</div>
                <div class="environment-value">{value}</div>
            </div>
            """
        
        # Replace environment items placeholder
        env_items_start = template_content.find('{% for key, value in results.environment.items %}')
        env_items_end = template_content.find('{% endfor %}', env_items_start) + len('{% endfor %}')
        if env_items_start != -1 and env_items_end != -1:
            template_content = template_content[:env_items_start] + env_items_html + template_content[env_items_end:]
        
        # Chart data
        # Status chart data
        status_data = [
            self.test_results['summary']['passed'],
            self.test_results['summary']['failed'],
            self.test_results['summary']['skipped'],
            self.test_results['summary']['errors']
        ]
        template_content = template_content.replace(
            '{{ results.summary.passed }}, {{ results.summary.failed }}, {{ results.summary.skipped }}, {{ results.summary.errors }}',
            ', '.join(map(str, status_data))
        )
        
        # Duration chart data
        duration_labels = []
        duration_data = []
        duration_colors = []
        duration_borders = []
        
        for test in self.test_results['tests']:
            duration_labels.append(f"'{test['method']}'")
            duration_data.append(f"{test.get('duration', 0):.2f}")
            
            if test['status'] == 'PASS':
                duration_colors.append("'rgba(39, 174, 96, 0.2)'")
                duration_borders.append("'rgba(39, 174, 96, 1)'")
            elif test['status'] == 'FAIL':
                duration_colors.append("'rgba(231, 76, 60, 0.2)'")
                duration_borders.append("'rgba(231, 76, 60, 1)'")
            elif test['status'] == 'SKIP':
                duration_colors.append("'rgba(243, 156, 18, 0.2)'")
                duration_borders.append("'rgba(243, 156, 18, 1)'")
            elif test['status'] == 'ERROR':
                duration_colors.append("'rgba(192, 57, 43, 0.2)'")
                duration_borders.append("'rgba(192, 57, 43, 1)'")
        
        template_content = template_content.replace(
            "labels: [{% for test in results.tests %}'{{ test.method }}',{% endfor %}]",
            f"labels: [{', '.join(duration_labels)}]"
        )
        
        template_content = template_content.replace(
            "data: [{% for test in results.tests %}{{ test.duration|floatformat:2 }},{% endfor %}]",
            f"data: [{', '.join(duration_data)}]"
        )
        
        template_content = template_content.replace(
            "backgroundColor: [{% for test in results.tests %}{% if test.status == 'PASS' %}'rgba(39, 174, 96, 0.2)'{% endif %}{% if test.status == 'FAIL' %}'rgba(231, 76, 60, 0.2)'{% endif %}{% if test.status == 'SKIP' %}'rgba(243, 156, 18, 0.2)'{% endif %}{% if test.status == 'ERROR' %}'rgba(192, 57, 43, 0.2)'{% endif %},{% endfor %}]",
            f"backgroundColor: [{', '.join(duration_colors)}]"
        )
        
        template_content = template_content.replace(
            "borderColor: [{% for test in results.tests %}{% if test.status == 'PASS' %}'rgba(39, 174, 96, 1)'{% endif %}{% if test.status == 'FAIL' %}'rgba(231, 76, 60, 1)'{% endif %}{% if test.status == 'SKIP' %}'rgba(243, 156, 18, 1)'{% endif %}{% if test.status == 'ERROR' %}'rgba(192, 57, 43, 1)'{% endif %},{% endfor %}]",
            f"borderColor: [{', '.join(duration_borders)}]"
        )
        
        # Write to file
        with open(output_path, 'w') as f:
            f.write(template_content)
