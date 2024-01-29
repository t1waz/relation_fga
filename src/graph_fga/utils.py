import networkx as nx


def visualize_g(g: nx.Graph) -> None:
    import matplotlib.pyplot as plt

    pos = nx.kamada_kawai_layout(g)

    relation_nodes = [node for node in g.nodes() if node.type == "relation"]
    type_nodes = [node for node in g.nodes() if node.type == "type"]
    permission_nodes = [node for node in g.nodes() if node.type == "permission"]

    nx.draw_networkx_nodes(g, pos, nodelist=relation_nodes, node_color="red", alpha=0.9)
    nx.draw_networkx_nodes(g, pos, nodelist=type_nodes, node_color="blue", alpha=0.9)
    nx.draw_networkx_nodes(
        g, pos, nodelist=permission_nodes, node_color="green", alpha=0.9
    )

    edge_labels = nx.get_edge_attributes(g, "allowed", default="")
    nx.draw_networkx_edge_labels(g, pos, edge_labels=edge_labels)

    nx.draw_networkx_edges(g, pos)
    nx.draw_networkx_labels(g, pos, labels={node: node for node in g.nodes()})

    plt.show()


def get_id_from_gid(gid_key: str) -> str:
    try:
        return gid_key.split(":")[1]
    except (KeyError, ValueError, IndexError):
        raise ValueError(f"invalid value for: '{gid_key}', no id")


def get_type_from_gid(gid_key: str) -> str:
    try:
        return gid_key.split(":")[0]
    except (KeyError, ValueError, IndexError):
        raise ValueError(f"invalid value for: '{gid_key}', no type")
