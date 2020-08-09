LEVELS = {
    ['1'] = {
        ['aliens'] = {
            
            x = {VIRTUAL_WIDTH - 80},
            y = {VIRTUAL_HEIGHT - TILE_SIZE - ALIEN_SIZE / 2},
            type = {'square'},
            
        },
        ['obstacles'] = {
            
            x = {VIRTUAL_WIDTH - 120, VIRTUAL_WIDTH - 35, VIRTUAL_WIDTH - 80},
            y = {VIRTUAL_HEIGHT - 35 - 110 / 2, VIRTUAL_HEIGHT - 35 - 110 / 2, VIRTUAL_HEIGHT - 35 - 110 - 35 / 2},
            type = {'vertical', 'vertical', 'horizontal'},
            
        },
    },
    ['2'] = {
        ['aliens'] = {
            
            x = {VIRTUAL_WIDTH - 280, VIRTUAL_WIDTH - 80},
            y = {VIRTUAL_HEIGHT - TILE_SIZE - ALIEN_SIZE / 2, VIRTUAL_HEIGHT - TILE_SIZE - (10 * ALIEN_SIZE) / 2},
            type = {'square', 'square'},
            
        },
        ['obstacles'] = {
            
            x = {VIRTUAL_WIDTH - 120 - (35 * 3), VIRTUAL_WIDTH - 120 - (35 * 3), VIRTUAL_WIDTH - 120, VIRTUAL_WIDTH - 35, VIRTUAL_WIDTH - 80},
            y = {VIRTUAL_HEIGHT - 35 - 110 / 2, VIRTUAL_HEIGHT - 35 - (110 * 3) / 2, VIRTUAL_HEIGHT - 35 - 110 / 2, VIRTUAL_HEIGHT - 35 - 110 / 2, VIRTUAL_HEIGHT - 35 - 110 - 35 / 2},
            type = {'vertical','vertical','vertical', 'vertical', 'horizontal'},
            
        },
    },
    ['3'] = {
        ['aliens'] = {
            
            x = {VIRTUAL_WIDTH - 180, VIRTUAL_WIDTH - 80},
            y = {VIRTUAL_HEIGHT - TILE_SIZE - ALIEN_SIZE / 2, VIRTUAL_HEIGHT - TILE_SIZE - (10 * ALIEN_SIZE) / 2},
            type = {'square', 'square'},
            
        },
        ['obstacles'] = {
            
            x = {VIRTUAL_WIDTH - 120 - (35 * 9), VIRTUAL_WIDTH - 120 - (35 * 9), VIRTUAL_WIDTH - 120 - (35 * 6), VIRTUAL_WIDTH - 35 - (35 * 6), VIRTUAL_WIDTH - 80 - (35 * 6), VIRTUAL_WIDTH - 120 - (35 * 3), VIRTUAL_WIDTH - 120 - (35 * 3), VIRTUAL_WIDTH - 120, VIRTUAL_WIDTH - 35, VIRTUAL_WIDTH - 80},
            y = {VIRTUAL_HEIGHT - 35 - 110 / 2, VIRTUAL_HEIGHT - 35 - (110 * 3) / 2, VIRTUAL_HEIGHT - 35 - 110 / 2, VIRTUAL_HEIGHT - 35 - 110 / 2, VIRTUAL_HEIGHT - 35 - 110 - 35 / 2, VIRTUAL_HEIGHT - 35 - 110 / 2, VIRTUAL_HEIGHT - 35 - (110 * 3) / 2, VIRTUAL_HEIGHT - 35 - 110 / 2, VIRTUAL_HEIGHT - 35 - 110 / 2, VIRTUAL_HEIGHT - 35 - 110 - 35 / 2},
            type = {'vertical','vertical','vertical', 'vertical', 'horizontal','vertical','vertical','vertical', 'vertical', 'horizontal'},
            
        },
    },
    ['4'] = {
        ['aliens'] = {
            
            x = {VIRTUAL_WIDTH - 180 - (35 * 3), VIRTUAL_WIDTH - 180 - (35 * 3), VIRTUAL_WIDTH - 180, VIRTUAL_WIDTH - 80},
            y = {VIRTUAL_HEIGHT - TILE_SIZE - (ALIEN_SIZE * 10) / 2, VIRTUAL_HEIGHT - TILE_SIZE - ALIEN_SIZE / 2, VIRTUAL_HEIGHT - TILE_SIZE - ALIEN_SIZE / 2, VIRTUAL_HEIGHT - TILE_SIZE - (10 * ALIEN_SIZE) / 2},
            type = {'square', 'square', 'square', 'square'},
            
        },
        ['obstacles'] = {
            
            x = {VIRTUAL_WIDTH - 120 - (35 * 7), VIRTUAL_WIDTH - 120 - (35 * 7), VIRTUAL_WIDTH - 120 - (35 * 7), VIRTUAL_WIDTH - 120 - (35 * 8), VIRTUAL_WIDTH - 120 - (35 * 8), VIRTUAL_WIDTH - 120 - (35 * 9), VIRTUAL_WIDTH - 120 - (35 * 6), VIRTUAL_WIDTH - 35 - (35 * 6), VIRTUAL_WIDTH - 80 - (35 * 6), VIRTUAL_WIDTH - 120 - (35 * 3), VIRTUAL_WIDTH - 120 - (35 * 3), VIRTUAL_WIDTH - 120, VIRTUAL_WIDTH - 35, VIRTUAL_WIDTH - 80},
            y = {VIRTUAL_HEIGHT - 35 - 110 / 2, VIRTUAL_HEIGHT - 35 - (110 * 3) / 2, VIRTUAL_HEIGHT - 35 - (110 * 4) / 2,VIRTUAL_HEIGHT - 35 - 110 / 2, VIRTUAL_HEIGHT - 35 - (110 * 3) / 2, VIRTUAL_HEIGHT - 35 - 110 / 2, VIRTUAL_HEIGHT - 35 - 110 / 2, VIRTUAL_HEIGHT - 35 - 110 / 2, VIRTUAL_HEIGHT - 35 - 110 - 35 / 2, VIRTUAL_HEIGHT - 35 - 110 / 2, VIRTUAL_HEIGHT - 35 - (110 * 3) / 2, VIRTUAL_HEIGHT - 35 - 110 / 2, VIRTUAL_HEIGHT - 35 - 110 / 2, VIRTUAL_HEIGHT - 35 - 110 - 35 / 2},
            type = {'vertical','vertical','horizontal','vertical','vertical','vertical','vertical', 'vertical', 'horizontal','vertical','vertical','vertical', 'vertical', 'horizontal'},
            
        },
    },
}