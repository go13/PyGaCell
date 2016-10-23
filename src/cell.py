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
        return {
            0: OpLink.random_operation,
            1: OpSum.random_operation,
        }[random.randint(0, 1)](hubs)

    def clone_hubs(self, mapped_hubs, hub_pairs, in_hub_pairs, node_pairs, cross_hub, mount_node):
        return [hub.clone_hub_tree(mapped_hubs, hub_pairs, in_hub_pairs, node_pairs, cross_hub, mount_node) for hub in self.hubs]

    def clone_node_tree(self, mapped_hubs, hub_pairs, in_hub_pairs, node_pairs, cross_hub, mount_node):
        cloned_hubs = self.clone_hubs(mapped_hubs, hub_pairs, in_hub_pairs, node_pairs, cross_hub, mount_node)
        cloned_node = self.clone(cloned_hubs)
        node_pairs += [(self, cloned_node)]

        return cloned_node

    def clone(self, cloned_hubs):
        return NotImplemented

    def clone_tree(self, mapped_hubs):
        hub_pairs = []
        in_hub_pairs = []
        node_pairs = []

        cloned_node = self.clone_node_tree(mapped_hubs, hub_pairs, in_hub_pairs, node_pairs, None, None)

        return cloned_node, hub_pairs, in_hub_pairs, node_pairs


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


class Hub:
    def __init__(self):
        self.outs = []
        self.val = None
        self.src = None

    def calc(self):
        return self.val if self.src is None else self.src.calc()

    def get_random_path(self):
        path = []
        next = self
        while next.src:
            path += [next]
            hub_ind = random.randint(0, len(next.src.hubs) - 1)
            next = next.src.hubs[hub_ind]

        return path

    def get_random_hub(self):
        random_path = self.get_random_path()
        path_len = len(random_path)
        if path_len > 0:
            hub_ind = random.randint(0, path_len - 1)
            return random_path[hub_ind]
        else:
            return []

    def clone_tree(self, mapped_hubs, cross_hub, mount_node):
        hub_pairs = []
        in_hub_pairs = []
        node_pairs = []

        cloned_hub = self.clone_hub_tree(mapped_hubs, hub_pairs, in_hub_pairs, node_pairs, cross_hub, mount_node)

        return cloned_hub, hub_pairs, in_hub_pairs, node_pairs

    def clone_hub_tree(self, mapped_hubs, hub_pairs, in_hub_pairs, node_pairs, cross_hub, mount_node):
        if cross_hub == self:
            hub = Hub()
            hub.src = mount_node
        else:
            if self in mapped_hubs:
                hub = mapped_hubs[self]
            else:
                hub = Hub()
            if self.src:
                hub.src = self.src.clone_node_tree(mapped_hubs, hub_pairs, in_hub_pairs, node_pairs)
            else:
                in_hub_pairs += [(self, hub)]
        hub_pairs += [(self, hub)]
        return hub


class Cell:
    def __init__(self, params):
        self.params = params
        self.rating = None
        self.in_hubs = None
        self.out_hubs = None

    @classmethod
    def create(cls, params):
        cell = Cell(params)

        cell.in_hubs = [Hub() for i in range(0, params.i_num)]
        cell.out_hubs = [Hub() for i in range(0, params.o_num)]

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

        mapped_hubs = dict()

        for i in range(0, params.i_num):
            mapped_hubs[a.in_hubs[i]] = cell.in_hubs[i]
            mapped_hubs[b.in_hubs[i]] = cell.in_hubs[i]

        for i in range(0, params.o_num):
            a_out_hubs = a.out_hubs[i]
            b_out_hubs = b.out_hubs[i]

            a_hub = a_out_hubs.get_random_hub()
            cross_hub = b_out_hubs.get_random_hub()

            a_small_node_tree, _, _, _ = a_hub.src.clone_tree(mapped_hubs)
            b_large_hub_tree, _, _, _ = b_out_hubs.clone_tree(mapped_hubs, cross_hub, a_small_node_tree)

            cell.out_hubs += [b_large_hub_tree]

        return cell

    def calc(self, inps):
        self.set_inputs(inps)

        results = [ot.calc() for ot in self.out_hubs]

        self.rating = self.params.fn(results)

    def get_outputs(self):
        return [ot.val for ot in self.out_hubs]

    def set_inputs(self, inps):
        for i in range(0, self.params.i_num):
            self.in_hubs[i].val = inps[i]

    def mutate(self):
        pass
