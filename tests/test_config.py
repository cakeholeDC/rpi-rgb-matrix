import configparser
from pathlib import Path

GIT_ROOT = Path(__file__).resolve().parent.parent

def test_git_root():
  assert "/tests" not in str(GIT_ROOT)

def test_read_config():
  config = configparser.ConfigParser()
  parsed_configs = config.read(f'{ GIT_ROOT / "config.ini" }')
  
  assert '/config.ini' in parsed_configs[0]
  assert config["Spotify"]["client_id"]
  assert type(config.getint('Matrix', 'brightness', fallback=64)) == int
  assert type(config.get('Matrix', 'brightness', fallback=64)) == str
