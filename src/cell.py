import random


class Operation:
    def __init__(self, hubs):
        self.hubs = hubs

    def calc(self):
        return NotImplemented

    def are_linked(self, hub):
        return hub in self.hubs

    def link(self, hub):
        self.hubs += [hub]

    @classmethod
    def random_operation(cls, hubs):
        op_ind = random.randint(0, 3)
        return {
            0: OpLink.random_operation,
            1: OpSum.random_operation,
            2: OpMul.random_operation,
            3: OpIntConst.random_operation,
        }[op_ind](hubs)

    def clone_node_tree(self, all_hubs, mapped_hubs, cross_hub, mount_node):
        return self.clone([hub.clone_hub_tree(all_hubs, mapped_hubs, cross_hub, mount_node) for hub in self.hubs])

    def clone(self, cloned_hubs):
        return NotImplemented


class OpIntConst(Operation):
    val = 0

    def __str__(self):
        return "OpConst(" + ", ".join([str(h) for h in self.hubs]) + ")"

    @classmethod
    def random_operation(cls, hubs):
        op_int_const = OpIntConst(hubs)
        op_int_const.val = random.randint(-9, 9)
        return op_int_const

    def clone(self, hubs):
        op_int_const = OpIntConst(hubs)
        op_int_const.val = self.val
        return op_int_const

    def calc(self):
        return self.val


class OpLink(Operation):
    def __str__(self):
        return "OpLink(" + ", ".join([str(h) for h in self.hubs]) + ")"

    @classmethod
    def random_operation(cls, hubs):
        hub_ind = random.randint(0, len(hubs) - 1)
        hub = hubs[hub_ind]

        op_link = OpLink([hub])

        return op_link

    def clone(self, hubs):
        return OpLink(hubs)

    def calc(self):
        return self.hubs[0].calc()


class OpSum(Operation):
    def __str__(self):
        return "OpSum(" + ", ".join([str(h) for h in self.hubs]) + ")"

    @classmethod
    def random_operation(cls, hubs):
        return OpSum(hubs)

    def clone(self, hubs):
        return OpSum(hubs)

    def calc(self):
        return sum([h.calc() for h in self.hubs])


class OpMul(Operation):
    def __str__(self):
        return "OpMul(" + ", ".join([str(h) for h in self.hubs]) + ")"

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
        self.val = None
        self.src = None

    def __str__(self):
        return "Hub (val = " + str(self.val) + ", " + str(self.src) + ")"

    def calc(self):
        if self.src is not None:
            self.val = self.src.calc()
        return self.val

    def get_random_path(self, include_inputs, include_self):
        path = []
        nxt = self
        while nxt.src:
            path += [nxt]
            hub_ind = random.randint(0, len(nxt.src.hubs) - 1)
            nxt = nxt.src.hubs[hub_ind]

        if include_inputs and not nxt.src:
            path += [nxt]

        if not include_self and self in path:
            path.remove(self)

        return path

    def get_random_hub(self, include_inputs=False, include_self=True):
        random_path = self.get_random_path(include_inputs, include_self)
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
            hub.src = self.src.clone_node_tree(all_hubs, mapped_hubs, None, None)

        return hub

    def mutate_hub(self, cell):
        op_ind = random.randint(0, 2)
        return {
            0: self.add_random_operation,
            1: self.add_random_link,
            2: self.change_random_operation,
        }[op_ind](cell)

    def add_random_link(self, cell):
        random_sub_hub = self.get_random_hub(include_inputs=True, include_self=False)
        if type(self.src) != OpIntConst and not self.src.are_linked(random_sub_hub):
            self.src.link(random_sub_hub)

    def change_random_operation(self, cell):
        self.src = Operation.random_operation(self.src.hubs)

    def add_random_operation(self, cell):
        new_hub = Hub()
        cell.all_hubs += [new_hub]
        new_hub.src = self.src
        op = Operation.random_operation([new_hub])
        self.src = op


class Cell:
    def __str__(self):
        return "Cell (" + ", ".join([str(h) for h in self.out_hubs]) + ")"

    def __init__(self, params):
        self.params = params
        self.rating = None
        self.pure_rating = None
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
        cell.all_hubs = cell.in_hubs

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

    def rate(self):
        experiment_rates = \
            [self.params.fn(self, experiment_number) for experiment_number in range(1, self.params.experiment_number)]

        hub_number_tax = 1 if self.get_hub_number() < self.params.hub_degrade_num else self.params.hub_degrade_tax

        pure_rate = sum(experiment_rates) / float(len(experiment_rates))

        self.pure_rating = pure_rate

        self.rating = hub_number_tax * pure_rate

    def calc(self):
        return [ot.calc() for ot in self.out_hubs]

    def get_hub_number(self):
        return len(self.all_hubs)

    def get_outputs(self):
        return [ot.val for ot in self.out_hubs]

    def set_inputs(self, inputs):
        for i in range(0, self.params.i_num):
            self.in_hubs[i].val = inputs[i]

    def mutate(self):
        if self.params.mutation_probability > random.random():
            rnd_out_hub = self.get_random_out_hub()

            random_hub = rnd_out_hub.get_random_hub(include_inputs=False)
            random_hub.mutate_hub(self)

    def get_random_out_hub(self):
        rnd_out_hub_ind = random.randint(0, len(self.out_hubs) - 1)
        rnd_out_hub = self.out_hubs[rnd_out_hub_ind]
        return rnd_out_hub
