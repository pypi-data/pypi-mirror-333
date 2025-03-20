import click
from .validator import EnvValidator

@click.command()
@click.option('--env-file', default='.env', help='Path to the .env file')
@click.option('--required', multiple=True, help='Required environment variables')
def validate_env(env_file, required):
    """
    Validate environment variables in the .env file.
    """
    validator = EnvValidator(env_file=env_file, required_vars=required)
    missing, is_valid = validator.validate()

    if is_valid:
        click.echo(click.style('All required environment variables are present!', fg='green'))
    else:
        click.echo(click.style('Missing or incorrect environment variables:', fg='red'))
        for var in missing:
            click.echo(click.style(f'- {var}', fg='yellow'))
        raise click.Abort()