module Main where

import Text.Read

data Edge = Edge {
    src :: String,
    dst :: String,
    weight :: Double
} deriving (Show)

main = do
    input <- getContents
    let graphlist = parseGraph input
    print graphlist

parseGraph :: String -> Either String [Edge]
parseGraph x = sequence (map parseGraphEdge (map words (lines x)))

parseGraphEdge :: [String] -> Either String Edge
parseGraphEdge [a, b, c] = case readMaybe c of
    Just weight -> Right (Edge a b weight)
    Nothing -> Left "Invalid Edge Weight"
parseGraphEdge _ = Left "Incorrect Number of Arguments"
