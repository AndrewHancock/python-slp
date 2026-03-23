from dataclasses import dataclass
from abc import ABC, abstractmethod


class Exp(ABC):
    pass


class Stmt(ABC):
    pass


@dataclass
class Program:
    stmts: list[Stmt]


@dataclass
class AssignStmt(Stmt):
    identifier: str
    value: Exp

@dataclass()
class PrintStmt(Stmt):
    expr_list: ExpList

@dataclass
class NumExp(Exp):
    value: int


@dataclass
class IdExp(Exp):
    identifier: str


@dataclass
class ExpList(Exp):
    exp_list: list[Exp]