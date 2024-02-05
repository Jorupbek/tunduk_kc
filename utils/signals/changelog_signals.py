import json
import time

from apps.history.models import ChangeLog, ACTION_CREATE, ACTION_UPDATE, ACTION_DELETE
from utils.middleware.changelog_middleware import LoggedInUser
from utils.mixins.changelog_mixins import ChangeloggableMixin
from utils.utils import merge, json_dumps


def journal_save_handler(sender, instance, created, **kwargs):
    if isinstance(instance, ChangeloggableMixin):
        loggedIn = LoggedInUser()
        last_saved = get_last_saved(loggedIn.request, instance)
        changed = merge(last_saved['changed'], instance.get_changed_fields())
        if changed:
            changed = json.loads(json_dumps(changed))
            if created:
                ChangeLog.add(instance, loggedIn.current_user, ACTION_CREATE, changed,
                              id=last_saved['id'])
            else:
                ChangeLog.add(instance, loggedIn.current_user, ACTION_UPDATE, changed,
                              id=last_saved['id'])


def journal_delete_handler(sender, instance, using, **kwargs):
    if isinstance(instance, ChangeloggableMixin):
        loggedIn = LoggedInUser()
        last_saved = get_last_saved(loggedIn.request, instance)
        ChangeLog.add(instance, loggedIn.current_user, ACTION_DELETE, {}, id=last_saved['id'])


_last_saved = {}


def get_last_saved(request, instance):
    last_saved = _last_saved[request] if request in _last_saved else None
    if (not last_saved or last_saved['instance'].__class__ != instance.__class__
            or last_saved['instance'].id != instance.id):
        last_saved = {
            'instance': instance,
            'changed': {},
            'id': None,
            'timestamp': time.time()
        }
        _last_saved[request] = last_saved
    return last_saved
