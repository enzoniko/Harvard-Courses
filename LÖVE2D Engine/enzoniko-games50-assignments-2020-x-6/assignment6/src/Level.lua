--[[
    GD50
    Angry Birds

    Author: Colton Ogden
    cogden@cs50.harvard.edu
]]

Level = Class{}

function Level:init()
    -- create a new "world" (where physics take place), with no x gravity
    -- and 30 units of Y gravity (for downward force)
    self.world = love.physics.newWorld(0, 300)

    -- bodies we will destroy after the world update cycle; destroying these in the
    -- actual collision callbacks can cause stack overflow and other errors
    self.destroyedBodies = {}

    -- define collision callbacks for our world; the World object expects four,
    -- one for different stages of any given collision
    function beginContact(a, b, coll)

        -- Handle all collision with every object
        self:handleCollide(a, b, 'Obstacle', 'Alien')
        self:handleCollide(a, b, 'Player', 'Alien')
        self:handleCollide(a, b, 'Ground', 'Alien')
        self:handleCollide(a, b, 'Ground', 'Obstacle')
        self:handleCollide(a, b, 'Obstacle', 'Player')
        self:handleCollide(a, b, 'Player', 'Ground')

    end

    -- the remaining three functions here are sample definitions, but we are not
    -- implementing any functionality with them in this demo; use-case specific
    function endContact(a, b, coll)
   
    end

    function preSolve(a, b, coll)

    end

    function postSolve(a, b, coll, normalImpulse, tangentImpulse)

    end

    -- register just-defined functions as collision callbacks for world
    self.world:setCallbacks(beginContact, endContact, preSolve, postSolve)

    -- shows alien before being launched and its trajectory arrow
    self.launchMarker = AlienLaunchMarker(self.world)

    -- aliens in our scene
    self.aliens = {}

    -- obstacles guarding aliens that we can destroy
    self.obstacles = {}

    -- simple edge shape to represent collision for ground
    self.edgeShape = love.physics.newEdgeShape(0, 0, VIRTUAL_WIDTH * 3, 0)

    -- spawn an alien to try and destroy
    local level = math.random(1, 4)
    for i = 1, #LEVELS[tostring(level)]['aliens'].type do
        table.insert(self.aliens, Alien(self.world, LEVELS[tostring(level)]['aliens'].type[i], LEVELS[tostring(level)]['aliens'].x[i], LEVELS[tostring(level)]['aliens'].y[i], 'Alien'))
    end

    for i = 1, #LEVELS[tostring(level)]['obstacles'].type do
        table.insert(self.obstacles, Obstacle(self.world, LEVELS[tostring(level)]['obstacles'].type[i],
            LEVELS[tostring(level)]['obstacles'].x[i], LEVELS[tostring(level)]['obstacles'].y[i]))
    end
    
    -- ground data
    self.groundBody = love.physics.newBody(self.world, -VIRTUAL_WIDTH, VIRTUAL_HEIGHT - 35, 'static')
    self.groundFixture = love.physics.newFixture(self.groundBody, self.edgeShape, 50)
    self.groundFixture:setFriction(50)
    self.groundFixture:setUserData('Ground')

    -- background graphics
    self.background = Background()
end

function Level:handleCollide(a, b, first, second)
    local types = {}
    types[a:getUserData()] = true
    types[b:getUserData()] = true

    -- if we collided between both a player and an obstacle...
    if types['Obstacle'] and types['Player'] then
        gSounds['bounce']:stop()
        gSounds['bounce']:play()

        -- destroy the obstacle if player's combined velocity is high enough
        self.launchMarker.collided = true
    
    -- if we hit the ground, play a bounce sound
    elseif types['Player'] and types['Ground'] then
        if self.launchMarker.alien then
            local xPos, yPos = self.launchMarker.alien.body:getPosition()
            if xPos < VIRTUAL_WIDTH then
                gSounds['bounce']:stop()
                gSounds['bounce']:play()
            end
        end
    else
        -- Destroy objects that collide 
        if types[first] and types[second] then
            self:handleDestroyedBodies(a, b)
        end
    end

end

function Level:handleDestroyedBodies(first, second)
   
    if first:getUserData() == 'Player' then
        local velX, velY = first:getBody():getLinearVelocity()
        local sumVel = math.abs(velX) + math.abs(velY)
        self.launchMarker.collided = true
        if sumVel > 50 then
            table.insert(self.destroyedBodies, second:getBody())
        end
    elseif first:getUserData() == 'Ground' then
        local velX, velY = second:getBody():getLinearVelocity()
        local sumVel = math.abs(velX) + math.abs(velY)

        if sumVel > 50 then
            table.insert(self.destroyedBodies, second:getBody())
        end
    else
        local velX, velY = second:getBody():getLinearVelocity()
        local sumVel = math.abs(velX) + math.abs(velY)

        if sumVel > 50 then
            table.insert(self.destroyedBodies, first:getBody())
        end
    end
end

function Level:update(dt)
    -- update launch marker, which shows trajectory
    self.launchMarker:update(dt)

    -- Box2D world update code; resolves collisions and processes callbacks
    self.world:update(dt)

    -- destroy all bodies we calculated to destroy during the update call
    for k, body in pairs(self.destroyedBodies) do
        if not body:isDestroyed() then 
            body:destroy()
        end
    end

    -- reset destroyed bodies to empty table for next update phase
    self.destroyedBodies = {}

    -- remove all destroyed obstacles from level
    for i = #self.obstacles, 1, -1 do
        if self.obstacles[i].body:isDestroyed() then
            table.remove(self.obstacles, i)

            -- play random wood sound effect
            local soundNum = math.random(5)
            gSounds['break' .. tostring(soundNum)]:stop()
            gSounds['break' .. tostring(soundNum)]:play()
        end
    end

    -- remove all destroyed aliens from level
    for i = #self.aliens, 1, -1 do
        if self.aliens[i].body:isDestroyed() then
            table.remove(self.aliens, i)
            gSounds['kill']:stop()
            gSounds['kill']:play()
        end
    end

    -- replace launch marker if original alien stopped moving
    if self.launchMarker.launched then
        local xPos, yPos = self.launchMarker.alien.body:getPosition()
        local xVel, yVel = self.launchMarker.alien.body:getLinearVelocity()
        
        -- if we fired our alien to the left or it's almost done rolling, respawn
        if xPos < 0 or (math.abs(xVel) + math.abs(yVel) < 1.5) then
            self.launchMarker.alien.body:destroy()
            if self.launchMarker.alien2 and self.launchMarker.alien3 then
                self.launchMarker.alien2.body:destroy()
                self.launchMarker.alien3.body:destroy()
            end
            self.launchMarker = AlienLaunchMarker(self.world)

            -- re-initialize level if we have no more aliens
            if #self.aliens == 0 then
                gStateMachine:change('start')
            end
        end
    end
end

function Level:render()
    -- render ground tiles across full scrollable width of the screen
    for x = -VIRTUAL_WIDTH, VIRTUAL_WIDTH * 2, 35 do
        love.graphics.draw(gTextures['tiles'], gFrames['tiles'][12], x, VIRTUAL_HEIGHT - 35)
    end

    self.launchMarker:render()

    for k, alien in pairs(self.aliens) do
        alien:render()
    end

    for k, obstacle in pairs(self.obstacles) do
        obstacle:render()
    end

    -- render instruction text if we haven't launched bird
    if not self.launchMarker.launched then
        love.graphics.setFont(gFonts['medium'])
        love.graphics.setColor(0, 0, 0, 1)
        love.graphics.printf('Click and drag circular alien to shoot!',
            0, 64, VIRTUAL_WIDTH, 'center')
        love.graphics.setColor(1, 1, 1, 1)
    end

    -- render victory text if all aliens are dead
    if #self.aliens == 0 then
        love.graphics.setFont(gFonts['huge'])
        love.graphics.setColor(0, 0, 0, 1)
        love.graphics.printf('VICTORY', 0, VIRTUAL_HEIGHT / 2 - 32, VIRTUAL_WIDTH, 'center')
        love.graphics.setColor(1, 1, 1, 1)
    end
end