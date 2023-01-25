import re


def cpf_formatter(cpf: str) -> str:
    return re.sub(r"(\d{3})(\d{3})(\d{3})(\d{2})", r"\1.\2.\3-\4", cpf)


def telefone_formatter(telefone: str) -> str | None:
    if telefone is None:
        return None
    return re.sub(r"(\d{2})(\d{4,5})(\d{4})", r"(\1) \2-\3", telefone)
