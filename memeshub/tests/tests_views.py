"""
    from django.test import TestCase,Client
    from django.urls import reverse
    from memeshub.models import Image
    import json
    
    class TestView(TestCase):
    
        def setUp(self):
            self.client = Client()
            self.homepage_url = reverse('homepage')
    
        def test_index_GET(self):
            response = self.client.get(self.homepage_url)
    
            self.assertEquals(response.status_code, 200)
            self.assertTemplateUsed(response, 'index.html')
"""

