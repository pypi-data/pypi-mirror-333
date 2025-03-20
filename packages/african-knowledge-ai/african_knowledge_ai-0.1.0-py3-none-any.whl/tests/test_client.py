import unittest
from african_knowledge_ai.client import AfricanKnowledgeAIClient

class TestAfricanKnowledgeAIClient(unittest.TestCase):
    def setUp(self):
        self.client = AfricanKnowledgeAIClient(api_key="test_key")

    def test_init(self):
        self.assertEqual(self.client.api_key, "test_key")

if __name__ == "__main__":
    unittest.main()
