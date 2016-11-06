import json
from copy import deepcopy
from urllib.parse import urlencode

from django.http import HttpResponse
from django.conf import settings
from django.shortcuts import render
from django.views.generic.base import TemplateView

from search_list.models import Document

from json import JSONEncoder


class Encoder(JSONEncoder):
    def default(self, o):
        return o.__dict__

client = settings.ES_CLIENT


def document_detail(request):
    document_id = request.GET.get('document_id')
    if document_id == {}:
        return HttpResponse("")
    else:
        document = Document.objects.get(pk=document_id)
        return HttpResponse(Encoder().encode(document))


def search_view(request):
    query = request.GET.get('term', '')
    resp = client.search(
        index='foo',
	q=query
    )
    context = [
            convert_hit_to_template(c) for c in resp['hits']['hits']
        ]
    mimetype = 'application/json'
    return HttpResponse(json.dumps(context), mimetype)


def list_view(request):
    start = request.GET.get('from', '0')
    search_result = client.search(index='foo', doc_type='t', from_=start)
    context = [
            convert_hit_to_template(c) for c in search_result['hits']['hits']
        ]
    print(len(search_result['hits']['hits']))

    return HttpResponse(Encoder().encode(context), content_type="application/json")


def convert_hit_to_template(hit1):
    hit = deepcopy(hit1)
    almost_ready = hit['_source']
    return almost_ready

class HomePageView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        body = {
            'aggs': {
                'title': {
                    'terms': {
                        'field': 'title'
                    }
                },
                'text': {
                    'terms': {
                        'field': 'text'
                    }
                },
                'h1': {
                    'terms': {
                        'field': 'h1', 'size': 0
                    }
                },
                'h2': {
                    'terms': {
                        'field': 'h2', 'size': 0
                    }
                },
                'h3': {
                    'terms': {
                        'field': 'h3', 'size': 0
                    }
                }
            },
            # 'query': {'match_all': {}}
        }
        es_query = self.gen_es_query(self.request)
        body.update({'query': es_query})
        search_result = client.search(index='foo', doc_type='t', body=body)
        context = super(HomePageView, self).get_context_data(**kwargs)
        context['hits'] = [
            self.convert_hit_to_template(c) for c in search_result['hits']['hits']
        ]
        context['aggregations'] = self.prepare_facet_data(
            search_result['aggregations'],
            self.request.GET
        )
        return context

    def convert_hit_to_template(self, hit1):
        hit = deepcopy(hit1)
        almost_ready = hit['_source']
        almost_ready['pk'] = hit['_id']
        return almost_ready

    def facet_url_args(self, url_args, field_name, field_value):
        is_active = False
        if url_args.get(field_name):
            base_list = url_args[field_name].split(',')
            if field_value in base_list:
                del base_list[base_list.index(field_value)]
                is_active = True
            else:
                base_list.append(field_value)
            url_args[field_name] = ','.join(base_list)
        else:
            url_args[field_name] = field_value
        return url_args, is_active

    def prepare_facet_data(self, aggregations_dict, get_args):
        resp = {}
        for area in aggregations_dict.keys():
            resp[area] = []
            if area == 'age':
                resp[area] = aggregations_dict[area]['buckets']
                continue
            for item in aggregations_dict[area]['buckets']:
                url_args, is_active = self.facet_url_args(
                    url_args=deepcopy(get_args.dict()),
                    field_name=area,
                    field_value=item['key']
                )
                resp[area].append({
                    'url_args': urlencode(url_args),
                    'name': item['key'],
                    'count': item['doc_count'],
                    'is_active': is_active
                })
        return resp

    def gen_es_query(self, request):
        req_dict = deepcopy(request.GET.dict())
        if not req_dict:
            return {'match_all': {}}
        filters = []
        for field_name in req_dict.keys():
            if '__' in field_name:
                filter_field_name = field_name.replace('__', '.')
            else:
                filter_field_name = field_name
            for field_value in req_dict[field_name].split(','):
                if not field_value:
                    continue
                filters.append(
                    {
                        'term': {filter_field_name: field_value},
                    }
                )
        return {
            'filtered': {
                'query': {'match_all': {}},
                'filter': {
                    'bool': {
                        'must': filters
                    }
                }
            }
        }
