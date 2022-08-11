import pytest


def test_get_report_service__with_orders(client, report_uri, create_orders):
    response = client.get(report_uri)
    pytest.assume(response.status.startswith('200'))
    pytest.assume(response.json['customers'])
    pytest.assume(response.json['ingredient'])
    pytest.assume(response.json['month'])


def test_get_report_service__without_orders(client, report_uri):
    response = client.get(report_uri)
    pytest.assume(response.status.startswith('400'))
    pytest.assume(response.json['error'])
