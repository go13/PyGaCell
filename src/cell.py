import random


class Operation:
    def __init__(self, hubs):
        self.hubs = hubs
        for h in hubs:
            h.outs += [self]

    def calc(self):
        return NotImplemented

    @classmethod
    def random_operation(cls, hubs):
        op_ind = random.randint(0, 2)
        return {
            0: OpLink.random_operation,
            1: OpSum.random_operation,
            2: OpMul.random_operation,
        }[op_ind](hubs)

    def clone_node_tree(self, all_hubs, mapped_hubs, cross_hub, mount_node):
        return self.clone([hub.clone_hub_tree(all_hubs, mapped_hubs, cross_hub, mount_node) for hub in self.hubs])

    def clone(self, cloned_hubs):
        return NotImplemented


class OpLink(Operation):
    @classmethod
    def random_operation(cls, hubs):
        hub_ind = random.randint(0, len(hubs) - 1)
        hub = hubs[hub_ind]

        op_link = OpLink([hub])

        op_link.hubs[0].outs += [op_link]

        return op_link

    def clone(self, hubs):
        return OpLink(hubs)

    def calc(self):
        return self.hubs[0].calc()


class OpSum(Operation):
    @classmethod
    def random_operation(cls, hubs):
        return OpSum(hubs)

    def clone(self, hubs):
        return OpSum(hubs)

    def calc(self):
        return sum([h.calc() for h in self.hubs])


class OpMul(Operation):
    @classmethod
    def random_operation(cls, hubs):
        return OpMul(hubs)

    def clone(self, hubs):
        return OpMul(hubs)

    def calc(self):
        res = 1
        for h in self.hubs:
            res = res * h.calc()
        return res


class Hub:
    def __init__(self):
        self.outs = []
        self.val = None
        self.src = None

    def calc(self):
        return self.val if self.src is None else self.src.calc()

    def get_random_path(self):
        path = []
        nxt = self
        while nxt.src:
            path += [nxt]
            hub_ind = random.randint(0, len(nxt.src.hubs) - 1)
            nxt = nxt.src.hubs[hub_ind]

        return path

    def get_random_hub(self):
        random_path = self.get_random_path()
        path_len = len(random_path)
        if path_len > 0:
            hub_ind = random.randint(0, path_len - 1)
            return random_path[hub_ind]
        else:
            return []

    def clone_hub_tree(self, all_hubs, mapped_hubs, cross_hub, mount_node):
        hub = mapped_hubs[self] if self in mapped_hubs else Hub()

        all_hubs += [hub]

        if cross_hub == self:
            hub.src = mount_node
        elif self.src:
            hub.src = self.src.clone_node_tree(all_hubs, mapped_hubs)

        return hub


class Cell:
    def __init__(self, params):
        self.params = params
        self.rating = None
        self.in_hubs = None
        self.out_hubs = None
        self.all_hubs = None

    @classmethod
    def create(cls, params):
        cell = Cell(params)

        cell.in_hubs = [Hub() for i in range(0, params.i_num)]
        cell.out_hubs = [Hub() for i in range(0, params.o_num)]
        cell.all_hubs = cell.in_hubs + cell.out_hubs

        for out_hub in cell.out_hubs:
            out_hub.src = Operation.random_operation(cell.in_hubs)

        return cell

    @classmethod
    def cross(cls, params, m, f):

        if random.random() > 0.5:
            a = m
            b = f
        else:
            a = f
            b = m

        cell = Cell(params)

        cell.in_hubs = [Hub() for i in range(0, params.i_num)]
        cell.out_hubs = []
        cell.all_hubs = [cell.in_hubs]

        mapped_hubs = dict()

        for i in range(0, params.i_num):
            mapped_hubs[a.in_hubs[i]] = cell.in_hubs[i]
            mapped_hubs[b.in_hubs[i]] = cell.in_hubs[i]

        for i in range(0, params.o_num):
            a_out_hubs = a.out_hubs[i]
            b_out_hubs = b.out_hubs[i]

            a_hub = a_out_hubs.get_random_hub()
            cross_hub = b_out_hubs.get_random_hub()

            a_small_node_tree = a_hub.src.clone_node_tree(cell.all_hubs, mapped_hubs, None, None)
            b_large_hub_tree = b_out_hubs.clone_hub_tree(cell.all_hubs, mapped_hubs, cross_hub, a_small_node_tree)

            cell.out_hubs += [b_large_hub_tree]

        return cell

    def calc(self, inputs):
        self.set_inputs(inputs)

        results = [ot.calc() for ot in self.out_hubs]

        self.rating = self.params.fn(results)

    def get_outputs(self):
        return [ot.val for ot in self.out_hubs]

    def set_inputs(self, inputs):
        for i in range(0, self.params.i_num):
            self.in_hubs[i].val = inputs[i]

    def mutate(self):
        pass
