# coding: utf-8
from __future__ import unicode_literals

from seabattle import dialog_manager as dm, game as gm


import pytest
import mock


user_id = 'user1'


def say(message):
    return dm.handle_message(user_id, message)[0]


def newgame(opponent):
    return dm.AFTER_SHOT_MESSAGES['newgame'] % {'opponent': opponent}


def shot(shot):
    return dm.AFTER_SHOT_MESSAGES['shot'] % {'shot': shot}


def miss(shot):
    return dm.AFTER_SHOT_MESSAGES['miss'] % {'shot': shot}


def kill():
    return dm.AFTER_SHOT_MESSAGES['kill']


def hit():
    return dm.AFTER_SHOT_MESSAGES['hit']


def test_game_1():
    assert say('новая игра. соперник яндекс') == newgame('яндекс')

    field = [gm.EMPTY, gm.EMPTY, gm.EMPTY,
             gm.SHIP,  gm.EMPTY, gm.SHIP,
             gm.EMPTY, gm.EMPTY, gm.SHIP]

    my_field = [gm.EMPTY, gm.SHIP,  gm.EMPTY,
                gm.EMPTY, gm.EMPTY, gm.EMPTY,
                gm.EMPTY, gm.SHIP,  gm.SHIP]

    shots = ['а, 1', 'а, 2', 'б, 3', 'в, 3', 'а, 3']

    game = gm.Game()
    game.start_new_game(3, field, [2, 1])
    game.do_shot = mock.Mock(side_effect=shots)

    dm.sessions[user_id]['game'] = game

    assert say('начинай') == shot(shots[0])
    assert say('мимо. я хожу б 2') == miss(shots[1])
    assert say('мимо. я хожу в 2') == hit()
    assert say('я хожу в 3') == kill()
    assert say('я хожу б 3') == miss(shots[2])
    assert say('ранил') == shot(shots[3])
    assert say('убил') == shot(shots[4])
    assert say('мимо. я хожу а 2') == kill()
    assert say('ура победа') == 'я проиграл'