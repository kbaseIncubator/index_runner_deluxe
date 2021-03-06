from kbase_workspace_client.exceptions import WorkspaceResponseError
from typing import Optional
import logging

from src.utils.config import config
from src.utils.logger import logger


def get_type_pieces(type_str):
    """
    Given a full type string, returns (module, name, ver)
     - Given "KBaseNarrative.Narrative-4.0"
     - Returns ("KBaseNarrative", "Narrative", "4.0")
    """
    (full_name, type_version) = type_str.split('-')
    (type_module, type_name) = full_name.split('.')
    return (type_module, type_name, type_version)


def get_obj_type(msg: dict) -> Optional[str]:
    """
    Get the versioned workspace type from a kafka message.
    """
    objtype = msg.get('objtype')
    if isinstance(objtype, str) and len(objtype) > 0:
        return objtype
    objid = msg.get('objid')
    wsid = msg.get('wsid')
    if objid is not None and wsid is not None:
        info = config()['ws_client'].admin_req('getObjectInfo', {
            'objects': [{'ref': f"{wsid}/{objid}"}]
        })
        return info['infos'][0][2]
    return None


def log_error(ws_err: WorkspaceResponseError, level: int = logging.ERROR):
    """Log a workspace response error"""
    err_str = ws_err.resp_data['error']['message']
    logger.log(level, f'Workspace response error: {err_str}')
