"""
    from django.test import TestCase
    from django.test import SimpleTestCase
    from django.urls import reverse,resolve
    from memeshub.views import index,signIn,signup,signOut,check,upload,about,blogs,privacy
    
    class TestUrls(SimpleTestCase):
    
        def test_homepage_url_is_resolved(self):
            url = reverse('homepage')
            print(resolve(url))
            self.assertEquals(resolve(url).func, index)
    
        def test_signIn_url_is_resolved(self):
            url = reverse('signIn')
            print(resolve(url))
            self.assertEquals(resolve(url).func, signIn)
    
        def test_signup_url_is_resolved(self):
            url = reverse('signup')
            print(resolve(url))
            self.assertEquals(resolve(url).func, signup)
    
        def test_signOut_url_is_resolved(self):
            url = reverse('signOut')
            print(resolve(url))
            self.assertEquals(resolve(url).func, signOut)
    
        def test_check_url_is_resolved(self):
            url = reverse('check_email')
            print(resolve(url))
            self.assertEquals(resolve(url).func, check)
    
        def test_upload_url_is_resolved(self):
            url = reverse('upload')
            print(resolve(url))
            self.assertEquals(resolve(url).func, upload)
    
        def test_about_url_is_resolved(self):
            url = reverse('about')
            print(resolve(url))
            self.assertEquals(resolve(url).func, about)
    
        def test_blogs_url_is_resolved(self):
            url = reverse('blogs')
            print(resolve(url))
            self.assertEquals(resolve(url).func, blogs)
    
        def test_privacy_url_is_resolved(self):
            url = reverse('privacy')
            print(resolve(url))
            self.assertEquals(resolve(url).func, privacy)
"""

