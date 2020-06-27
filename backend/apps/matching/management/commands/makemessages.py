import fileinput
import re

from django.core.management.commands.makemessages import Command as MakeMessageCommand


class Command(MakeMessageCommand):

    help = (  # noqa
        MakeMessageCommand.help
        + "Modified behaviour: Will reset creation date in all po files to 1900-01-01 00:00+0000"
        "to prevent diffs from being created when the only change would be a rerun of makemessages"
    )

    def build_potfiles(self):
        potfiles = super().build_potfiles()
        print("Using constant POT-Creation-Date: 1900-01-01 00:00+0000")
        pattern = re.compile(r"POT-Creation-Date: .*\\n")
        for line in fileinput.input(files=potfiles, inplace=True):
            line = pattern.sub(r"POT-Creation-Date: 1900-01-01 00:00+0000\\n", line)
            print(line, end="")

        return potfiles
