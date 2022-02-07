# this script takes submission and country as input (from make) and
# runs the appropriate script to extract the submission data

import sys
if len(sys.argv) > 2:
    raise TypeError('Too many arguments given. '
                    'Need exactly two arguments (country, submission)')
elif len(sys.argv) < 2:
    raise TypeError('Too few arguments given. '
                    'Need exactly two arguments (country, submission)')

country = sys.argv[0]
submission = sys.argv[1]


