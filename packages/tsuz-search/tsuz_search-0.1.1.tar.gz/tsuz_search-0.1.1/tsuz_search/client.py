from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import requests


class PackageName(BaseModel):
    code: int
    mxikCode: str
    nameUz: str
    packageType: str
    nameRu: str
    nameLat: str


class MxikSearchItem(BaseModel):
    mxikCode: str
    name: str
    description: Optional[str] = None
    internationalCode: Optional[str] = None
    label: Optional[str] = None
    fullName: Optional[str] = None
    groupCode: Optional[str] = None
    groupName: Optional[str] = None
    classCode: Optional[str] = None
    className: Optional[str] = None
    positionCode: Optional[str] = None
    positionName: Optional[str] = None
    subPositionCode: Optional[str] = None
    subPositionName: Optional[str] = None
    brandCode: Optional[str] = None
    brandName: Optional[str] = None
    attributeName: Optional[str] = None
    usePackage: Optional[str] = None
    categoryUnitId: Optional[Any] = None
    categoryUnitName: Optional[str] = None
    unitsName: Optional[str] = None
    surveyCategoryId: Optional[str] = None
    nonChangeable: Optional[str] = None
    lgotaId: Optional[Any] = None
    lgotaName: Optional[Any] = None
    recommendedCategoryUnitName: Optional[Any] = None
    recommendedUnitsName: Optional[Any] = None
    packageName: Optional[Any] = None
    useCard: Optional[Any] = None
    property: Optional[Any] = None
    categoryCode: Optional[str] = None
    categoryName: Optional[str] = None
    mnnName: Optional[Any] = None


class MxikData(BaseModel):
    id: str
    pkey: Optional[Any] = None
    parentPkey: Optional[Any] = None
    mxikCode: str
    groupNameUz: str
    groupNameRu: str
    groupNameLat: Optional[str] = None
    classNameUz: str
    classNameRu: str
    classNameLat: Optional[str] = None
    positionNameUz: str
    positionNameRu: str
    positionNameLat: Optional[str] = None
    subPositionNameUz: str
    subPositionNameRu: str
    subPositionNameLat: Optional[str] = None
    brandName: Optional[str] = None
    attributeNameUz: Optional[str] = None
    attributeNameRu: Optional[str] = None
    attributeNameLat: Optional[str] = None
    description: Optional[str] = None
    isActive: str
    createdAt: str
    updatedBy: Optional[str] = None
    updatedAt: str
    status: int
    packageNames: List[PackageName] | None = None


class MxikResponse(BaseModel):
    success: bool
    code: int
    reason: str
    data: MxikData | None = None
    errors: Optional[Any] = None


class SearchResponse(BaseModel):
    success: bool
    code: int
    reason: str
    data: list[MxikSearchItem] | None = None
    errors: Optional[Any] = None


class SearchParams(BaseModel):
    params: Dict[str, Any]
    size: int = 20
    page: int = 0
    lang: str = "uz"


class ElasticSearch(BaseModel):
    search: str
    size: int = 20
    page: int = 0
    lang: str = "uz"


class Client:
    def __init__(self, base_url: str = "https://tasnif.soliq.uz/api/cls-api"):
        self.base_url = base_url

    def get_by_mxik_code(self, mxik_code: str) -> MxikResponse:
        response = requests.get(
            f"{self.base_url}/integration-mxik/get/history/{mxik_code}",
        )
        print("Response for get_by_mxik_code: ", response.json())
        return MxikResponse(**response.json())

    def search(self, params: ElasticSearch) -> List[MxikData]:

        response = requests.get(
            f"{self.base_url}/elasticsearch/search", params=params.model_dump()
        )
        print("Response for search: ", response.json())
        return SearchResponse(**response.json())

    def search_by_params(self, params: SearchParams) -> List[MxikData]:

        params = params.model_dump()
        for key, value in params["params"].items():
            params[key] = value
        del params["params"]

        response = requests.get(f"{self.base_url}/mxik/search/by-params", params=params)
        return SearchResponse(**response.json())

    def search_dv_cert(self, params: SearchParams) -> List[MxikData]:
        response = requests.get(
            f"{self.base_url}/mxik/search/dv-cert-number", params=params.model_dump()
        )
        print(response.json())
        return SearchResponse(**response.json())
