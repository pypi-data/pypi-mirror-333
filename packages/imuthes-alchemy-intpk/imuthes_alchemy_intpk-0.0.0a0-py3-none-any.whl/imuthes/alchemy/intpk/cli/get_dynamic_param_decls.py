def get_dynamic_param_decls(short, name) -> list[str]:
    param_decls = [f"--{name}"]
    if name[0] not in short:
        short.add(name[0])
        param_decls.insert(0, f"-{name[0]}")
    return param_decls
