--[[
    GD50
    Pokemon

    Author: Colton Ogden
    cogden@cs50.harvard.edu
]]

DialogueState = Class{__includes = BaseState}

function DialogueState:init(text, callback)
    self.t = {}
    self.str = text
    self.x = 1
    self.actualText = ''
    self.textbox = Textbox(6, 6, VIRTUAL_WIDTH - 12, 64, 'Hey!', gFonts['small'])
    self.callback = callback or function() end
end

function DialogueState:update(dt)
    for i = 1, string.len(self.str) do 
        self.t[i] = (string.sub(self.str, i, i))
    end
    
    Timer.every(self.x, function()
        
        if self.x > #self.t then
            self.actualText = self.actualText
        else
            self.actualText = self.actualText .. self.t[self.x]
        end
        self.textbox = Textbox(6, 6, VIRTUAL_WIDTH - 12, 64, self.actualText, gFonts['small'])
        self.x = self.x + 1
    end)
    
    self.textbox:update(dt)

    if self.textbox:isClosed() then
        self.callback()
        gStateStack:pop()
    end
end

function DialogueState:render()
    self.textbox:render()
end