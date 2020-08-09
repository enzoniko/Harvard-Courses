--[[
    GD50
    Super Mario Bros. Remake

    Author: Colton Ogden
    cogden@cs50.harvard.edu
]]

PlayerIdleState = Class{__includes = BaseState}

function PlayerIdleState:init(player)
    self.player = player

    self.animation = Animation {
        frames = {1},
        interval = 1
    }

    self.player.currentAnimation = self.animation
end

function PlayerIdleState:update(dt)
    if love.keyboard.isDown('left') or love.keyboard.isDown('right') then
        self.player:changeState('walking')
    end

    if love.keyboard.wasPressed('space') then
        self.player:changeState('jump')
    end

    -- check if we've collided with any entities and die if so
    for k, entity in pairs(self.player.level.entities) do
        if entity:collides(self.player) then
            gSounds['death']:play()
            gStateMachine:change('start')
            gWidth = 50
            gScore = 0
            GAMEOVER = true
        end
    end

    for k, object in pairs(self.player.level.objects) do
        if object:collides(self.player) then
            if object.consumable then
                object.onConsume(self.player)
                table.remove(self.player.level.objects, k)
                if self.player.newLevel == true then
                    gWidth = gWidth + 10
                    gStateMachine:change('start')
                    self.player.newLevel = false 
                    gStateMachine:change('play')
                end
            end
        end
    end
end