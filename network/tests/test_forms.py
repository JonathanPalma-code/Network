from django.test import SimpleTestCase
from network.forms import AddPostForm

class TestForm(SimpleTestCase):
    def test_add_post_form_valid_data(self):
        form = AddPostForm(data={
            'content': 'This is my first post',
        })

        self.assertTrue(form.is_valid())

    def test_add_post_form_no_data(self):
        form = AddPostForm(data={})

        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)
        