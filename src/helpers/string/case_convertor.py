class CaseConvertor:
    @staticmethod
    def to_camel_case(snake_case: str, capital_first: bool = False) -> str:
        res = ''
        index = 0
        tokens = snake_case.split('_')
        if not capital_first:
            res = tokens[index]
            index += 1
        res += ''.join(token.title() for token in tokens[index:])
        return res
