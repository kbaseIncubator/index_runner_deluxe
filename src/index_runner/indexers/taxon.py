_TAXON_INDEX_VERSION = 1


def index_taxon(obj_data, ws_info, obj_data_v1):
    """
    Currently indexes following workspace types:
        KBaseGenomeAnnotations.Taxon-1.0
    """
    info = obj_data['info']
    data = obj_data['data']

    workspace_id = info[6]
    object_id = info[0]

    yield {
        'doc': {
            'scientific_name': data.get('scientific_name'),
            'scientific_lineage': data.get('scientific_lineage'),
            'domain': data.get('domain'),
            'kingdom': data.get('kingdom'),
            'parent_taxon_ref': data.get('parent_taxon_ref', None),
            'genetic_code': data.get('genetic_code', None),
            'aliases': data.get('aliases', [])
        },
        'index': 'taxon:' + str(_TAXON_INDEX_VERSION),
        'id': f"{workspace_id}:{object_id}"
    }
