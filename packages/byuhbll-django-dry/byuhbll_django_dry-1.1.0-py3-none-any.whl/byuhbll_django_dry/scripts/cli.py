"""
Django Dry CLI

Usage:
    # Database utilities (requires psycopg2)
    byuhbll-django-dry db create
    byuhbll-django-dry db delete --yes

To see all available commands:
    byuhbll-django-dry <command> --help
"""

from dataclasses import dataclass
from os import environ

import byuhbll_configuro as configuro
import click


@dataclass
class DBConfig:
    host: str
    user: str
    password: str
    name: str


def get_database_config() -> DBConfig:
    """Get the database configuration from a config file."""
    config_filename = environ.get('DJANGO_CONFIG', 'application.yml')
    print(f'using config file: {config_filename}')
    config = configuro.load(config_filename=config_filename)
    default_db = config.get('django/databases/default')

    return DBConfig(
        default_db.get('HOST'),
        default_db.get('USER'),
        default_db.get('PASSWORD'),
        default_db.get('NAME'),
    )


def execute_pg_command(
    sql: str, config: DBConfig, top_level: bool = True, auto_commit: bool = True
) -> bool:
    """
    Execute a PostgreSQL command. Requires psycopg2 or psycopg.

    Arguments:
        sql (str): The SQL command to execute.
        config (DBConfig): The database configuration (host, user, password, name).
        top_level (bool): Execute on top-level database (postgres). Defaults to True.
        auto_commit (bool): Execute without transaction block. Defaults to True.

    Returns:
        bool: Whether or not the command was successful.
    """
    try:
        import psycopg as pg
    except ImportError:
        import psycopg2 as pg

    db_name = 'postgres' if top_level else config.name

    conn = pg.connect(
        f"host='{config.host}' user='{config.user}' "
        f"password='{config.password}' dbname='{db_name}'"
    )
    if auto_commit:
        if hasattr(pg, 'extensions'):  # psycopg2
            conn.set_isolation_level(pg.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
        else:  # psycopg
            conn.autocommit = True

    cursor = conn.cursor()
    try:
        cursor.execute(sql)
    except pg.Error as e:
        click.echo(click.style(f'Error: {e}', fg='red'), err=True)
        return False
    finally:
        conn.close()

    return True


@click.group()
def cli():
    """byuhbll-django-dry CLI - A collection of utilities for django projects."""


@click.group()
def db():
    """Database management utilities."""


@db.command()
def create():
    """Create the database."""
    db_config = get_database_config()
    success = execute_pg_command(f'CREATE DATABASE "{db_config.name}"', db_config)
    if success:
        click.echo(
            click.style(
                f'Database "{db_config.name}" created successfully.', fg='green'
            )
        )


@db.command()
@click.option(
    '-y',
    '--yes',
    is_flag=True,
    help='Skip confirmation and drop the database immediately.',
)
def delete(yes):
    """Delete the database with confirmation."""
    db_config = get_database_config()

    if not yes:
        confirmation = click.confirm(
            f'Are you sure you want to delete the database "{db_config.name}"?'
        )
        if not confirmation:
            click.echo('Aborted. No changes made.', err=True)
            return

    success = execute_pg_command(
        f'DROP DATABASE IF EXISTS "{db_config.name}"', db_config
    )
    if success:
        click.echo(
            click.style(f'Database "{db_config.name}" dropped successfully.', fg='red')
        )


# Attach sub groups to the main CLI
cli.add_command(db)

if __name__ == '__main__':
    cli()
