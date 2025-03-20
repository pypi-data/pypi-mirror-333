from pesten.pesten import Pesten


def test_reshuffle_with_mirror_as_topcard():
    game = Pesten(2,2, [0,0,0,0,0], {0: 'change_suit'})
    game.play_turn(0)
    game.play_turn(1)
    game.play_turn(-1)
    assert len(game.play_stack) == 2
    