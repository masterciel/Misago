from misago.monitor.fixtures import load_monitor_fixture
from misago.utils import ugettext_lazy as _
from misago.utils import get_msgid

monitor_fixtures = {
                  'users': 0,
                  'users_inactive': 0,
                  'users_reported': 0,
                  'last_user': None,
                  'last_user_name': None,
                  'last_user_slug': None,
                  }


def load_fixtures():
    load_monitor_fixture(monitor_fixtures)
