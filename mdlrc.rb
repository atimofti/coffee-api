################################################################################
# Style file for markdownlint.
#
# https://github.com/markdownlint/markdownlint/blob/master/docs/configuration.md
#
# This file is referenced by the file `.mdlrc`.
#
# Example taken from:
# https://github.com/jumanjihouse/pre-commit-hooks/blob/master/ci/jumanjistyle.rb
################################################################################

#===============================================================================
# Start with all built-in rules.
# https://github.com/markdownlint/markdownlint/blob/master/docs/RULES.md
all

#===============================================================================
# Override default parameters for some built-in rules.
# https://github.com/markdownlint/markdownlint/blob/master/docs/creating_styles.md#parameters

# Ignore line length in tables.
rule 'MD013', tables: false

# Ignore inline HTML rule
exclude_rule 'MD033'
