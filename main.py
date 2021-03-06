import agent
import environment
import policy

bandit = agent.HorseBandit(mode='dividend')
n_trials = 2500
n_experiments = 2500

agents = [  agent.Agent(bandit, policy.RandomPolicy()),
            agent.Agent(bandit, policy.EpsilonGreedyPolicy(.01)),
            agent.Agent(bandit, policy.EpsilonGreedyPolicy(.1)),
            agent.Agent(bandit, policy.UCBPolicy(1)),
            agent.Agent(bandit, policy.UCBPolicy(2))]
env = environment.Environment(bandit, agents)
scores, optimal = env.run(n_trials, n_experiments)
env.plot_results(scores, optimal)

