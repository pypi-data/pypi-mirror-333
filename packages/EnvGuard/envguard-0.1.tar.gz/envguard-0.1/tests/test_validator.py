import os
from envguard.validator import EnvValidator

def test_check_missing_vars(tmpdir):
    env_file = tmpdir.join('.env')
    env_file.write('EXISTING_VAR=value\n')

    validator = EnvValidator(env_file=str(env_file), required_vars=['EXISTING_VAR', 'MISSING_VAR'])
    missing = validator.check_missing_vars()

    assert 'MISSING_VAR' in missing
    assert len(missing) == 1

def test_validate(tmpdir):
    env_file = tmpdir.join('.env')
    env_file.write('EXISTING_VAR=value\n')

    validator = EnvValidator(env_file=str(env_file), required_vars=['EXISTING_VAR'])
    missing, is_valid = validator.validate()

    assert is_valid
    assert len(missing) == 0