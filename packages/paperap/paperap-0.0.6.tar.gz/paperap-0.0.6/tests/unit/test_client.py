"""



 ----------------------------------------------------------------------------

    METADATA:

        File:    test_client.py
        Project: paperap
        Created: 2025-03-04
        Version: 0.0.5
        Author:  Jess Mann
        Email:   jess@jmann.me
        Copyright (c) 2025 Jess Mann

 ----------------------------------------------------------------------------

    LAST MODIFIED:

        2025-03-04     By Jess Mann

"""
from __future__ import annotations
import json
import os
from typing import Iterator
import unittest
from unittest.mock import MagicMock, patch
from pathlib import Path
from paperap.resources.documents import DocumentResource
from paperap.tests import UnitTestCase, load_sample_data
from paperap.models.abstract import BaseQuerySet
from paperap.models.document import Document
from paperap.models.tag import Tag

# Load sample response from tests/sample_data/documents_list.json
sample_data = load_sample_data('documents_list.json')

class TestClient(UnitTestCase):
    resource_class = DocumentResource

    @patch("paperap.client.PaperlessClient.request")
    def test_get_documents(self, mock_request):
        mock_request.return_value = sample_data
        documents = self.client.documents()
        self.assertIsInstance(documents, BaseQuerySet)
        total = documents.count()
        self.assertEqual(total, sample_data['count'], "Count of documents incorrect")
        total_on_page = documents.count_this_page()
        self.assertEqual(total_on_page, len(sample_data['results']), "Count of documents on this page incorrect")

        count = 0
        # Ensure paging works, then break
        test_iterations = total_on_page + 2

        # A warning should be issued for repeating the same url
        # this happens because when the 2nd page is requested, the next url is populated, even though we're going to break before using it.
        # Log was turned to a debug (maybe temporarily?)
        #with self.assertLogs(level='WARNING'):
        for document in documents:
            count += 1
            self.assertIsInstance(document, Document, f"Expected Document, got {type(document)}")
            self.assertIsInstance(document.id, int, f"Document id is wrong type: {type(document.id)}")
            self.assertIsInstance(document.title, str, f"Document title is wrong type: {type(document.title)}")
            if document.correspondent_id:
                self.assertIsInstance(document.correspondent_id, int, f"Document correspondent is wrong type: {type(document.correspondent_id)}")
            self.assertIsInstance(document.document_type_id, int, f"Document document_type is wrong type: {type(document.document_type_id)}")
            self.assertIsInstance(document.tag_ids, list, f"Document tags is wrong type: {type(document.tag_ids)}")

            for tag in document.tag_ids:
                self.assertIsInstance(tag, int, f"Document tag is wrong type: {type(tag)}")

            # Ensure paging works, then break
            if count >= test_iterations:
                break

        self.assertEqual(count, test_iterations, "Document queryset did not iterate over 3 pages.")

if __name__ == "__main__":
    unittest.main()
