import re

path = 'src/models.py'

# Read the file content.
with open(path, 'r', encoding='utf-8') as file:
    lines = file.readlines()

# Add the extra import (after `from __future__` to avoid errors).
lines.insert(5, 'from pydantic import RootModel, ConfigDict, WithJsonSchema\n')
content = ''.join(lines)

# Perform string replacements.
content = content.replace('__root__', 'RootModel').replace('ResponseModel', 'Response')

# Replace
# ```
#    class Config:
#        extra = Extra.forbid
# ```
# with 
# `model_config = ConfigDict(extra='forbid')`
# to avoid warnings when running pytest.
content = content.replace('class Config:', "model_config = ConfigDict(extra='forbid')")\
    .replace('    extra = Extra.forbid', '')

# Fix datetime fields that cause JSON schema validation errors.
# The QuantConnect API returns dates in a format that doesn't match the strict
# ISO 8601 "date-time" format, causing jsonschema validation to fail.
# We replace datetime usages with DateTimeStr (a custom type that uses 
# WithJsonSchema to override the schema to just "type": "string").

# Replace datetime usages with DateTimeStr BEFORE adding the type alias,
# so the alias definition itself isn't affected.
# Replace Optional[datetime] with Optional[DateTimeStr]
content = re.sub(r'Optional\[datetime\]', 'Optional[DateTimeStr]', content)

# Replace non-optional datetime usages in Annotated (e.g., Annotated[datetime, Field(...)])
content = re.sub(r'Annotated\[datetime,', 'Annotated[DateTimeStr,', content)

# Now add the DateTimeStr type alias after the imports.
datetime_type_alias = '''
# Custom datetime type that doesn't enforce ISO 8601 format in JSON schema validation.
# This allows the API response dates (which may not be strict ISO 8601) to pass validation.
DateTimeStr = Annotated[datetime, WithJsonSchema({"type": "string"})]

'''

import_end_marker = 'from pydantic import BaseModel, Field'
content = content.replace(
    import_end_marker, 
    import_end_marker + '\n' + datetime_type_alias
)

# Fix parameterSet/parameters fields that can be empty lists.
# The API returns [] when there are no parameters, but the schema expects a dict.
# Add List to the union type to accept empty lists.
content = content.replace(
    'Optional[Union[ParameterSet1, Dict[str, Union[str, float, int]]]]',
    'Optional[Union[ParameterSet1, Dict[str, Union[str, float, int]], List]]'
)

# Save the new file content.
with open(path, 'w', encoding='utf-8') as file:
    file.write(content)
