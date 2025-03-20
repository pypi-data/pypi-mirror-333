import app.modules as modules
from app.helpers import load_module_from_string

SCHEMA_NAME = 'TestSchema'

CODE = '''\
from d42 import schema
TestSchema = schema.list(schema.int)
'''

CODE_PYI = '''\
from typing import List
from d42.declaration.types import IntSchema

class TestSchema:
    type = List[IntSchema.type]\
'''

FAKE_PYI = '''\
from typing import overload
from typing import List
from test.module import TestSchema
from typing import Type

@overload
def fake(schema: Type[TestSchema]) -> List[int]:
    pass\
'''


def test_list_of_int_pyi():
    module = load_module_from_string('test_scalar', CODE)
    schema_description = getattr(module, SCHEMA_NAME)

    typed_module = modules.TypedSchemaModule('file_name')
    typed_module.generate(SCHEMA_NAME, schema_description)

    assert typed_module.get_printable_content() == CODE_PYI


def test_list_of_int_pyi_blahblah():
    module = load_module_from_string('test_scalar', CODE)
    schema_description = getattr(module, SCHEMA_NAME)

    blahblah_module = modules.FakeModule()
    blahblah_module.generate('test.module', SCHEMA_NAME, schema_description)

    assert blahblah_module.get_printable_content() == FAKE_PYI
