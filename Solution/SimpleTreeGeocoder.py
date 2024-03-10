from api import API, TreeNode
from geocoders.geocoder import Geocoder

class SimpleTreeGeocoder(Geocoder):
    def __init__(self, samples: int | None = None, data: list[TreeNode] | None = None):
        super().__init__(samples=samples)
        if data is None:
            self.__data = API.get_areas()
        else:
            self.__data = data

    def _apply_geocoding(self, area_id: str) -> str:
        """
        Геокодирование области с использованием метода обхода дерева.
        """
        # Находим узел дерева с заданным area_id
        node = self._find_node_by_id(self.__data, area_id)
        # Собираем адрес обходом дерева к корню
        address_parts = []
        while node:
            address_parts.insert(0, node.address)
            node = self._find_node_by_id(self.__data, node.parent_id)
        return ', '.join(address_parts)

    def _find_node_by_id(self, nodes: list[TreeNode], area_id: str) -> TreeNode | None:
        """
        Поиск узла по его ID в списке узлов.
        """
        for node in nodes:
            if node.area_id == area_id:
                return node
            if node.children:
                found_node = self._find_node_by_id(node.children, area_id)
                if found_node:
                    return found_node
        return None
