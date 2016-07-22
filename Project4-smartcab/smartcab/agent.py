import random
from environment import Agent, Environment
from planner import RoutePlanner
from simulator import Simulator

class LearningAgent(Agent):
    """An agent that learns to drive in the smartcab world."""

    def __init__(self, env):
        super(LearningAgent, self).__init__(env)  # sets self.env = env, state = None, next_waypoint = None, and a default color
        self.color = 'red'  # override color
        self.planner = RoutePlanner(self.env, self)  # simple route planner to get next_waypoint
        # TODO: Initialize any additional variables here
        self.q_values = {}
        self.alpha = 1

    def reset(self, destination=None):
        self.planner.route_to(destination)
        # TODO: Prepare for a new trip; reset any variables here, if required

    def update(self, t):
        # Gather inputs
        self.next_waypoint = self.planner.next_waypoint()  # from route planner, also displayed by simulator
        inputs = self.env.sense(self)
        deadline = self.env.get_deadline(self)

        # TODO: Update state
#        clear_left, clear_forward, clear_right = [False]*3
#        if inputs['light'] == 'green': 
#            clear_right = True
#            clear_forward = True
#            if inputs['oncoming'] != 'forward'and inputs['oncoming'] != 'right':
#                clear_left = True
#        elif inputs['left'] != 'forward': clear_right = True

        self.state = (self.get_next_waypoint(), inputs['light'], 
                      inputs['left'], inputs['oncoming'], inputs['right'])
        
        # TODO: Select action according to your policy
        print "State:", self.state
        print "Q Values:"
        print "---------"
        for k, v in self.q_values.iteritems(): print k, v
        print
        unknown_actions = []
        best_action = None
        for p_action in Environment.valid_actions:
            if (self.state + (p_action,)) in self.q_values:
                r = self.q_values[self.state + (p_action,)]
                print "action '{}' found with reward {}".format(p_action, r)
                if best_action == None or r > best_action[1]:
                    best_action = (p_action, r)
                    print "best action updated to:", best_action
            else:
                unknown_actions.append(p_action)
        print "Unknown Actions:", unknown_actions
        print "Best Action:", best_action
        if len(unknown_actions) > 0:
            action = unknown_actions[random.randint(0, len(unknown_actions)-1)]
        else:
            action = best_action[0]
        print "Action selected is '{}'".format(action)
        #action = Environment.valid_actions[random.randint(0, len(Environment.valid_actions)-1)]

        # Execute action and get reward
        reward = self.env.act(self, action)

        # TODO: Learn policy based on state, action, reward
        self.q_values[self.state + (action,)] = reward
#        if len(self.q_values) % 10 == 0:
#            print            
#            print "Q Values:"
#            print "---------"
#            for k, v in self.q_values.iteritems(): print k, v
#            print

        #print "LearningAgent.update(): deadline = {}, inputs = {}, action = {}, reward = {}".format(deadline, inputs, action, reward)  # [debug]


def run():
    """Run the agent for a finite number of trials."""

    # Set up environment and agent
    e = Environment()  # create environment (also adds some dummy traffic)
    a = e.create_agent(LearningAgent)  # create agent
    e.set_primary_agent(a, enforce_deadline=False)  # specify agent to track
    # NOTE: You can set enforce_deadline=False while debugging to allow longer trials

    # Now simulate it
    sim = Simulator(e, update_delay=0.5, display=True)  # create simulator (uses pygame when display=True, if available)
    # NOTE: To speed up simulation, reduce update_delay and/or set display=False

    sim.run(n_trials=5)  # run for a specified number of trials
    # NOTE: To quit midway, press Esc or close pygame window, or hit Ctrl+C on the command-line


if __name__ == '__main__':
    run()
