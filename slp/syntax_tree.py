from dataclasses import dataclass
from abc import ABC, abstractmethod


class Exp(ABC):
    pass


class Stmt(ABC):
    pass


@dataclass
class CompoundStmt(Stmt):
    stmt1: Stmt
    stmt2: Stmt

@dataclass
class AssignStmt(Stmt):
    identifier: Id
    value: Exp

@dataclass
class PrintStmt(Stmt):
    expr_list: list[Exp]

@dataclass
class Num(Exp):
    value: int

@dataclass
class Id(Exp):
    identifier: str
