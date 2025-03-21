import asyncio
import ssl
from contextlib import contextmanager
from typing import (
    Generator,
    List,
    TypeVar,
    Generic,
    Annotated,
    Optional,
    Type,
    Tuple,
    Any,
    Callable,
)

from pydantic import ConfigDict

import httpx
from loguru import logger
from pydantic import BaseModel, Field
from pydantic.alias_generators import to_camel
from tenacity import retry, wait_exponential


from .models.emass_models import EmassSystemBase
from .settings import get_settings

T = TypeVar("T")
DType = TypeVar("DType", bound=BaseModel)

EMASS_ORG_ID = 1179


class MetaRequestResponse(BaseModel):
    code: int


class ResponsePage(BaseModel):
    total_count: int
    total_pages: int
    page_index: int
    page_size: int
    prev_page_url: Optional[str] = None
    next_page_url: Optional[str] = None

    model_config = ConfigDict(alias_generator=to_camel)


class EmassApiResponse(BaseModel, Generic[T]):
    meta: MetaRequestResponse
    data: T
    pagination: Optional[ResponsePage] = None


@contextmanager
def get_http_client() -> Generator[httpx.AsyncClient, None, None]:
    settings = get_settings()
    cert = (
        f"{settings.client_cert_path}",
        f"{settings.client_cert_key_path}",
        settings.client_cert_key_pass,
    )

    headers = {"api-key": settings.api_key}

    timeout = httpx.Timeout(connect=10, read=60 * 3, write=10, pool=10)

    yield httpx.AsyncClient(
        base_url=settings.api_url,
        headers=headers,
        cert=cert,
        verify=ssl.create_default_context(),
        timeout=timeout,
    )


async def make_initial_test_connection() -> None:
    with get_http_client() as client:
        r = await client.get("/api")

    r.raise_for_status()
    response = EmassApiResponse.model_validate(r.json())
    logger.info(response.data)


async def generate_api_key() -> None:
    class ApiKeyResponse(BaseModel):
        api_key: Annotated[str, Field(alias="api-key")]

    with get_http_client() as client:
        r = await client.post("/api/api-key")

    r.raise_for_status()
    response = EmassApiResponse[ApiKeyResponse].model_validate(r.json())

    print(response.data.api_key)


async def get_systems() -> List[EmassSystemBase]:
    with get_http_client() as client:
        r = await client.get("/api/systems", params={"includeDecommissioned": False})

    r.raise_for_status()

    response = EmassApiResponse[List[EmassSystemBase]].model_validate(r.json())

    return __return_data(EmassSystemBase, response.data)


@retry(wait=wait_exponential(multiplier=1, min=1, max=6))
async def get_dashboard_payload_helper(
    dashboard: str,
    page_size: int = 10,
    page_index: int = 0,
    client: Optional[httpx.AsyncClient] = None,
) -> Any:
    async def execute(_client: httpx.AsyncClient) -> httpx.Response:
        _r = await client.get(
            f"/api/dashboards/{dashboard}",
            params={
                "pageSize": page_size,
                "pageIndex": page_index,
                "orgId": EMASS_ORG_ID,
            },
            follow_redirects=True,
        )
        _r.raise_for_status()

        return _r

    if not client:
        with get_http_client() as client:
            r = await execute(client)

    else:
        r = await execute(client)

    return r.json()


async def get_dashboard_payload(
    model_type: Type[DType],
    dashboard: str,
    page_size: int = 10,
    page_index: int = 0,
    client: Optional[httpx.AsyncClient] = None,
) -> Tuple[int, List[DType]]:
    logger.info(
        f"Pulling Dashboard Payload [{model_type.__name__} | {dashboard}] with page size {page_size} for page index {page_index}"
    )

    r = await get_dashboard_payload_helper(dashboard, page_size, page_index, client)
    response = EmassApiResponse[List[model_type]].model_validate(r)

    data = __return_data(model_type, response.data)

    logger.info(
        f"Finished Pulling Dashboard Payload [{model_type.__name__} | {dashboard}] at page index {page_index}"
    )
    return response.pagination.total_pages, data


async def load_all_dashboard_data_in_batches(
    loader_handler: Callable[[List[DType]], None],
    model_type: Type[DType],
    dashboard: str,
    batch_size: int = 50,
    sleep_time: int = 10,
    page_size: int = 20000,
) -> None:
    current_page = 0
    logger.info(f"Pulling APs with page size {page_size}")
    with get_http_client() as client:
        (
            total_pages,
            first_results,
        ) = await get_dashboard_payload(
            model_type=model_type,
            dashboard=dashboard,
            page_size=page_size,
            page_index=current_page,
            client=client,
        )
        loader_handler(first_results)

        async def __load_payload_into_db(
            page_index: int,
        ) -> None:
            _, data = await get_dashboard_payload(
                model_type=model_type,
                dashboard=dashboard,
                page_size=page_size,
                page_index=page_index,
                client=client,
            )

            loader_handler(data)

        futures = [
            __load_payload_into_db(page_index)
            for page_index in range(1, total_pages)
        ]

        if len(futures) > batch_size:
            for i in range(0, len(futures), batch_size):
                await asyncio.gather(*futures[i : i + batch_size])
                logger.info(f"Sleeping for {sleep_time} seconds...")
                await asyncio.sleep(sleep_time)
        else:
            await asyncio.gather(*futures)



def __return_data(model_type: Type[DType], data: List[DType]) -> List[DType]:
    all_data = []
    for item in data:
        all_data.append(model_type.model_validate(item))

    return all_data

