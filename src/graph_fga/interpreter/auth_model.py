from __future__ import annotations

import uuid
from typing import Optional, List, Any

import networkx as nx

from graph_fga.interpreter.entites import (
    ModelType,
    ModelTypeRelation,
    ModelTypePermission,
)
from graph_fga.interpreter.interpreter import lexer


class AuthModel:
    """
    TODO regex don't work with relation like foo-bar but works with foo_bar
    """

    def __init__(self, config: str, id: Optional[str] = None) -> None:
        self._id = id or str(uuid.uuid4())

        self._config = config
        self._relations = []
        self._model_types = []
        self._permissions = []
        self._g = nx.DiGraph()

        try:
            self._read()
        except Exception as exc:
            raise ValueError("invalid config") from exc

    def get_type(self, name: str) -> Optional[ModelType]:
        return next(iter((t for t in self._model_types if t.name == name)), None)

    def get_relation(self, name: str, type_name: str) -> Optional[ModelTypeRelation]:
        return next(
            iter(
                (
                    t
                    for t in self._relations
                    if t.name == name and t.model_type.name == type_name
                )
            ),
            None,
        )

    def get_relation_related_names(self, relation: ModelTypeRelation) -> List[str]:
        related_types = []
        for p in self._g.predecessors(relation):
            if p.type == "type":
                related_types.append(p.name)
            elif p.type == "relation":
                related_types.append(f"{p.model_type.name}#{p.name}")

        return related_types

    def get_permission(self, name: str, type_name: str):
        return next(
            iter(
                (
                    t
                    for t in self._permissions
                    if t.name == name and t.model_type.name == type_name
                )
            ),
            None,
        )

    def _load_type(self, name: str) -> ModelType:
        existing_type = self.get_type(name=name.strip())
        if existing_type:
            return existing_type

        model_type = ModelType(name=name)
        self.g.add_node(model_type)
        self._model_types.append(model_type)

        return model_type

    def _load_permission(self, name, model_type: ModelType) -> ModelTypePermission:
        existing_permission = self.get_permission(name=name, type_name=model_type.name)
        if existing_permission:
            return existing_permission

        permission = ModelTypePermission(name=name, model_type=model_type)
        self.g.add_edge(permission, model_type)
        self._permissions.append(permission)

        return permission

    def _load_relation(self, name: str, model_type: ModelType) -> ModelTypeRelation:
        existing_relation = self.get_relation(name=name, type_name=model_type.name)
        if existing_relation:
            return existing_relation

        relation = ModelTypeRelation(name=name, model_type=model_type)
        if relation not in self._relations:
            self.g.add_node(relation)
            self.g.add_edge(relation, model_type)
            self._relations.append(relation)

        return relation

    def _load_relation_type(self, name: str, relation: ModelTypeRelation) -> None:
        if "#" not in name:
            model_type = self._load_type(name=name)
            self.g.add_edge(model_type, relation)
        else:
            type_name, relation_name = name.split("#")
            related_model_type = self._load_type(name=type_name.strip())
            related_relation = self._load_relation(
                name=relation_name.strip(), model_type=related_model_type
            )
            self.g.add_edge(related_relation, relation)

    def _load_permission_type(
        self, relation_name: str, permission: ModelTypePermission
    ) -> None:
        if "from" not in relation_name:
            p_r = self.get_relation(
                name=relation_name, type_name=permission.model_type.name
            )
            if p_r:
                self.g.add_edge(p_r, permission)
                return
            p_r = self._load_permission(
                name=relation_name, model_type=permission.model_type
            )
            self.g.add_edge(p_r, permission)
            return

        related_name, relation_name = relation_name.split("from")
        related_name, relation_name = related_name.strip(), relation_name.strip()
        relation = self.get_relation(
            name=relation_name, type_name=permission.model_type.name
        )
        for p in [a for a in self.g.predecessors(relation) if a.type == "type"]:
            p_r = self.get_relation(name=related_name, type_name=p.name)
            if p_r:
                self.g.add_edge(p_r, permission, allowed=relation_name)
                return
            p_r = self._load_permission(name=related_name, model_type=p)
            self.g.add_edge(p_r, permission, allowed=relation_name)

    def _read_relations(self) -> None:
        lexer.input(self._config)

        current_relation_name = None
        current_model_type_name = None
        while True:
            lex_token = lexer.token()
            if not lex_token:
                break
            token_type = lex_token.type
            if token_type == "TYPE":
                current_model_type_name = lex_token.value
            elif token_type == "RELATION":
                current_relation_name = lex_token.value
            elif token_type == "RELATION_TYPE":
                model_type = self._load_type(name=current_model_type_name)
                relation = self._load_relation(
                    model_type=model_type, name=current_relation_name
                )
                for model_type_name in lex_token.value:
                    self._load_relation_type(name=model_type_name, relation=relation)

    def _read_permissions(self) -> None:
        lexer.input(self._config)

        current_model_type = None
        current_permission_name = None
        while True:
            lex_token = lexer.token()
            if not lex_token:
                break
            if lex_token.type == "TYPE":
                current_model_type = self._load_type(name=lex_token.value)
            elif lex_token.type == "RELATION":
                current_permission_name = lex_token.value
            elif lex_token.type == "PERMISSION_TYPE":
                permission = self._load_permission(
                    name=current_permission_name, model_type=current_model_type
                )
                for relation_name in lex_token.value:
                    self._load_permission_type(
                        relation_name=relation_name, permission=permission
                    )

    def _read(self) -> nx.DiGraph:
        self._read_relations()
        self._read_permissions()

        return self.g

    def get_type_relation(self, name: str, type_name: str) -> Any:
        type_relation = self.get_relation(name=name, type_name=type_name)
        if type_relation:
            return type_relation

        return self.get_permission(name=name, type_name=type_name)

    @property
    def config(self) -> str:
        return self._config

    @property
    def relations(self) -> List[ModelTypeRelation]:
        return self._relations

    @property
    def is_valid(self) -> bool:
        return len(self._relations) >= 0 and len(self._model_types) > 0

    @property
    def type_names(self) -> List[str]:
        return [t.name for t in self._model_types]

    @property
    def g(self) -> nx.DiGraph:
        return self._g

    @property
    def id(self) -> str:
        return self._id
