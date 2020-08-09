--[[
    GD50
    Flappy Bird Remake

    bird11
    "The Audio Update"

    Author: Colton Ogden
    cogden@cs50.harvard.edu

    A mobile game by Dong Nguyen that went viral in 2013, utilizing a very simple 
    but effective gameplay mechanic of avoiding pipes indefinitely by just tapping 
    the screen, making the player's bird avatar flap its wings and move upwards slightly. 
    A variant of popular games like "Helicopter Game" that floated around the internet
    for years prior. Illustrates some of the most basic procedural generation of game
    levels possible as by having pipes stick out of the ground by varying amounts, acting
    as an infinitely generated obstacle course for the player.
]]

-- push is a library that will allow us to draw our game at a virtual
-- resolution, instead of however large our window is; used to provide
-- a more retro aesthetic
--
-- https://github.com/Ulydev/push
push = require 'push'

-- the "Class" library we're using will allow us to represent anything in
-- our game as code, rather than keeping track of many disparate variables and
-- methods
--
-- https://github.com/vrld/hump/blob/master/class.lua
Class = require 'class'

-- a basic StateMachine class which will allow us to transition to and from
-- game states smoothly and avoid monolithic code in one file
require 'StateMachine'

require 'states/BaseState'
require 'states/CountdownState'
require 'states/PlayState'
require 'states/ScoreState'
require 'states/TitleScreenState'

require 'Bird'
require 'Pipe'
require 'PipePair'

-- physical screen dimensions
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720

-- virtual resolution dimensions
VIRTUAL_WIDTH = 512
VIRTUAL_HEIGHT = 288

COUNTDOWN_TIME = 0.75
count = 120
timer = 0
noite = false
tarde = false
tarde1 = false
tarde2 = false
local backgroundDay = love.graphics.newImage('backgroundDia.png')
local backgroundAfterNoon = love.graphics.newImage('backgroundTarde.png')
local backgroundAfterNoon1 = love.graphics.newImage('backgroundTarde1.png')
local backgroundAfterNoon2 = love.graphics.newImage('backgroundTarde2.png')
local backgroundNight = love.graphics.newImage('backgroundNoite.png')

local backgroundScroll = 0

local groundDay = love.graphics.newImage('ground.png')
local groundScroll = 0

local BACKGROUND_SCROLL_SPEED = 30
local GROUND_SCROLL_SPEED = 60

local BACKGROUND_LOOPING_POINT = 413

-- global variable we can use to scroll the map
scrolling = true
sound = true
music = true
play = false
function love.load()
    -- initialize our nearest-neighbor filter
    love.graphics.setDefaultFilter('nearest', 'nearest')
    
    -- seed the RNG
    math.randomseed(os.time())

    -- app window title
    love.window.setTitle('Fifty Bird')

    -- initialize our nice-looking retro text fonts
    smallFont = love.graphics.newFont('font.ttf', 8)
    mediumFont = love.graphics.newFont('flappy.ttf', 14)
    flappyFont = love.graphics.newFont('flappy.ttf', 28)
    hugeFont = love.graphics.newFont('flappy.ttf', 56)
    love.graphics.setFont(flappyFont)

    -- initialize our table of sounds
    sounds = {
        ['jump'] = love.audio.newSource('jump.wav', 'static'),
        ['explosion'] = love.audio.newSource('explosion.wav', 'static'),
        ['hurt'] = love.audio.newSource('hurt.wav', 'static'),
        ['score'] = love.audio.newSource('score.wav', 'static'),

        -- https://freesound.org/people/xsgianni/sounds/388079/
        ['music'] = love.audio.newSource('marios_way.mp3', 'static')
    }

    -- kick off music
    
    sounds['music']:setLooping(true)
    sounds['music']:play()

    -- initialize our virtual resolution
    push:setupScreen(VIRTUAL_WIDTH, VIRTUAL_HEIGHT, WINDOW_WIDTH, WINDOW_HEIGHT, {
        vsync = true,
        fullscreen = false,
        resizable = true
    })

    -- initialize state machine with all state-returning functions
    gStateMachine = StateMachine {
        ['title'] = function() play = false return TitleScreenState() end,
        ['countdown'] = function() play = false return CountdownState() end,
        ['play'] = function() play = true return PlayState() end,
        ['score'] = function() play = false return ScoreState() end
    }
    gStateMachine:change('title')

    -- initialize input table
    love.keyboard.keysPressed = {}
end

function love.resize(w, h)
    push:resize(w, h)
end

function love.keypressed(key)
    -- add to our table of keys pressed this frame
    love.keyboard.keysPressed[key] = true

    if key == 'escape' then
        love.event.quit()
    end

    if key == 'p' and play == true then 
        sounds['hurt']:play()
        if scrolling then
            scrolling = false
            if sound then
            sound = false
            sounds['music']:setVolume(0)
            sounds['jump']:setVolume(0)
            sounds['explosion']:setVolume(0)
            sounds['hurt']:setVolume(0)
            sounds['score']:setVolume(0)
            end
        else
            if not sound then
                sound = true
                sounds['music']:setVolume(1)
                sounds['jump']:setVolume(1)
                sounds['explosion']:setVolume(1)
                sounds['hurt']:setVolume(1)
                sounds['score']:setVolume(1)
            end
            scrolling = true      
        end
    end

    if key == 'm' then
        if music then
            music = false
            sounds['music']:setVolume(0)
        else
            music = true
            sounds['music']:setVolume(1)
        end
    end

    if key == 's' then
        if sound then
            sound = false
            sounds['music']:setVolume(0)
            sounds['jump']:setVolume(0)
            sounds['explosion']:setVolume(0)
            sounds['hurt']:setVolume(0)
            sounds['score']:setVolume(0)

        else
            sound = true
            sounds['music']:setVolume(1)
            sounds['jump']:setVolume(1)
            sounds['explosion']:setVolume(1)
            sounds['hurt']:setVolume(1)
            sounds['score']:setVolume(1)
        end
    end
end

function love.keyboard.wasPressed(key)
    if love.keyboard.keysPressed[key] then
        return true
    else
        return false
    end
end

function love.update(dt)
    if scrolling then
        timer = timer + dt
        if timer > COUNTDOWN_TIME then
            timer = timer % COUNTDOWN_TIME
            count = count - 1

            if count == 120 then
                noite = false
                tarde = false
                tarde1 = false
                tarde2 = false
            end

            if count == 90 then
                tarde = true
                tarde1 = false
                tarde2 = false
            end
            
            if count == 60 then
                tarde1 = true
                tarde2 = false 
            end

            if count == 30 then
                tarde2 = true
                tarde1 = false
            end

            if count == 0 then
                noite = true
                tarde = false
                tarde1 = false 
                tarde2 = false
                count = 120
                timer = 0
            end
        end
        backgroundScroll = (backgroundScroll + BACKGROUND_SCROLL_SPEED * dt) % BACKGROUND_LOOPING_POINT
        groundScroll = (groundScroll + GROUND_SCROLL_SPEED * dt) % VIRTUAL_WIDTH
    end

    gStateMachine:update(dt)
    
    love.keyboard.keysPressed = {}
end

function love.draw()
    push:start()
    
    
    if noite == false and tarde == false then
        -- dia
        love.graphics.draw(backgroundDay, -backgroundScroll, 0)
        gStateMachine:render()
        love.graphics.draw(groundDay, -groundScroll, VIRTUAL_HEIGHT - 16)
    elseif noite == true and tarde == false and tarde1 == false and tarde2 == false then
        -- noite
        love.graphics.draw(backgroundNight, -backgroundScroll, 0)
        gStateMachine:render()
        love.graphics.draw(groundDay, -groundScroll, VIRTUAL_HEIGHT - 16)
    elseif tarde == true then 
        if tarde1 == false and tarde2 == false then
            -- começo da tarde
            love.graphics.draw(backgroundAfterNoon, -backgroundScroll, 0)
            gStateMachine:render()
            love.graphics.draw(groundDay, -groundScroll, VIRTUAL_HEIGHT - 16)
        elseif tarde1 == true and tarde2 == false then
            -- meio da tarde
            love.graphics.draw(backgroundAfterNoon1, -backgroundScroll, 0)
            gStateMachine:render()
            love.graphics.draw(groundDay, -groundScroll, VIRTUAL_HEIGHT - 16)
        elseif tarde1 == false and tarde2 == true then 
            -- fim da tarde
            love.graphics.draw(backgroundAfterNoon2, -backgroundScroll, 0)
            gStateMachine:render()
            love.graphics.draw(groundDay, -groundScroll, VIRTUAL_HEIGHT - 16)
        end
    end
    push:finish()
end
