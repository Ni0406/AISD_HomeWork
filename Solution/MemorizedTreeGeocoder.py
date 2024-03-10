from api import API, TreeNode
from geocoders.geocoder import Geocoder

class MemorizedTreeGeocoder(Geocoder):
    def __init__(self, samples: int | None = None, data: list[TreeNode] | None = None):
        super().__init__(samples=samples)
        if data is None:
            self.__data = API.get_areas()
        else:
            self.__data = data
        self.__address_dict = {}

        # Заполняем словарь адресов во время инициализации
        self._populate_address_dict()

    def _populate_address_dict(self):
        """
        Заполняем словарь адресов, обходя дерево.
        """
        for node in self.__data:
            address = self._get_full_address(node)
            self.__address_dict[node.area_id] = address

    def _get_full_address(self, node: TreeNode) -> str:
        """
        Получаем полный адрес узла и всех его родительских узлов.
        """
        address_parts = [node.address]
        parent_id = node.parent_id
        while parent_id:
            parent_node = self._find_node_by_id(self.__data, parent_id)
            address_parts.insert(0, parent_node.address)
            parent_id = parent_node.parent_id
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

    def _apply_geocoding(self, area_id: str) -> str:
        """
        Геокодирование области с использованием метода запоминания дерева.
        """
        return self.__address_dict.get(area_id, "Адрес не найден")
