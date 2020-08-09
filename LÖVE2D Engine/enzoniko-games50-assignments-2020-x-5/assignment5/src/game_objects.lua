--[[
    GD50
    Legend of Zelda

    Author: Colton Ogden
    cogden@cs50.harvard.edu
]]

GAME_OBJECT_DEFS = {
    ['switch'] = {
        type = 'switch',
        texture = 'switches',
        frame = 2,
        width = 16,
        height = 16,
        solid = false,
        defaultState = 'unpressed',
        states = {
            ['unpressed'] = {
                frame = 2
            },
            ['pressed'] = {
                frame = 1
            }
        }
    },
    ['pot'] = {
        type = 'pot',
        texture = 'tiles',
        frame = 33,
        width = 16,
        height = 16,
        solid = true,
        defaultState = 'ground1',
        states = {
            ['ground1'] = {
                frame = 33
            },
            ['broke1'] = {
                frame = 52
            },
        },
        lifted = false,
        broken = false,
        enemyCollided = false
    },
    ['heart'] = {
        type = 'heart',
        texture = 'hearts',
        frame = 5,
        defaultState = 'unconsumed-1sec',
        states = {
            ['unconsumed-1sec'] = {
                frame = 5
            },
            ['unconsumed-2sec'] = {
                frame = 4
            },
            ['unconsumed-3sec'] = {
                frame = 3
            },
            ['unconsumed-4sec'] = {
                frame = 2
            },
            ['unconsumed-5sec'] = {
                frame = 1
            },
        },
        width = 16,
        height = 16,
        solid = false,
        consumed = false,
    }
}