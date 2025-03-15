import click
import httpx
from datetime import datetime, timedelta, timezone


@click.command()
@click.option("-a", "--api-url", default="http://127.0.0.1:8000", help="API-URL")
@click.option("-u", "--username", required=True)
@click.option("-p", "--password", required=True)
@click.option("-v", "--verbose", type=bool, default=False, is_flag=True)
@click.option(
    "-d", "--days", type=int, default=30, help="delete all beacons older than N days"
)
def cleanup(
    api_url: str, username: str, password: str, days: int, verbose: bool
) -> None:
    clean_before = datetime.now(tz=timezone.utc) - timedelta(days=days)

    try:
        response = httpx.delete(
            f"{ api_url }/cleanup/",
            params={"since": clean_before.isoformat()},
            auth=(username, password),
        )
    except Exception as e:
        click.secho(e, fg="red")
        raise click.Abort()

    if response.status_code != 200:
        click.secho("Server failed to delete beacons", fg="red")
        raise click.Abort()

    if verbose:
        click.secho(
            f"Deleted beacons older than { clean_before.astimezone() }", fg="green"
        )
        for beacon in response.json():
            click.echo(beacon)
