from prometheus_client.core import CounterMetricFamily, GaugeMetricFamily
from requests.auth import HTTPBasicAuth

import json, requests, sys, time, os, ast, signal, datetime

class VarnishCollector(object):

  def __init__(self, name, host, port, user, password):
        """ initializing name and cuisine attributes"""
        self.name = name
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.METRIC_PREFIX = 'varnish'

  def collect(self):



    gauges = {}

    self._collect_metrics(gauges)
    # print("Metrics collected for varnish host")


    # Yield all metrics returned
    for gauge_key, gauge in gauges.items():
      yield gauge


  def _collect_metrics(self, gauges):
      url = 'http://%s:%s/stats' % (self.host, self.port)
      response_json = self._get_json(url,self.user,self.password)
      self._add_metrics(gauges, response_json)

  def _get_json(self, url, user, password ):
    #  print("Getting JSON Payload for " + url)

    response_json = json.loads(requests.get(url, auth=HTTPBasicAuth(user, password)).content.decode('UTF-8'))
    return response_json


  def _add_metrics(self, gauges, response_json):
    for metric, field in response_json.items():
      if metric == "timestamp" :
        metric = 'timestamp'
        description = ''
        data = datetime.datetime.strptime(field, "%Y-%m-%dT%H:%M:%S").timestamp()
        gauges[metric] = GaugeMetricFamily(('%s_%s' % (self.METRIC_PREFIX, metric)).lower(), '%s' % description, value=data)
        # continue
      elif field['type'] in ['MAIN', 'LCK'] :
        gauges[metric] = GaugeMetricFamily(('%s_%s' % (self.METRIC_PREFIX, metric)).lower(), '%s' % field['description'], value=field['value'])

    # metrics_calculated

    metric = 'main.ratio_hit'
    description = ''
    data = round((response_json['MAIN.cache_hit']['value']/response_json['MAIN.client_req']['value'])*100,2)
    gauges[metric] = GaugeMetricFamily(('%s_%s' % (self.METRIC_PREFIX, metric)).lower(), '%s' % description, value=data)

    metric = 'main.req_bytes'
    description = ''
    data = int(response_json['MAIN.s_req_hdrbytes']['value'])+int(response_json['MAIN.s_req_bodybytes']['value'])
    gauges[metric] = GaugeMetricFamily(('%s_%s' % (self.METRIC_PREFIX, metric)).lower(), '%s' % description, value=data)

    metric = 'main.resp_bytes'
    description = ''
    data = int(response_json['MAIN.s_resp_hdrbytes']['value'])+int(response_json['MAIN.s_resp_bodybytes']['value'])
    gauges[metric] = GaugeMetricFamily(('%s_%s' % (self.METRIC_PREFIX, metric)).lower(), '%s' % description, value=data)

    # metric = 'main.host'
    # description = ''
    # data = self.name
    # gauges[metric] = GaugeMetricFamily(('%s_%s' % (self.METRIC_PREFIX, metric)).lower(), '%s' % description, value=data)
