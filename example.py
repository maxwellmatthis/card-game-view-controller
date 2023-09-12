import pygame
from time import sleep
from lib import ViewController, Collection

"""
This example shows how two piles can be displayed along with two hands.
The left and right arrow keys can be used to add the top card in the `mixed_cards`
pile to either the left or right hand respectively.
"""

# create a new vc
vc = ViewController()

# create players and piles
player_a_hand = Collection("A", [])
player_b_hand = Collection("B", [])
mixed_cards = Collection("Mixed", vc.get_available_cards())
mixed_cards.shuffle()
discarded = Collection("Discard", [mixed_cards.cards.pop(0)])

while True:
    # only allow taking cards while there are cards left
    if len(mixed_cards.cards) >= 1:
      # handle keyboard events
      keys = vc.get_pressed()
      if keys[pygame.K_LEFT]:
          player_a_hand.cards.append(mixed_cards.cards.pop(0))
      elif keys[pygame.K_RIGHT]:
          player_b_hand.cards.append(mixed_cards.cards.pop(0))

    # render the current game state
    vc.render(
        [mixed_cards, discarded],
        [player_a_hand, player_b_hand]
    )

    # slows the game loop to 30fps so that the user has time to release the arrow keys
    sleep(120 / 1000)
