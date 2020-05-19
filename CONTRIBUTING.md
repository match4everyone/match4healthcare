We are happy that you want to contribute to our project! To get you started, we have collected a few things you should know in order to add helpful issues, well-formatted pull requests and well-structured code from the beginning:

- Please use our issue and pull request templates. Github will automatically offer them to you. Our base-branch is `staging`.
- To ensure well-formatted code, we use pre-commit hooks in git. Since they cannot be checked into the git history, please run `pre-commit install` in the repo folder after installing the requirements from `requirements.txt`
- Our project is currently translated based on German and translated into English, please use `python3 manage.py makemessages --no-location` to generate missing translations and fill them out in `backend/locale/en/django.po`. If you are not fluent enough in one of them, state so and we will help you in the pull request.
- If you want to propose an idea or draft with code that is not ready to merge yet, please use the _Draft_ option Github provides. Draft PRs can also be helpful to you, since we can give early feedback while knowing that it is still a work-in-progress.

If you have any questions, feel free to reach out to the maintaining developers @maltezacharias, @bjrne, @Baschdl, @kevihiin, @feeds, and @josauder.
