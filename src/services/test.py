from src.repositories.test import *

def get_helloworld_service() -> str:
  if 'test' in list_tables():
    test_setup()
  return get_test()