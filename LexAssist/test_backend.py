"""
Integration tests for StartupLex Backend
Run with: python -m pytest test_backend.py
Or: python test_backend.py
"""

import unittest
import json
from app import app
from test_queries import TEST_QUERIES, get_test_query

class StartupLexBackendTests(unittest.TestCase):
    """Test cases for StartupLex Flask backend"""
    
    def setUp(self):
        """Set up test client"""
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
    
    def test_health_check(self):
        """Test health check endpoint"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'active')
        self.assertEqual(data['service'], 'StartupLex Backend')
    
    def test_query_missing_question(self):
        """Test query endpoint with missing question field"""
        response = self.client.post('/api/query',
            data=json.dumps({}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)
    
    def test_query_valid_format(self):
        """Test query endpoint with valid format (will fail if RAG API not running)"""
        test_data = {
            'question': 'What documents do I need to incorporate?',
            'context': ''
        }
        response = self.client.post('/api/query',
            data=json.dumps(test_data),
            content_type='application/json'
        )
        # Expect 502 if RAG API not running, 200 if it is
        self.assertIn(response.status_code, [200, 502])
        data = json.loads(response.data)
        self.assertIn('status', data)
    
    def test_documents_endpoint(self):
        """Test documents listing endpoint"""
        response = self.client.get('/api/documents')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)
    
    def test_document_by_id(self):
        """Test getting specific document"""
        response = self.client.get('/api/documents/1')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('id', data)
    
    def test_chat_endpoint(self):
        """Test chat endpoint"""
        chat_data = {
            'messages': [
                {'role': 'user', 'content': 'Hello'}
            ]
        }
        response = self.client.post('/api/chat',
            data=json.dumps(chat_data),
            content_type='application/json'
        )
        # Expect 502 if RAG API not running, 200 if it is
        self.assertIn(response.status_code, [200, 502])
        data = json.loads(response.data)
        self.assertIn('status', data)
    
    def test_404_error(self):
        """Test 404 error handling"""
        response = self.client.get('/nonexistent')
        self.assertEqual(response.status_code, 404)


class MockRAGTests(unittest.TestCase):
    """Tests using mock RAG responses"""
    
    def test_all_test_queries_have_responses(self):
        """Verify all test queries have sample responses"""
        for query in TEST_QUERIES:
            self.assertIn('sample_rag_response', query)
            self.assertTrue(len(query['sample_rag_response']) > 0)
    
    def test_query_retrieval(self):
        """Test retrieving test queries"""
        query = get_test_query(1)
        self.assertIsNotNone(query)
        self.assertEqual(query['id'], 1)
        self.assertIn('question', query)
        self.assertIn('category', query)
        self.assertIn('sample_rag_response', query)
    
    def test_test_queries_count(self):
        """Verify we have test queries"""
        self.assertGreater(len(TEST_QUERIES), 0)
        self.assertEqual(len(TEST_QUERIES), 10)


def run_mock_tests():
    """Run mock API tests without RAG API running"""
    print("\n" + "="*80)
    print("STARTUPLEX BACKEND - TEST QUERIES & SAMPLE RESPONSES")
    print("="*80)
    
    for query in TEST_QUERIES:
        print(f"\n[Query #{query['id']}] {query['question']}")
        print(f"Category: {query['category']}")
        print(f"\nExpected RAG Response:")
        print(f"{query['sample_rag_response']}")
        print("-" * 80)


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == 'mock':
        # Run mock test display
        run_mock_tests()
    else:
        # Run unit tests
        unittest.main()
