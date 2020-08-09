--[[
    GD50
    Breakout Remake

    -- PlayState Class --

    Author: Colton Ogden
    cogden@cs50.harvard.edu

    Represents the state of the game in which we are actively playing;
    player should control the paddle, with the ball actively bouncing between
    the bricks, walls, and the paddle. If the ball goes below the paddle, then
    the player should lose one point of health and be taken either to the Game
    Over screen if at 0 health or the Serve screen otherwise.
]]

PlayState = Class{__includes = BaseState}

--[[
    We initialize what's in our PlayState via a state table that we pass between
    states as we go from playing to serving.
]]
function PlayState:enter(params)
    self.paddle = params.paddle
    self.bricks = params.bricks
    self.health = params.health
    self.score = params.score
    self.highScores = params.highScores

    self.balls = {params.ball}
    self.ballCount = 1

    self.level = params.level
    self.recoverPoints = params.recoverPoints

    self.hasKeyPowerup = false

    self.timer = 1

    -- give ball random starting velocity
    self.balls[1].dx = math.random(-200, 200)
    self.balls[1].dy = math.random(-50, -60)

    self.powerups = {}

    self.numLockedBricks = params.numLockedBricks

    self.inferno = false
end

function PlayState:update(dt)
    if self.paused then
        if love.keyboard.wasPressed('space') then
            self.paused = false
            gSounds['pause']:play()
        else
            return
        end
    elseif love.keyboard.wasPressed('space') then
        self.paused = true
        gSounds['pause']:play()
        return
    end

    
    if self.timer >= 0 then
        self.timer = self.timer - dt
    else
        powerup = Powerup(math.random(0, VIRTUAL_WIDTH - 16), -20, (self.numLockedBricks > 0) and (not self.hasKeyPowerup))
        table.insert(self.powerups, powerup)
        self.timer = math.random(5, 15)
    end

     -- update positions based on velocity
     self.paddle:update(dt)

    for k, powerup in pairs(self.powerups) do
        powerup:update(dt)
        if powerup:collides(self.paddle) then
            if powerup.type == 3 then
                self:plusHeartPowerup()
            elseif powerup.type == 4 then
                self.inferno = true
            elseif powerup.type == 9 then
                self:moreBallsPowerup()
            elseif powerup.type == 10 then
                self.hasKeyPowerup = true
                gSounds['powerup']:play()
            end
            table.remove(self.powerups, k)
        end
    end

    
    if self.inferno == true then
        self:DragonBallsPowerup()
    end

  


    for k, ball in pairs(self.balls) do 
        ball:update(dt)

        if ball:collides(self.paddle) then
            -- raise ball above paddle in case it goes below it, then reverse dy
            ball.y = self.paddle.y - 8
            ball.dy = -ball.dy
    
            --
            -- tweak angle of bounce based on where it hits the paddle
            --
    
            -- if we hit the paddle on its left side while moving left...
            if ball.x < self.paddle.x + (self.paddle.width / 2) and self.paddle.dx < 0 then
                ball.dx = -50 + -(8 * (self.paddle.x + self.paddle.width / 2 - ball.x))
            
            -- else if we hit the paddle on its right side while moving right...
            elseif ball.x > self.paddle.x + (self.paddle.width / 2) and self.paddle.dx > 0 then
                ball.dx = 50 + (8 * math.abs(self.paddle.x + self.paddle.width / 2 - ball.x))
            end
    
            gSounds['paddle-hit']:play()
        end
    
        -- detect collision across all bricks with the ball
        for i, brick in pairs(self.bricks) do

            -- only check collision if we're in play
            if brick.inPlay and ball:collides(brick) then

                local brickUnlocked = false
                if brick.locked == true and self.hasKeyPowerup then
                    self.score = self.score + 1000
                    brickUnlocked = true
                elseif brick.locked == true then

                else
                    -- add to score
                    self.score = self.score + (brick.tier * 200 + brick.color * 25)
                end

                -- trigger the brick's hit function, which removes it from play
                brick:hit(self.hasKeyPowerup)
                if brickUnlocked then
                    self.hasKeyPowerup = false
                    self.numLockedBricks = self.numLockedBricks - 1
                end

                if self.score > self.recoverPoints then
                    -- Somar vida sem que passe de 3
                    self.health = math.min(3, self.health + 1)

                    if self.paddle.size < 4 then
                        self.paddle:resize(self.paddle.size + 1)
                    end

                    self.recoverPoints = math.min(100000, self.recoverPoints * 2)
                
                    gSounds['recover']:play()
                end

                -- go to our victory screen if there are no more bricks left
                if self:checkVictory() then
                    gSounds['victory']:play()
                    

                    gStateMachine:change('victory', {
                        level = self.level,
                        paddle = self.paddle,
                        health = self.health,
                        score = self.score,
                        highScores = self.highScores,

                        ball = ball,
                        recoverPoints = self.recoverPoints,
                    })
                end

                --
                -- collision code for bricks
                --
                -- we check to see if the opposite side of our velocity is outside of the brick;
                -- if it is, we trigger a collision on that side. else we're within the X + width of
                -- the brick and should check to see if the top or bottom edge is outside of the brick,
                -- colliding on the top or bottom accordingly 
                --

                -- left edge; only check if we're moving right, and offset the check by a couple of pixels
                -- so that flush corner hits register as Y flips, not X flips
                if ball.x + 2 < brick.x and ball.dx > 0 then
                    
                    -- flip x velocity and reset position outside of brick
                    ball.dx = -ball.dx
                    ball.x = brick.x - 8
                
                -- right edge; only check if we're moving left, , and offset the check by a couple of pixels
                -- so that flush corner hits register as Y flips, not X flips
                elseif ball.x + 6 > brick.x + brick.width and ball.dx < 0 then
                    
                    -- flip x velocity and reset position outside of brick
                    ball.dx = -ball.dx
                    ball.x = brick.x + 32
                
                -- top edge if no X collisions, always check
                elseif ball.y < brick.y then
                    
                    -- flip y velocity and reset position outside of brick
                    ball.dy = -ball.dy
                    ball.y = brick.y - 8
                
                -- bottom edge if no X collisions or top collision, last possibility
                else
                    
                    -- flip y velocity and reset position outside of brick
                    ball.dy = -ball.dy
                    ball.y = brick.y + 16
                end

                -- slightly scale the y velocity to speed up the game, capping at +- 150
                if math.abs(ball.dy) < 150 then
                    ball.dy = ball.dy * 1.02
                end

                -- only allow colliding with one brick, for corners
                break
            end
        end

        -- if ball goes below bounds, revert to serve state and decrease health
        if ball.y >= VIRTUAL_HEIGHT then
            self.inferno = false
            if self.ballCount <= 1 then
                self.health = self.health - 1
                gSounds['hurt']:play()

                if self.paddle.size > 1 then
                    self.paddle:resize(self.paddle.size - 1)
                end
            
                if self.health == 0 then
                    gStateMachine:change('game-over', {
                        score = self.score,
                        highScores = self.highScores
                    })
                else
                    gStateMachine:change('serve', {
                        paddle = self.paddle,
                        bricks = self.bricks,
                        health = self.health,
                        score = self.score,
                        highScores = self.highScores,
                        level = self.level,

                        recoverPoints = self.recoverPoints,
                    })
                end
            else 
                table.remove(self.balls, k)
                self.ballCount = self.ballCount - 1
            end
        end
    end
    -- for rendering particle systems
    for k, brick in pairs(self.bricks) do
        brick:update(dt)
    end

    if love.keyboard.wasPressed('escape') then
        love.event.quit()
    end
end

function PlayState:render()
      -- render bricks
      for k, brick in pairs(self.bricks) do
        brick:render()
    end

    -- render all particle systems
    for k, brick in pairs(self.bricks) do
        brick:renderParticles()
    end

    self.paddle:render()

    for k, powerup in pairs(self.powerups) do
        powerup:render()
    end

    for k, ball in pairs(self.balls) do
        ball:render()
    end

    renderScore(self.score)
    renderHealth(self.health)
    Powerup:renderBar(self.hasKeyPowerup)

    -- pause text, if paused
    if self.paused then
        love.graphics.setFont(gFonts['large'])
        love.graphics.printf("PAUSED", 0, VIRTUAL_HEIGHT / 2 - 16, VIRTUAL_WIDTH, 'center')
    end
end

function PlayState:checkVictory()
    for k, brick in pairs(self.bricks) do
        if brick.inPlay then
            return false
        end 
    end

    return true
end

function PlayState:plusHeartPowerup()
    self.health = math.min(3, self.health + 1)
    gSounds['powerup']:play()
end

function PlayState:DragonBallsPowerup()
    ball3 = Ball(3)

    ball3.x = self.paddle.x + self.paddle.width / 2
    ball3.y = self.paddle.y
    ball3.dx = self.paddle.x + self.paddle.width / 2
    ball3.dy = -300
    table.insert(self.balls, ball3)

    self.ballCount = self.ballCount + 1

    gSounds['powerup']:play()
end

function PlayState:moreBallsPowerup()
    ball1 = Ball(math.random(7))

    ball1.x = self.balls[1].x
    ball1.y = self.balls[1].y
    ball1.dx = self.balls[1].dx
    ball1.dy = math.abs(self.balls[1].dy / 2)
    table.insert(self.balls, ball1)

    ball2 = Ball(math.random(7))

    ball2.x = self.balls[1].x
    ball2.y = self.balls[1].y
    ball2.dx = self.balls[1].dx
    ball2.dy = math.abs(self.balls[1].dy / 4)
    table.insert(self.balls, ball2)

    self.ballCount = self.ballCount + 2

    gSounds['powerup']:play()
end


