import json
import re
import typing

nlp_like = {
    "(\\w+) contains (\\w+)": 'CONTAINS(\\1, "\\2")',
    "(\\w+) is (\\w+)": '\\1 == "\\2"',
    "(\\w+) startswith (\\w+)": '\\1.startswith("\\2")',
    "(\\w+) endswith (\\w+)": '\\1.endswith("\\2")',
    "(\\w+) pattern of (.*)": 'REGEX(\\1, "\\2")',
}


def regex_func(x, y, ignore_case=True):
    if ".*" not in y:
        y = y.replace("*", ".*")

    if ".?" not in y:
        y = y.replace("?", ".?")

    try:
        return re.fullmatch(y, x, re.IGNORECASE if ignore_case else 0) is not None
    except re.error:
        return False


funcs_maps = {
    "CONTAINS": lambda container, substring: substring in container,
    "REGEX": lambda x, y, ignore_case=False: regex_func(x, y, ignore_case),
    "REGEXI": regex_func,
}


def _parse_symbols_logic2(query: str):
    in_quote = False
    current_quote = None
    i = 0
    while i < len(query):
        char = query[i]
        if char in "\"'":
            if not in_quote:
                current_quote = char
                in_quote = True
            elif char == current_quote:
                in_quote = False
            i += 1
            continue

        if not in_quote and char in "&|!":
            if char == "&":
                query = query[:i] + " and " + query[i + 1 :]
                i += 5
            elif char == "|":
                query = query[:i] + " or " + query[i + 1 :]
                i += 4
            elif char == "!":
                query = query[:i] + " not " + query[i + 1 :]
                i += 5
        else:
            i += 1

    return query


def _parse_symbols_logic(query: str):
    in_quote = False
    current_quote = None
    i = 0
    query_list = list(query)
    while i < len(query_list):
        char = query_list[i]
        if char in "\"'":
            if not in_quote:
                current_quote = char
                in_quote = True
            elif char == current_quote:
                in_quote = False
            i += 1
            continue

        if not in_quote:
            if char == "&" and i + 1 < len(query_list) and query_list[i + 1] == "&":
                query_list[i : i + 2] = list(" and ")
                i += 5
            elif char == "|" and i + 1 < len(query_list) and query_list[i + 1] == "|":
                query_list[i : i + 2] = list(" or ")
                i += 4
            elif char == "!":
                query_list[i : i + 1] = list(" not ")
                i += 5
            else:
                i += 1
        else:
            i += 1

    return "".join(query_list)


def _collapse_spaces(query: str):
    new_query = []
    in_quote = False
    current_quote = None
    prev_was_space = False

    for char in query:
        if char in "\"'":
            if not in_quote:
                current_quote = char
                in_quote = True
            elif char == current_quote:
                in_quote = False
            new_query.append(char)
            prev_was_space = False
        elif in_quote:
            new_query.append(char)
            prev_was_space = False
        else:
            if char == " ":
                if not prev_was_space:
                    new_query.append(" ")
                prev_was_space = True
            else:
                new_query.append(char)
                prev_was_space = False

    return "".join(new_query)


class QueryObj:
    @classmethod
    def parse(cls, query: str):
        stats = {"isCompound": False, "simple": False}

        # if theres no space in query, consider it as a regex pattern
        if " " not in query and "(" not in query:
            query = 'REGEX(__default__, "{query}")'.replace("{query}", query)
            stats["simple"] = True
        elif " and " in query or " or " in query or "not " in query:
            stats["isCompound"] = True
        elif (
            any(char in query for char in ["&&", "||", "!"])
            and (query2 := _parse_symbols_logic(query)) != query
        ):
            stats["isCompound"] = True
            query = query2
        elif (
            any(char in query for char in "&|!")
            and (query2 := _parse_symbols_logic2(query)) != query
        ):
            stats["isCompound"] = True
            query = query2

        # match all the nlp like queries and replace them to correct value
        if not stats["simple"]:
            for pattern, replacement in nlp_like.items():
                query = re.sub(pattern, replacement, query)

        # Collapse multiple spaces outside quotes
        query = _collapse_spaces(query)
        query = query.strip()

        return QueryObj(query, stats)

    def __init__(self, query: str, stats: dict, verify : bool = True):
        self.query = query
        self.stats = stats
        self.__objectSerializable = None
        self.__cache = {}
        self.__cachedFunc = self.__func_maker()
        self.__defaultKey = None

        if verify:
            try:
                self.validate({"test" : "test"})
            except NameError:
                pass
            except Exception as e:
                raise ValueError(f"Invalid query: {self.query}") from e

    @property
    def defaultKey(self):
        return self.__defaultKey

    @defaultKey.setter
    def defaultKey(self, value):
        assert isinstance(value, str), "defaultKey must be a string"
        self.__defaultKey = value


    def __toDictRepresentation(self, obj: typing.Any):
        def _func(obj):

            if isinstance(obj, (list, tuple, int, float, bool, str)):
                return {"value": obj}

            if isinstance(obj, dict):
                return obj

            if hasattr(obj, "__dict__"):
                return {k: v for k, v in obj.__dict__.items() if not k.startswith("_")}

        res = _func(obj)
        if res is None:
            return None

        return {k: str(v) if isinstance(v, (int, float)) else v for k, v in res.items()}

    def __toCacheKey(self, obj: typing.Any):
        if isinstance(obj, (tuple, int, float, bool, str)):
            return obj

        try:
            return json.dumps(obj)
        except:  # noqa
            pass

    def __func_maker(self):
        def func(data: dict):
            default = data.get("__default__", None)

            if default is None:
                if "name" in data:
                    default = data["name"]
                elif "id" in data:
                    default = data["id"]
                else:
                    default = next(iter(data.keys()))


            try:
                return eval(
                    self.query,
                    {
                        **funcs_maps,
                        "x": data,
                        **{k: v for k, v in data.items() if not k.startswith("_")},
                        "__default__": default,
                    },
                )
            except NameError:
                return False

        return func

    def validate(self, obj: typing.Any):
        if self.__objectSerializable is None:
            self.__objectSerializable = self.__toCacheKey(obj) is not None

        if self.__objectSerializable and self.__cache is None:
            self.__cache = {}

        rep = self.__toDictRepresentation(obj)

        if not self.__objectSerializable:
            return self.__cachedFunc(rep)

        cacheKey = self.__toCacheKey(rep)
        if cacheKey in self.__cache:
            return self.__cache[cacheKey]

        self.__cache[cacheKey] = self.__cachedFunc(rep)
        return self.__cache[cacheKey]


__all__ = ["QueryObj"]
