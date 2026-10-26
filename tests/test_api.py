"""Independent API tests. All data is ephemeral and synthetic."""

def test_health_and_static_frontend(client):
    assert client.get('/health').json()['status'] == 'ok'
    assert client.get('/').status_code == 200
    assert '<title>SignalDesk' in client.get('/').text
    assert 'api' in client.get('/assets/app.js').text


def test_full_crud_workflow(client, example):
    created = client.post('/api/contacts', json=example)
    assert created.status_code == 201
    contact = created.json()
    assert contact['outlet'] == 'Demo Radio'
    assert contact['id'] > 0
    assert client.get(f"/api/contacts/{contact['id']}").json()['notes'] == example['notes']
    assert len(client.get('/api/contacts').json()) == 1
    updated = client.patch(f"/api/contacts/{contact['id']}", json={'status': 'confirmed', 'notes': 'Reviewed'}).json()
    assert updated['status'] == 'confirmed'
    assert updated['notes'] == 'Reviewed'
    assert client.get('/api/summary').json()['by_status']['confirmed'] == 1
    assert client.delete(f"/api/contacts/{contact['id']}").status_code == 204
    assert client.get(f"/api/contacts/{contact['id']}").status_code == 404
    assert client.get('/api/summary').json()['total'] == 0


def test_filtering_and_literal_special_characters(client, example):
    client.post('/api/contacts', json=example)
    client.post('/api/contacts', json={**example, 'outlet': 'Press 100% Times', 'channel': 'press', 'status': 'sent'})
    assert len(client.get('/api/contacts?status=sent').json()) == 1
    assert len(client.get('/api/contacts?q=radio').json()) == 1
    assert len(client.get('/api/contacts?q=%25').json()) == 1
    assert len(client.get('/api/contacts?status=planned&q=press').json()) == 0


def test_validation_and_missing_ids(client, example):
    assert client.post('/api/contacts',json={**example,'outlet':'x'}).status_code == 422
    assert client.post('/api/contacts',json={**example,'outlet':'   '}).status_code == 422
    assert client.post('/api/contacts',json={**example,'status':'hacked'}).status_code == 422
    assert client.post('/api/contacts',json={**example,'unexpected':'bad'}).status_code == 422
    assert client.get('/api/contacts?limit=200').status_code == 422
    assert client.get('/api/contacts?status=invalid').status_code == 422
    assert client.patch('/api/contacts/999',json={'status':'sent'}).status_code == 404
    assert client.delete('/api/contacts/999').status_code == 404


def test_patch_rejects_null_for_required_fields(client, example):
    contact=client.post('/api/contacts',json=example).json()
    assert client.patch(f"/api/contacts/{contact['id']}",json={'outlet':None}).status_code == 422
    assert client.patch(f"/api/contacts/{contact['id']}",json={'notes':None}).status_code == 422
    assert client.patch(f"/api/contacts/{contact['id']}",json={'due_date':None}).status_code == 200
    assert client.patch(f"/api/contacts/{contact['id']}",json={}).status_code == 200


def test_readonly_portfolio_demo_blocks_mutation(read_only_client, example):
    client=read_only_client
    assert client.get('/api/config').json()['read_only'] is True
    assert client.get('/api/summary').json()['total'] == 4
    row=client.get('/api/contacts').json()[0]
    assert client.post('/api/contacts',json=example).status_code == 403
    assert client.patch(f"/api/contacts/{row['id']}",json={'status':'sent'}).status_code == 403
    assert client.delete(f"/api/contacts/{row['id']}").status_code == 403


def test_api_matches_openapi_contract(client):
    specs = client.get('/openapi.json').json()
    for path in ['/api/contacts', '/api/contacts/{contact_id}', '/api/summary', '/api/config', '/health','/ops/metrics']:
        assert path in specs['paths']


def test_ops_metrics_counts(client, example):
    assert client.get('/ops/metrics').json()['contacts_total'] == 0
    client.post('/api/contacts',json=example)
    metrics=client.get('/ops/metrics').json()
    assert metrics['contacts_total']==1
    assert metrics['uptime_seconds']>=0


def test_pagination(client, example):
    for n in range(3):
        client.post('/api/contacts',json={**example, 'outlet':f'Demo Radio {n}'})
    assert len(client.get('/api/contacts?limit=2').json())==2
    assert len(client.get('/api/contacts?limit=2&offset=2').json())==1
