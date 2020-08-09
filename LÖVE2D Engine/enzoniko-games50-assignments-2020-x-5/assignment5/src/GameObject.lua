--[[
    GD50
    Legend of Zelda

    Author: Colton Ogden
    cogden@cs50.harvard.edu
]]

GameObject = Class{}

function GameObject:init(def, x, y)
    -- string identifying this object type
    self.type = def.type

    self.texture = def.texture
    self.frame = def.frame or 1

    -- whether it acts as an obstacle or not
    self.solid = def.solid

    self.defaultState = def.defaultState
    self.state = self.defaultState
    self.states = def.states

    -- dimensions
    self.x = x
    self.y = y
    self.width = def.width
    self.height = def.height

    -- Heart animation 
    self.timer = 100
    self.heartStates = {'unconsumed-2sec', 'unconsumed-3sec', 'unconsumed-4sec', 'unconsumed-5sec', 'unconsumed-1sec'}
    self.counter = 1


    -- default empty collision callback
    self.onCollide = function() end

    self.onConsume = function() end
end

function GameObject:update(dt)
    -- If the object is a heart then run the timer an change the sprite every second
    if self.type == 'heart' then
        if self.timer > 0 then
            self.timer = self.timer - 1
        else
            self.state = self.heartStates[self.counter]
            self.timer = 100
            self.counter = self.counter + 1
            gSounds['heart']:play()
            if self.counter == 5 then
                self.consumed = true 
                self.counter = 1
            end
        end
    end

    
    

end

function GameObject:render(adjacentOffsetX, adjacentOffsetY)
    love.graphics.draw(gTextures[self.texture], gFrames[self.texture][self.states[self.state].frame or self.frame],
        self.x + adjacentOffsetX, self.y + adjacentOffsetY)
end