from collections import deque


class ActionQueue:

    def __init__(self):
        self.immediate = []
        self.to_invoke = deque()

    def add(self, func, args, frames):
        if frames <= 0:
            self.immediate.append([func, args])
        else:
            if len(self.to_invoke) - 1 < frames:
                for i in range(max(0, len(self.to_invoke) - 1), frames):
                    self.to_invoke.append([])
                self.to_invoke.append([func,args])
            else:
                self.to_invoke[frames].append([func, args])

    def step(self):
        if len(self.to_invoke):
            next_actions = self.to_invoke.popleft()
            self.immediate.append(next_actions)

        for action in self.immediate:
            if action:
                if action[1]:
                    action[0](*action[1])
                else:
                    action[0]()

        self.immediate = []