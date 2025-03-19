import json

from httpx import AsyncClient, Client

from get_car_info.base import BaseCarInfo
from get_car_info.models import CarSnapshotModel


class CarInfo(BaseCarInfo):
    class Auth(BaseCarInfo.Auth["CarInfo"]):
        def _get_auth_data(self, car_number: str) -> tuple:
            res = self.car_info._client.get(f"order/create?object={car_number}&mode=gosnumber")
            return self._parse_auth_data(res)

    class API(BaseCarInfo.API["CarInfo"]):
        def _get_result(self, car_number: str) -> dict:
            token, snapshot = self.car_info.auth._get_auth_data(car_number)
            res = self.car_info._client.post("livewire/update", json=self._get_json_data(token, snapshot))
            res = res.json().get("components")[0].get("snapshot")
            return json.loads(res)

    def __init__(self) -> None:
        super().__init__()
        self._client = Client(base_url="https://vinvision.ru/")

    def get_data(self, car_number: str) -> CarSnapshotModel:
        res = self.api._get_result(car_number)

        try:
            first_result = res.get("data").get("details")[0].get("result")[0]
        except Exception:
            raise ValueError("I doesn't found your car...") from None
        res = {i.lower(): k for i, k in first_result.items()}

        return self._get_model(CarSnapshotModel, res)


class AsyncCarInfo(BaseCarInfo):
    class Auth(BaseCarInfo.Auth["AsyncCarInfo"]):
        async def _get_auth_data(self, car_number: str) -> tuple:
            res = await self.car_info._client.get(f"order/create?object={car_number}&mode=gosnumber")
            return self._parse_auth_data(res)

    class API(BaseCarInfo.API["AsyncCarInfo"]):
        async def _get_result(self, car_number: str) -> dict:
            token, snapshot = await self.car_info.auth._get_auth_data(car_number)
            res = await self.car_info._client.post("livewire/update", json=self._get_json_data(token, snapshot))
            res = res.json().get("components")[0].get("snapshot")
            return json.loads(res)

    def __init__(self) -> None:
        super().__init__()
        self._client = AsyncClient(base_url="https://vinvision.ru/")

    async def get_data(self, car_number: str) -> CarSnapshotModel:
        res = await self.api._get_result(car_number)

        try:
            first_result = await res.get("data").get("details")[0].get("result")[0]
        except Exception:
            raise ValueError("I doesn't found your car...") from None
        res = {i.lower(): k for i, k in first_result.items()}

        return self._get_model(CarSnapshotModel, res)