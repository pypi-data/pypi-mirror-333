import promql_parser
from promql_parser import parse

l = 'prometheus_http_requests_total{code="200", job="prometheus"}'

print(parse('min_over_time(rate(foo{bar="baz"}[2s])[5m:] @ 1603775091)[4m:3s]'))

print(parse('1'))

print(parse('1 + 1'))

print(parse('1 + 2/(3*1)').prettify())

print(parse('+some_metric'))

print(promql_parser.display_duration(promql_parser.parse_duration('4w4d2h59m120s')))
