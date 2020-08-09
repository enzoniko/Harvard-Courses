--[[
    GD50
    Match-3 Remake

    -- Tile Class --

    Author: Colton Ogden
    cogden@cs50.harvard.edu

    The individual tiles that make up our game board. Each Tile can have a
    color and a variety, with the varietes adding extra points to the matches.
]]

Tile = Class{}

function Tile:init(x, y, color, variety)
    -- board positions
    self.gridX = x
    self.gridY = y

    -- coordinate positions
    self.x = (self.gridX - 1) * 32
    self.y = (self.gridY - 1) * 32

    -- tile appearance/points
    self.color = color
    self.variety = variety
end

function Tile:update(dt)

end

--[[
    Function to swap this tile with another tile, tweening the two's positions.
]]
function Tile:swap(tile)


end

function Tile:render(x, y)
    -- draw shadow for all tile varietys
    if self.variety > 6 then
        love.graphics.setColor(34/255, 32/255, 52/255, 1)
        love.graphics.draw(gTextures['main'], gFrames['tiles'][self.color][self.variety - 2],
            self.x + x + 2, self.y + y + 2)
    else
        love.graphics.setColor(34/255, 32/255, 52/255, 1)
        love.graphics.draw(gTextures['main'], gFrames['tiles'][self.color][self.variety],
            self.x + x + 2, self.y + y + 2)
    end

    -- draw tile itself
    if self.variety == 7 then
        -- if the tile variety is 7 (shiny) make the tile blink and have alternating patterns 
        love.graphics.setColor(1, 1, 1, 1)
        love.graphics.draw(gTextures['main'], gFrames['tiles'][self.color][self.variety - math.random(1, 4)],
        self.x + x, self.y + y)

        love.graphics.setBlendMode('add')

        if math.random(1, 4) == 1 then
            love.graphics.setColor(0, 1, 1, 96/255)
            love.graphics.rectangle('fill', self.x + x, self.y + y, 32, 32, 4)
        else
            love.graphics.setColor(0, 1, 1, 0)
            love.graphics.rectangle('fill', self.x + x, self.y + y, 32, 32, 4)
        end

        -- back to alpha
        love.graphics.setBlendMode('alpha')
    else
        love.graphics.setColor(1, 1, 1, 1)
        love.graphics.draw(gTextures['main'], gFrames['tiles'][self.color][self.variety],
        self.x + x, self.y + y)
    end
end