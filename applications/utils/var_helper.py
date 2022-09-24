def parse_variable(var):
    if "${" not in var:
        key = "${%s}" % var
    else:
        key = var
    return key
