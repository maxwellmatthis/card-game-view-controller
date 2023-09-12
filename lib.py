from typing import *
from dataclasses import dataclass
import pygame
import os
import random

ASSETS_DIR = "assets"
WIDTH_PX = 1280
HEIGHT_PX = 720


@dataclass
class Collection:
    id: str
    cards: List[str]

    """Shuffle the collection in place."""

    def shuffle(self):
        random.shuffle(self.cards)


class ViewController:
    assets: Dict[str, pygame.Surface]
    screen: pygame.Surface

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH_PX, HEIGHT_PX))
        self.assets = {}
        self.__load_assets()

    def __load_assets(self):
        """Loads cards from the cards directory.
        The names of the cards are determined by the file names in the assets directory."""
        for assetName in [
            item for item in os.listdir(ASSETS_DIR)
            if os.path.isfile(os.path.join(ASSETS_DIR, item))
        ]:
            self.assets[assetName.split(".")[0]] = pygame.image.load(
                os.path.join(ASSETS_DIR, assetName))

    def get_available_cards(self) -> [str]:
        return list(self.assets.keys())

    def render(self, piles: List[Collection], hands: List[Collection]):
        """Renders the entire game based on the piles and hands"""
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()

        # fill the screen with a color to wipe away anything from last frame
        self.screen.fill("gray")

        # draw cards
        self.__draw_piles(piles)
        self.__draw_hands(hands)

        # flip() the display to put your work on screen
        pygame.display.flip()

    def __draw_piles(self, piles: List[Collection]):
        pile_index = 0
        for pile in piles:
            if len(pile.cards) == 0:
                # todo: maybe render an empty indicator instead?
                continue
            card = self.assets[pile.cards[0]]
            SINGLE_CARD_HEIGHT = self.screen.get_height() / len(piles) - 20
            scale = SINGLE_CARD_HEIGHT / card.get_height()
            card = pygame.transform.scale(card, (
                scale * card.get_width(),
                scale * card.get_height()
            ))
            self.screen.blit(card, (
                self.screen.get_width() / 2 - card.get_width() / 2,
                10 + pile_index * (SINGLE_CARD_HEIGHT + 10)
            ))
            pile_index += 1

    def __draw_hands(self, hands: List[Collection]):
        hand_index = 0
        last_offsets = [0, 0]
        for hand in hands:
            if len(hand.cards) == 0:
                # todo: maybe render an empty indicator instead?
                continue
            card_index = 0
            sample_card = self.assets[hand.cards[0]]
            # proof: height = card_height + card_height * 25% * cards => height = card_height * ((25% * cards) + 1)
            SINGLE_CARD_HEIGHT = self.screen.get_height() / (0.25 * len(hand.cards) + 1)
            scale = SINGLE_CARD_HEIGHT / sample_card.get_height()
            MAX_WIDTH = 160
            actual_width = scale * sample_card.get_width()
            if actual_width > MAX_WIDTH:
                scale = MAX_WIDTH / sample_card.get_width()
                actual_width = MAX_WIDTH
            left = hand_index % 2 == 0
            x_offset = 10 + last_offsets.pop(0)
            last_offsets.append(x_offset + actual_width)
            for next_card in hand.cards:
                card = self.assets[next_card]
                card = pygame.transform.scale(card, (
                    # this could be `scale * card.get_width()` but would lead to malformed cards
                    # taking multiple columns; these are assumed to be equal at all times anyway
                    actual_width,
                    scale * card.get_height()
                ))
                self.screen.blit(card, (
                    x_offset if left else (
                        self.screen.get_width() - x_offset - card.get_width()),
                    10 + card_index * SINGLE_CARD_HEIGHT * 0.25
                ))
                card_index += 1
            hand_index += 1

    def get_pressed(self):
        """Returns the pressed keys.

        These can be checked like so:
        ```python
        import pygame

        keys = view_controller.get_pressed()

        # checks if the A-key is being pressed
        if keys[pygame.K_a]:
          # do something
          pass
        ```
        """
        return pygame.key.get_pressed()

    def quit():
        """quits the pygame instance, which closes the window"""
        pygame.quit()
