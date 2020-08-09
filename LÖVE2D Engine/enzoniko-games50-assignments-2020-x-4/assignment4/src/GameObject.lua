--[[
    GD50
    -- Super Mario Bros. Remake --

    Author: Colton Ogden
    cogden@cs50.harvard.edu
]]

GameObject = Class{}

function GameObject:init(def)
    self.x = def.x
    self.y = def.y
    self.texture = def.texture
    self.width = def.width
    self.height = def.height
    self.frame = def.frame
    self.unlocked = false
    self.solid = def.solid
    self.collidable = def.collidable
    self.consumable = def.consumable
    self.onCollide = def.onCollide
    self.onConsume = def.onConsume
    self.hit = def.hit
    self.unlocked = false
end

function GameObject:collides(target)
    return not (target.x + 3 > self.x + self.width or self.x > target.x - 3 + target.width or
            target.y > self.y + self.height or self.y > target.y + target.height)
end

function GameObject:update(dt)

end

function GameObject:render()
    if self.texture == 'flags' then
        love.graphics.draw(gTextures[self.texture], gFrames[self.texture][self.frame], self.x, self.y, 0, self.direction == 'right' and 1 or -1, 1, 8, 10)
    elseif self.unlocked == false then
        love.graphics.draw(gTextures[self.texture], gFrames[self.texture][self.frame], self.x, self.y)
    else 
        self.solid = false
    end
end