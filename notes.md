

verbose name in tables.py


anfragen auf slack


PRs strategie


intro in production






So, django templates probably won't get any styling

https://github.com/prettier/prettier/issues/5944#issuecomment-549805364
https://github.com/prettier/prettier/issues/5581

crackered on:

>    this is actually quite challenging because the template language allows you to insert template tags into any location in the template file, and while people usually put them in reasonable places, there’s no guarantee. For example, someone could do a thing like `{{ less_than }}div class="foo">abc</div>` and that would be totally valid but a nightmare to parse.
>    That’s different from a more structured template-style language like JSX, where there are only a few valid places to embed JS expressions so it isn’t too challenging to make them all look good.

https://www.reddit.com/r/django/comments/fnzrxv/is_there_an_autoformatter_plugin_for_vs_code_that/



Regardless, we could also give this a try:
https://github.com/rory/django-template-i18n-lint





  - repo: https://github.com/thibaudcolas/curlylint
    rev: "" # select a tag / sha to point at
    hooks:
      - id: curlylint







        exclude: |
          (?x)(
              ^[0-9A-z/-_]*.html
          )





              ^backend/static/css/[0-9A-z/_\-\.]*[0-9]|
              ^backend/static/js/[0-9A-z/_\-\.]*[0-9]






              So, django templates probably won't get any styling

https://github.com/prettier/prettier/issues/5944#issuecomment-549805364
https://github.com/prettier/prettier/issues/5581

crackered on:

>    this is actually quite challenging because the template language allows you to insert template tags into any location in the template file, and while people usually put them in reasonable places, there’s no guarantee. For example, someone could do a thing like `{{ less_than }}div class="foo">abc</div>` and that would be totally valid but a nightmare to parse.
>    That’s different from a more structured template-style language like JSX, where there are only a few valid places to embed JS expressions so it isn’t too challenging to make them all look good.

https://www.reddit.com/r/django/comments/fnzrxv/is_there_an_autoformatter_plugin_for_vs_code_that/



Regardless, we could also give this a try:
https://github.com/rory/django-template-i18n-lint
