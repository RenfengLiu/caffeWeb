#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    

#     app_root = os.path.dirname(__file__) 
#     sys.path.insert(0, os.path.join(app_root, 'GlucoGuide')) 
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "foodRec.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
