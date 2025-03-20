"""
Hooks for special DAVAI processings.
"""

import json

from bronx.fancies import loggers

from ..util import SummariesStack, DavaiException, send_task_to_DAVAI_server, _send_to_davai_server_build_proxy

#: No automatic export
__all__ = []

logger = loggers.getLogger(__name__)


def take_the_DAVAI_train(t, rh,
                         fatal=True,
                         wagons='__all__'):
    """Usual double put of summaries for DAVAI."""
    if wagons == '__all__':
        wagons = ['ciboulai', 'stack']
    elif isinstance(wagons, str):
        wagons = wagons.split(',')
    # call sub-puts
    if 'ciboulai' in wagons:
        send_to_DAVAI_server(t, rh, fatal=fatal)
    if 'stack' in wagons:
        throw_summary_on_stack(t, rh)


def throw_summary_on_stack(t, rh):
    """
    Put summary on stack (cache directory in which are gathered all summaries).

    :param reload_trolley: if True, reload trolley on-the-fly right afterwards
    """
    stack = SummariesStack(ticket=t,
                           vapp=rh.provider.vapp,
                           vconf=rh.provider.vconf,
                           xpid=rh.provider.experiment)
    stack.throw_on_stack(rh)


def send_to_DAVAI_server(t, rh, fatal=True):  # @UnusedVariables
    """
    Send a JSON summary to DAVAI server.

    :param t: The Ticket object representing the current session.
    :param rh: The resource's Handler on which the hook is called.
    :param fatal: If False, catch errors, log but do not raise.
    """
    server_syntax = 'http[s]://<host>[:<port>]/<url> (port is optional)'
    try:
        # get data from file
        summary = t.sh.json_load(rh.container.localpath())
        if rh.resource.kind == 'xpinfo':
            jsonData = {rh.resource.kind: summary}
        elif rh.resource.kind in ('taskinfo', 'statictaskinfo'):
            jsonData = {rh.provider.block: {rh.resource.scope: summary}}
        else:
            raise DavaiException("Only kind=('xpinfo','taskinfo', 'statictaskinfo') resources can be sent.")
        # get URL to post to
        davai_server_url = t.env.get('DAVAI_SERVER')
        if davai_server_url == '':
            raise DavaiException("DAVAI_SERVER must be defined ! Expected syntax: " +
                                 server_syntax)
        else:
            if not davai_server_url.endswith('/api/'):
                davai_server_url = '/'.join([davai_server_url, 'api', ''])
        with _send_to_davai_server_build_proxy(t.sh) as proxies:
            send_task_to_DAVAI_server(davai_server_url,
                                      rh.provider.experiment,
                                      json.dumps(jsonData),
                                      kind=rh.resource.kind,
                                      fatal=fatal,
                                      proxies=proxies)
    except Exception as e:
        if fatal:
            raise
        else:
            logger.error(str(e))
