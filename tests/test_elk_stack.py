import pytest
import json

def test_logstash_health(connector):
    response = connector.get('http://localhost:9600/_node/logging?pretty')
    out = json.loads(response.content)
    assert response.status_code == 200
    assert out['status'] == 'green'

def test_elasticsearch_health(connector):
    response = connector.get('http://localhost:9200')
    out = json.loads(response.content)
    assert response.status_code == 200
    assert out['tagline'] == 'You Know, for Search'

def test_kibana_health(connector):
    response = connector.get('http://localhost:5601/api/status')
    out = json.loads(response.content)
    assert response.status_code == 200
    assert out['status']['overall']['state'] == 'green'
