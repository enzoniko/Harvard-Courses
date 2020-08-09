--[[
    GD50
    Legend of Zelda

    Author: Colton Ogden
    cogden@cs50.harvard.edu
]]

Room = Class{}

function Room:init(player)
    self.width = MAP_WIDTH
    self.height = MAP_HEIGHT

    self.tiles = {}
    self:generateWallsAndFloors()

    -- entities in the room
    self.entities = {}
    self:generateEntities()
    
    -- game objects in the room
    self.objects = {}
    self:generateObjects()

    -- doorways that lead to other dungeon rooms
    self.doorways = {}
    table.insert(self.doorways, Doorway('top', false, self))
    table.insert(self.doorways, Doorway('bottom', false, self))
    table.insert(self.doorways, Doorway('left', false, self))
    table.insert(self.doorways, Doorway('right', false, self))

    -- reference to player for collisions, etc.
    self.player = player

    -- used for centering the dungeon rendering
    self.renderOffsetX = MAP_RENDER_OFFSET_X
    self.renderOffsetY = MAP_RENDER_OFFSET_Y

    -- used for drawing when this room is the next room, adjacent to the active
    self.adjacentOffsetX = 0
    self.adjacentOffsetY = 0
end

--[[
    Randomly creates an assortment of enemies for the player to fight.
]]
function Room:generateEntities()
    local types = {'skeleton', 'slime', 'bat', 'ghost', 'spider'}
    local entityHealth = 1
    for i = 1, 10 do

        -- Health has a chance to be greater
        if math.random(1, 20) == 2 then
            entityHealth = math.random(20, 40)
        else
            entityHealth = 1
        end

        local type = types[math.random(#types)]

        table.insert(self.entities, Entity {
            animations = ENTITY_DEFS[type].animations,
            walkSpeed = ENTITY_DEFS[type].walkSpeed or 20,

            -- ensure X and Y are within bounds of the map
            x = math.random(MAP_RENDER_OFFSET_X + TILE_SIZE,
                VIRTUAL_WIDTH - TILE_SIZE * 2 - 16),
            y = math.random(MAP_RENDER_OFFSET_Y + TILE_SIZE,
                VIRTUAL_HEIGHT - (VIRTUAL_HEIGHT - MAP_HEIGHT * TILE_SIZE) + MAP_RENDER_OFFSET_Y - TILE_SIZE - 16),
            
            width = 16,
            height = 16,
            health = entityHealth,

            
            
        })

        self.entities[i].stateMachine = StateMachine {
            ['walk'] = function() return EntityWalkState(self.entities[i]) end,
            ['idle'] = function() return EntityIdleState(self.entities[i]) end
        }

        self.entities[i]:changeState('walk')
    end
end

function Room:generateObjects()
    table.insert(self.objects, GameObject(
        GAME_OBJECT_DEFS['switch'],
        math.random(MAP_RENDER_OFFSET_X + TILE_SIZE,
                    VIRTUAL_WIDTH - TILE_SIZE * 2 - 16),
        math.random(MAP_RENDER_OFFSET_Y + TILE_SIZE,
                    VIRTUAL_HEIGHT - (VIRTUAL_HEIGHT - MAP_HEIGHT * TILE_SIZE) + MAP_RENDER_OFFSET_Y - TILE_SIZE - 16)
    ))

    -- get a reference to the switch
    local switch = self.objects[1]

    -- define a function for the switch that will open all doors in the room
    switch.onCollide = function()
        if switch.state == 'unpressed' then
            switch.state = 'pressed'
            
            -- open every door in the room if we press the switch
            for k, doorway in pairs(self.doorways) do
                doorway.open = true
            end

            gSounds['door']:play()
        end
    end

    -- A5.2 -> Gera as poções na caverna 
    for i = 2, math.random(4, 6) do
        local x = math.random(MAP_RENDER_OFFSET_X + TILE_SIZE, VIRTUAL_WIDTH - TILE_SIZE * 2 - 16)
        local y = math.random(MAP_RENDER_OFFSET_Y + TILE_SIZE, VIRTUAL_HEIGHT - (VIRTUAL_HEIGHT - MAP_HEIGHT * TILE_SIZE) + MAP_RENDER_OFFSET_Y - TILE_SIZE - 16)
        
        while x == self.objects[1].x do
            x = math.random(MAP_RENDER_OFFSET_X + TILE_SIZE, VIRTUAL_WIDTH - TILE_SIZE * 2 - 16)
        end

        while y == self.objects[1].y do
            y = math.random(MAP_RENDER_OFFSET_Y + TILE_SIZE, VIRTUAL_HEIGHT - (VIRTUAL_HEIGHT - MAP_HEIGHT * TILE_SIZE) + MAP_RENDER_OFFSET_Y - TILE_SIZE - 16)
        end

        table.insert(self.objects, GameObject(GAME_OBJECT_DEFS['pot'], x, y))

        local pot = self.objects[i]

        -- Quando a poção colide se pressionarmos return ou enter e a poção não estiver quebrada, levantamos a poção e diminuimos a velocidade do player
        pot.onCollide = function()
            if love.keyboard.wasPressed('return') or love.keyboard.wasPressed('enter') then
                if not pot.broken then
                    pot.lifted = true
                    self.player.lifting = true
                    self.player.walkSpeed = self.player.walkSpeed - 30
                end
            end  
        end 
    end
end

-- A5.1 -> Função que gera os corações
function Room:generateHeart(x, y)
    local heart = GameObject(GAME_OBJECT_DEFS['heart'], x, y)

    -- Quando consumido cura o player por um coração
    heart.onConsume = function()
        heart.consumed = true
        
        self.player.health = math.min(6, self.player.health + 1)
        
        gSounds['broke']:play()
    end

    table.insert(self.objects, heart)
end

--[[
    Generates the walls and floors of the room, randomizing the various varieties
    of said tiles for visual variety.
]]
function Room:generateWallsAndFloors()
    for y = 1, self.height do
        table.insert(self.tiles, {})

        for x = 1, self.width do
            local id = TILE_EMPTY

            if x == 1 and y == 1 then
                id = TILE_TOP_LEFT_CORNER
            elseif x == 1 and y == self.height then
                id = TILE_BOTTOM_LEFT_CORNER
            elseif x == self.width and y == 1 then
                id = TILE_TOP_RIGHT_CORNER
            elseif x == self.width and y == self.height then
                id = TILE_BOTTOM_RIGHT_CORNER
            
            -- random left-hand walls, right walls, top, bottom, and floors
            elseif x == 1 then
                id = TILE_LEFT_WALLS[math.random(#TILE_LEFT_WALLS)]
            elseif x == self.width then
                id = TILE_RIGHT_WALLS[math.random(#TILE_RIGHT_WALLS)]
            elseif y == 1 then
                id = TILE_TOP_WALLS[math.random(#TILE_TOP_WALLS)]
            elseif y == self.height then
                id = TILE_BOTTOM_WALLS[math.random(#TILE_BOTTOM_WALLS)]
            else
                id = TILE_FLOORS[math.random(#TILE_FLOORS)]
            end
            
            table.insert(self.tiles[y], {
                id = id
            })
        end
    end
end
function Room:update(dt)
    -- don't update anything if we are sliding to another room (we have offsets)
    if self.adjacentOffsetX ~= 0 or self.adjacentOffsetY ~= 0 then return end
    
    self.player:update(dt)

    for i = #self.entities, 1, -1 do
        local entity = self.entities[i]

        -- remove entity from the table if health is <= 0
        if entity.health <= 0 then
            -- A5.1 -> 1 in 4 chance of spawning a heart when an entity dies
            if math.random(1, 4) == 2 and not entity.dead then
                self:generateHeart(entity.x, entity.y)
            end
            entity.dead = true
            entity.x = 0
            entity.y = 0
            
        elseif not entity.dead then
            entity:processAI({room = self}, dt)
            entity:update(dt)
            
        end

        -- collision between the player and entities in the room
        if not entity.dead and self.player:collides(entity) and not self.player.invulnerable then
            gSounds['hit-player']:play()
            self.player:damage(1)
            self.player:goInvulnerable(1.5)

            if self.player.health == 0 then
                gStateMachine:change('game-over')
            end
        end
    end
    for k, object in pairs(self.objects) do
        object:update(dt)

        -- A5.1 -> If object is consumed remove it from the table
        if object.consumed == true then
            table.remove(self.objects, k)
        end

        -- A5.3 -> Se o objeto estiver quebrado roda um timer pra apagar ele da table
        if object.broken then
            object.solid = false
            if object.enemyCollided then
                if object.timer - 96 > 0 then
                    object.state = 'broke1'
                    object.timer = object.timer - 1
                else
                    table.remove(self.objects, k)
                    object.timer = 4
                end
            else
                if object.timer > 0 then
                    object.timer = object.timer - 1
                else
                    table.remove(self.objects, k)
                    object.timer = 100
                end
            end
        end

        -- A5.2 -> Se o objeto não estiver levantado o player não está levantando nada
        if object.lifted == false then
            self.player.lifting = false 
        end

        -- A5.2 -> Se o objeto for levantado siga o player e o player está levantando o objeto
        if object.lifted == true then 
            self.player.lifting = true
            object.solid = false
            object.x = self.player.x 
            object.y = self.player.y - 8
            
            -- A5.3 -> Define as variáveis que vão ser usadas na interpolação
            local tiles = 4
            local time

            -- A5.3 -> Se enquanto segurar o objeto clicar space joga o objeto
            if love.keyboard.wasPressed('space') then
                -- Objeto não está mais levantado
                object.lifted = false
                -- Volta a velocidade normal do player
                self.player.walkSpeed = 60
                
                -- Joga pra cima 
                if self.player.direction == 'up' then

                    -- Cálculo das paredes
                    if object.y - (TILE_SIZE * 4) <= MAP_RENDER_OFFSET_Y then
                        tiles = math.min(4, - ((MAP_RENDER_OFFSET_Y - object.y) / TILE_SIZE) - 1)
                    else
                        tiles = 4
                    end
                    time = 0.15 * tiles

                    -- Da dano se o player quebra a poção em cima dele mesmo
                    if tiles < 0 then
                        gSounds['hit-player']:play()
                        self.player:damage(1)
                        self.player:goInvulnerable(1.5)
                    end

                    Timer.tween(time, {
                        [object] = {y = object.y - (TILE_SIZE * tiles)}
                    }):finish(function() object.state = 'broke1' object.broken = true gSounds['broke']:play() end)

                -- Joga pra baixo
                elseif self.player.direction == 'down' then

                    -- Corrige a posição do objeto
                    object.y = object.y + 14
                    -- Cálculo das paredes
                    if (object.y + object.height) + (TILE_SIZE * 4) >= MAP_RENDER_OFFSET_Y + (TILE_SIZE * 9) then
                        tiles = math.min(4, ((MAP_RENDER_OFFSET_Y + TILE_SIZE * 10) - (object.y + object.height)) / TILE_SIZE)
                    else
                        tiles = 4
                    end
                    time = 0.15 * tiles

                    -- Da dano se o player quebra a poção em cima dele mesmo
                    if tiles < 1 then
                        gSounds['hit-player']:play()
                        self.player:damage(1)
                        self.player:goInvulnerable(1.5)
                    end

                    Timer.tween(time, {
                        [object] = {y = object.y + (TILE_SIZE * tiles)}
                    }):finish(function() object.state = 'broke1' object.broken = true gSounds['broke']:play() end)

                -- Joga pra esquerda
                elseif self.player.direction == 'left' then

                    -- Corrige a posição do objeto
                    object.y = object.y + 14
                    -- Cálculo das paredes
                    if (object.x) - (TILE_SIZE * 4) <= MAP_RENDER_OFFSET_X then
                        tiles = math.min(4, - ((MAP_RENDER_OFFSET_X - object.x) / TILE_SIZE) - 1)
                    else
                        tiles = 4
                    end
                    time = 0.15 * tiles

                    -- Da dano se o player quebra a poção em cima dele mesmo
                    if tiles < 0.5 then
                        gSounds['hit-player']:play()
                        self.player:damage(1)
                        self.player:goInvulnerable(1.5)
                    end

                    Timer.tween(time, {
                        [object] = {x = object.x - TILE_SIZE * tiles}
                    }):finish(function() object.state = 'broke1' object.broken = true gSounds['broke']:play() end)

                -- Joga pra direita
                elseif self.player.direction == 'right' then

                    -- Corrige a posição do objeto
                    object.y = object.y + 14
                    -- Cálculo das paredes
                    if (object.x + object.width) + (TILE_SIZE * 4) >= MAP_RENDER_OFFSET_X + (TILE_SIZE * 20) then
                        tiles = math.min(4, ((MAP_RENDER_OFFSET_X + TILE_SIZE * 21) - (object.x + object.width)) / TILE_SIZE)
                    else
                        tiles = 4
                    end
                    time = 0.15 * tiles
                        
                    -- Da dano se o player quebra a poção em cima dele mesmo
                    if tiles < 0.5 then
                        gSounds['hit-player']:play()
                        self.player:damage(1)
                        self.player:goInvulnerable(1.5)
                    end

                    Timer.tween(time, {
                        [object] = {x = object.x + TILE_SIZE * tiles}
                    }):finish(function() object.state = 'broke1' object.broken = true gSounds['broke']:play() end)
                end
            end
        end
  
        -- trigger collision callback on object
        if self.player:collides(object) then
            object:onCollide()
            -- A5.1 -> Se o objeto não for uma poção, consume ele
            if object.type ~= 'pot' then
                object:onConsume()
            end

            -- A5.2 -> Se o objeto for sólido, não deixa o player atravessar
            if object.solid == true then
                if self.player.direction == 'down' then
                    self.player.y = self.player.y - 1
                elseif self.player.direction == 'up' then
                    self.player.y = self.player.y + 1
                elseif self.player.direction == 'left' then
                    self.player.x = self.player.x + 1 
                elseif self.player.direction == 'right' then
                    self.player.x = self.player.x - 1
                end
            end
        end

        for i = #self.entities, 1, -1 do
            local entity = self.entities[i]

            -- A5.3 -> Se um monstro colide com um objeto que não estã levantado
            if entity:collides(object) and object.lifted == false then
                -- Da um de dano no monstro    
                gSounds['broke']:play()            
                object.enemyCollided = true
                object.broken = true
                entity:damage(1)
                entity:goInvulnerable(1.5)
        
                -- Muda a direção do monstro
                if entity.direction == 'left' then
                    entity.x = entity.x + entity.walkSpeed * dt
                elseif entity.direction == 'right' then
                    entity.x = entity.x - entity.walkSpeed * dt
                elseif entity.direction == 'up' then
                    entity.y = entity.y + entity.walkSpeed * dt
                elseif entity.direction == 'down' then
                    entity.y = entity.y - entity.walkSpeed * dt
                end
            end
        end

    end
end

function Room:render()
    for y = 1, self.height do
        for x = 1, self.width do
            local tile = self.tiles[y][x]
            love.graphics.draw(gTextures['tiles'], gFrames['tiles'][tile.id],
                (x - 1) * TILE_SIZE + self.renderOffsetX + self.adjacentOffsetX, 
                (y - 1) * TILE_SIZE + self.renderOffsetY + self.adjacentOffsetY)
        end
    end

    -- render doorways; stencils are placed where the arches are after so the player can
    -- move through them convincingly
    for k, doorway in pairs(self.doorways) do
        doorway:render(self.adjacentOffsetX, self.adjacentOffsetY)
    end

    for k, object in pairs(self.objects) do
        object:render(self.adjacentOffsetX, self.adjacentOffsetY)
    end

    for k, entity in pairs(self.entities) do
        if not entity.dead then entity:render(self.adjacentOffsetX, self.adjacentOffsetY) end
    end

    -- stencil out the door arches so it looks like the player is going through
    love.graphics.stencil(function()
        -- left
        love.graphics.rectangle('fill', -TILE_SIZE - 6, MAP_RENDER_OFFSET_Y + (MAP_HEIGHT / 2) * TILE_SIZE - TILE_SIZE,
            TILE_SIZE * 2 + 6, TILE_SIZE * 2)
        
        -- right
        love.graphics.rectangle('fill', MAP_RENDER_OFFSET_X + (MAP_WIDTH * TILE_SIZE) - 6,
            MAP_RENDER_OFFSET_Y + (MAP_HEIGHT / 2) * TILE_SIZE - TILE_SIZE, TILE_SIZE * 2 + 6, TILE_SIZE * 2)
        
        -- top
        love.graphics.rectangle('fill', MAP_RENDER_OFFSET_X + (MAP_WIDTH / 2) * TILE_SIZE - TILE_SIZE,
            -TILE_SIZE - 6, TILE_SIZE * 2, TILE_SIZE * 2 + 12)
        
        --bottom
        love.graphics.rectangle('fill', MAP_RENDER_OFFSET_X + (MAP_WIDTH / 2) * TILE_SIZE - TILE_SIZE,
            VIRTUAL_HEIGHT - TILE_SIZE - 6, TILE_SIZE * 2, TILE_SIZE * 2 + 12)
    end, 'replace', 1)

    love.graphics.setStencilTest('less', 1)
    
    if self.player then
        self.player:render()
    end

    -- A5.3 -> Se o objeto estiver levantado renderiza em cima do player
    for k, object in pairs(self.objects) do
        if object.lifted == true then
            object:render(self.adjacentOffsetX, self.adjacentOffsetY)
        end
    end

    love.graphics.setStencilTest()
end