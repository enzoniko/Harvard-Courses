--[[
    GD50
    Match-3 Remake

    -- Board Class --

    Author: Colton Ogden
    cogden@cs50.harvard.edu

    The Board is our arrangement of Tiles with which we must try to find matching
    sets of three horizontally or vertically.
]]

Board = Class{}

function Board:init(x, y, level)
    self.x = x
    self.y = y
    self.matches = {}
    
    self.level = level
    
    self.variety = 1

    self:initializeTiles()
end

function Board:initializeTiles()
    self.tiles = {}
    for tileY = 1, 8 do
        -- the chance of more variated tiles rises with the level
        if self.level == 1 then
            self.variety = math.random(1)
        elseif self.level > 1 and self.level < 4 then
            self.variety = math.random(1, 2)
        end
        if self.level >= 4 then
            if math.random(1, 10) == 5 then
                self.variety = math.random(1, 7)
            else
                self.variety = math.random(1, 6)
            end
        end
        
        -- empty table that will serve as a new row
        table.insert(self.tiles, {})

        for tileX = 1, 8 do

            if self.level == 1 then
                self.variety = math.random(1)
            elseif self.level > 1 and self.level < 4 then
                self.variety = math.random(1, 2)
            end
            if self.level >= 4 then
                if math.random(1, 10) == 5 then
                    self.variety = math.random(1, 7)
                else
                    self.variety = math.random(1, 6)
                end
            end
            -- create a new tile at X,Y with a random color and variety
            table.insert(self.tiles[tileY], Tile(tileX, tileY, math.random(6), self.variety))
        end
    end

    while self:calculateMatches() do
        -- recursively initialize if matches were returned so we always have
        -- a matchless board on start
        self:initializeTiles()
    end
end

-- function to verify if is possible to make a match in the board
function Board:matchesAreImpossible()
	for y = 1, 8 do
		for x = 1, 8 do
			local selectTile = self.tiles[y][x]

            -- tile above and to the left will be redundant, because
            -- they will already have been checked on previous run
            local adjacentTiles = {}
            -- tile below
            if y < 8 then
                table.insert(adjacentTiles, self.tiles[y + 1][x])
            end
            -- tile right
            if x < 8 then
                table.insert(adjacentTiles, self.tiles[y][x + 1])
            end
            -- Will return false if any matches are found
            for k, adjTile in pairs(adjacentTiles) do
                -- Swapping tiles
                local tempX = selectTile.gridX
                local tempY = selectTile.gridY

                selectTile.gridX = adjTile.gridX
                selectTile.gridY = adjTile.gridY
                adjTile.gridX = tempX
                adjTile.gridY = tempY

                -- swap tiles in the tiles table
                self.tiles[selectTile.gridY][selectTile.gridX] =
                    selectTile

                self.tiles[adjTile.gridY][adjTile.gridX] = adjTile

                -- Checking matches
                if self:calculateMatches() ~= false then
                    -- Swap back
                    local tempX = selectTile.gridX
                    local tempY = selectTile.gridY

                    selectTile.gridX = adjTile.gridX
                    selectTile.gridY = adjTile.gridY
                    adjTile.gridX = tempX
                    adjTile.gridY = tempY

                    -- swap tiles in the tiles table
                    self.tiles[selectTile.gridY][selectTile.gridX] =
                        selectTile

                    self.tiles[adjTile.gridY][adjTile.gridX] = adjTile
                    return false
                else
                    -- Swap back
                    local tempX = selectTile.gridX
                    local tempY = selectTile.gridY

                    selectTile.gridX = adjTile.gridX
                    selectTile.gridY = adjTile.gridY
                    adjTile.gridX = tempX
                    adjTile.gridY = tempY

                    -- swap tiles in the tiles table
                    self.tiles[selectTile.gridY][selectTile.gridX] =
                        selectTile

                    self.tiles[adjTile.gridY][adjTile.gridX] = adjTile
                end
			end
		end
	end
	-- Will only get here if no matches found
	return true
end

--[[
    Goes left to right, top to bottom in the board, calculating matches by counting consecutive
    tiles of the same color. Doesn't need to check the last tile in every row or column if the 
    last two haven't been a match.
]]
function Board:calculateMatches()
    local matches = {}

    -- how many of the same color blocks in a row we've found
    local matchNum = 1

    -- horizontal matches first
    for y = 1, 8 do
        local colorToMatch = self.tiles[y][1].color

        matchNum = 1
        
        -- every horizontal tile
        for x = 2, 8 do
            -- if this is the same color as the one we're trying to match...
            
            if self.tiles[y][x].color == colorToMatch then
                matchNum = matchNum + 1  
            else
                -- set this as the new color we want to watch for
                colorToMatch = self.tiles[y][x].color

                -- if we have a match of 3 or more up to now, add it to our matches table
                if matchNum >= 3 then
                  
                    local match = {}

                    -- go backwards from here by matchNum
                    for x2 = x - 1, x - matchNum, -1 do
                        -- add each tile to the match that's in that match
                        table.insert(match, self.tiles[y][x2])
                    end
                   

                    -- add this match to our total matches table
                    table.insert(matches, match)
                end

                -- don't need to check last two if they won't be in a match
                if x >= 7 then
                    break
                end

                matchNum = 1
            end
        end

        -- account for the last row ending with a match
        if matchNum >= 3 then
            local match = {}
            
            -- go backwards from end of last row by matchNum
            for x = 8, 8 - matchNum + 1, -1 do
                table.insert(match, self.tiles[y][x])
            end

            table.insert(matches, match)
        end
    end

    -- vertical matches
    for x = 1, 8 do
        local colorToMatch = self.tiles[1][x].color

        matchNum = 1

        -- every vertical tile
        for y = 2, 8 do
            if self.tiles[y][x].color == colorToMatch then
                matchNum = matchNum + 1
            else
                colorToMatch = self.tiles[y][x].color

                if matchNum >= 3 then
                    local match = {}

                    for y2 = y - 1, y - matchNum, -1 do

                        table.insert(match, self.tiles[y2][x])
                    end

                    table.insert(matches, match)
                end

                matchNum = 1

                -- don't need to check last two if they won't be in a match
                if y >= 7 then
                    break
                end
            end
        end

        -- account for the last column ending with a match
        if matchNum >= 3 then
            local match = {}
            
            -- go backwards from end of last row by matchNum
            for y = 8, 8 - matchNum, -1 do
                table.insert(match, self.tiles[y][x])
            end

            table.insert(matches, match)
        end
    end

    -- store matches for later reference
    self.matches = matches

    -- return matches table if > 0, else just return false
    return #self.matches > 0 and self.matches or false
end


--[[
    Remove the matches from the Board by just setting the Tile slots within
    them to nil, then setting self.matches to nil.
]]
function Board:removeMatches()
    
    for k, match in pairs(self.matches) do
        for k, tile in pairs(match) do
            if tile.variety == 7 then
                for x = 1, 8 do
                    self.tiles[tile.gridY][x] = nil 
                end
            end
            self.tiles[tile.gridY][tile.gridX] = nil
        end
    end

    self.matches = nil
end

--[[
    Shifts down all of the tiles that now have spaces below them, then returns a table that
    contains tweening information for these new tiles.
]]
function Board:getFallingTiles()
    -- tween table, with tiles as keys and their x and y as the to values
    local tweens = {}

    -- for each column, go up tile by tile till we hit a space
    for x = 1, 8 do
        local space = false
        local spaceY = 0

        local y = 8
        while y >= 1 do
            -- if our last tile was a space...
            local tile = self.tiles[y][x]
            
            if space then
                -- if the current tile is *not* a space, bring this down to the lowest space
                if tile then
                    -- put the tile in the correct spot in the board and fix its grid positions
                    self.tiles[spaceY][x] = tile
                    tile.gridY = spaceY

                    -- set its prior position to nil
                    self.tiles[y][x] = nil

                    -- tween the Y position to 32 x its grid position
                    tweens[tile] = {
                        y = (tile.gridY - 1) * 32
                    }

                    -- set space back to 0, set Y to spaceY so we start back from here again
                    space = false
                    y = spaceY
                    spaceY = 0
                end
            elseif tile == nil then
                space = true
                
                if spaceY == 0 then
                    spaceY = y
                end
            end

            y = y - 1
        end
    end

    -- create replacement tiles at the top of the screen
    for x = 1, 8 do
        if self.level == 1 then
            self.variety = math.random(1)
        elseif self.level > 1 and self.level < 4 then
            self.variety = math.random(1, 2)
        end
        if self.level >= 4 then
            if math.random(1, 10) == 5 then
                self.variety = math.random(1, 7)
            else
                self.variety = math.random(1, 6)
            end
        end
        for y = 8, 1, -1 do
            if self.level == 1 then
                self.variety = math.random(1)
            elseif self.level > 1 and self.level < 4 then
                self.variety = math.random(1, 2)
            end
            if self.level >= 4 then
                if math.random(1, 10) == 5 then
                    self.variety = math.random(1, 7)
                else
                    self.variety = math.random(1, 6)
                end
            end
            local tile = self.tiles[y][x]

            -- if the tile is nil, we need to add a new one
            if not tile then
                local tile = Tile(x, y, math.random(6), self.variety)

                tile.y = -32
                self.tiles[y][x] = tile

                tweens[tile] = {
                    y = (tile.gridY - 1) * 32
                }
            end
        end
    end

    return tweens
end

function Board:getNewTiles()
    return {}
end

function Board:render()
    for y = 1, #self.tiles do
        for x = 1, #self.tiles[1] do
            self.tiles[y][x]:render(self.x, self.y)
        end
    end
end
