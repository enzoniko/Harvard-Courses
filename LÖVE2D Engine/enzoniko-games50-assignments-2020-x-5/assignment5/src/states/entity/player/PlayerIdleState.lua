--[[
    GD50
    Legend of Zelda

    Author: Colton Ogden
    cogden@cs50.harvard.edu
]]

PlayerIdleState = Class{__includes = EntityIdleState}

function PlayerIdleState:enter(params)
    -- render offset for spaced character sprite
    self.entity.offsetY = 5
    self.entity.offsetX = 0
end

function PlayerIdleState:update(dt)
    EntityIdleState.update(self, dt)
end

function PlayerIdleState:update(dt)
    if love.keyboard.isDown('left') or love.keyboard.isDown('right') or
       love.keyboard.isDown('up') or love.keyboard.isDown('down') then
        -- A5.2 -> Se o player está levantando alguma coisa muda pro Walk Pot state em vez do walk state
        if self.entity.lifting == true then
            self.entity:changeState('pot-walk')
        elseif self.entity.lifting == false then 
            self.entity:changeState('walk')
        end
    end

    if love.keyboard.wasPressed('space') then
        -- A5.2 -> Se o player estiver levantando e pressionar espaço, faz com que ele não esteja mais levantando nada e muda pro estado idle em vez de swing sword
        if self.entity.lifting == true then
            self.entity.lifting = false
            self.entity:changeState('idle')
        else
            self.entity:changeState('swing-sword')
        end
    end

    -- A5.2 -> Sempre que for pressionado o enter ou o return muda pro lift pot state
    if love.keyboard.wasPressed('return') or love.keyboard.wasPressed('enter') then
        self.entity:changeState('lift-pot')
    end
end