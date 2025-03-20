from typing import Iterable, Generator
from xml.etree.ElementTree import fromstring, Element

from .llm import LLM
from .types import PageInfo, TextInfo, TextIncision
from .splitter import group, allocate_segments, get_and_clip_pages, PageXML
from .asset_matcher import AssetMatcher, ASSET_TAGS
from .chunk_file import ChunkFile
from .utils import encode_response


def analyse_citations(
    llm: LLM,
    file: ChunkFile,
    pages: list[PageInfo],
    request_max_tokens: int,
    tail_rate: float,
  ):
  prompt_tokens = llm.prompt_tokens_count("citation", {})
  data_max_tokens = request_max_tokens - prompt_tokens
  if data_max_tokens <= 0:
    raise ValueError(f"Request max tokens is too small (less than system prompt tokens count {prompt_tokens})")

  for start_idx, end_idx, task_group in file.filter_groups(group(
    max_tokens=data_max_tokens,
    gap_rate=tail_rate,
    tail_rate=1.0,
    items=allocate_segments(
      text_infos=_extract_citations(pages),
      max_tokens=data_max_tokens,
    ),
  )):
    page_xml_list = get_and_clip_pages(
      llm=llm,
      group=task_group,
      get_element=lambda i: _get_citation_with_file(pages, i),
    )
    raw_pages_root = Element("pages")
    for i, page_xml in enumerate(page_xml_list):
      element = page_xml.xml
      element.set("idx", str(i + 1))
      raw_pages_root.append(element)

    asset_matcher = AssetMatcher().register_raw_xml(raw_pages_root)
    response = llm.request("citation", raw_pages_root, {})

    response_xml = encode_response(response)
    chunk_xml = Element("chunk", {
      "start-idx": str(start_idx + 1),
      "end-idx": str(end_idx + 1),
    })
    asset_matcher.add_asset_hashes_for_xml(response_xml)

    for citation in _search_and_filter_and_split_citations(
      response_xml=response_xml,
      page_xml_list=page_xml_list,
    ):
      chunk_xml.append(citation)

    file.atomic_write_chunk(start_idx, end_idx, chunk_xml)

def _extract_citations(pages: Iterable[PageInfo]) -> Generator[TextInfo, None, None]:
  citations_matrix: list[list[TextInfo]] = []
  current_citations: list[TextInfo] = []

  for page in pages:
    citation = page.citation
    if citation is not None:
      current_citations.append(citation)
    elif len(current_citations) > 0:
      citations_matrix.append(current_citations)
      current_citations = []

  if len(current_citations) > 0:
    citations_matrix.append(current_citations)

  for citations in citations_matrix:
    citations[0].start_incision = TextIncision.IMPOSSIBLE
    citations[-1].end_incision = TextIncision.IMPOSSIBLE

  for citations in citations_matrix:
    yield from citations

def _get_citation_with_file(pages: list[PageInfo], index: int) -> Element:
  page = next((p for p in pages if p.page_index == index), None)
  assert page is not None
  assert page.citation is not None

  with page.file() as file:
    root: Element = fromstring(file.read())
    citation = root.find("citation")
    for child in citation:
      if child.tag not in ASSET_TAGS:
        child.attrib = {}
    return citation

def _search_and_filter_and_split_citations(response_xml: Element, page_xml_list: list[PageXML]):
  for citation in response_xml:
    page_indexes: list[int] = [int(p) for p in citation.get("idx").split(",")]
    page_indexes.sort()
    page_xml = page_xml_list[page_indexes[0] - 1]

    if page_xml.is_gap:
      continue

    attributes = {
      **citation.attrib,
      "idx": ",".join([
        str(page_xml_list[p - 1].page_index + 1)
        for p in page_indexes
      ]),
    }
    # after testing, LLM will merge multiple citations together, which will result in multiple
    # labels for one citation. the code here handles this as a backup.
    splitted_citation: Element | None = None

    for child in citation:
      if child.tag == "label":
        if splitted_citation is not None:
          yield splitted_citation
        splitted_citation = Element("citation", {**attributes})

      if splitted_citation is not None:
        splitted_citation.append(child)

    if splitted_citation is not None:
      yield splitted_citation
