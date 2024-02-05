from core.settings import SUBSYSTEM_CODE, MEMBER_CODE

HEADERS = {
    'Content-Type': 'text/xml; charset=utf-8',
    'X-Road-Client': f'central-server/COM/{MEMBER_CODE}/{SUBSYSTEM_CODE}',
    'accept': 'application/json'
}
