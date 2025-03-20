# vto_frontend
This is a custom reusable Django frontend app.

It includes admin override templates (e.g., to display the project name and current environment in a header in the admin interface), a minimal login page template, a custom template tag to render Markdown partials, custom context processors to convey settings variables to templates, and middleware to activate user time zones in templates.

## Disclaimer
This is just a personal test app, it is not intended for use by anyone else.

## Required By
- https://pypi.org/project/djinntoux/

## Requires
- [Markdown](https://pypi.org/project/Markdown/) (may switch to [commonmark](https://pypi.org/project/commonmark/) or [markdown2](https://pypi.org/project/markdown2/))