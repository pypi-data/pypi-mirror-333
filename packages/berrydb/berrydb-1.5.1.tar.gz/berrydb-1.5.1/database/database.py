import json
import logging

import requests

import constants.constants as bdb_constants
from berrydb.berrydb_settings import Settings
from constants.constants import (ALZHEIMER_SE_TYPE,
                                 AUDIO_TRANSCRIPTION_SE_TYPE, FASHION_SE_TYPE,
                                 IMAGE_CAPTIONING_SE_TYPE,
                                 IMAGE_CLASSIFICATION_SE_TYPE, LOGGING_LEVEL,
                                 MEDICAL_NER_SE_TYPE, NER_SE_TYPE,
                                 PNEUMONIA_SE_TYPE, SEMANTICS_ANNOTATE_URL,
                                 SEMANTICS_PREDICT_URL,
                                 TEXT_CLASSIFICATION_SE_TYPE,
                                 TEXT_SUMMARIZATION_SE_TYPE,
                                 bulk_upsert_documents_url, caption_url,
                                 chat_with_database_url, debug_mode,
                                 document_by_id_url, documents_url,
                                 embed_database_url, extract_pdf_url, fts_url,
                                 label_summary_url, query_url,
                                 transcription_url, transcription_yt_url)
from utils.utils import Utils

logging.basicConfig(level=LOGGING_LEVEL, format="%(asctime)s - %(levelname)s - %(message)s")


logger = logging.getLogger(__name__)


class Database:
    __api_key: str
    __bucket_name: str
    __database_name: str
    __org_name: str
    __settings: Settings

    def __init__(self, api_key: str, bucket_name: str, org_name: str, database_name: str):
        if api_key is None:
            Utils.print_error_and_exit("API Key cannot be None")
        if bucket_name is None:
            Utils.print_error_and_exit("Bucket name cannot be None")
        if org_name is None:
            Utils.print_error_and_exit("Organization name cannot be None")
        self.__api_key = api_key
        self.__bucket_name = bucket_name
        self.__database_name = database_name
        self.__org_name = org_name
        self.__settings = Settings.Builder().build()
        self.__settings_name = None

    def settings(self, settings: Settings | str) -> Settings:
        if settings is None:
            Utils.print_error_and_exit("Settings cannot be None")
        elif isinstance(settings, str):
            self.__settings_name = settings
            settings_obj = Settings.get(self.__api_key, settings)
            self.__settings = settings_obj
        elif isinstance(settings, Settings):
            self.__settings = settings
            self.__settings_name = None
        else:
            Utils.print_error_and_exit("settings must be an instance of class Settings. import using 'from berrydb.settings import Settings'")
        return self.__settings

    def api_key(self):
        return self.__api_key

    def bucket_name(self):
        return self.__bucket_name

    def org_name(self):
        """To get the name of the organization of the connected database

        Args:
                No Arguments

        Returns:
                str: Get the organization ID of the connected database
        """
        return self.__org_name

    def database_name(self):
        """Function summary

        Args:
                No Arguments

        Returns:
                str: Get the database name of the connected database
        """
        return self.__database_name

    def get_all_documents(self, document_ids=None):
        """Function summary

        Args:
                document_ids arg1: list of document IDs to retrieve (Optional)

        Returns:
                list: Return a list of documents in the connected database or list of documents with IDs mentioned in document_ids
        """

        url = bdb_constants.BASE_URL + documents_url
        params = {
            "apiKey": self.__api_key,
            "bucket": self.__bucket_name,
            "databaseName": self.__database_name,
        }
        if document_ids is not None:
            if isinstance(document_ids, str):
                params['id'] = document_ids
            if isinstance(document_ids, list):
                params['id'] = ",".join(document_ids)

        if debug_mode:
            print("url:", url)
            print("params:", params)

        try:
            response = requests.get(url, params=params)
            if response.status_code != 200:
                Utils.handleApiCallFailure(response.json(), response.status_code)
            if debug_mode:
                print("documents result ", response.json())
            return json.loads(response.text)
        except Exception as e:
            print("Failed to fetch document: {}".format(str(e)))
            return []


    def get_all_documents_with_col_filter(self, col_filter=["*"]):
        """Function summary

        Args:
                arg1 (list<str>): Column list (Optional)

        Returns:
                list: Return a list of filtered documents in the connected database
        """

        url = bdb_constants.BASE_URL + documents_url

        url += "?apiKey=" + self.__api_key
        url += "&bucket=" + self.__bucket_name
        url += "&databaseName=" + str(self.__database_name)
        url += "&columns=" + (",".join(col_filter))

        if debug_mode:
            print("url:", url)
        try:
            response = requests.get(url)
            if response.status_code != 200:
                Utils.handleApiCallFailure(response.json(), response.status_code)
            if debug_mode:
                print("documents result ", response.json())
            # return response.json()
            return json.loads(response.text)
        except Exception as e:
            print("Failed to fetch document: {}".format(str(e)))
            return []

    def get_document_by_object_id(
        self,
        document_id,
        key_name=None,
        key_value=None,
    ):
        """Function summary

        Args:
                arg1 (str): Document Key/Id
                arg2 (str): Key Name (optional)
                arg3 (str): Key Value (optional)

        Returns:
                list: List of Documents matching the document ID in the connected database
        """

        from urllib.parse import quote
        url = bdb_constants.BASE_URL + document_by_id_url.format(quote(document_id))
        params = {
            "apiKey": self.__api_key,
            "bucket": self.__bucket_name,
            "databaseName": self.__database_name,
        }

        if document_id is not None:
            params["docId"] = document_id
        if key_name is not None:
            params["keyName"] = key_name
        if key_value is not None:
            params["keyValue"] = key_value

        if debug_mode:
            print("url:", url)
            print("params:", params)

        try:
            response = requests.get(url, params=params)
            if response.status_code != 200:
                Utils.handleApiCallFailure(response.text, response.status_code)
            jsonRes = response.json()
            if debug_mode:
                print("docById result ", jsonRes)
            return jsonRes
        except Exception as e:
            print("Failed to fetch document by id {} : {}".format(document_id, str(e)))
            return ""

    def query(self, query: str):
        """Function summary

        Args:
                arg1 (str): Query String

        Returns:
                list: Return a list of documents that match the query on the connected database.
        """

        url = bdb_constants.BASE_URL + query_url
        params = {
            "apiKey": self.__api_key,
            "bucket": self.__bucket_name,
            "databaseName": self.__database_name,
        }
        payload = {"query": query}

        if debug_mode:
            print("url:", url)
            print("params:", params)
            print("payload:", payload)
        headers = Utils.get_headers(self.__api_key)

        try:
            response = requests.post(url, data=payload, headers=headers, params=params)
            if response.status_code != 200:
                Utils.handleApiCallFailure(response.json(), response.status_code)
            if debug_mode:
                print("query result ", response.json())
            return json.loads(response.text)
        except Exception as e:
            print("Failed to query : {}".format(str(e)))
            return ""

    def __upsert(self, documents) -> str:
        url = bdb_constants.BASE_URL + bulk_upsert_documents_url
        params = {
            "apiKey": self.__api_key,
            "bucket": self.__bucket_name,
            "databaseName": self.__database_name,
        }

        payload = json.dumps(documents)
        if debug_mode:
            print("url:", url)
            print("payload:", payload)
        headers = Utils.get_headers(self.__api_key)

        try:
            response = requests.post(url, data=payload, headers=headers, params=params)
            if response.status_code != 200:
                try:
                    resp_content = response.json()
                except ValueError:
                    resp_content = response.text
                Utils.handleApiCallFailure(resp_content, response.status_code)
            if debug_mode:
                print("upsert result ", response)
            return response.text
        except Exception as e:
            print("Failed to upsert document: {}".format(str(e)))
            return ""

    def upsert(self, documents) -> str:
        """Function summary

        Args:
                arg1 (str): List of documents Object to add/update (Each document should have a key 'id' else a random string is assigned)

        Returns:
                str: Success/Failure message
        """
        try:
            if type(documents) != list:
                documents = [documents]
            return self.__upsert(documents)
        except Exception as e:
            print("Failed to upsert documents: {}".format(str(e)))
            return ""

    def delete_document(self, document_id):
        """Function summary

        Args:
                arg1 (str): Document ID

        Returns:
                str: Success/Failure message
        """

        from urllib.parse import quote
        url = bdb_constants.BASE_URL + document_by_id_url.format(quote(document_id))
        params = {
            "apiKey": self.__api_key,
            "bucket": self.__bucket_name,
            "databaseName": self.__database_name,
        }

        if debug_mode:
            print("url:", url)
            print("params:", params)

        try:
            response = requests.delete(url, params=params)
            if response.status_code != 200:
                Utils.handleApiCallFailure(response.json(), response.status_code)
            jsonRes = response.text
            if debug_mode:
                print("Delete document result ", jsonRes)
            return jsonRes
        except Exception as e:
            print("Failed to delete document by id {}, reason : {}".format(document_id, str(e)))
            return ""

    def transcribe(self, video_url: str):
        url = bdb_constants.ML_BACKEND_BASE_URL + transcription_url

        body = {
            "url": video_url,
        }

        payload = json.dumps(body)
        if debug_mode:
            print("url:", url)
            print("payload:", payload)
        headers = Utils.get_headers(self.__api_key)

        try:
            response = requests.post(url, headers=headers, data=payload)
            if response.status_code != 200:
                Utils.handleApiCallFailure(response.json(), response.status_code)
            res = response.text
            if debug_mode:
                print("Transcription result: ", res)
            return res
        except Exception as e:
            print(f"Failed to get transcription for the url {video_url}, reason : {str(e)}")
            return ""

    def transcribe_yt(self, video_url: str):

        url = bdb_constants.ML_BACKEND_BASE_URL + transcription_yt_url

        body = {
            "url": video_url,
        }

        payload = json.dumps(body)
        if debug_mode:
            print("url:", url)
            print("payload:", payload)
        headers = Utils.get_headers(self.__api_key)

        try:
            response = requests.post(url, headers=headers, data=payload)
            if response.status_code != 200:
                Utils.handleApiCallFailure(response.json(), response.status_code)
            res = response.text
            if debug_mode:
                print("Youtube transcription result: ", res)
            return res
        except Exception as e:
            print(f"Failed to get transcription for the youtube url {video_url}, reason : {str(e)}")
            return ""

    def caption(self, image_url: str):
        url = bdb_constants.ML_BACKEND_BASE_URL + caption_url

        body = {
            "url": image_url,
        }

        payload = json.dumps(body)
        if debug_mode:
            print("url:", url)
            print("payload:", payload)
        headers = Utils.get_headers(self.__api_key)

        try:
            response = requests.post(url, headers=headers, data=payload)
            if response.status_code != 200:
                Utils.handleApiCallFailure(response.json(), response.status_code)
            res = response.text
            if debug_mode:
                print("Caption result: ", res)
            return res
        except Exception as e:
            print(f"Failed to get caption for the url {image_url}, reason : {str(e)}")
            return ""

    def enable_fts(self, fields = None, override = False):
        """Creates a new full-text search (FTS) index on the database.

        Args:
                fields (list): List of fields (JSON paths) to build the index on. If empty, the index fields set on the schema is considered
                override (bool): If True, replaces any existing index

        Returns:
                FTS: An instance of FTS object
        """
        from fts.fts import FTS

        url = bdb_constants.BASE_URL + fts_url

        params = {
            "databaseName": self.__database_name,
            "apiKey": self.__api_key,
        }

        body = {
            "fields": fields,
            "override": override,
        }
        payload = json.dumps(body)

        if debug_mode:
            print("url:", url)
            print("params:", params)
            print("payload:", payload)

        try:
            response = requests.post(url, params=params, data=payload, headers={'Content-Type': 'application/json'})

            if response.status_code != 201:
                Utils.handleApiCallFailure(response.json(), response.status_code)

            res = response.json()
            if debug_mode:
                print("FTS result: ", res)

            return FTS(self.__api_key, self.__database_name, res['indexedFields'])
        except Exception as e:
            errMsg = "Failed to enable FTS"
            print(f"{errMsg}, reason : {str(e)}")
            return

    def embed(
        self,
        embedding_api_key:str,
    ):
        """Embeds your database to help you chat with it.

        Args:
                arg1 llm_api_key (str): LLM API key to embed the database [OpenAI, HuggingFace, ...]
                arg2 embed_config (str): Settings

        Returns:
                str: Success/error message of embedding the database
        """

        url = bdb_constants.BERRY_GPT_BASE_URL + embed_database_url

        body = {
            "database": self.__database_name,
            "apiKey": self.__api_key,
            "orgName": self.__org_name,
            "llmApiKey": embedding_api_key,
            "settingsName": self.__settings_name,
            "embeddingApiKey": embedding_api_key,
        }
        if self.__settings_name is None:
            body["settings"] = self.__settings.__dict__

        if debug_mode:
            print("url:", url)
            print("body:", body)
        payload = json.dumps(body)
        headers = Utils.get_headers(self.__api_key)

        try:
            response = requests.post(url, headers=headers, data=payload)
            if response.status_code != 200:
                Utils.handleApiCallFailure(response.json(), response.status_code)
            res = response.json()
            if debug_mode:
                print("Embed result: ", res)
            return res
        except Exception as e:
            errMsg = "Failed to embed the database. Please try again later."
            print(f"{errMsg}, reason : {str(e)}")
            raise e

    def chat(
        self,
        llm_api_key:str,
        question:str,
        embedding_model_api_key:str | None = None,
    ):
        """Chat with your BerryDB database after successfully embedding it.

        Args:
                llm_api_key [arg1] (str): LLM API key to embed the database [OpenAI, HuggingFace, ...]
                question [arg2] (str): Query/Question to for your database
                embedding_model_api_key (str): The API key/token of your embedding model (Only used if the embedding and chat providers do not match)

        Returns:
                str: Answer/error to the query
        """

        url = bdb_constants.BERRY_GPT_BASE_URL + chat_with_database_url

        body = {
            key: value
            for key, value in {
                "question": question,
                "apiKey": self.__api_key,
                "database": self.__database_name,
                "orgName": self.__org_name,
                "llmApiKey": llm_api_key,
                "embeddingApiKey": embedding_model_api_key,
                "settingsName": self.__settings_name,
            }.items()
            if value is not None
        }
        if self.__settings_name is None:
            body["settings"] = self.__settings.__dict__

        if debug_mode:
            print("url:", url)
            print("body:", body)
        payload = json.dumps(body)
        headers = Utils.get_headers(self.__api_key)

        try:
            response = requests.post(url, headers=headers, data=payload)
            if response.status_code != 200:
                Utils.handleApiCallFailure(response.json(), response.status_code)
            res = response.json()
            if debug_mode:
                print("Database chat result: ", res)
            return res['answer']
        except Exception as e:
            errMsg = "Failed to chat with the database. Please try again later."
            print(f"{errMsg}, reason : {str(e)}")
            raise e

    def chat_for_eval(
        self,
        llm_api_key:str,
        question:str,
        embedding_model_api_key:str | None = None,
    ) -> dict:
        """
        Chat with your BerryDB database after successfully embedding it.
        This method is used for evaluating the LLM response and context.

        Args:
                llm_api_key (str): LLM API key to embed the database [OpenAI, HuggingFace, ...]
                question (str): Query/Question to for your database
                embedding_model_api_key (str): The API key/token of your embedding model (Only used if the embedding and chat providers do not match)

        Returns:
                dict: Includes the answer and the context for the answer from BerryDB
        """

        url = bdb_constants.BERRY_GPT_BASE_URL + chat_with_database_url

        body = {
            key: value
            for key, value in {
                "question": question,
                "database": self.__database_name,
                "orgName": self.__org_name,
                "apiKey": self.__api_key,
                "llmApiKey": llm_api_key,
                "embeddingApiKey": embedding_model_api_key,
                "settingsName": self.__settings_name,
            }.items()
            if value is not None
        }
        if self.__settings_name is None:
            body["settings"] = self.__settings.__dict__

        if debug_mode:
            print("url:", url)
            print("body:", body)
        payload = json.dumps(body)
        headers = Utils.get_headers(self.__api_key)

        try:
            response = requests.post(url, headers=headers, data=payload)
            if response.status_code != 200:
                Utils.handleApiCallFailure(response.json(), response.status_code)
            res = response.json()
            if debug_mode:
                print("Database chat result: ", res)
            return res
        except Exception as e:
            errMsg = "Failed to chat with the database. Please try again later."
            print(f"{errMsg}, reason : {str(e)}")
            raise e

    def similarity_search(self, llm_api_key:str, query:str):

        url = bdb_constants.BERRY_GPT_BASE_URL + bdb_constants.similarity_search_url
        body = {
            "question": query,
            "database": self.__database_name,
            "orgName": self.__org_name,
            "apiKey": self.__api_key,
            "llmApiKey": llm_api_key,
            "embeddingApiKey": llm_api_key,
            "settingsName": self.__settings_name,
        }
        if self.__settings_name is None:
            body["settings"] = self.__settings.__dict__

        if debug_mode:
            print("url:", url)
            print("body:", body)
        payload = json.dumps(body)
        response = requests.post(url, data=payload)
        if response.status_code != 200:
            Utils.handleApiCallFailure(response.json(), response.status_code)
        return response.json()

    def ingest_pdf(self, file_list, extract_json_path=None):
        """Ingests a list of PDF files and extracts their content.

        Args:
            file_list (list[File]): List of PDF files to be processed.
            extract_json_path (str, optional): Path to save the extracted data in JSON format. Defaults to None, which saves the data under 'content'.

        Returns:
            Returns a list of extracted documents. Otherwise, returns a success/failure message.

        """
        try:
            if type(file_list) is str:
                file_list = [file_list]
            if not file_list or not len(file_list):
                raise ValueError("At least one file must be provided")
            if len(file_list) > 5:
                raise ValueError("Exceeded maximum allowed files (5)")

            for file in file_list:
                if not file.endswith(".pdf"):
                    raise ValueError("All files must be of type PDF")

            extract_json_path = extract_json_path or "content"

            Utils.validate_json_path(extract_json_path)

            files = []
            for file_path in file_list:
                files.append(("files", open(file_path, "rb")))

            url = bdb_constants.BERRY_GPT_BASE_URL + extract_pdf_url

            params = {
                "databaseName": self.__database_name,
                "apiKey": self.__api_key,
                "extractJsonPath": extract_json_path,
            }

            if debug_mode:
                print("url:", url)
                print("params:", params)

            response = requests.post(url, files=files, params=params)

            if response.status_code == 200:
                print("Success")
                response_json = response.json()
                if response_json["success"]:
                    return response_json["message"]
            else:
                print(f"Failed with ingest PDFs, status code: {response.status_code}")
        except Exception as e:
            print(f"Failed with ingest PDFs, reason: {e}")
            if debug_mode:
                raise e

    # Sematic Extraction methods
    def ner(self, json_path, document_ids=[], annotate=False):
        """Function summary

        Args:
                arg1 (str): JSON path to the object you want to extract semantic for
                arg2 (str): document IDs of the documents you want to extract the data of (optional)
                arg3 (str): Add sematic data to the document (optional)

        Returns:
                list | str: sematic data | hash
        """
        extraction_type = NER_SE_TYPE
        try:
            return self.__semantic_extraction_base(extraction_type, json_path, document_ids, None, annotate)

        except Exception as e:
            logger.exception("Failed to extract semantics for {}, reason: {}".format(extraction_type, str(e)))
            raise e

    def medical_ner(self, json_path, document_ids=[], annotate=False):
        """Function summary

        Args:
                arg1 (str): JSON path to the object you want to extract semantic for
                arg2 (str): document IDs of the documents you want to extract the data of (optional)
                arg3 (str): Add sematic data to the document (optional)

        Returns:
                list | str: sematic data | hash
        """
        extraction_type = MEDICAL_NER_SE_TYPE
        try:
            return self.__semantic_extraction_base(extraction_type, json_path, document_ids, None, annotate)

        except Exception as e:
            logger.exception("Failed to extract semantics for {}, reason: {}".format(extraction_type, str(e)))
            raise e

    def text_summarization(self, json_path, document_ids=[], annotate=False):
        """Function summary

        Args:
                arg1 (str): JSON path to the object you want to extract semantic for
                arg2 (str): document IDs of the documents you want to extract the data of (optional)
                arg3 (str): Add sematic data to the document (optional)

        Returns:
                list | str: sematic data | hash
        """
        extraction_type = TEXT_SUMMARIZATION_SE_TYPE
        try:
            return self.__semantic_extraction_base(extraction_type, json_path, document_ids, None, annotate)

        except Exception as e:
            logger.exception("Failed to extract semantics for {}, reason: {}".format(extraction_type, str(e)))
            raise e

    def image_classification(self, json_path, labels, document_ids=[], annotate=False):
        """Function summary

        Args:
                arg1 (str): JSON path to the object you want to extract semantic for
                arg2 (str): Labels for the classification of text
                arg3 (str): document IDs of the documents you want to extract the data of (optional)
                arg4 (str): Add sematic data to the document (optional)

        Returns:
                list | str: sematic data | hash
        """
        extraction_type = IMAGE_CLASSIFICATION_SE_TYPE
        try:
            return self.__semantic_extraction_base(extraction_type, json_path, document_ids, labels, annotate)

        except Exception as e:
            logger.exception("Failed to extract semantics for {}, reason: {}".format(extraction_type, str(e)))
            raise e

    def image_captioning(self, json_path, document_ids=[], annotate=False):
        """Function summary

        Args:
                arg1 (str): JSON path to the object you want to extract semantic for
                arg2 (str): document IDs of the documents you want to extract the data of (optional)
                arg3 (str): Add sematic data to the document (optional)

        Returns:
                list | str: sematic data | hash
        """
        extraction_type = IMAGE_CAPTIONING_SE_TYPE
        try:
            return self.__semantic_extraction_base(extraction_type, json_path, document_ids, None, annotate)

        except Exception as e:
            logger.exception("Failed to extract semantics for {}, reason: {}".format(extraction_type, str(e)))
            raise e

    def pneumonia_detection(self, json_path, document_ids=[], annotate=False):
        """Function summary

        Args:
                arg1 (str): JSON path to the object you want to extract semantic for
                arg2 (str): document IDs of the documents you want to extract the data of (optional)
                arg3 (str): Add sematic data to the document (optional)

        Returns:
                list | str: sematic data | hash
        """
        extraction_type = PNEUMONIA_SE_TYPE
        try:
            return self.__semantic_extraction_base(extraction_type, json_path, document_ids, None, annotate)

        except Exception as e:
            logger.exception("Failed to extract semantics for {}, reason: {}".format(extraction_type, str(e)))
            raise e

    def alzheimer_detection(self, json_path, document_ids=[], annotate=False):
        """Function summary

        Args:
                arg1 (str): JSON path to the object you want to extract semantic for
                arg2 (str): document IDs of the documents you want to extract the data of (optional)
                arg3 (str): Add sematic data to the document (optional)

        Returns:
                list | str: sematic data | hash
        """
        extraction_type = ALZHEIMER_SE_TYPE
        try:
            return self.__semantic_extraction_base(extraction_type, json_path, document_ids, None, annotate)

        except Exception as e:
            logger.exception("Failed to extract semantics for {}, reason: {}".format(extraction_type, str(e)))
            raise e

    def fashion(self, json_path, document_ids=[], annotate=False):
        """Function summary

        Args:
                arg1 (str): JSON path to the object you want to extract semantic for
                arg2 (str): document IDs of the documents you want to extract the data of (optional)
                arg3 (str): Add sematic data to the document (optional)

        Returns:
                list | str: sematic data | hash
        """
        extraction_type = FASHION_SE_TYPE
        try:
            return self.__semantic_extraction_base(extraction_type, json_path, document_ids, None, annotate)

        except Exception as e:
            logger.exception("Failed to extract semantics for {}, reason: {}".format(extraction_type, str(e)))
            raise e

    def audio_transcription(self, json_path, document_ids=[], annotate=False):
        """Function summary

        Args:
                arg1 (str): JSON path to the object you want to extract semantic for
                arg2 (str): document IDs of the documents you want to extract the data of (optional)
                arg3 (str): Add sematic data to the document (optional)

        Returns:
                list | str: sematic data | hash
        """
        extraction_type = AUDIO_TRANSCRIPTION_SE_TYPE
        try:
            return self.__semantic_extraction_base(extraction_type, json_path, document_ids, None, annotate)

        except Exception as e:
            logger.exception("Failed to extract semantics for {}, reason: {}".format(extraction_type, str(e)))
            raise e

    def text_classification(self, json_path, labels, document_ids=[], annotate=False):
        """Function summary

        Args:
                arg1 (str): JSON path to the object you want to extract semantic for
                arg2 (str): Labels for the classification of text
                arg3 (str): document IDs of the documents you want to extract the data of (optional)
                arg4 (str): Add sematic data to the document (optional)

        Returns:
                list | str: sematic data | hash
        """
        extraction_type = TEXT_CLASSIFICATION_SE_TYPE
        if not (labels and len(labels)):
            raise ValueError(f"Labels are required for {extraction_type} to classify the text.")
        try:

            return self.__semantic_extraction_base(extraction_type, json_path, document_ids, labels, annotate)

        except Exception as e:
            logger.exception("Failed to extract semantics for {}, reason: {}".format(extraction_type, str(e)))
            raise e

    def __semantic_extraction_base(self, extraction_type, json_path, document_ids=None, labels=None, annotate=False):

        if not json_path:
            raise ValueError("JSON path is required")
        if not annotate and not (document_ids and len(document_ids)):
            raise ValueError("Document IDs are required if you are not annotating the document")

        url = bdb_constants.BASE_URL + SEMANTICS_PREDICT_URL
        if annotate:
            url = bdb_constants.BASE_URL + SEMANTICS_ANNOTATE_URL

        params = {
            "apiKey": self.__api_key,
        }

        body = {
            "databaseName": self.__database_name,
            "documentIds": document_ids,
            "extract": extraction_type,
            "jsonPath": json_path,
        }

        if labels and len(labels):
            body["labels"] = labels

        payload = json.dumps(body)
        headers = Utils.get_headers(self.__api_key)

        logger.debug("url:" + url)
        logger.debug("params:" + repr(params))
        logger.debug("payload:" + payload)
        logger.debug("headers:" + repr(headers))

        if not annotate:
            print("Retrieving predictions for documents with IDs ", document_ids)
        from requests import Response
        response: Response = requests.post(url, params=params, data=payload, headers=headers)

        if response.status_code == 200:
            if not annotate:
                print("Predictions retrieved Successfully!")
            return response.json()

        if not annotate:
            print("Failed to retrieve predictions!")
        Utils.handleApiCallFailure(response.json(), response.status_code)

    def label_summary(self):
        url = bdb_constants.ML_BACKEND_BASE_URL + label_summary_url
        headers = {
            "Content-Type": "application/json"
        }
        data = {
            "databaseName": self.database_name(),
            "apiKey": self.api_key()
        }

        try:
            print("Starting to summarize labels for database: ", self.database_name())
            response = requests.post(url, headers=headers, json=data)
            if response.status_code != 200:
                Utils.handleApiCallFailure(response.json(), response.status_code)

            print("Response:", response.json())
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error while summarizing database: {e}")
            return None

    def evaluator(self, llm_api_key:str, embedding_api_key: str | None = None, metrics_database_name="EvalMetricsDB"):
        from evaluator.berrydb_rag_evaluator import BerryDBRAGEvaluator
        return BerryDBRAGEvaluator(
                    api_key=self.__api_key,
                    settings=self.__settings,
                    llm_api_key=llm_api_key,
                    database=self,
                    embedding_api_key=embedding_api_key,
                    metrics_database_name=metrics_database_name,
                )