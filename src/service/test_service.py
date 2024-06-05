from src.repos.test_repos import *

def get_helloworld_service() -> str:
  if 'test' in list_tables_repos():
    test_setup_repos()
  return get_test_repos()