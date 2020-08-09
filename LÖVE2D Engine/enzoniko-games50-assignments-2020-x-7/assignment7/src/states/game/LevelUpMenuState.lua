LevelUpMenuState = Class{__includes = BaseState}

function LevelUpMenuState:init(current, increment)
    self.currentStats = current
    self.incrementStats = increment
    self.stats = {'HP -> ', 'Attack -> ', 'Defense -> ', 'Speed -> '}
    self.items = {}

    for i = 1, 4 do
        table.insert(self.items, {
            text = self.stats[i] .. tostring(self.currentStats[i]) .. ' + ' .. tostring(self.incrementStats[i]) .. ' = ' .. tostring(self.currentStats[i] + self.incrementStats[i]),
            onSelect = function()
                gStateStack:pop()
                TakeTurnState:fadeOutWhite()
            end
        })
    end
    
    self.statsMenu = Menu {
        x = 0,
        y = VIRTUAL_HEIGHT - 64,
        width = VIRTUAL_WIDTH,
        height = 64,
        cursorEnabled = false,
        items = self.items
    }
end

function LevelUpMenuState:update(dt)
    self.statsMenu:update(dt)
end

function LevelUpMenuState:render()
    self.statsMenu:render()
end