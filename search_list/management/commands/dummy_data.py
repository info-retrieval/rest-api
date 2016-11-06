import json

from model_mommy import mommy
from django.core.management.base import BaseCommand

from search_list.models import Document, H1, H2, H3

content = open("parser.json", "r").read()


class Command(BaseCommand):
    help = "My shiny new management command."

    def __init__(self):
        super().__init__(stdout=None, stderr=None, no_color=False)
        self.docs = [json.loads(str(item)) for item in content.strip().split('\n')]
        self.documents = []

    def add_documents(self):
        for txt in self.docs:
            doc = mommy.prepare(
                Document,
                id=txt['id'],
                text=txt['content'],
                title=txt['title']
            )
            self.documents.append(doc)
        Document.objects.bulk_create(self.documents)

    def connect_headers(self):
        headers = (
            'header 1', 'header 2', 'header 3'
        )
        doc_header1 = []
        doc_header2 = []
        doc_header3 = []
        ThroughModel = Document.h1.through
        for doc in self.docs:
            doc_id = doc['id']
            for h in doc['h1']:
                doc_header1.append(
                    ThroughModel(
                        document_id=doc_id,
                        h1_id=mommy.make(H1, title=h).pk
                    )
                )

        ThroughModel.objects.bulk_create(doc_header1)
        ThroughModel = Document.h2.through
        for doc in self.docs:
            doc_id = doc['id']
            for h in doc['h2']:
                doc_header2.append(
                    ThroughModel(
                        document_id=doc_id,
                        h2_id=mommy.make(H2, title=h).pk
                    )
                )

        ThroughModel.objects.bulk_create(doc_header2)
        ThroughModel = Document.h3.through
        for doc in self.docs:
            doc_id = doc['id']
            for h in doc['h3']:
                doc_header3.append(
                    ThroughModel(
                        document_id=doc_id,
                        h3_id=mommy.make(H3, title=h).pk
                    )
                )

        ThroughModel.objects.bulk_create(doc_header3)

    def clear(self):
        Document.objects.all().delete()

    def handle(self, *args, **options):
        self.clear()
        self.add_documents()
        self.connect_headers()
