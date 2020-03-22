#!/bin/bash
for filename in *; do
	echo "    path('""$filename""', RedirectView.as_view(url=staticfiles_storage.url('img/""$filename""'))),"
done
