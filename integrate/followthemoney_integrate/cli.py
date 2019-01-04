import sys
import click
import logging

from followthemoney.dedupe import Recon
from followthemoney_util.util import read_object
from followthemoney_integrate.model import metadata, Session, Entity, Match


@click.group(help="Utility for the FollowTheMoney integration tool")
def cli():
    fmt = '%(name)s [%(levelname)s] %(message)s'
    logging.basicConfig(stream=sys.stderr, level=logging.INFO, format=fmt)


@cli.command('init', help="Initalise database")
@click.option('--drop/--no-drop', default=False)
def init(drop):
    if drop:
        metadata.drop_all()
    metadata.create_all()


@cli.command('load-entities', help="Load entities")
@click.option('-e', '--entities', type=click.File('r'), default='-')  # noqa
def load_entities(entities):
    session = Session()
    try:
        while True:
            entity = read_object(entities)
            if entity is None:
                break
            Entity.save(session, entities.name, entity)
        session.commit()
    except BrokenPipeError:
        pass


@cli.command('load-results', help="Load results")
@click.option('-r', '--results', type=click.File('r'), default='-')  # noqa
def load_results(results):
    session = Session()
    try:
        while True:
            result = read_object(results)
            if result is None:
                break
            for entity in result.entities:
                Entity.save(session, result.enricher.name, entity)
            Match.save(session, result.subject, result.candidate,
                       score=result.score)
            session.flush()
    except BrokenPipeError:
        pass
    session.commit()


@cli.command('load-recon', help="Import recon judgements")
@click.option('-r', '--recon', type=click.File('r'), default='-')  # noqa
def load_recon(recon):
    session = Session()
    for recon in Recon.from_file(recon):
        Match.save(session, recon.subject, recon.canonical,
                   judgement=recon.judgement)
    session.commit()


@cli.command('dump-recon', help="Export recon judgements")
@click.option('-r', '--recon', type=click.File('w'), default='-')  # noqa
def dump_recon(fh):
    # TODO: tally votes.
    session = Session()
    for match in Match.all(session):
        if match.judgement is not None:
            recon = Recon(match.left, match.canonical, match.judgement)
            fh.write(recon.to_json())
