"""Dry signals"""

import logging

from asgiref.sync import async_to_sync
from byuhbll.person_client import PersonClient

logger = logging.getLogger(__name__)


@async_to_sync
async def get_library_id(net_id):
    """
    Get the Library ID for the given NetID.

    Args:
        net_id (str): The NetID of the patron

    Returns:
        str: The Library ID
    """
    async with PersonClient() as client:
        library_id = await client.get_library_id('net_id', net_id)
        return library_id


@async_to_sync
async def get_person_summary(library_id):
    """
    Get the person summary for the given Library ID.

    Args:
        library_id (str): The Library ID of the patron

    Returns:
        byuhbll.person_client.models.PersonSummary: The person summary
    """
    async with PersonClient() as client:
        person_summary = await client.get_summary(library_id)
        return person_summary


def get_person_from_university(net_id: str = None, library_id: str = None):
    """
    Retrieves person data from the university.

    A Library ID is preferred over a NetID. If neither a Library ID or NetID
    is provided, an exception is raised.

    Args:
        net_id (str): The net id of the patron
        library_id (str): The library id of the patron

    Returns:
        byuhbll.person_client.models.PersonSummary: The person summary
    """
    if not (net_id or library_id):
        raise ValueError('Either net_id or library_id must be provided')
    if not library_id:
        library_id = get_library_id(net_id)
    return get_person_summary(library_id)


def update_user_info(user, save=True):
    """
    Updates a users email, library id, first_name, and last_name
    from the university data.
    """
    person_summary = get_person_from_university(
        user.username, library_id=user.library_id
    )

    user.email = person_summary.email_address or user.email
    user.first_name = person_summary.preferred_first_name or user.first_name
    user.last_name = person_summary.last_name or user.last_name
    user.library_id = person_summary.library_id or user.library_id

    if save:
        user.save()

    return user
