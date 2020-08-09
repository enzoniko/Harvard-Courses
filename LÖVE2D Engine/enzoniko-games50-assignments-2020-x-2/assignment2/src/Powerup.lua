-- Create class Powerup
-- This Powerup should spawn randomly, be it on a timer or when the Ball hits a Block enough times,
-- and gradually descend toward the player. Once collided with the Paddle, 
-- two more Balls should spawn and behave identically to the original, 
-- including all collision and scoring points for the player. 
-- Once the player wins and proceeds to the VictoryState for their current level, 
-- the Balls should reset so that there is only one active again.

Powerup = Class{}

function Powerup:init(x, y, keyValid)
    self.width = 16
    self.height = 16

    self.dx = 0
    self.dy = 2

    self.x = x
    self.y = y

    if keyValid then
        self.type = 10
    else
        if math.random(1, 3) == 1 then
            self.type = 4
        elseif math.random(1, 3) == 2 then
            self.type = 9 
        else 
            self.type = 3
        end
    end

    self.startupTimer = 0

    self.collided = false

    self.visible = true
end

function Powerup:collides(target)
    -- first, check to see if the left edge of either is farther to the right
    -- than the right edge of the other
    if self.x > target.x + target.width or target.x > self.x + self.width then
        return false
    end

    -- then check to see if the bottom edge of either is higher than the top
    -- edge of the other
    if self.y > target.y + target.height or target.y > self.y + self.height then
        return false
    end 


    -- if the above aren't true, they're overlapping
    return true
    
end

function Powerup:update(dt)
    if self.startupTimer < 1.5 then
        self.startupTimer = self.startupTimer + dt
    else
        self.y = self.y + 2
    end
end

function Powerup:render()
    if self.visible then
        love.graphics.draw(gTextures['main'], gFrames['powerup'][self.type], self.x, self.y)
    end
end

function Powerup:renderBar(key)
    local x = 4
    local y = VIRTUAL_HEIGHT - 20 
    if key == true then
        love.graphics.draw(gTextures['main'], gFrames['powerup'][10], x, y)
        x = x + 16
    end
end