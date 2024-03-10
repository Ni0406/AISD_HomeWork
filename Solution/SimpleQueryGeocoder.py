import requests
from api import API, TreeNode
from geocoders.geocoder import Geocoder

class SimpleQueryGeocoder(Geocoder):
    def _apply_geocoding(self, area_id: str) -> str:
        """
        Геокодирование области с использованием простого запроса.
        """
        # Выполняем запрос к API, чтобы получить данные об области по её ID
        area_data = API.get_area_by_id(area_id)
        # Получаем адрес области
        address = area_data['address']
        # Если у области есть родительская область, получаем её ID и выполняем рекурсивный запрос
        while area_data.get('parent_id'):
            area_data = API.get_area_by_id(area_data['parent_id'])
            address = f"{area_data['address']}, {address}"
        return address
