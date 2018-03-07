# From the perspective of a gambler who can play only 10 games, the law of large numbers no longer holds true, so we must
# use a transient state analysis/projection interval to determine expected rewards. This projection interval can then be
# interpreted as an estimate of the interval in which future rewards will fall, with a given probability. Unfortunately, we ran
# out of time during class while covering this type of analysis, so I am unable to calculate the actual projection interval at this time.

# Given what we have covered thus far, the best approximation I am able to perform is as follows:
import numpy as np
import scr.FigureSupport as figureLibrary
import scr.StatisticalClasses as Stat

class Game(object):
    def __init__(self, id, prob_head):
        self._id = id
        self._rnd = np.random
        self._rnd.seed(id)
        self._probHead = prob_head  # probability of flipping a head
        self._countWins = 0  # number of wins, set to 0 to begin

    def simulate(self, n_of_flips):

        count_tails = 0  # number of consecutive tails so far, set to 0 to begin

        # flip the coin 20 times
        for i in range(n_of_flips):

            # in the case of flipping a heads
            if self._rnd.random_sample() < self._probHead:
                if count_tails >= 2:  # if the series is ..., T, T, H
                    self._countWins += 1  # increase the number of wins by 1
                count_tails = 0  # the tails counter needs to be reset to 0 because a heads was flipped

            # in the case of flipping a tails
            else:
                count_tails += 1  # increase tails count by one

    def get_reward(self):
        # calculate the reward from playing a single game
        return 100*self._countWins - 250


class SetOfGames:
    def __init__(self, prob_head, n_games):
        self._gameRewards = [] # create an empty list where rewards will be stored
        self._lossList = [] # create an empty list where losses will be stored
        self._value = self._gameRewards
        self._loss_count = 0

    def simulation(self, n_games, prob_head):
        # simulate the games
        for n in range(n_games):
            # create a new game
            game = Game(id=n, prob_head=prob_head)
            # simulate 20 flips
            game.simulate(20)
            self._gameRewards.append(game.get_reward())

        for k in self._gameRewards:
            if k < 0:
                self._loss_count +=1
                j=1
                self._lossList.append(j)
            elif k >0:
                j=0
                self._lossList.append(j)
        return SetOfGamesOutcomes(self)

    def get_loss_list(self):
        return self._lossList

    def get_ave_reward(self):
        """ returns the average reward from all games"""
        return sum(self._gameRewards) / len(self._gameRewards)

    def get_reward_list(self):
        """ returns all the rewards from all game to later be used for creation of histogram """
        return self._gameRewards


    def get_max(self):
        """ returns maximum reward"""
        return max(self._gameRewards)

    def get_min(self):
        """ returns minimum reward"""
        return min(self._gameRewards)



class SetOfGamesOutcomes:
    def __init__(self, sim_cohort):
        self._simCohort = sim_cohort
        self._sumStat_rewardStats = \
            Stat.SummaryStat('Set of expected reward statistics', self._simCohort.get_reward_list())
        self._sumStat_lossStats = \
            Stat.SummaryStat('Set of loss probability statistics', self._simCohort.get_loss_list())

    def get_CI_expected_reward(self, alpha):
        """
        :param alpha: confidence level
        :return: t-based confidence interval
        """
        return self._sumStat_rewardStats.get_t_CI(alpha)

    def get_CI_probability_loss(self, alpha):
        """
        :param alpha: confidence level
        :return: t-based confidence interval
        """
        return self._sumStat_lossStats.get_t_CI(alpha)


trial10 = SetOfGames(prob_head=0.50, n_games=10)
gamble10 = trial10.simulation(n_games=10, prob_head=0.5)
print('95% t-based confidence interval for expected reward from gambling only 10 games:', gamble10.get_CI_expected_reward(alpha=0.05))














