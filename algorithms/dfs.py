from puzzle.base_search import BaseSearch
from puzzle.state import State
from puzzle.result import SearchResult

DEFAULT_DEPTH_LIMIT = 50


class DFS(BaseSearch):
    """Busca em Profundidade com limite de profundidade (pilha LIFO).

    Não é ótima: a solução encontrada pode ser mais longa que a mínima.
    Para não perder soluções por causa do limite, um estado já visto só é
    descartado se foi alcançado antes com profundidade menor ou igual.
    """

    def __init__(self, depth_limit: int = DEFAULT_DEPTH_LIMIT):
        self.depth_limit = depth_limit

    def search(self, initial: State) -> SearchResult:
        generated = 1
        expanded = 0

        frontier = [initial]
        max_frontier = 1
        best_depth = {initial.tiles: initial.cost}

        while frontier:
            current = frontier.pop()

            if current.is_goal:
                return SearchResult(current, expanded, generated, max_frontier, current.cost)

            if current.cost >= self.depth_limit:
                continue

            expanded += 1

            # reversed(): o primeiro vizinho (UP) fica no topo da pilha e é explorado primeiro
            for child in reversed(current.neighbors()):
                known = best_depth.get(child.tiles)
                if known is not None and known <= child.cost:
                    continue
                best_depth[child.tiles] = child.cost
                frontier.append(child)
                generated += 1

            max_frontier = max(max_frontier, len(frontier))

        return SearchResult(None, expanded, generated, max_frontier, 0)