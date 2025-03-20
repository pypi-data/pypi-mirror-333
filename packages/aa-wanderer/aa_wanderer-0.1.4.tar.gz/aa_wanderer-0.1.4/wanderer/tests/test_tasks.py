"""Tasks tests"""

from unittest.mock import MagicMock, call

from django.test import TestCase

from wanderer.models import WandererAccount, WandererManagedMap
from wanderer.tasks import (
    add_alts_to_map,
    cleanup_access_list,
    remove_user_characters_from_map,
)

from ..wanderer import AccessListRoles
from .utils import create_managed_map, create_wanderer_users


class TestTasks(TestCase):

    def test_add_character_to_acl(self):
        """Checks that characters properly get added to the access list"""
        WandererManagedMap.get_character_ids_on_access_list = MagicMock(
            return_value=[1001, 1002]
        )  # Creating fake ids to be returned
        WandererManagedMap.add_character_to_acl = MagicMock()
        WandererAccount.get_all_character_ids = MagicMock(
            return_value=[1001, 1003]
        )  # Missing id 1003

        wanderer_map = create_managed_map()
        user = create_wanderer_users(wanderer_map)[0]

        add_alts_to_map(user.id, wanderer_map.id)

        WandererManagedMap.get_character_ids_on_access_list.assert_called_once()
        WandererManagedMap.add_character_to_acl.assert_called_once_with(1003)
        WandererAccount.get_all_character_ids.assert_called_once()

    def test_remove_user_characters_from_acl(self):
        WandererManagedMap.get_character_ids_on_access_list = MagicMock(
            return_value=[1001, 1002, 1003]
        )
        WandererManagedMap.remove_member_from_access_list = MagicMock()
        WandererAccount.get_all_character_ids = MagicMock(return_value=[1001, 1002])

        wanderer_map = create_managed_map()
        user = create_wanderer_users(wanderer_map)[0]

        remove_user_characters_from_map(user.id, wanderer_map.id)

        WandererManagedMap.get_character_ids_on_access_list.assert_called_once()
        WandererAccount.get_all_character_ids.assert_called_once()

        remove_member_calls = [call(1001), call(1002)]
        WandererManagedMap.remove_member_from_access_list.assert_has_calls(
            remove_member_calls, any_order=True
        )

    def test_cleanup_access_list(self):
        WandererManagedMap.get_character_ids_on_access_list = MagicMock(
            return_value=[1000, 1011, 1020]
        )
        WandererManagedMap.remove_member_from_access_list = MagicMock()
        WandererManagedMap.add_character_to_acl = MagicMock()
        WandererManagedMap.get_non_member_characters = MagicMock(
            return_value=[
                (1030, AccessListRoles.VIEWER),
                (1031, AccessListRoles.BLOCKED),
            ]
        )
        WandererManagedMap.set_character_to_member = MagicMock()

        wanderer_map = create_managed_map()
        create_wanderer_users(wanderer_map, 2)

        cleanup_access_list(wanderer_map.id)

        WandererManagedMap.get_character_ids_on_access_list.assert_called_once()
        WandererManagedMap.remove_member_from_access_list.assert_called_once_with(1020)
        add_character_calls = [call(1001), call(1010)]
        WandererManagedMap.add_character_to_acl.assert_has_calls(
            add_character_calls, any_order=True
        )
        WandererManagedMap.get_non_member_characters.assert_called_once()
        set_character_to_member_calls = [call(1030), call(1031)]
        WandererManagedMap.set_character_to_member.assert_has_calls(
            set_character_to_member_calls, any_order=True
        )

    def test_dont_cleanup_access_list(self):
        """Test where the access list is correct and has different roles than member"""
        WandererManagedMap.get_character_ids_on_access_list = MagicMock(
            return_value=[1000, 1001, 1010, 1011]
        )
        WandererManagedMap.get_all_accounts_characters_ids = MagicMock(
            return_value=[1000, 1001, 1010, 1011]
        )
        WandererManagedMap.add_character_to_acl = MagicMock()
        WandererManagedMap.remove_member_from_access_list = MagicMock()
        WandererManagedMap.get_non_member_characters = MagicMock(
            return_value=[
                (1000, AccessListRoles.ADMIN),
                (1001, AccessListRoles.MANAGER),
                (1010, AccessListRoles.MEMBER),
                (1011, AccessListRoles.MEMBER),
            ]
        )
        WandererManagedMap.set_character_to_member = MagicMock()

        wanderer_map = create_managed_map()
        create_wanderer_users(wanderer_map, 2)

        cleanup_access_list(wanderer_map.id)

        WandererManagedMap.get_character_ids_on_access_list.assert_called_once()
        WandererManagedMap.get_all_accounts_characters_ids.assert_called_once()
        WandererManagedMap.add_character_to_acl.assert_not_called()
        WandererManagedMap.remove_member_from_access_list.assert_not_called()
        WandererManagedMap.get_non_member_characters.assert_called_once()
        WandererManagedMap.set_character_to_member.assert_not_called()
