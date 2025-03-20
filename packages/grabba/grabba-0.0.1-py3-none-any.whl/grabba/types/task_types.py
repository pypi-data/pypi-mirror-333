from typing import List, Optional, Union
from dataclasses import dataclass

from .enums import (
    JobTaskType,
    WebDataSelectorType, SpecificDataExtractionType,
    SpecificDataExtractionOutputFormat, WebScreenCaptureFormat, 
    StructuredDataExtractionAttribute, PdfPaperFormat, PdfOrientation
)

# Data Models
@dataclass
class WebDataSelector:
    type: WebDataSelectorType
    value: str

@dataclass
class StructuredDataExtractionParameter:
    name: str
    selector: Optional[WebDataSelector] = None
    parentSelector: Optional[WebDataSelector] = None
    attribute: Optional[StructuredDataExtractionAttribute] = None
    customAttribute: Optional[str] = None
    sample: Optional[str] = None

@dataclass
class StructuredDataExtractionOptions:
    parameters: List[StructuredDataExtractionParameter]
    autoPopulateParameters: bool
    parseWithAI: bool
    executeWithAI: bool
    parentSelector: Optional[WebDataSelector] = None

@dataclass
class FormDataExtractionOptions:
    selector: Optional[WebDataSelector] = None

@dataclass
class TableDataExtractionOptions:
    selector: Optional[WebDataSelector] = None

@dataclass
class PresetDataExtractionOptions:
    selector: Optional[WebDataSelector] = None

@dataclass
class CustomDataExtractionOptions:
    regexPattern: Optional[str] = None
    selector: Optional[WebDataSelector] = None

@dataclass
class SpecificDataExtractionOptions:
    type: SpecificDataExtractionType
    options: Union[PresetDataExtractionOptions, TableDataExtractionOptions, FormDataExtractionOptions, StructuredDataExtractionOptions, None]
    maxResults: int
    outputFormat: SpecificDataExtractionOutputFormat

@dataclass
class WebScreenCaptureOptions:
    format: Optional[WebScreenCaptureFormat] = None
    fullPage: Optional[bool] = None
    omitBackground: Optional[bool] = None
    pdfFormat: Optional[PdfPaperFormat] = None
    pdfOrientation: Optional[PdfOrientation] = None
    pdfPrintBackground: Optional[bool] = None

@dataclass
class WebpageAsMarkdownOptions:
    onlyMainContent: Optional[bool] = None

@dataclass
class JobTask:
    type: JobTaskType
    options: Optional[Union[SpecificDataExtractionOptions, WebpageAsMarkdownOptions, WebScreenCaptureOptions]] = None
