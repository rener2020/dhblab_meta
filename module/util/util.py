def chaos2order(buffer: str, start_sep: str, end_sep: str) -> (list, bool, bool):
    # data packet is less than 1024
    # only exist broken tail | broken head
    # do not exist broken body
    # and broken packet can be split to two part
    broken_head, broken_tail = False, False
    if buffer[0] != start_sep:
        broken_tail, buffer = buffer.split(end_sep, 1)
        broken_tail += end_sep
    order = [start_sep + pack for pack in buffer.split(start_sep)[1:]]
    if len(order) == 0 or len(order[-1]) == 0:
        return order, broken_head, broken_tail
    if order[-1][-1] != end_sep:
        broken_head = order[-1]
        order = order[:-1]
    return order, broken_head, broken_tail
