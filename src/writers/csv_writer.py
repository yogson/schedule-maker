from models import Pair


def build_csv_dicts(pairs: list[Pair]) -> list[dict[str, str]]:
    res = []
    for n, pair in enumerate(pairs):
        res.append({"N": n + 1} | pair.to_dict())
    return res
