import re
from typing import Dict, List, Optional


class BaseProcessor:
    """XML处理器基类"""
    @classmethod
    def compile(cls, xml: str) -> str:
        raise NotImplementedError

    @staticmethod
    def retrieve(dict_, keys):
        """字典解构赋值
        params = {'a': 1, 'b': 2}
        a, b = get(params, ['a', 'b'])
        a, c = get(params, ['a', 'c'])
        """
        tmp = ()
        for key in keys:
            tmp += (dict_.get(key),)
        return tmp

    @classmethod
    def _process_tag(cls, xml: str, pattern: str, process_func) -> str:
        """通用标签处理方法"""
        return re.sub(pattern, process_func, xml, flags=re.DOTALL)

    @classmethod
    def _extract_attrs(cls, attrs_str: str, attr_names: List[str]) -> Dict[str, Optional[str]]:
        """提取属性值"""
        result = {}
        for name in attr_names:
            match = re.search(f'{name}="([^"]*)"', attrs_str)
            result[name] = match.group(1) if match else None
        return result

    @classmethod
    def _build_props(cls, props: List[str], indent: str = '') -> str:
        """构建属性字符串"""
        if not props:
            return ''
        return f'\n{indent}' + f'\n{indent}'.join(props) + f'\n{indent}'
