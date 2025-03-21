MathJax for Django
==================

This package provides a copy of MathJax, a JavaScript library for
displaying mathematics on the web, packaged for use with the Django
web framework.

To use MathJax with Django:

1. Install this package.

2. Add `'mathjax'` to your list of `INSTALLED_APPS`.

3. Add a script tag to your page templates, such as:
```
<script src="{% static 'mathjax/es5/tex-mml-chtml.js' %}"></script>
```

For more information about MathJax, refer to https://www.mathjax.org/.

For more information about Django, refer to https://www.djangoproject.com/.
